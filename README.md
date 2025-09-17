# 🚀 Crypto Tracker

A comprehensive cryptocurrency tracking application consisting of a FastAPI backend and a Telegram bot. Track real-time cryptocurrency prices, market data, and trends using the CoinMarketCap API.

## ✨ Features

### 🔧 Backend (FastAPI)
- **RESTful API** for cryptocurrency data
- **Real-time data** from CoinMarketCap API
- **Comprehensive error handling** and logging
- **Data validation** with Pydantic models
- **Health checks** and monitoring
- **CORS support** for web integration
- **Dockerized** for easy deployment

### 🤖 Telegram Bot
- **Interactive commands** for cryptocurrency data
- **Top cryptocurrencies** listing with custom limits
- **Detailed crypto information** by CoinMarketCap ID
- **Trending cryptocurrencies** (24h gainers)
- **Rich formatting** with emojis and markdown
- **Error handling** and retry mechanisms
- **Configurable** via environment variables

## 🏗️ Architecture

```
Crypto_Tracker/
├── app/
│   ├── backend/           # FastAPI backend
│   │   ├── src/
│   │   │   ├── main.py           # FastAPI application
│   │   │   ├── router.py         # API endpoints
│   │   │   ├── models.py         # Pydantic models
│   │   │   ├── config.py         # Configuration management
│   │   │   ├── http_client.py    # HTTP client for CMC API
│   │   │   └── cmc_client.py     # CoinMarketCap client wrapper
│   │   ├── requirements.txt      # Python dependencies
│   │   └── .env                  # Environment variables
│   ├── bot/               # Telegram bot
│   │   ├── bot.py               # Bot main file
│   │   ├── router.py            # Bot command handlers
│   │   ├── config.py            # Bot configuration
│   │   ├── requirements.txt     # Bot dependencies
│   │   └── Dockerfile           # Bot containerization
│   └── Dockerfile         # Backend containerization
├── docker-compose.yml     # Multi-service orchestration
├── .env.example          # Environment variables template
└── README.md             # This file
```

## 🚀 Quick Start

### Prerequisites

