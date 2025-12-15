# AI Stock Analytics

A web-based stock analysis tool that uses an AI agent plus technical indicators to analyze stock price trends. Built as a college project to make market analysis simple and visual.

## What Does It Do?

This minimal viable product (MVP):
- Fetches historical prices for a stock (OHLCV)
- Computes moving averages and Bollinger Bands
- Generates a chart image served from the backend
- Uses an AI agent to summarize findings in plain English
- Shows a clean UI to submit queries and view results

The goal is to help students understand market signals (trend, volatility) without reading raw CSV data.

## Tech Stack

### Frontend
- React (Vite + TypeScript)
- Tailwind CSS
- Axios (API calls)

### Backend
- FastAPI (Python web framework)
- LangChain (agent orchestration)
- Alpha Vantage API (market data)
- Uvicorn (ASGI server)

## Prerequisites

Before running this project, you need:
- An Alpha Vantage API key (free tier available)
- Python 3.10+ and Node.js 18+

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/KhushalID7/AI-Stock-analytics.git
```

### 2. Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file in the `backend` folder:

```env
ALPHA_VANTAGE_API_KEY=your_api_key_here
```

### 3. Frontend Setup

```bash
cd ../frontend
npm install
```

## How to Run

Open two terminals.

### Terminal 1 - Start Backend

```bash
cd backend
uvicorn apps.main:app --reload --port 8000
```

### Terminal 2 - Start Frontend

```bash
cd frontend
npm run dev
```

Visit the app:
- http://localhost:3000 (or the port Vite prints)

## Usage

1. Type a query like: "Show me AAPL stock prices for the last 3 days"
2. Click "Analyze Stock"
3. Read the AI summary
4. View the generated chart(s) under "Charts"
5. Expand "Raw Output" for detailed tool results

## Project Structure

```
AI-Stock-analytics/
├── backend/
│   ├── apps/
│   │   ├── main.py            # FastAPI app + static mounting
│   │   ├── api/               # API routes (agent, health)
│   │   ├── agents/            # Agent + tools (prices, MA, bands, plot)
│   │   ├── services/          # Alpha Vantage client
│   │   └── static/charts/     # Generated chart images
│   └── requirements.txt
└── frontend/
	├── src/                   # React + hooks + components
	├── vite.config.ts         # Dev server + proxy to backend
	└── package.json
```

## Known Limitations

- Free Alpha Vantage rate limits may cause delayed or empty data
- Charts are static images (no live updating yet)
- No auth or persistence (demo app)

## Testing

Run backend tests:
```bash
cd backend
python -m apps.tests.test_moving_tools
```

## Credits

Built as a college project for learning purposes.

Technologies used:
- FastAPI + LangChain for the AI agent
- Alpha Vantage for market data
- Tailwind CSS + React for UI
AI Stock Analytics

- Tech Stack:
	- Backend: FastAPI (Python), LangChain, Alpha Vantage API
	- Frontend: Vite + React + TypeScript, Tailwind CSS
	- Charts: Static images served from backend (/static/charts)

- Prerequisites:
	- Python 3.10+
	- Node.js 18+

- Setup Backend:
	- Create .env in backend with keys
		- ALPHA_VANTAGE_API_KEY=your_key
	- Install deps
		- pip install -r backend/requirements.txt
	- Run server
		- cd backend
		- uvicorn apps.main:app --reload

- Setup Frontend:
	- Install deps
		- cd frontend
		- npm install
	- Start dev
		- npm run dev
	- Open the app in browser
		- http://localhost:3000 (or the port Vite shows)

- How it works:
	- Type a query like "Show me AAPL stock prices for the last 3 days"
	- Frontend calls backend at /api/agent/query
	- Backend runs tools, creates charts, and returns summary + chart URLs
	- Charts load from /static/charts

- Notes:
	- Keep API keys only in backend .env
	- If charts 404, make sure backend is running and serving /static
