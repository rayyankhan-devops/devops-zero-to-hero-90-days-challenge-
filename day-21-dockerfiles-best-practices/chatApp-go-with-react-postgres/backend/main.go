package main

import (
	"encoding/json"
	"log"
	"net/http"

	"chatapp-backend/config"
	"chatapp-backend/db"
	"chatapp-backend/handlers"

	"github.com/rs/cors"
)

func main() {
	cfg := config.LoadConfig()

	log.Printf("Starting Go Chat Server...")

	// Initialize Database Connection
	_, err := db.InitDB(cfg)
	if err != nil {
		log.Fatalf("Fatal Error initializing database: %v", err)
	}

	// Start WebSocket Hub in background goroutine
	go handlers.GlobalHub.Run()

	mux := http.NewServeMux()

	// Health check endpoint
	mux.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(map[string]string{
			"status":  "healthy",
			"service": "chatapp-backend-go",
		})
	})

	// Chat message history endpoint
	mux.HandleFunc("/api/messages", handlers.GetMessagesHandler)

	// Real-time WebSocket endpoint
	mux.HandleFunc("/ws", handlers.ServeWS)

	// Configure CORS for web requests
	c := cors.New(cors.Options{
		AllowedOrigins:   []string{"*"},
		AllowedMethods:   []string{"GET", "POST", "OPTIONS"},
		AllowedHeaders:   []string{"Content-Type", "Authorization"},
		AllowCredentials: true,
	})

	handler := c.Handler(mux)

	log.Printf("Server listening on port :%s", cfg.Port)
	if err := http.ListenAndServe(":"+cfg.Port, handler); err != nil {
		log.Fatalf("Server shutdown with error: %v", err)
	}
}
