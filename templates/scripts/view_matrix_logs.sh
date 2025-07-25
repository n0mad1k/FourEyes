#!/bin/bash

echo "🔍 Matrix Logs Viewer"
echo "===================="
echo

if [ ! -f "/var/log/matrix-synapse/homeserver.log" ]; then
    echo "❌ Matrix log file not found"
    exit 1
fi

echo "Choose an option:"
echo "1. View last 50 lines"
echo "2. View last 100 lines" 
echo "3. Follow live logs (tail -f)"
echo "4. Search for errors"
echo "5. Search for warnings"
echo "6. Search for specific text"
echo "7. View logs from last hour"
echo

read -p "Enter choice (1-7): " choice

case $choice in
    1)
        echo "📝 Last 50 lines of Matrix logs:"
        echo "================================"
        tail -n 50 /var/log/matrix-synapse/homeserver.log
        ;;
    2)
        echo "📝 Last 100 lines of Matrix logs:"
        echo "================================="
        tail -n 100 /var/log/matrix-synapse/homeserver.log
        ;;
    3)
        echo "📺 Following live Matrix logs (Ctrl+C to stop):"
        echo "==============================================="
        tail -f /var/log/matrix-synapse/homeserver.log
        ;;
    4)
        echo "🚨 Recent errors in Matrix logs:"
        echo "================================"
        grep -i error /var/log/matrix-synapse/homeserver.log | tail -n 20
        ;;
    5)
        echo "⚠️  Recent warnings in Matrix logs:"
        echo "==================================="
        grep -i warning /var/log/matrix-synapse/homeserver.log | tail -n 20
        ;;
    6)
        read -p "Enter text to search for: " search_text
        echo "🔍 Searching for '$search_text':"
        echo "==============================="
        grep -i "$search_text" /var/log/matrix-synapse/homeserver.log | tail -n 20
        ;;
    7)
        echo "⏰ Logs from last hour:"
        echo "======================"
        # Get logs from last hour (simplified)
        tail -n 1000 /var/log/matrix-synapse/homeserver.log | grep "$(date '+%Y-%m-%d %H')"
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac
