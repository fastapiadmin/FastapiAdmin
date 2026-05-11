---
outline: "deep"
title: Deployment Guide
---
# Deployment Guide

## 📋Deployment Overview

FastapiAdmin supports multiple deployment methods to meet different production environment needs, including Docker Compose, manual deployment, and cloud service deployment.

### Deployment Methods Comparison

| Method | Advantages | Disadvantages | Recommended Scenario |
|--------|------------|---------------|---------------------|
| **Docker Compose** | Easy deployment, consistent environment, easy scaling | Requires Docker knowledge | Production environment, testing environment |
| **Manual Deployment** | Full control, no Docker dependency | Complex setup, environment inconsistencies | Specialized environments, small-scale deployment |
| **Cloud Service** | Managed infrastructure, auto-scaling | Higher cost, less control | Enterprise production, rapid deployment |

## 🐳Docker Compose Deployment

### 1. Prerequisites

- **Docker** installed on the server
- **Docker Compose** installed on the server
- **Server ports** 80 (Nginx) and 8001 (backend) available
- **Minimum server requirements**: 2GB RAM, 2 CPU cores, 20GB disk space

### 2. Deployment Steps

#### Step 1: Clone the repository

```sh
git clone https://github.com/fastapiadmin/FastapiAdmin.git
cd FastapiAdmin
```

#### Step 2: Configure environment variables

```sh
# Copy environment configuration files
cp backend/env/.env.prod.example backend/env/.env.prod
cp frontend/.env.production.example frontend/.env.production

# Edit environment configuration files
# Backend: Set database connection, Redis connection, JWT secret key, etc.
# Frontend: Set API base URL
```

#### Step 3: Execute deployment script

```sh
# Give script execution permission
chmod +x start.sh

# Execute deployment script
./start.sh

# Check deployment status
docker compose ps

# View logs
docker logs -f fastapiadmin-backend
```

### 3. Docker Compose Configuration

```yaml
# docker-compose.yaml
version: '3.8'

networks:
  fastapiadmin-network:
    driver: bridge

volumes:
  mysql-data:
  redis-data:
  logs:



services:
  mysql:
    image: mysql:8.0
    container_name: fastapiadmin-mysql
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: "${MYSQL_ROOT_PASSWORD:-root}"
      MYSQL_DATABASE: "${MYSQL_DATABASE:-fastapiadmin}"
      MYSQL_USER: "${MYSQL_USER:-admin}"
      MYSQL_PASSWORD: "${MYSQL_PASSWORD:-123456}"
    volumes:
      - mysql-data:/var/lib/mysql
      - ./devops/mysql/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "3306:3306"
    networks:
      - fastapiadmin-network


  redis:
    image: redis:7.0
    container_name: fastapiadmin-redis
    restart: always
    volumes:
      - redis-data:/data
    ports:
      - "6379:6379"
    networks:
      - fastapiadmin-network


  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: fastapiadmin-backend
    restart: always
    environment:
      - ENVIRONMENT=prod
    volumes:
      - ./backend:/app
      - logs:/app/logs
    ports:
      - "8001:8001"
    depends_on:
      - mysql
      - redis
    networks:
      - fastapiadmin-network


  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: fastapiadmin-frontend
    restart: always
    volumes:
      - ./frontend:/app
    ports:
      - "5173:5173"
    networks:
      - fastapiadmin-network


  nginx:
    build:
      context: ./devops/nginx
      dockerfile: Dockerfile
    container_name: fastapiadmin-nginx
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./devops/nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./devops/nginx/ssl:/etc/nginx/ssl
    depends_on:
      - backend
      - frontend
    networks:
      - fastapiadmin-network
```

### 4. Nginx Configuration

```nginx
# devops/nginx/nginx.conf
worker_processes  1;

events {
    worker_connections  1024;
}

http {
    include       mime.types;
    default_type  application/octet-stream;

    sendfile        on;
    keepalive_timeout  65;

    server {
        listen       80;
        server_name  localhost;

        location / {
            root   /usr/share/nginx/html;
            index  index.html index.htm;
            try_files $uri $uri/ /index.html;
        }

        location /api/ {
            proxy_pass http://backend:8001;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        location /web/ {
            proxy_pass http://frontend:5173;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   /usr/share/nginx/html;
        }
    }
}
```

### 5. Common Docker Commands

```sh
# View all containers
docker compose ps

# Start all services
docker compose up -d

# Stop all services
docker compose down

# Restart all services
docker compose restart

# View logs for a specific container
docker logs -f fastapiadmin-backend

# View logs for all containers
docker compose logs

# Enter a container
docker exec -it fastapiadmin-backend bash

# Check container resource usage
docker stats

# Remove unused containers, networks, images
docker system prune -f
```

