# FourEyes - Secure Chat Server Deployment Platform

![FourEyes Logo](https://img.shields.io/badge/FourEyes-Secure%20Chat-green)
![Version](https://img.shields.io/badge/version-2.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## 🔒 Overview

FourEyes is a modular deployment platform for secure Matrix chat servers with VPN-only access. Built for teams requiring secure, private communications with enterprise-grade security features.

## 🚀 Quick Start

```bash
# 1. Clone and setup
git clone <repository>
cd FourEyes

# 2. Configure deployment
cp vars-template.yaml vars.yaml
# Edit vars.yaml with your settings

# 3. Deploy basic chat server
python3 setup.py

# 4. Select deployment type:
# - Basic Chat Server (Matrix + Element)
# - Red Team Chat Server (Enhanced security + tactical features)
# - Intel Chat Server (OSINT bots + data feeds)
# - ATAK Integration Server (Military coordination)
```

## 📁 Deployment Types

### 🗣️ Basic Chat Server (`basic-chat.yaml`)
- Matrix-Synapse homeserver
- Element web client
- Tailscale VPN integration
- Self-signed SSL certificates
- Basic security hardening

**Use Case:** General secure team communications

### ⚔️ Red Team Chat Server (`redteam-chat.yaml`)
- All basic features plus:
- Advanced security monitoring
- Geographic IP filtering
- Enhanced encryption
- Operational security features
- Covert communication channels

**Use Case:** Red team operations, penetration testing

### 🕵️ Intel Chat Server (`intel-chat.yaml`)
- All basic features plus:
- OSINT data collection bots
- Threat intelligence feeds
- Automated reporting channels
- Dark web monitoring
- CVE/vulnerability alerts

**Use Case:** Threat intelligence, security research

### 🎯 ATAK Integration Server (`atak-chat.yaml`)
- All basic features plus:
- ATAK-CIV server integration
- Tactical data webhooks
- Geospatial data sharing
- Mission coordination features
- Real-time situational awareness

**Use Case:** Military/tactical operations, emergency response

## 🔧 Configuration

### Core Configuration (`vars.yaml`)
```yaml
# Deployment Settings
deployment_name: "my-secure-chat"  # Used for all service naming
deployment_type: "basic"           # basic, redteam, intel, atak

# Infrastructure
linode_token: "your-token"
tailscale_auth_key: "your-key"
ssh_public_key: "your-key"

# Matrix Settings
matrix_admin_user: "admin"
matrix_admin_password: "secure-password"

# Optional: Type-specific settings
redteam_features:
  covert_mode: true
  advanced_monitoring: true

intel_features:
  osint_bots: true
  threat_feeds: true

atak_features:
  server_port: 8089
  ssl_enabled: true
```

### Security Settings
- **VPN-Only Access:** All deployments require Tailscale VPN
- **Geographic Filtering:** Optional US-only access restriction
- **SSL/TLS:** Auto-generated certificates with deployment naming
- **Fail2Ban:** Advanced intrusion prevention
- **Firewall:** UFW with VPN-only rules

## 🏗️ Architecture

```
FourEyes Deployment
├── Matrix Homeserver (Port 8008 → 443)
├── Element Web Client (Served via nginx)
├── Tailscale VPN (100.x.x.x network)
├── Dashboard (Port 8443, VPN-only)
└── Security Layer (Fail2Ban, UFW, Geographic filtering)
```

## 📊 Management

### Status Check
```bash
# On deployed server
sudo /usr/local/bin/foureyes-status.sh
```

### Access URLs
- **Matrix Chat:** `https://[TAILSCALE-IP]`
- **Dashboard:** `https://[TAILSCALE-IP]:8443`
- **CA Certificate:** `https://[TAILSCALE-IP]:8443/ca/`

### User Management
```bash
# Create additional users
sudo /opt/venvs/matrix-synapse/bin/register_new_matrix_user \
  -c /etc/matrix-synapse/homeserver.yaml \
  -u newuser -p password -a
```

## 🔄 Deployment Workflow

1. **Infrastructure Setup:** Linode instance with SSH keys
2. **VPN Configuration:** Tailscale with consistent naming
3. **Base Services:** nginx, Matrix-Synapse, Element
4. **Security Hardening:** UFW, Fail2Ban, SSL/TLS
5. **Type-Specific Features:** Based on deployment type
6. **User Creation:** Admin user with secure credentials
7. **Health Checks:** Service validation and status

## 🛡️ Security Features

- **Zero-Trust Network:** VPN required for all access
- **Certificate Pinning:** Self-signed with deployment-specific naming
- **Access Control:** nginx-level IP restrictions
- **Intrusion Detection:** Real-time monitoring and alerting
- **Audit Logging:** Comprehensive security event tracking
- **Geographic Filtering:** Optional country-based restrictions

## 🔧 Troubleshooting

### Common Issues

**Matrix Login Hangs:**
```bash
# Check service status
sudo systemctl status matrix-synapse
sudo journalctl -u matrix-synapse -f

# Verify Tailscale IP consistency
sudo tailscale ip -4
sudo grep server_name /etc/matrix-synapse/homeserver.yaml
```

**VPN Access Issues:**
```bash
# Check Tailscale status
sudo tailscale status
sudo tailscale ping [PEER-IP]

# Verify nginx configuration
sudo nginx -t
sudo systemctl status nginx
```

**Certificate Problems:**
```bash
# Regenerate certificates
sudo openssl req -new -newkey rsa:4096 -days 365 -nodes -x509 \
  -keyout /etc/ssl/private/nginx-selfsigned.key \
  -out /etc/ssl/certs/nginx-selfsigned.crt \
  -subj "/CN=[TAILSCALE-IP]/O=[DEPLOYMENT-NAME]/C=US"
```

## 📈 Monitoring

### Built-in Monitoring
- Service health checks
- VPN connectivity monitoring
- Security event alerting
- Resource usage tracking

### Log Locations
- **Matrix:** `/var/log/matrix-synapse/`
- **nginx:** `/var/log/nginx/`
- **Security:** `/var/log/foureyes-security.log`
- **VPN:** `/var/log/nginx/foureyes_vpn.log`

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-deployment-type`
3. Add your deployment type in `deployments/`
4. Update documentation
5. Submit pull request

## 📋 Roadmap

- [ ] **v2.1:** Kubernetes deployment support
- [ ] **v2.2:** Multi-homeserver federation
- [ ] **v2.3:** Mobile app integration
- [ ] **v2.4:** Advanced ATAK features
- [ ] **v2.5:** AI-powered threat detection

## 📞 Support

- **Documentation:** See `docs/` directory
- **Issues:** GitHub Issues
- **Security:** Report to security@foureyes.local

## 📄 License

MIT License - see LICENSE file for details.

---

*Built for secure communications by security professionals.*
