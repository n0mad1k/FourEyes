#!/bin/bash

echo "🔍 Matrix Server Diagnostic Script"
echo "=================================="
echo

# Check if this is being run on the server
if [ ! -f "/etc/matrix-synapse/homeserver.yaml" ]; then
    echo "❌ This script should be run on the Matrix server"
    echo "💡 Matrix Synapse not found - ensure deployment completed successfully"
    exit 1
fi

echo "1. 🔧 Matrix Synapse Service Status"
echo "-----------------------------------"
systemctl status matrix-synapse --no-pager
echo

echo "2. 📊 Matrix Synapse Process"
echo "----------------------------"
ps aux | grep synapse | grep -v grep
echo

echo "3. 🌐 Network Listening Ports"
echo "-----------------------------"
echo "Matrix API (port 8008):"
netstat -tlnp | grep :8008
echo "Element Web (port 443):"
netstat -tlnp | grep :443
echo "CA Download (port 8443):"
netstat -tlnp | grep :8443
echo

echo "4. 📝 Recent Matrix Logs (last 30 lines)"
echo "----------------------------------------"
tail -n 30 /var/log/matrix-synapse/homeserver.log
echo

echo "5. 📝 Nginx Error Logs (last 20 lines)"
echo "--------------------------------------"
tail -n 20 /var/log/nginx/error.log
echo

echo "6. 🔐 SSL Certificate Check"
echo "---------------------------"
echo "Checking certificate at /etc/ssl/private/matrix.crt:"
if [ -f "/etc/ssl/private/matrix.crt" ]; then
    openssl x509 -in /etc/ssl/private/matrix.crt -text -noout | grep -E "(Subject:|DNS:|IP Address:|Not After)"
else
    echo "❌ Certificate not found at /etc/ssl/private/matrix.crt"
fi
echo

echo "7. 🌍 Tailscale Status"
echo "---------------------"
tailscale status
echo

echo "8. 📂 Matrix Database Check"
echo "---------------------------"
echo "Database file:"
ls -la /var/lib/matrix-synapse/homeserver.db 2>/dev/null || echo "❌ Database file not found"
echo
echo "Database permissions:"
ls -la /var/lib/matrix-synapse/ | grep homeserver.db 2>/dev/null || echo "❌ No database permissions to check"
echo

echo "9. 🔧 Configuration File Check"
echo "------------------------------"
echo "Homeserver config exists:"
ls -la /etc/matrix-synapse/homeserver.yaml
echo
echo "Server name in config:"
grep "server_name:" /etc/matrix-synapse/homeserver.yaml
echo

echo "10. 🌐 Element Web Check"
echo "------------------------"
echo "Element web files:"
ls -la /var/www/element/ | head -5
echo
echo "Element config:"
if [ -f "/var/www/element/config.json" ]; then
    echo "Config file exists, checking server URL:"
    grep "base_url" /var/www/element/config.json
else
    echo "❌ Element config.json not found"
fi
echo

echo "11. 🔍 Quick Connection Test"
echo "----------------------------"
echo "Testing Matrix API locally:"
curl -s -k https://localhost:8008/_matrix/client/versions | head -3
echo
echo "Testing Element web locally:"
curl -s -k https://localhost/ | grep -i element | head -2
echo

echo "✅ Diagnostic complete!"
echo "📋 Check the output above for any issues"
echo "💡 Common problems:"
echo "   - Matrix service not running (check section 1)"
echo "   - Wrong IP in SSL certificate (check section 6)"  
echo "   - Database permissions issues (check section 8)"
echo "   - Element config pointing to wrong server (check section 10)"
echo "   - Network connectivity issues (check section 3)"
