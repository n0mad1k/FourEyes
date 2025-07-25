# Matrix Server Helper Scripts

This directory contains helper scripts for troubleshooting and managing your Matrix server.

## Scripts Available

### 🔍 matrix_diagnostics.sh
Comprehensive diagnostic script that checks:
- Matrix Synapse service status
- Network ports and connectivity
- SSL certificates
- Database permissions
- Configuration files
- Recent logs

**Usage:** `sudo ./matrix_diagnostics.sh`

### 🔄 restart_matrix.sh
Safely restarts Matrix Synapse with proper cleanup:
- Stops Matrix service cleanly
- Fixes database permissions
- Restarts service and checks status

**Usage:** `sudo ./restart_matrix.sh`

### 🔧 fix_matrix_config.sh
Fixes common configuration issues:
- Updates server name to use Tailscale IP
- Regenerates SSL certificates with correct IP
- Fixes Element web configuration
- Restarts services

**Usage:** `sudo ./fix_matrix_config.sh`

### 👀 monitor_matrix.sh
Real-time monitoring of Matrix services:
- Continuous status checks
- API response monitoring
- Error detection

**Usage:** `./monitor_matrix.sh`

### 📝 view_matrix_logs.sh
Interactive log viewer with options:
- View recent logs
- Follow live logs
- Search for errors/warnings
- Custom text search

**Usage:** `./view_matrix_logs.sh`

## Quick Troubleshooting

If Element UI is hanging or showing black screen:

1. Run diagnostics: `sudo ./matrix_diagnostics.sh`
2. If issues found, try: `sudo ./fix_matrix_config.sh`
3. If still issues: `sudo ./restart_matrix.sh`
4. Monitor status: `./monitor_matrix.sh`

## Common Issues

- **Black screen in Element**: Usually SSL certificate or server configuration
- **Login hanging**: Often database permissions or API connectivity
- **Can't connect**: Check Tailscale IP and firewall settings
