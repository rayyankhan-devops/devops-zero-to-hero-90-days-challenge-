package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"strconv"
	"strings"
	"sync"
	"time"

	_ "github.com/go-sql-driver/mysql"
)

// Item represents a task/note stored in MariaDB
type Item struct {
	ID          int       `json:"id"`
	Title       string    `json:"title"`
	Description string    `json:"description"`
	CreatedAt   time.Time `json:"created_at"`
}

// Response represents standard API response
type Response struct {
	Success bool        `json:"success"`
	Message string      `json:"message,omitempty"`
	Data    interface{} `json:"data,omitempty"`
}

// HealthResponse represents DB connection status
type HealthResponse struct {
	Status      string `json:"status"`
	DBConnected bool   `json:"db_connected"`
	DBHost      string `json:"db_host"`
	DBName      string `json:"db_name"`
	Message     string `json:"message"`
}

var (
	db     *sql.DB
	dbErr  error
	dbLock sync.RWMutex
)

func getEnv(key, fallback string) string {
	if val, ok := os.LookupEnv(key); ok && val != "" {
		return val
	}
	return fallback
}

func initDB() {
	host := getEnv("DB_HOST", "localhost")
	port := getEnv("DB_PORT", "3306")
	user := getEnv("DB_USER", "mariadb_user")
	pass := getEnv("DB_PASSWORD", "mariadb_password")
	dbname := getEnv("DB_NAME", "mariadb_db")

	dsn := fmt.Sprintf("%s:%s@tcp(%s:%s)/%s?parseTime=true", user, pass, host, port, dbname)

	log.Printf("Connecting to MariaDB at %s:%s (database: %s)...", host, port, dbname)

	dbConn, err := sql.Open("mysql", dsn)
	if err != nil {
		log.Printf("Error opening database connection: %v", err)
		dbLock.Lock()
		dbErr = err
		dbLock.Unlock()
		return
	}

	dbConn.SetMaxOpenConns(25)
	dbConn.SetMaxIdleConns(5)
	dbConn.SetConnMaxLifetime(5 * time.Minute)

	if err := dbConn.Ping(); err != nil {
		log.Printf("MariaDB ping failed: %v", err)
		dbLock.Lock()
		dbErr = err
		dbLock.Unlock()
		return
	}

	// Create table if not exists
	query := `
	CREATE TABLE IF NOT EXISTS items (
		id INT AUTO_INCREMENT PRIMARY KEY,
		title VARCHAR(255) NOT NULL,
		description TEXT,
		created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
	) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;`

	if _, err := dbConn.Exec(query); err != nil {
		log.Printf("Failed to create table: %v", err)
		dbLock.Lock()
		dbErr = err
		dbLock.Unlock()
		return
	}

	dbLock.Lock()
	db = dbConn
	dbErr = nil
	dbLock.Unlock()

	log.Println("Successfully connected to MariaDB and initialized database schema!")
}

func tryReconnectPeriodically() {
	ticker := time.NewTicker(10 * time.Second)
	for range ticker.C {
		dbLock.RLock()
		connected := db != nil && dbErr == nil
		dbLock.RUnlock()

		if !connected {
			log.Println("Attempting database reconnection...")
			initDB()
		}
	}
}

func jsonResponse(w http.ResponseWriter, statusCode int, payload interface{}) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(statusCode)
	json.NewEncoder(w).Encode(payload)
}

func enableCORS(next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type")

		if r.Method == http.MethodOptions {
			w.WriteHeader(http.StatusOK)
			return
		}

		next(w, r)
	}
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
	dbLock.RLock()
	defer dbLock.RUnlock()

	host := getEnv("DB_HOST", "localhost")
	dbname := getEnv("DB_NAME", "mariadb_db")

	connected := false
	msg := "Database connected successfully"

	if db != nil && dbErr == nil {
		if err := db.Ping(); err == nil {
			connected = true
		} else {
			msg = fmt.Sprintf("Ping failed: %v", err)
		}
	} else if dbErr != nil {
		msg = fmt.Sprintf("Connection error: %v", dbErr)
	} else {
		msg = "Database connection not initialized"
	}

	jsonResponse(w, http.StatusOK, HealthResponse{
		Status:      "up",
		DBConnected: connected,
		DBHost:      host,
		DBName:      dbname,
		Message:     msg,
	})
}

