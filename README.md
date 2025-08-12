# PT MARS DATA TELEKOMUNIKASI
## Network Management System

A comprehensive network management system with MikroTik API integration, RADIUS billing, and automated traffic monitoring.

## Features

### 🔐 Authentication & Authorization
- Role-based access control (Admin, Operator, Viewer)
- JWT token authentication
- Secure login system

### 🌐 MikroTik Integration
- Real-time device monitoring
- Interface traffic statistics
- CPU and memory monitoring
- PPPoE session management
- User traffic tracking
- Remote device configuration

### 💰 Billing System
- Automated invoice generation
- Payment tracking and management
- Overdue account isolation
- Revenue reporting
- Multiple payment methods support

### 📊 RADIUS Integration
- User authentication via RADIUS
- Accounting data collection
- Session management
- Bandwidth profile enforcement

### 📈 Reporting & Analytics
- Daily, weekly, monthly, yearly reports
- Traffic usage reports
- Billing and revenue reports
- Downloadable reports (CSV, Excel, PDF)
- Real-time dashboard

### 🔒 Security Features
- Firewall configuration
- Fail2ban integration
- Security headers
- Input validation
- SQL injection protection

## Quick Installation (Ubuntu 20.04)

### One-Click Installation
```bash
# Download and run the installation script
wget https://github.com/your-repo/mars-data/archive/main.zip
unzip main.zip
cd mars-data-main
chmod +x install_ubuntu.sh
./install_ubuntu.sh
```

### Manual Installation

#### 1. System Requirements
- Ubuntu 20.04 LTS
- Python 3.8+
- Nginx
- SQLite/PostgreSQL
- Redis (optional)

#### 2. Install Dependencies
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv nginx
```

#### 3. Clone and Setup
```bash
git clone https://github.com/your-repo/mars-data.git
cd mars-data
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 4. Configure Environment
```bash
cp .env.example .env
# Edit .env with your configuration
```

#### 5. Initialize Database
```bash
python -c "from app.database import engine; from app.models import *; Base.metadata.create_all(engine)"
```

#### 6. Start Application
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Configuration

### Environment Variables
```bash
# Database
DATABASE_URL=sqlite:///./mars_data.db

# Security
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# MikroTik
MIKROTIK_DEFAULT_PORT=8728
MIKROTIK_API_TIMEOUT=10

# RADIUS
RADIUS_SECRET=your-radius-secret
RADIUS_AUTH_PORT=1812
RADIUS_ACCT_PORT=1813

# Billing
BILLING_CURRENCY=IDR
BILLING_TIMEZONE=Asia/Jakarta
```

### Default Credentials
- **Username**: admin
- **Password**: admin123

⚠️ **Important**: Change the default password immediately after installation!

## API Documentation

After installation, access the interactive API documentation at:
- Swagger UI: `http://your-server/docs`
- ReDoc: `http://your-server/redoc`

### Key API Endpoints

#### Authentication
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/me` - Get current user info

#### MikroTik Management
- `GET /api/v1/mikrotik/devices` - List MikroTik devices
- `POST /api/v1/mikrotik/devices` - Add new device
- `GET /api/v1/mikrotik/devices/{id}/stats` - Get device statistics
- `GET /api/v1/mikrotik/devices/{id}/interfaces` - Interface statistics
- `GET /api/v1/mikrotik/devices/{id}/pppoe` - PPPoE users

#### Billing
- `GET /api/v1/billing/accounts` - List billing accounts
- `POST /api/v1/billing/accounts` - Create new account
- `GET /api/v1/billing/payments` - List payments
- `GET /api/v1/billing/stats` - Billing statistics

#### Reports
- `GET /api/v1/reports/traffic` - Traffic reports
- `GET /api/v1/reports/billing` - Billing reports
- `GET /api/v1/reports/download/{type}` - Download reports

## Usage

### Adding MikroTik Devices
1. Login to the web interface
2. Navigate to "MikroTik Devices"
3. Click "Add Device"
4. Enter device details (IP, username, password)
5. Test connection and save

### Managing Billing Accounts
1. Go to "Billing" section
2. Add customer accounts with package details
3. Set up automatic billing schedules
4. Monitor payment status

### Generating Reports
1. Navigate to "Reports" section
2. Select report type and date range
3. View online or download in various formats

### User Management
1. Access "Users" section (Admin only)
2. Create users with appropriate roles
3. Manage permissions and access levels

## Monitoring & Maintenance

### Service Management
```bash
# Check service status
sudo systemctl status mars-data

# Start/Stop/Restart
sudo systemctl start mars-data
sudo systemctl stop mars-data
sudo systemctl restart mars-data

# View logs
sudo journalctl -u mars-data -f
```

### Database Backup
```bash
# SQLite backup
cp mars_data.db mars_data_backup_$(date +%Y%m%d).db

# PostgreSQL backup (if using PostgreSQL)
pg_dump mars_data > mars_data_backup_$(date +%Y%m%d).sql
```

### Security Updates
```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Update Python dependencies
pip install --upgrade -r requirements.txt
```

## Troubleshooting

### Common Issues

#### Service won't start
```bash
# Check logs
sudo journalctl -u mars-data -n 50

# Check Python environment
source venv/bin/activate
python -c "import app.main"
```

#### Database connection errors
- Verify DATABASE_URL in .env
- Check database file permissions
- Ensure database tables are created

#### MikroTik connection issues
- Verify MikroTik API is enabled
- Check firewall rules (port 8728)
- Validate credentials and IP address

### Performance Optimization

#### Database Optimization
- Use PostgreSQL for production
- Add database indexes
- Regular database maintenance

#### Caching
- Enable Redis for session storage
- Implement API response caching
- Use CDN for static files

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

Copyright © 2024 PT MARS DATA TELEKOMUNIKASI
All rights reserved.

## Support

For technical support and inquiries:
- Email: support@marsdata.com
- Phone: +62-xxx-xxxx-xxxx
- Website: https://marsdata.com

## Changelog

### Version 1.0.0 (2024-01-01)
- Initial release
- MikroTik API integration
- RADIUS billing system
- Traffic monitoring
- User management
- Automated reporting
- Ubuntu 20.04 installer