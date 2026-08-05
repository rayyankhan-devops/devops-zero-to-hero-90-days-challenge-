package handlers

import (
	"encoding/json"
	"log"
	"net/http"
	"sync"

	"github.com/gorilla/websocket"
	"chatapp-backend/db"
	"chatapp-backend/models"
)

var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		// Allow connection from any origin (React frontend)
		return true
	},
}

type Client struct {
	Conn     *websocket.Conn
	Send     chan models.Message
	Room     string
	Username string
}

type Hub struct {
	Clients    map[*Client]bool
	Broadcast  chan models.Message
	Register   chan *Client
	Unregister chan *Client
	mu         sync.Mutex
}

var GlobalHub = &Hub{
	Clients:    make(map[*Client]bool),
	Broadcast:  make(chan models.Message),
	Register:   make(chan *Client),
	Unregister: make(chan *Client),
}

func (h *Hub) Run() {
	for {
		select {
		case client := <-h.Register:
			h.mu.Lock()
			h.Clients[client] = true
			h.mu.Unlock()
			log.Printf("Client connected: %s (Room: %s)", client.Username, client.Room)

		case client := <-h.Unregister:
			h.mu.Lock()
			if _, ok := h.Clients[client]; ok {
				delete(h.Clients, client)
				close(client.Send)
				log.Printf("Client disconnected: %s (Room: %s)", client.Username, client.Room)
			}
			h.mu.Unlock()

		case msg := <-h.Broadcast:
			// Save message to Postgres database
			err := db.SaveMessage(&msg)
			if err != nil {
				log.Printf("Error saving message to DB: %v", err)
			}

			// Broadcast message to all connected clients in the same room
			h.mu.Lock()
			for client := range h.Clients {
				if client.Room == msg.Room {
					select {
					case client.Send <- msg:
					default:
						close(client.Send)
						delete(h.Clients, client)
					}
				}
			}
			h.mu.Unlock()
		}
	}
}

func GetMessagesHandler(w http.ResponseWriter, r *http.Request) {
	room := r.URL.Query().Get("room")
	if room == "" {
		room = "general"
	}

	messages, err := db.GetRecentMessages(room, 50)
	if err != nil {
		http.Error(w, "Failed to retrieve messages", http.StatusInternalServerError)
		log.Printf("Error fetching messages: %v", err)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(messages)
}

func ServeWS(w http.ResponseWriter, r *http.Request) {
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Printf("WebSocket Upgrade Error: %v", err)
		return
	}

	room := r.URL.Query().Get("room")
	if room == "" {
		room = "general"
	}

	username := r.URL.Query().Get("username")
	if username == "" {
		username = "Anonymous"
	}

	client := &Client{
		Conn:     conn,
		Send:     make(chan models.Message, 256),
		Room:     room,
		Username: username,
	}

	GlobalHub.Register <- client

	// Read loop
	go func() {
		defer func() {
			GlobalHub.Unregister <- client
			client.Conn.Close()
		}()

		for {
			_, p, err := client.Conn.ReadMessage()
			if err != nil {
				if websocket.IsUnexpectedCloseError(err, websocket.CloseGoingAway, websocket.CloseAbnormalClosure) {
					log.Printf("WebSocket Read error: %v", err)
				}
				break
			}

			var incoming struct {
				Room     string `json:"room"`
				Username string `json:"username"`
				Content  string `json:"content"`
			}

			if err := json.Unmarshal(p, &incoming); err != nil {
				log.Printf("Invalid message payload: %v", err)
				continue
			}

			if incoming.Content == "" {
				continue
			}

			msg := models.Message{
				Room:     client.Room,
				Username: client.Username,
				Content:  incoming.Content,
			}

			GlobalHub.Broadcast <- msg
		}
	}()

	// Write loop
	go func() {
		defer client.Conn.Close()
		for msg := range client.Send {
			w, err := client.Conn.NextWriter(websocket.TextMessage)
			if err != nil {
				return
			}
			json.NewEncoder(w).Encode(msg)

			if err := w.Close(); err != nil {
				return
			}
		}
	}()
}
