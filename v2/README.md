# 🎲📈 DiceTrader v2

A modern web implementation of the DiceTrader financial simulator with FastAPI backend and React frontend.

## Key Features

- **Modern Web Architecture**: FastAPI backend + React/Material-UI frontend
- **Dynamic Market Simulation**: Market trends affect dice probabilities
- **AI Strategy Advisor**: Real-time betting recommendations
- **Multiple Betting Strategies**: Martingale, Kelly, Fibonacci and more
- **Interactive Dice Animations**: Visual representation of dice rolls
- **Responsive Design**: Desktop and mobile compatibility

## Technical Stack

### Backend
- FastAPI with Pydantic models
- Real-time probability adjustments
- AI integration with OpenRouter/DeepSeek
- Reinforcement learning system

### Frontend
- React with Material-UI components
- Interactive components
- Responsive layout
- Real-time API communication

## Probability Simulation

In DiceTrader, probabilities are dynamically adjusted based on the current market trend:
- **Bull Market**: Higher probabilities for sums 7-12
- **Bear Market**: Higher probabilities for sums 2-6
- **Volatility**: Affects extreme outcomes (2,3,11,12)

This creates a more realistic trading simulation where market conditions influence outcomes.

## Quick Start

### Docker Deployment

```bash
# Clone repository
git clone https://github.com/YourUsername/dicetrader.git
cd dicetrader/v2

# Configure API keys (optional)
cp .env.example .env
# Edit .env with your API keys

# Start the application
docker-compose up
```

Access:
- Frontend: http://localhost:3003
- API docs: http://localhost:8000/docs

### Local Development

#### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm start
```

## API Endpoints

### Core Endpoints
- `POST /init`: Start new game
- `GET /state`: Get current game state
- `POST /bet`: Place a bet
- `GET /strategy/advice`: Get AI recommendations
- `POST /strategy/change/{strategy}`: Change strategy

### Portfolio Management
- `POST /portfolio/add`: Add bet to portfolio
- `GET /portfolio/risk`: Get risk metrics

## Directory Structure

```
v2/
├── backend/               # FastAPI backend
│   ├── main.py            # Entry point
│   ├── game_logic.py      # Game mechanics
│   ├── strategies/        # Betting strategies
│   └── ai_services/       # AI integration
│
├── frontend/              # React frontend
│   ├── src/
│   │   ├── components/    # UI components
│   │   ├── App.jsx        # Main application
│   │   └── api.js         # API client
│   └── public/
│
└── docker-compose.yml     # Docker configuration
```

## License

MIT License - see LICENSE file for details