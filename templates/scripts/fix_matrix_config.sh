#!/bin/bash

echo "🔧 Matrix Configuration Fixer"
echo "============================="
echo

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Please run as root (use sudo)"
    exit 1
fi

# Get Tailscale IP
TAILSCALE_IP=$(tailscale ip -4 2>/dev/null | head -1)
if [ -z "$TAILSCALE_IP" ]; then
    echo "❌ Could not get Tailscale IP - ensure Tailscale is running"
    exit 1
fi

echo "🌍 Found Tailscale IP: $TAILSCALE_IP"

echo "🔧 Fixing Matrix homeserver configuration..."
# Update server_name to use Tailscale IP
sed -i "s/^server_name:.*/server_name: \"$TAILSCALE_IP\"/" /etc/matrix-synapse/homeserver.yaml

echo "🔧 Fixing Element configuration..."
# Fix Element config to point to correct server
cat > /var/www/element/config.json << EOF
{
    "default_server_config": {
        "m.homeserver": {
            "base_url": "https://$TAILSCALE_IP:8008",
            "server_name": "$TAILSCALE_IP"
        }
    },
    "disable_custom_urls": false,
    "disable_guests": true,
    "disable_login_language_selector": false,
    "disable_3pid_login": false,
    "brand": "Element",
    "integrations_ui_url": "https://scalar.vector.im/",
    "integrations_rest_url": "https://scalar.vector.im/api",
    "integrations_widgets_urls": [
        "https://scalar.vector.im/_matrix/integrations/v1",
        "https://scalar.vector.im/api",
        "https://scalar-staging.vector.im/_matrix/integrations/v1",
        "https://scalar-staging.vector.im/api",
        "https://scalar-staging.riot.im/scalar/api"
    ],
    "bug_report_endpoint_url": "https://element.io/bugreports/submit",
    "defaultCountryCode": "US",
    "showLabsSettings": false,
    "features": {},
    "default_federate": true,
    "default_theme": "dark",
    "roomDirectory": {
        "servers": [
            "$TAILSCALE_IP"
        ]
    }
}
EOF

echo "🔐 Regenerating SSL certificate with correct IP..."
# Backup old certificate
mv /etc/ssl/private/matrix.crt /etc/ssl/private/matrix.crt.backup 2>/dev/null
mv /etc/ssl/private/matrix.key /etc/ssl/private/matrix.key.backup 2>/dev/null

# Generate new certificate with Tailscale IP
openssl req -x509 -newkey rsa:4096 -keyout /etc/ssl/private/matrix.key -out /etc/ssl/private/matrix.crt -days 365 -nodes \
  -subj "/CN=$TAILSCALE_IP/O=FourEyes Chat Server/C=US" \
  -addext "subjectAltName=IP:$TAILSCALE_IP"

# Set proper permissions
chmod 600 /etc/ssl/private/matrix.key
chmod 644 /etc/ssl/private/matrix.crt

echo "🔄 Restarting services..."
systemctl restart matrix-synapse
systemctl restart nginx

echo "⏱️  Waiting for services to start..."
sleep 10

echo "✅ Configuration fixes complete!"
echo "🔍 Testing Matrix API..."
curl -s -k https://localhost:8008/_matrix/client/versions > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ Matrix API is responding"
else
    echo "❌ Matrix API not responding - run matrix_diagnostics.sh for details"
fi

echo
echo "📋 Updated configuration:"
echo "   Server Name: $TAILSCALE_IP"
echo "   Element URL: https://$TAILSCALE_IP/"
echo "   Matrix API: https://$TAILSCALE_IP:8008"
echo
echo "🌐 Try accessing Element at: https://$TAILSCALE_IP/"