func itemsHandler(w http.ResponseWriter, r *http.Request) {
	dbLock.RLock()
	currentDB := db
	currentErr := dbErr
	dbLock.RUnlock()

	if currentDB == nil || currentErr != nil {
		jsonResponse(w, http.StatusServiceUnavailable, Response{
			Success: false,
			Message: fmt.Sprintf("MariaDB database unavailable: %v. Please ensure MariaDB container or service is running.", currentErr),
		})
		return
	}

	switch r.Method {
	case http.MethodGet:
		rows, err := currentDB.Query("SELECT id, title, description, created_at FROM items ORDER BY id DESC")
		if err != nil {
			jsonResponse(w, http.StatusInternalServerError, Response{
				Success: false,
				Message: fmt.Sprintf("Failed to query items: %v", err),
			})
			return
		}
		defer rows.Close()

		var items []Item = make([]Item, 0)
		for rows.Next() {
			var item Item
			if err := rows.Scan(&item.ID, &item.Title, &item.Description, &item.CreatedAt); err != nil {
				log.Printf("Row scan error: %v", err)
				continue
			}
			items = append(items, item)
		}

		jsonResponse(w, http.StatusOK, Response{
			Success: true,
			Data:    items,
		})

	case http.MethodPost:
		var req struct {
			Title       string `json:"title"`
			Description string `json:"description"`
		}

		if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
			jsonResponse(w, http.StatusBadRequest, Response{
				Success: false,
				Message: "Invalid JSON request body",
			})
			return
		}

		req.Title = strings.TrimSpace(req.Title)
		if req.Title == "" {
			jsonResponse(w, http.StatusBadRequest, Response{
				Success: false,
				Message: "Title cannot be empty",
			})
			return
		}

		res, err := currentDB.Exec("INSERT INTO items (title, description) VALUES (?, ?)", req.Title, req.Description)
		if err != nil {
			jsonResponse(w, http.StatusInternalServerError, Response{
				Success: false,
				Message: fmt.Sprintf("Failed to insert item: %v", err),
			})
			return
		}

		id, _ := res.LastInsertId()
		jsonResponse(w, http.StatusCreated, Response{
			Success: true,
			Message: "Item created successfully",
			Data: Item{
				ID:          int(id),
				Title:       req.Title,
				Description: req.Description,
				CreatedAt:   time.Now(),
			},
		})

	case http.MethodDelete:
		idStr := r.URL.Query().Get("id")
		if idStr == "" {
			jsonResponse(w, http.StatusBadRequest, Response{
				Success: false,
				Message: "Missing required 'id' query parameter",
			})
			return
		}

		id, err := strconv.Atoi(idStr)
		if err != nil {
			jsonResponse(w, http.StatusBadRequest, Response{
				Success: false,
				Message: "Invalid 'id' parameter",
			})
			return
		}

		res, err := currentDB.Exec("DELETE FROM items WHERE id = ?", id)
		if err != nil {
			jsonResponse(w, http.StatusInternalServerError, Response{
				Success: false,
				Message: fmt.Sprintf("Failed to delete item: %v", err),
			})
			return
		}

		rowsAffected, _ := res.RowsAffected()
		if rowsAffected == 0 {
			jsonResponse(w, http.StatusNotFound, Response{
				Success: false,
				Message: fmt.Sprintf("Item with ID %d not found", id),
			})
			return
		}

		jsonResponse(w, http.StatusOK, Response{
			Success: true,
			Message: fmt.Sprintf("Item %d deleted successfully", id),
		})

	default:
		jsonResponse(w, http.StatusMethodNotAllowed, Response{
			Success: false,
			Message: "Method not allowed",
		})
	}
}

func main() {
	port := getEnv("PORT", "8080")

	// Initialize DB asynchronously so server starts immediately
	go initDB()
	go tryReconnectPeriodically()

	mux := http.NewServeMux()

	// API Endpoints
	mux.HandleFunc("/api/health", enableCORS(healthHandler))
	mux.HandleFunc("/api/items", enableCORS(itemsHandler))

	// Static Files (Frontend UI)
	staticDir := getEnv("STATIC_DIR", "../public")
	if _, err := os.Stat(staticDir); os.IsNotExist(err) {
		staticDir = "./public"
	}

	fs := http.FileServer(http.Dir(staticDir))
	mux.Handle("/", fs)

	log.Printf("==================================================")
	log.Printf("🚀 Server running on http://localhost:%s", port)
	log.Printf("📁 Serving frontend files from %s", staticDir)
	log.Printf("==================================================")

	if err := http.ListenAndServe(":"+port, mux); err != nil {
		log.Fatalf("Server failed to start: %v", err)
	}
}
