# LawViksh Backend API

A FastAPI-based backend server for the LawViksh joining list and feedback system.

## 🚀 Features

- **User Registration**: Join as user or creator
- **Not Interested Form**: Collect feedback from non-interested users
- **Feedback System**: Comprehensive feedback collection with ratings
- **Admin Panel**: Secure admin access with JWT authentication
- **Data Analytics**: User and feedback analytics
- **Data Export**: Download data in JSON format
- **MySQL Integration**: Robust database management

## 📋 Prerequisites

- Python 3.8+
- MySQL 8.0+
- pip (Python package manager)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd betajoin
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up MySQL database**
   ```bash
   # Import the database schema
   mysql -u root -p < lawdata.sql
   ```

4. **Configure environment variables**
   ```bash
   # Copy and edit the config.py file
   # Update database credentials and other settings
   ```

## ⚙️ Configuration

Edit `config.py` to configure your settings:

```python
# Database Configuration
db_host: str = "localhost"
db_port: int = 3306
db_name: str = "lawviksh_joining_list"
db_user: str = "your_username"
db_password: str = "your_password"

# Security Configuration
secret_key: str = "your_super_secret_key_here"
admin_username: str = "admin"
admin_password: str = "admin123"
```

## 🚀 Running the Application

### Development Mode
```bash
python appmain.py
```

### Production Mode
```bash
python wsgi.py
```

### Using Uvicorn
```bash
uvicorn appmain:app --host 0.0.0.0 --port 8000
```

### Using Gunicorn (Production)
```bash
gunicorn wsgi:application -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **Health Check**: `http://localhost:8000/health`

## 🔐 API Endpoints

### Authentication
- `POST /api/auth/adminlogin` - Admin login
- `GET /api/auth/verify` - Verify admin token

### User Management
- `POST /api/users/userdata` - Register user
- `POST /api/users/creatordata` - Register creator
- `POST /api/users/notinteresteddata` - Submit not interested feedback
- `GET /api/users/registereduserdata` - Get all users (Admin)
- `GET /api/users/registeredcreatordata` - Get all creators (Admin)
- `GET /api/users/analytics` - Get user analytics (Admin)

### Feedback
- `POST /api/feedback/submit` - Submit feedback
- `GET /api/feedback/all` - Get all feedback (Admin)
- `GET /api/feedback/analytics` - Get feedback analytics (Admin)
- `GET /api/feedback/summary` - Get feedback summary (Admin)

### Data Management
- `POST /api/data/downloaddata` - Download all data (Admin)
- `GET /api/data/export/json` - Export data as JSON file (Admin)
- `GET /api/data/stats` - Get data statistics (Admin)

## 🔒 Security

- JWT-based authentication for admin endpoints
- Password hashing with bcrypt
- CORS middleware for cross-origin requests
- Input validation with Pydantic models
- SQL injection protection with parameterized queries

## 📊 Database Schema

The application uses the following main tables:
- `users` - User and creator registrations
- `not_interested_users` - Not interested feedback
- `feedback_forms` - Main feedback records
- `ui_ratings` - User interface ratings
- `ux_ratings` - User experience ratings
- `suggestions_and_needs` - Suggestions and legal needs
- `form_submissions_log` - Audit trail

## 🏗️ Project Structure

```
betajoin/
├── app/
│   ├── models/          # Pydantic models
│   ├── schemas/         # Response schemas
│   ├── repository/      # Database operations
│   ├── services/        # Business logic
│   └── routing/         # API routes
├── config.py           # Configuration settings
├── database.py         # Database connection
├── appmain.py          # Main application
├── wsgi.py            # WSGI application
├── requirements.txt    # Dependencies
├── lawdata.sql        # Database schema
└── README.md          # This file
```

## 🚀 Deployment

### VPS Deployment

1. **Install system dependencies**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip mysql-server nginx
   ```

2. **Set up MySQL**
   ```bash
   sudo mysql_secure_installation
   mysql -u root -p < lawdata.sql
   ```

3. **Install Python dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

4. **Configure Nginx**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

5. **Run with systemd**
   ```bash
   # Create service file
   sudo nano /etc/systemd/system/lawviksh.service
   
   [Unit]
   Description=LawViksh Backend
   After=network.target
   
   [Service]
   User=www-data
   WorkingDirectory=/path/to/betajoin
   Environment="PATH=/path/to/betajoin/venv/bin"
   ExecStart=/path/to/betajoin/venv/bin/gunicorn wsgi:application -w 4 -k uvicorn.workers.UvicornWorker --bind 127.0.0.1:8000
   
   [Install]
   WantedBy=multi-user.target
   ```

6. **Start the service**
   ```bash
   sudo systemctl enable lawviksh
   sudo systemctl start lawviksh
   ```

## 🔧 Environment Variables

Create a `.env` file for production:

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=lawviksh_joining_list
DB_USER=your_db_user
DB_PASSWORD=your_db_password
SECRET_KEY=your_super_secret_key
ADMIN_USERNAME=admin
ADMIN_PASSWORD=secure_password
HOST=0.0.0.0
PORT=8000
DEBUG=False
```

## 📝 Usage Examples

### Register a User
```bash
curl -X POST "http://localhost:8000/api/users/userdata" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone_number": "+1234567890",
    "gender": "Male",
    "profession": "Student",
    "interest_reason": "Interested in legal resources"
  }'
```

### Admin Login
```bash
curl -X POST "http://localhost:8000/api/auth/adminlogin" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

### Submit Feedback
```bash
curl -X POST "http://localhost:8000/api/feedback/submit" \
  -H "Content-Type: application/json" \
  -d '{
    "user_email": "user@example.com",
    "visual_design_rating": 4,
    "ease_of_navigation_rating": 5,
    "overall_satisfaction_rating": 4,
    "liked_features": "Clean interface",
    "improvement_suggestions": "Add more features"
  }'
```

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check MySQL service is running
   - Verify database credentials in config.py
   - Ensure database exists

2. **Import Errors**
   - Install all dependencies: `pip install -r requirements.txt`
   - Check Python version (3.8+ required)

3. **Permission Errors**
   - Ensure proper file permissions
   - Check database user permissions

### Logs

Check application logs:
```bash
# If using systemd
sudo journalctl -u lawviksh -f

# If running directly
python appmain.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

For support and questions:
- Create an issue in the repository
- Contact the development team

---

**LawViksh Backend API** - Built with FastAPI and MySQL 