#!/bin/bash

echo "🔄 Matrix Service Restart Script"
echo "================================"
echo

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Please run as root (use sudo)"
    exit 1
fi

echo "🛑 Stopping Matrix Synapse..."
systemctl stop matrix-synapse
sleep 3

echo "🔧 Checking for any remaining processes..."
pkill -f synapse || echo "No remaining synapse processes found"

echo "🔍 Checking database permissions..."
chown -R matrix-synapse:matrix-synapse /var/lib/matrix-synapse/
chmod 750 /var/lib/matrix-synapse/
chmod 640 /var/lib/matrix-synapse/homeserver.db 2>/dev/null || echo "Database file not found - will be created on startup"

echo "📝 Checking log permissions..."
chown -R matrix-synapse:matrix-synapse /var/log/matrix-synapse/
chmod 750 /var/log/matrix-synapse/

echo "🚀 Starting Matrix Synapse..."
systemctl start matrix-synapse
sleep 5

echo "✅ Service status:"
systemctl status matrix-synapse --no-pager

echo
echo "🔍 Checking if Matrix API is responding..."
sleep 10
curl -s -k https://localhost:8008/_matrix/client/versions > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ Matrix API is responding"
else
    echo "❌ Matrix API not responding - check logs"
    echo "📝 Recent logs:"
    tail -n 20 /var/log/matrix-synapse/homeserver.log
fi
