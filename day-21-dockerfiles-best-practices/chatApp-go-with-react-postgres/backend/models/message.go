package models

import "time"

type Message struct {
	ID        int64     `json:"id"`
	Room      string    `json:"room"`
	Username  string    `json:"username"`
	Content   string    `json:"content"`
	CreatedAt time.Time `json:"createdAt"`
}
