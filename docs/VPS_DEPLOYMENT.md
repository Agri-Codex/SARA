# SARA VPS Deployment Guide

## Recommended stack
- Ubuntu VPS
- Docker + Docker Compose
- Nginx reverse proxy
- Domain + SSL (Let's Encrypt)

## Steps
1. Clone repository
2. Install Docker + Docker Compose
3. Configure domain DNS
4. Run:
   docker-compose up -d
5. Configure Nginx:
   - frontend -> port 5173
   - backend -> port 8000
6. Enable HTTPS with Certbot

## Recommended providers
- DigitalOcean
- Hetzner
- AWS Lightsail
- Linode

## Future upgrades
- PostgreSQL
- Redis
- Kubernetes
- CDN
- Monitoring dashboards
