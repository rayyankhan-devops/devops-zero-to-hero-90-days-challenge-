import React, { useState, useEffect, useRef } from 'react';
import { MessageSquare, Send, Hash, Users, Sparkles } from 'lucide-react';

// Read API & WebSocket URLs from Vite Environment variables (.env.local / .env)
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080';
const WS_BASE_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8080';

const ROOMS = [
  { id: 'general', name: 'general', label: 'General Chat' },
  { id: 'devops', name: 'devops', label: 'DevOps & Docker' },
  { id: 'random', name: 'random', label: 'Random Lounge' },
];

export default function App() {
  const [username, setUsername] = useState('');
  const [inputUsername, setInputUsername] = useState('');
  const [activeRoom, setActiveRoom] = useState('general');
  const [messages, setMessages] = useState([]);
  const [messageInput, setMessageInput] = useState('');
  const [isConnected, setIsConnected] = useState(false);

  const wsRef = useRef(null);
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom of chat messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Fetch Message History via HTTP REST API
  const fetchMessageHistory = async (room) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/messages?room=${room}`);
      if (response.ok) {
        const data = await response.json();
        setMessages(data || []);
      }
    } catch (err) {
      console.error('Error fetching chat history:', err);
    }
  };

  // Setup WebSocket Connection
  useEffect(() => {
    if (!username) return;

    // Load historical messages first
    fetchMessageHistory(activeRoom);

    // Close previous WS connection if switching rooms
    if (wsRef.current) {
      wsRef.current.close();
    }

    const wsUrl = `${WS_BASE_URL}/ws?room=${activeRoom}&username=${encodeURIComponent(username)}`;
    console.log(`Connecting to WebSocket: ${wsUrl}`);

    const ws = new WebSocket(wsUrl);
    wsRef.current = ws;

    ws.onopen = () => {
      console.log('WebSocket Connection Established');
      setIsConnected(true);
    };

    ws.onmessage = (event) => {
      try {
        const newMsg = JSON.parse(event.data);
        setMessages((prev) => [...prev, newMsg]);
      } catch (err) {
        console.error('Error parsing incoming WebSocket message:', err);
      }
    };

    ws.onclose = () => {
      console.log('WebSocket Disconnected');
      setIsConnected(false);
    };

    ws.onerror = (err) => {
      console.error('WebSocket Error:', err);
    };

    return () => {
      ws.close();
    };
  }, [username, activeRoom]);

  // Handle Username Submission
  const handleJoinChat = (e) => {
    e.preventDefault();
    if (inputUsername.trim()) {
      setUsername(inputUsername.trim());
    }
  };

  // Send Message via WebSocket
  const handleSendMessage = (e) => {
    e.preventDefault();
    if (!messageInput.trim() || !wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) {
      return;
    }

    const payload = {
      room: activeRoom,
      username: username,
      content: messageInput.trim(),
    };

    wsRef.current.send(JSON.stringify(payload));
    setMessageInput('');
  };

  // If user hasn't set username, show Join Modal
  if (!username) {
    return (
      <div className="join-overlay">
        <div className="join-card">
          <div className="app-logo-icon" style={{ margin: '0 auto 16px auto', width: '48px', height: '48px' }}>
            <MessageSquare color="white" size={26} />
          </div>
          <h1 className="join-title">Welcome to GoChat</h1>
          <p className="join-subtitle">Go + React + PostgreSQL Dockerized Chat</p>

          <form onSubmit={handleJoinChat}>
            <input
              type="text"
              className="join-input"
              placeholder="Enter your username (e.g. Alex)..."
              value={inputUsername}
              onChange={(e) => setInputUsername(e.target.value)}
              autoFocus
              required
            />
            <button type="submit" className="join-btn">
              Start Chatting
            </button>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="chat-app-wrapper">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <div className="app-brand">
            <div className="app-logo-icon">
              <MessageSquare color="white" size={20} />
            </div>
            <span>GoChat</span>
          </div>
        </div>

        <div className="rooms-section">
          <div className="section-label">Chat Channels</div>
          {ROOMS.map((room) => (
            <div
              key={room.id}
              className={`room-item ${activeRoom === room.id ? 'active' : ''}`}
              onClick={() => setActiveRoom(room.id)}
            >
              <Hash size={18} />
              <span>{room.name}</span>
            </div>
          ))}
        </div>

        <div className="user-profile">
          <div className="avatar">{username.charAt(0).toUpperCase()}</div>
          <div className="user-info">
            <span className="user-name">{username}</span>
            <span className="user-status">
              <span className="status-dot" style={{ background: isConnected ? '#34d399' : '#f87171', boxShadow: isConnected ? '0 0 8px #34d399' : '0 0 8px #f87171' }} />
              {isConnected ? 'Connected' : 'Connecting...'}
            </span>
          </div>
        </div>
      </aside>

      {/* Main Chat Content */}
      <main className="chat-main">
        {/* Header */}
        <header className="chat-header">
          <div className="chat-title">
            <Hash size={22} color="#818cf8" />
            <span>{activeRoom}</span>
          </div>

          <div className="tech-pills">
            <span className="tech-badge go">Go 1.21</span>
            <span className="tech-badge react">React + Vite</span>
            <span className="tech-badge postgres">PostgreSQL</span>
          </div>
        </header>

        {/* Message Stream */}
        <div className="messages-container">
          {messages.length === 0 ? (
            <div style={{ textAlign: 'center', color: '#94a3b8', marginTop: '40px' }}>
              <Sparkles size={32} style={{ margin: '0 auto 8px auto', opacity: 0.6 }} />
              <p>No messages in #{activeRoom} yet. Send the first message!</p>
            </div>
          ) : (
            messages.map((msg, idx) => {
              const isSelf = msg.username === username;
              const formattedTime = msg.createdAt
                ? new Date(msg.createdAt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
                : 'Just now';

              return (
                <div key={idx} className={`message-wrapper ${isSelf ? 'sent' : 'received'}`}>
                  <div className="message-meta">
                    {!isSelf && <strong>{msg.username} • </strong>}
                    <span>{formattedTime}</span>
                  </div>
                  <div className="message-bubble">{msg.content}</div>
                </div>
              );
            })
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Message Input Bar */}
        <div className="chat-input-area">
          <form className="input-form" onSubmit={handleSendMessage}>
            <input
              type="text"
              className="message-input"
              placeholder={`Message #${activeRoom}...`}
              value={messageInput}
              onChange={(e) => setMessageInput(e.target.value)}
            />
            <button type="submit" className="send-btn" disabled={!isConnected}>
              <Send size={20} />
            </button>
          </form>
        </div>
      </main>
    </div>
  );
}
