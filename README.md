# Flask Web Application with Redis

A Flask web application that demonstrates Redis integration with Docker deployment. The app connects to a Redis instance running on the host machine with authentication.

## Project Structure

```
flask-redis-app/
├── app.py                 # Main Flask application
├── templates/
│   └── index.html        # Web interface
├── requirements.txt      # Python dependencies
├── Dockerfile           # Docker image configuration
├── docker-compose.yaml  # Docker Compose configuration
├── .env.example         # Environment variables template
└── README.md           # This file
```

## Prerequisites

1. **Docker and Docker Compose** installed on your system
2. **Redis server** running on your host machine with:
   - Authentication enabled (username and password)
   - Accessible on port 6379 (or your custom port)

## Redis Setup on Host

Before running the Flask app, ensure Redis is configured with authentication:

### Option 1: Redis with ACL (Redis 6+)

```bash
# Edit redis.conf
sudo nano /etc/redis/redis.conf

# Add or modify these lines:
user myuser on >mypassword ~* &* +@all
requirepass mypassword

# Restart Redis
sudo systemctl restart redis
```

### Option 2: Redis with Basic Password

```bash
# Edit redis.conf
sudo nano /etc/redis/redis.conf

# Add or modify:
requirepass mypassword

# Restart Redis
sudo systemctl restart redis
```

### Test Redis Connection

```bash
# Test with password
redis-cli -a mypassword ping
# Should return: PONG

# Test with user and password (Redis 6+)
redis-cli --user myuser --pass mypassword ping
# Should return: PONG
```

## Setup Instructions

### 1. Clone or Create Project Directory

```bash
mkdir flask-redis-app
cd flask-redis-app
```

### 2. Create Project Files

Copy all the provided files into your project directory:
- `app.py`
- `templates/index.html`
- `requirements.txt`
- `Dockerfile`
- `docker-compose.yaml`

### 3. Configure Environment Variables

Update the `docker-compose.yaml` file with your Redis credentials:

```yaml
environment:
  - REDIS_HOST=host.docker.internal
  - REDIS_PORT=6379
  - REDIS_USER=myuser          # Change this
  - REDIS_PASSWORD=mypassword  # Change this
  - REDIS_DB=0
```

### 4. Build and Run with Docker Compose

```bash
# Build the Docker image
docker-compose build

# Start the application
docker-compose up -d

# View logs
docker-compose logs -f
```

### 5. Access the Application

Open your browser and navigate to:
```
http://localhost:5000
```

## Application Features

The web interface provides:

1. **Connection Status** - Check Redis connectivity
2. **Set Key-Value** - Store data in Redis
3. **Get Value** - Retrieve data by key
4. **Delete Key** - Remove data from Redis
5. **Counter Operations** - Increment counters
6. **View All Data** - Display all stored keys and values

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Web interface |
| GET | `/health` | Health check endpoint |
| POST | `/set` | Set a key-value pair |
| GET | `/get/<key>` | Get value by key |
| DELETE | `/delete/<key>` | Delete a key |
| GET | `/all` | Get all stored data |
| POST | `/counter/increment` | Increment a counter |

## Docker Commands

```bash
# Start the application
docker-compose up -d

# Stop the application
docker-compose down

# View logs
docker-compose logs -f flask-app

# Rebuild after code changes
docker-compose up -d --build

# Access container shell
docker exec -it flask-redis-app /bin/bash
```

## Troubleshooting

### Connection Refused Error

If you see "Connection refused" errors:

1. Verify Redis is running on host:
   ```bash
   sudo systemctl status redis
   ```

2. Check Redis is listening:
   ```bash
   netstat -tulpn | grep 6379
   ```

3. Ensure Redis allows connections from Docker:
   ```bash
   # In redis.conf, set:
   bind 127.0.0.1 ::1
   ```

### Authentication Errors

If you get authentication errors:

1. Verify credentials in `docker-compose.yaml`
2. Test Redis authentication:
   ```bash
   redis-cli --user myuser --pass mypassword ping
   ```

### Docker Network Issues

For Windows/Mac, `host.docker.internal` should work automatically.

For Linux, you may need to use:
```yaml
environment:
  - REDIS_HOST=172.17.0.1  # Docker bridge IP
```

Or run Redis in Docker and use Docker networking instead.

## Development Mode

To run without Docker for development:

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export REDIS_HOST=localhost
export REDIS_USER=myuser
export REDIS_PASSWORD=mypassword

# Run the app
python app.py
```

## Technologies Used

- **Flask** - Web framework
- **Redis** - In-memory data store
- **Docker** - Containerization
- **Gunicorn** - WSGI HTTP Server
- **HTML/CSS/JavaScript** - Frontend

## Security Notes

- Never commit real passwords to version control
- Use environment variables for sensitive data
- Consider using Docker secrets for production
- Implement proper authentication for production deployments

## License

This is a lab exercise project for educational purposes.