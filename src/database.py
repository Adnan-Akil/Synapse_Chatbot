import sqlite3
from pathlib import Path

DB_PATH = Path("data/chat.db")

def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Conversations table
    c.execute('''CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    title TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )''')
    
    # Messages table
    c.execute('''CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id TEXT,
                    role TEXT,
                    content TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(conversation_id) REFERENCES conversations(id)
                )''')
    
    conn.commit()
    conn.close()

def save_message(conversation_id: str, role: str, content: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Ensure conversation exists
    c.execute("INSERT OR IGNORE INTO conversations (id, title) VALUES (?, ?)", 
              (conversation_id, "New Conversation"))
    
    # Update title if it's the first user message
    if role == "user":
        # Check if title is default
        c.execute("SELECT title FROM conversations WHERE id = ?", (conversation_id,))
        current_title = c.fetchone()[0]
        if current_title == "New Conversation":
            new_title = content[:30] + "..." if len(content) > 30 else content
            c.execute("UPDATE conversations SET title = ? WHERE id = ?", (new_title, conversation_id))

    c.execute("INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)",
              (conversation_id, role, content))
    
    c.execute("UPDATE conversations SET updated_at = CURRENT_TIMESTAMP WHERE id = ?", (conversation_id,))
    
    conn.commit()
    conn.close()

def get_history(conversation_id: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT role, content FROM messages WHERE conversation_id = ? ORDER BY created_at ASC", (conversation_id,))
    rows = c.fetchall()
    conn.close()
    return [{"role": r[0], "content": r[1]} for r in rows]

def get_all_conversations():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, title, created_at FROM conversations ORDER BY updated_at DESC")
    rows = c.fetchall()
    conn.close()
    return [{"id": r[0], "title": r[1], "date": r[2]} for r in rows]