1. **CoinMarketCap API Key**: Get your free API key from [CoinMarketCap API](https://coinmarketcap.com/api/)
2. **Telegram Bot Token**: Create a bot via [@BotFather](https://t.me/BotFather) on Telegram
3. **Docker & Docker Compose** (recommended) or **Python 3.9+**

### 🐳 Docker Setup (Recommended)

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Crypto_Tracker
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Configure your .env file**
   ```env
   CMC_API_KEY=your-coinmarketcap-api-key
   TELEGRAM_BOT_TOKEN=your-telegram-bot-token
   ```

4. **Start the services**
   ```bash
   docker-compose up -d
   ```

5. **Check service health**
   ```bash
   # Check backend health
   curl http://localhost:8000/health
   
   # Check logs
   docker-compose logs -f
   ```

### 🐍 Manual Setup

#### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd app/backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   # Create .env file with your CMC_API_KEY
   echo "CMC_API_KEY=your-api-key-here" > .env
   ```

5. **Run the backend**
   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
   ```

#### Bot Setup

1. **Navigate to bot directory**
   ```bash
   cd app/bot
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   export TELEGRAM_BOT_TOKEN="your-bot-token"
   export BACKEND_URL="http://localhost:8000"
   ```

5. **Run the bot**
   ```bash
   python bot.py
   ```

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|--------------|
| `/health` | GET | Service health check |
| `/cryptocurrency/` | GET | Get top cryptocurrencies |
| `/cryptocurrency/{id}` | GET | Get specific cryptocurrency by ID |

### Query Parameters

- `limit`: Number of results (1-5000, default: 100)
- `convert`: Currency to convert to (default: USD)

## 🤖 Bot Commands

| Command | Description | Example |
|---------|-------------|----------|
| `/start` | Welcome message and help | `/start` |
| `/help` | Show all commands | `/help` |
| `/top [limit]` | Get top cryptocurrencies | `/top 5` |
| `/crypto <id>` | Get crypto by CoinMarketCap ID | `/crypto 1` |
| `/trending` | Get top 5 trending (24h gainers) | `/trending` |

### Popular Cryptocurrency IDs

- **Bitcoin (BTC)**: 1
- **Ethereum (ETH)**: 1027
- **Tether (USDT)**: 825
- **BNB**: 1839
- **Solana (SOL)**: 5426
- **XRP**: 52
- **Dogecoin (DOGE)**: 74
- **Cardano (ADA)**: 2010

## ⚙️ Configuration

### Environment Variables

#### Backend Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `CMC_API_KEY` | **Required** | CoinMarketCap API key |
| `CMC_BASE_URL` | `https://pro-api.coinmarketcap.com` | CMC API base URL |
| `HOST` | `0.0.0.0` | Server host |
| `PORT` | `8000` | Server port |
| `DEBUG` | `false` | Debug mode |
| `LOG_LEVEL` | `INFO` | Logging level |
| `REQUEST_TIMEOUT` | `30` | HTTP request timeout (seconds) |

#### Bot Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `TELEGRAM_BOT_TOKEN` | **Required** | Telegram bot token |
| `BACKEND_URL` | `http://localhost:8000` | Backend API URL |
| `REQUEST_TIMEOUT` | `10` | HTTP request timeout (seconds) |
| `MAX_RETRIES` | `3` | Maximum retry attempts |
| `LOG_LEVEL` | `INFO` | Logging level |

## 🔧 Development

### Running Tests

```bash
# Backend tests (when implemented)
cd app/backend
pytest

# Bot tests (when implemented)
cd app/bot
pytest
```

### Development with Docker

Create a `docker-compose.override.yml` for development:

```yaml
version: '3.8'
services:
  backend:
    volumes:
      - ./app/backend:/app
    environment:
      - DEBUG=true
      - LOG_LEVEL=DEBUG
    command: ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
  
  bot:
    volumes:
      - ./app/bot:/app
    environment:
      - LOG_LEVEL=DEBUG
```

### Code Style

The project follows Python best practices:
- **Type hints** for better code documentation
- **Comprehensive error handling**
- **Logging** throughout the application
- **Configuration validation** with Pydantic
- **Dockerized** services for consistent deployment

## 🚀 Deployment

### Production Deployment

1. **Set up production environment variables**
2. **Use Docker Compose for orchestration**
3. **Set up reverse proxy** (nginx) if needed
4. **Configure logging** and monitoring
5. **Set up SSL/TLS** for HTTPS

### Health Monitoring

Both services include health checks:
- **Backend**: `/health` endpoint
- **Bot**: Built-in health check in Docker

## 🐛 Troubleshooting

### Common Issues

1. **"CMC_API_KEY must be a valid API key"**
   - Ensure your CoinMarketCap API key is set correctly
   - Check that the key has sufficient permissions

2. **"TOKEN must be a valid Telegram bot token"**
   - Verify your bot token from @BotFather
   - Ensure the token format is correct (contains ":")

3. **Bot not responding**
   - Check if the backend is running and accessible
   - Verify `BACKEND_URL` configuration
   - Check bot logs for error messages

4. **Docker container issues**
   ```bash
   # Check container logs
   docker-compose logs backend
   docker-compose logs bot
   
   # Restart services
   docker-compose restart
   ```

### Logs and Debugging

```bash
# View real-time logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f bot

# Enable debug logging
# Set LOG_LEVEL=DEBUG in your .env file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

**📋 See our [ROADMAP.md](ROADMAP.md) for planned features and contribution opportunities!**

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [CoinMarketCap](https://coinmarketcap.com/) for providing the cryptocurrency data API
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [aiogram](https://aiogram.dev/) for the Telegram bot framework

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review the logs for error messages
3. Open an issue on GitHub with detailed information

---

**Happy Trading!** 📈🚀
