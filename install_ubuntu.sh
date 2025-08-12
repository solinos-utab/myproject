#!/bin/bash

# PT MARS DATA TELEKOMUNIKASI - Auto Installation Script for Ubuntu 20.04
# This script installs the complete network management system with MikroTik integration

set -e

echo "=========================================="
echo "PT MARS DATA TELEKOMUNIKASI"
echo "Network Management System Installation"
echo "=========================================="

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo "This script should not be run as root for security reasons"
   echo "Please run as a regular user with sudo privileges"
   exit 1
fi

# Update system
echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python 3.9+ and pip
echo "Installing Python and dependencies..."
sudo apt install -y python3 python3-pip python3-venv python3-dev
sudo apt install -y build-essential libssl-dev libffi-dev
sudo apt install -y nginx supervisor redis-server

# Install Node.js for frontend (if needed)
echo "Installing Node.js..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Create application directory
APP_DIR="/opt/mars-data"
echo "Creating application directory: $APP_DIR"
sudo mkdir -p $APP_DIR
sudo chown $USER:$USER $APP_DIR

# Copy application files
echo "Setting up application..."
cp -r . $APP_DIR/
cd $APP_DIR

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create environment file
echo "Creating environment configuration..."
cat > .env << EOF
# PT MARS DATA TELEKOMUNIKASI Configuration
DATABASE_URL=sqlite:///./mars_data.db
SECRET_KEY=mars-data-$(openssl rand -hex 32)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# MikroTik Settings
MIKROTIK_DEFAULT_PORT=8728
MIKROTIK_API_TIMEOUT=10

# RADIUS Settings
RADIUS_SECRET=mars-radius-$(openssl rand -hex 16)
RADIUS_AUTH_PORT=1812
RADIUS_ACCT_PORT=1813

# Billing Settings
BILLING_CURRENCY=IDR
BILLING_TIMEZONE=Asia/Jakarta

# Report Settings
REPORT_STORAGE_PATH=./reports
EOF

# Create directories
mkdir -p reports logs static

# Set up database
echo "Setting up database..."
python -c "
from sqlalchemy import create_engine
from app.models.user import Base as UserBase
from app.models.mikrotik import Base as MikroTikBase  
from app.models.billing import Base as BillingBase
from app.models.radius import Base as RadiusBase
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
UserBase.metadata.create_all(engine)
MikroTikBase.metadata.create_all(engine)
BillingBase.metadata.create_all(engine)
RadiusBase.metadata.create_all(engine)
print('Database tables created successfully')
"

# Create systemd service
echo "Creating systemd service..."
sudo tee /etc/systemd/system/mars-data.service > /dev/null << EOF
[Unit]
Description=PT MARS DATA TELEKOMUNIKASI Network Management System
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$APP_DIR
Environment=PATH=$APP_DIR/venv/bin
ExecStart=$APP_DIR/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Configure Nginx
echo "Configuring Nginx..."
sudo tee /etc/nginx/sites-available/mars-data << EOF
server {
    listen 80;
    server_name _;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'" always;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    location /static {
        alias $APP_DIR/static;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/mars-data /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Configure firewall
echo "Configuring firewall..."
sudo ufw --force enable
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 8728/tcp  # MikroTik API
sudo ufw allow 1812/udp  # RADIUS Auth
sudo ufw allow 1813/udp  # RADIUS Accounting

# Install fail2ban for additional security
echo "Installing fail2ban..."
sudo apt install -y fail2ban

sudo tee /etc/fail2ban/jail.local << EOF
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[sshd]
enabled = true

[nginx-http-auth]
enabled = true

[nginx-noscript]
enabled = true

[nginx-badbots]
enabled = true

[nginx-noproxy]
enabled = true
EOF

# Start services
echo "Starting services..."
sudo systemctl daemon-reload
sudo systemctl enable mars-data
sudo systemctl start mars-data
sudo systemctl enable nginx
sudo systemctl restart nginx
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# Create admin user script
echo "Creating admin user setup script..."
cat > create_admin.py << EOF
#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from passlib.context import CryptContext
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.user import User, UserRole
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_admin_user():
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    # Check if admin exists
    existing_admin = db.query(User).filter(User.username == "admin").first()
    if existing_admin:
        print("Admin user already exists!")
        return
    
    # Create admin user
    hashed_password = pwd_context.hash("admin123")
    admin_user = User(
        username="admin",
        email="admin@marsdata.com",
        hashed_password=hashed_password,
        full_name="System Administrator",
        role=UserRole.ADMIN,
        is_active=True
    )
    
    db.add(admin_user)
    db.commit()
    db.close()
    
    print("Admin user created successfully!")
    print("Username: admin")
    print("Password: admin123")
    print("Please change the password after first login!")

if __name__ == "__main__":
    create_admin_user()
EOF

chmod +x create_admin.py

# Run admin user creation
echo "Creating default admin user..."
$APP_DIR/venv/bin/python create_admin.py

# Final status check
echo "Checking service status..."
sleep 5
sudo systemctl status mars-data --no-pager
sudo systemctl status nginx --no-pager

echo "=========================================="
echo "Installation completed successfully!"
echo "=========================================="
echo ""
echo "Service Information:"
echo "- Application: http://$(hostname -I | awk '{print $1}')"
echo "- API Documentation: http://$(hostname -I | awk '{print $1}')/docs"
echo "- Admin Username: admin"
echo "- Admin Password: admin123"
echo ""
echo "Important Notes:"
echo "1. Change the default admin password immediately"
echo "2. Configure your MikroTik devices in the web interface"
echo "3. Set up RADIUS server integration"
echo "4. Configure SSL certificate for production use"
echo "5. Backup the database regularly"
echo ""
echo "Log files location: $APP_DIR/logs"
echo "Configuration file: $APP_DIR/.env"
echo ""
echo "To manage the service:"
echo "- Start: sudo systemctl start mars-data"
echo "- Stop: sudo systemctl stop mars-data"
echo "- Restart: sudo systemctl restart mars-data"
echo "- Status: sudo systemctl status mars-data"
echo ""
echo "For support, contact PT MARS DATA TELEKOMUNIKASI"
echo "=========================================="
EOF

chmod +x install_ubuntu.sh