## 🔧Manual Deployment

### 1. Prerequisites

- **Python 3.10+** installed
- **Node.js 20+** installed
- **MySQL 8.0+** installed and running
- **Redis 7.0+** installed and running
- **Nginx** installed (for reverse proxy)
- **System dependencies**: build-essential, libpq-dev, etc.

### 2. Backend Deployment

#### Step 1: Install dependencies

```sh
cd FastapiAdmin/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### Step 2: Configure environment variables

```sh
cp env/.env.prod.example env/.env.prod
# Edit env/.env.prod file
```

#### Step 3: Database initialization

```sh
# Generate migration files
python main.py revision "Initial migration" --env=prod

# Apply migration
python main.py upgrade --env=prod

# Initialize system data
python main.py init
```

#### Step 4: Start backend service

```sh
# Using Gunicorn with Uvicorn workers
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8001

# Or using systemd service (recommended for production)
# Create systemd service file
```

### 3. Frontend Deployment

#### Step 1: Install dependencies

```sh
cd FastapiAdmin/frontend
npm install -g pnpm
pnpm install
```

#### Step 2: Configure environment variables

```sh
cp .env.production.example .env.production
# Edit .env.production file
```

#### Step 3: Build frontend

```sh
pnpm run build
# The built files will be in the dist directory
```

#### Step 4: Deploy frontend files

```sh
# Copy built files to Nginx web root
cp -r dist/* /usr/share/nginx/html/
```

### 4. Nginx Configuration

```nginx
# /etc/nginx/sites-available/fastapiadmin
server {
    listen 80;
    server_name your-domain.com;

    location / {
        root /usr/share/nginx/html;
        index index.html index.htm;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://localhost:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static/ {
        alias /usr/share/nginx/html/static/;
        expires 30d;
    }

    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root /usr/share/nginx/html;
    }
}
```

### 5. Systemd Service Configuration

#### Backend Service

```ini
# /etc/systemd/system/fastapiadmin-backend.service
[Unit]
Description=FastapiAdmin Backend Service
After=network.target mysql.service redis.service

[Service]
User=ubuntu
WorkingDirectory=/path/to/FastapiAdmin/backend
ExecStart=/path/to/FastapiAdmin/backend/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8001
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

#### Start and enable service

```sh
sudo systemctl daemon-reload
sudo systemctl start fastapiadmin-backend
sudo systemctl enable fastapiadmin-backend
sudo systemctl status fastapiadmin-backend
```

## ☁️Cloud Service Deployment

### 1. AWS Deployment

#### Architecture

- **EC2**: For running application containers
- **RDS**: Managed MySQL database
- **ElastiCache**: Managed Redis cache
- **Elastic Load Balancing**: For distributing traffic
- **Auto Scaling**: For automatic scaling based on load
- **S3**: For storing static files and backups
- **CloudWatch**: For monitoring and logging

#### Deployment Steps

1. **Create VPC**: Set up a Virtual Private Cloud
2. **Launch EC2 Instances**: Create EC2 instances for application
3. **Set up RDS**: Create MySQL database instance
4. **Set up ElastiCache**: Create Redis cache cluster
5. **Configure Security Groups**: Set up proper security rules
6. **Deploy Application**: Use Docker Compose on EC2 instances
7. **Set up Load Balancer**: Configure ELB for traffic distribution
8. **Configure Auto Scaling**: Set up scaling policies
9. **Set up CloudWatch**: Configure monitoring and alerts

### 2. Azure Deployment

#### Architecture

- **App Service**: For running application
- **Azure Database for MySQL**: Managed MySQL database
- **Azure Cache for Redis**: Managed Redis cache
- **Azure Load Balancer**: For distributing traffic
- **Azure Storage**: For storing static files
- **Azure Monitor**: For monitoring and logging

#### Deployment Steps

1. **Create Resource Group**: Set up a resource group
2. **Create App Service Plan**: Choose appropriate plan
3. **Deploy App Service**: Deploy application to App Service
4. **Create Azure Database for MySQL**: Set up managed database
5. **Create Azure Cache for Redis**: Set up managed cache
6. **Configure Connection Strings**: Set up environment variables
7. **Set up Monitoring**: Configure Azure Monitor
8. **Enable Auto Scaling**: Set up scaling rules

### 3. Google Cloud Deployment

#### Architecture

- **Compute Engine**: For running application containers
- **Cloud SQL**: Managed MySQL database
- **Memorystore**: Managed Redis cache
- **Load Balancing**: For distributing traffic
- **Auto Scaling**: For automatic scaling
- **Cloud Storage**: For storing static files
- **Cloud Monitoring**: For monitoring and logging

#### Deployment Steps

1. **Create Project**: Set up a Google Cloud project
2. **Enable APIs**: Enable necessary APIs
3. **Create Compute Engine Instances**: Set up VM instances
4. **Create Cloud SQL Instance**: Set up managed MySQL database
5. **Create Memorystore Instance**: Set up managed Redis cache
6. **Deploy Application**: Use Docker Compose on Compute Engine
7. **Set up Load Balancer**: Configure load balancing
8. **Set up Auto Scaling**: Configure instance groups and scaling
9. **Set up Monitoring**: Configure Cloud Monitoring

### 4. Aliyun Deployment

#### Architecture

- **ECS**: Elastic Compute Service for running application
- **RDS**: Relational Database Service for MySQL
- **Redis**: ApsaraDB for Redis
- **SLB**: Server Load Balancer
- **Auto Scaling**: Auto Scaling Service
- **OSS**: Object Storage Service for static files
- **CloudMonitor**: For monitoring and alerts

#### Deployment Steps

1. **Create ECS Instances**: Set up virtual servers
2. **Create RDS Instance**: Set up managed MySQL database
3. **Create Redis Instance**: Set up managed Redis cache
4. **Configure Security Groups**: Set up network security
5. **Deploy Application**: Use Docker Compose on ECS
6. **Set up SLB**: Configure load balancing
7. **Set up Auto Scaling**: Configure scaling rules
8. **Set up OSS**: Configure object storage
9. **Set up CloudMonitor**: Configure monitoring

## 📊Monitoring and Maintenance

### 1. Monitoring Tools

#### Server Monitoring

- **Prometheus + Grafana**: Comprehensive monitoring solution
- **CloudWatch**: For AWS deployments
- **Azure Monitor**: For Azure deployments
- **Cloud Monitoring**: For GCP deployments
- **Nagios**: Open-source monitoring

#### Application Monitoring

- **New Relic**: Application performance monitoring
- **Datadog**: Comprehensive monitoring platform
- **Sentry**: Error tracking and monitoring
- **ELK Stack**: Log management and analysis

### 2. Key Monitoring Metrics

#### Server Metrics

- **CPU Usage**: Monitor CPU utilization
- **Memory Usage**: Monitor memory consumption
- **Disk Usage**: Monitor disk space and I/O
- **Network Traffic**: Monitor network throughput
- **Load Average**: Monitor system load

#### Application Metrics

- **Response Time**: Monitor API response times
- **Request Rate**: Monitor number of requests
- **Error Rate**: Monitor error rates
- **Database Queries**: Monitor database performance
- **Cache Hit Rate**: Monitor Redis cache performance

#### Business Metrics

- **Active Users**: Monitor number of active users
- **Transaction Volume**: Monitor business transactions
- **Conversion Rates**: Monitor conversion metrics
- **Revenue**: Monitor business revenue

### 3. Log Management

#### Centralized Logging

- **ELK Stack**: Elasticsearch, Logstash, Kibana
- **Graylog**: Log management platform
- **Fluentd**: Log collector and aggregator
- **Splunk**: Enterprise log management

#### Log Rotation

```sh
# Configure log rotation for application logs
# /etc/logrotate.d/fastapiadmin
/path/to/FastapiAdmin/backend/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 644 ubuntu ubuntu
}
```

### 4. Backup and Recovery

#### Database Backup

- **Automated Backups**: Enable automated RDS/Azure SQL/Cloud SQL backups
- **Manual Backups**: Schedule regular manual backups
- **Point-in-Time Recovery**: Set up for critical data
- **Off-site Backups**: Store backups in separate location

#### Application Backup

- **Code Repository**: Use Git for code versioning
- **Configuration Files**: Back up configuration files
- **Static Files**: Back up user-uploaded files
- **Docker Images**: Store Docker images in registry

#### Recovery Plan

- **Disaster Recovery Plan**: Document recovery procedures
- **Regular Testing**: Test backup restoration process
- **Recovery Time Objective**: Define acceptable downtime
- **Recovery Point Objective**: Define acceptable data loss

### 5. Security Maintenance

#### Regular Updates

- **Operating System**: Keep OS updated
- **Application Dependencies**: Update dependencies regularly
- **Security Patches**: Apply security patches promptly
- **Docker Images**: Use official, updated images

#### Security Scanning

- **Vulnerability Scanning**: Regularly scan for vulnerabilities
- **Penetration Testing**: Periodic penetration testing
- **Security Audits**: Regular security audits
- **Compliance Checks**: Ensure compliance with standards

#### Access Control

- **Least Privilege**: Follow least privilege principle
- **Access Reviews**: Regularly review user access
- **Multi-factor Authentication**: Enable MFA for admin access
- **SSH Key Management**: Properly manage SSH keys

## 🐛Common Issues and Solutions

### 1. Deployment Issues

#### Docker Compose Issues

**Issue**: Docker Compose fails to start
**Solution**: Check Docker logs, ensure ports are available, verify environment variables

**Issue**: Database connection fails
**Solution**: Check MySQL service status, verify database credentials, ensure network connectivity

**Issue**: Redis connection fails
**Solution**: Check Redis service status, verify Redis URL, ensure network connectivity

#### Nginx Issues

**Issue**: 502 Bad Gateway error
**Solution**: Check backend service status, verify proxy configuration, ensure backend is running

**Issue**: 404 Not Found error
**Solution**: Check Nginx root directory, verify file permissions, ensure files exist

**Issue**: SSL certificate errors
**Solution**: Check SSL configuration, verify certificate validity, ensure proper certificate chain

### 2. Performance Issues

**Issue**: High CPU usage
**Solution**: Optimize application code, increase server resources, implement caching

**Issue**: Slow database queries
**Solution**: Optimize SQL queries, add indexes, consider database sharding

**Issue**: Memory leaks
**Solution**: Profile application, fix memory leaks, increase memory limit

**Issue**: Network latency
**Solution**: Use CDN for static files, optimize API responses, consider edge caching

### 3. Security Issues

**Issue**: Unauthorized access
**Solution**: Implement proper authentication, use HTTPS, configure firewalls

**Issue**: SQL injection
**Solution**: Use parameterized queries, validate input, use ORM

**Issue**: Cross-site scripting (XSS)
**Solution**: Sanitize user input, use Content Security Policy, escape output

**Issue**: Cross-site request forgery (CSRF)
**Solution**: Implement CSRF tokens, validate Origin header, use SameSite cookies

### 4. Scaling Issues

**Issue**: Application not scaling properly
**Solution**: Check auto-scaling configuration, ensure load balancer is working, optimize application for scaling

**Issue**: Database bottleneck
**Solution**: Implement database replication, use read replicas, consider sharding

**Issue**: Cache inconsistency
**Solution**: Implement proper cache invalidation, use distributed cache, consider cache warming

**Issue**: Session management
**Solution**: Use Redis for session storage, implement stateless sessions, consider JWT

## 📚Best Practices

### 1. Deployment Best Practices

- **Infrastructure as Code**: Use Terraform or CloudFormation for infrastructure
- **CI/CD Pipeline**: Implement continuous integration and deployment
- **Environment Consistency**: Use Docker for consistent environments
- **Rolling Deployments**: Use rolling deployments to minimize downtime
- **Blue-Green Deployment**: Use blue-green deployment for zero downtime
- **Canary Releases**: Test new versions with a subset of users

### 2. Monitoring Best Practices

- **Comprehensive Monitoring**: Monitor all components of the system
- **Proactive Alerting**: Set up alerts for potential issues
- **Anomaly Detection**: Use machine learning for anomaly detection
- **Log Aggregation**: Centralize logs for easier analysis
- **Performance Baselines**: Establish performance baselines for comparison
- **Dashboards**: Create comprehensive monitoring dashboards

### 3. Security Best Practices

- **Defense in Depth**: Implement multiple layers of security
- **Principle of Least Privilege**: Grant minimum required permissions
- **Regular Audits**: Conduct regular security audits
- **Security Training**: Train developers on security best practices
- **Incident Response Plan**: Have a plan for security incidents
- **Compliance**: Ensure compliance with relevant regulations

### 4. Maintenance Best Practices

- **Regular Backups**: Schedule regular backups
- **Backup Testing**: Test backup restoration regularly
- **Documentation**: Keep comprehensive documentation
- **Change Management**: Implement change management process
- **Disaster Recovery Plan**: Have a disaster recovery plan
- **Knowledge Transfer**: Ensure knowledge is shared among team members

## 🎉Conclusion

FastapiAdmin provides flexible deployment options to meet different production environment needs. Whether you choose Docker Compose for ease of deployment, manual deployment for full control, or cloud services for managed infrastructure, FastapiAdmin can be deployed reliably and securely.

By following the best practices outlined in this guide, you can ensure that your FastapiAdmin deployment is scalable, secure, and maintainable. Regular monitoring, backups, and security maintenance are essential for keeping your application running smoothly and securely.

For more detailed information about specific deployment methods or cloud providers, please refer to their official documentation.