#!/usr/bin/env python3
"""Export Hermes session to Markdown"""
import json
import sys
import os
from datetime import datetime

def export_session(dump_file, output_file):
    with open(dump_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    lines = []
    lines.append(f"# Chat Export — {os.path.basename(dump_file)}")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Extract messages from the dump
    messages = data.get('messages', [])
    
    for msg in messages:
        role = msg.get('role', 'unknown')
        content = msg.get('content', '')
        
        if role == 'user':
            lines.append(f"## 👤 Usuario")
            lines.append(content)
            lines.append("")
        elif role == 'assistant':
            lines.append(f"## 🤖 Asistente")
            lines.append(content)
            lines.append("")
        elif role == 'tool':
            lines.append(f"## 🔧 Herramienta")
            lines.append(content)
            lines.append("")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"Exported to: {output_file}")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python export_session.py <dump_file> <output_file>")
        sys.exit(1)
    export_session(sys.argv[1], sys.argv[2])
