#!/bin/bash

echo "👀 Matrix Live Monitor"
echo "====================="
echo

echo "📊 Press Ctrl+C to stop monitoring"
echo "-----------------------------------"
echo

# Function to check matrix status
check_matrix() {
    echo "$(date '+%H:%M:%S') - Checking Matrix status..."
    
    # Check service
    if systemctl is-active --quiet matrix-synapse; then
        echo "  ✅ Matrix Synapse service: RUNNING"
    else
        echo "  ❌ Matrix Synapse service: STOPPED"
    fi
    
    # Check API
    if curl -s -k https://localhost:8008/_matrix/client/versions > /dev/null 2>&1; then
        echo "  ✅ Matrix API: RESPONDING"
    else
        echo "  ❌ Matrix API: NOT RESPONDING"
    fi
    
    # Check Element
    if curl -s -k https://localhost/ | grep -q element 2>/dev/null; then
        echo "  ✅ Element Web: RESPONDING"
    else
        echo "  ❌ Element Web: NOT RESPONDING"
    fi
    
    # Check recent errors
    ERROR_COUNT=$(tail -n 50 /var/log/matrix-synapse/homeserver.log 2>/dev/null | grep -i error | wc -l)
    if [ "$ERROR_COUNT" -gt 0 ]; then
        echo "  ⚠️  Recent errors in log: $ERROR_COUNT"
    else
        echo "  ✅ No recent errors in log"
    fi
    
    echo
}

# Monitor loop
while true; do
    check_matrix
    sleep 30
done
