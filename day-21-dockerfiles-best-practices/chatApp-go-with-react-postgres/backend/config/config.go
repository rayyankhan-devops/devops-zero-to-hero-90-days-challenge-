package config

import (
	"fmt"
	"log"
	"os"

	"github.com/joho/godotenv"
)

type Config struct {
	Port        string
	DBHost      string
	DBPort      string
	DBUser      string
	DBPassword  string
	DBName      string
	DatabaseURL string
}

func LoadConfig() *Config {
	// Attempt to load .env file; if it fails, fallback to environment variables
	if err := godotenv.Load(); err != nil {
		log.Println("Note: .env file not found or couldn't be loaded. Using system environment variables.")
	}

	port := getEnv("PORT", "8080")
	dbHost := getEnv("DB_HOST", "localhost")
	dbPort := getEnv("DB_PORT", "5432")
	dbUser := getEnv("DB_USER", "postgres")
	dbPassword := getEnv("DB_PASSWORD", "postgres")
	dbName := getEnv("DB_NAME", "chatapp")

	// Build PostgreSQL connection string
	dbURL := fmt.Sprintf("host=%s port=%s user=%s password=%s dbname=%s sslmode=disable",
		dbHost, dbPort, dbUser, dbPassword, dbName)

	return &Config{
		Port:        port,
		DBHost:      dbHost,
		DBPort:      dbPort,
		DBUser:      dbUser,
		DBPassword:  dbPassword,
		DBName:      dbName,
		DatabaseURL: dbURL,
	}
}

func getEnv(key, fallback string) string {
	if val, ok := os.LookupEnv(key); ok && val != "" {
		return val
	}
	return fallback
}
