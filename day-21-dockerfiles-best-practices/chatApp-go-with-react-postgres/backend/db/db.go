package db

import (
	"database/sql"
	"fmt"
	"log"
	"time"

	_ "github.com/lib/pq"
	"chatapp-backend/config"
	"chatapp-backend/models"
)

var DB *sql.DB

func InitDB(cfg *config.Config) (*sql.DB, error) {
	var err error
	
	// Retries for connecting to DB (useful when running in Docker Compose while DB starts up)
	for i := 1; i <= 10; i++ {
		DB, err = sql.Open("postgres", cfg.DatabaseURL)
		if err == nil {
			err = DB.Ping()
			if err == nil {
				log.Printf("Successfully connected to PostgreSQL at %s:%s", cfg.DBHost, cfg.DBPort)
				break
			}
		}
		log.Printf("Waiting for PostgreSQL connection (Attempt %d/10)... %v", i, err)
		time.Sleep(2 * time.Second)
	}

	if err != nil {
		return nil, fmt.Errorf("failed to connect to database after 10 attempts: %w", err)
	}

	// Create messages table if it doesn't exist
	query := `
	CREATE TABLE IF NOT EXISTS messages (
		id SERIAL PRIMARY KEY,
		room VARCHAR(50) NOT NULL DEFAULT 'general',
		username VARCHAR(50) NOT NULL,
		content TEXT NOT NULL,
		created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
	);`

	_, err = DB.Exec(query)
	if err != nil {
		return nil, fmt.Errorf("failed to create messages table: %w", err)
	}

	log.Println("Database schema initialized: 'messages' table ready.")
	return DB, nil
}

func SaveMessage(msg *models.Message) error {
	query := `
	INSERT INTO messages (room, username, content, created_at)
	VALUES ($1, $2, $3, NOW())
	RETURNING id, created_at;`

	err := DB.QueryRow(query, msg.Room, msg.Username, msg.Content).Scan(&msg.ID, &msg.CreatedAt)
	if err != nil {
		return fmt.Errorf("error saving message to DB: %w", err)
	}
	return nil
}

func GetRecentMessages(room string, limit int) ([]models.Message, error) {
	if room == "" {
		room = "general"
	}
	if limit <= 0 {
		limit = 50
	}

	query := `
	SELECT id, room, username, content, created_at
	FROM (
		SELECT id, room, username, content, created_at
		FROM messages
		WHERE room = $1
		ORDER BY id DESC
		LIMIT $2
	) sub
	ORDER BY id ASC;`

	rows, err := DB.Query(query, room, limit)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var messages []models.Message
	for rows.Next() {
		var m models.Message
		if err := rows.Scan(&m.ID, &m.Room, &m.Username, &m.Content, &m.CreatedAt); err != nil {
			return nil, err
		}
		messages = append(messages, m)
	}

	if messages == nil {
		messages = []models.Message{}
	}

	return messages, nil
}
