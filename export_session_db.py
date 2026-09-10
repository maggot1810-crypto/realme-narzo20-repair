#!/usr/bin/env python3
"""Export Hermes session from SQLite to Markdown"""
import sqlite3
import json
import os
from datetime import datetime

def export_session(db_path, output_file):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get column names first
    cursor.execute("PRAGMA table_info(messages)")
    columns = [col[1] for col in cursor.fetchall()]
    print(f"Columns: {columns}")
    
    # Get all messages ordered by created_at
    cursor.execute(f"""
        SELECT {', '.join(columns)}
        FROM messages 
        ORDER BY timestamp ASC
    """)
    
    messages = cursor.fetchall()
    
    lines = []
    lines.append(f"# Chat Export — Sesión Hermes")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"Total messages: {len(messages)}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    for msg in messages:
        # Extract role and content based on column names
        role = None
        content = None
        
        for i, col in enumerate(columns):
            if col == 'role':
                role = msg[i]
            elif col == 'content':
                content = msg[i]
        
        if not role or not content:
            continue
        
        # Clean content
        if len(content) > 5000:
            content = content[:5000] + "\n... [truncated]"
        
        if role == 'user':
            lines.append(f"## 👤 Usuario")
        elif role == 'assistant':
            lines.append(f"## 🤖 Asistente")
        elif role == 'tool':
            lines.append(f"## 🔧 Herramienta")
        else:
            lines.append(f"## {role}")
        
        lines.append(content)
        lines.append("")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"Exported {len(messages)} messages to: {output_file}")
    conn.close()

if __name__ == '__main__':
    db_path = 'D:/Usuarios/Administrador/AppData/Local/hermes/state.db'
    output_file = 'D:/Usuarios/Administrador/Documents/hermes_chat_export.md'
    export_session(db_path, output_file)
