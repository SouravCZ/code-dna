# Code DNA 🧬

A fun web app that analyzes your GitHub profile and generates a personalized "Developer DNA Card" using AI.

> Built for the Microsoft Agents League Hackathon - Creative Apps track using GitHub Copilot

## Features

✨ **Developer DNA Cards** - Get a personality-driven analysis of your coding style
- Personality archetype based on your coding patterns
- Top programming languages with insights
- Commit message style analysis
- README quality scoring
- Strengths and "Brutal Truths"
- Shareable card image (like Spotify Wrapped)

## Tech Stack

- **Frontend**: React + Tailwind CSS
- **Backend**: Python + Flask
- **APIs**: GitHub REST API, OpenAI/Anthropic API
- **Tools**: GitHub Copilot

## Project Structure

```
code-dna/
├── backend/                 # Flask Python backend
│   ├── app.py              # Main Flask application
│   ├── config.py           # Configuration settings
│   ├── requirements.txt    # Python dependencies
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── github_api.py   # GitHub API integration
│   │   └── ai_analysis.py  # AI analysis routes
│   └── utils/
│       ├── __init__.py
│       ├── github_client.py    # GitHub API client
│       ├── ai_client.py        # AI API client
│       └── prompt_templates.py # AI prompt templates
│
├── frontend/                # React frontend
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── DNACard.jsx     # Main DNA Card component
│   │   │   ├── SearchBar.jsx   # GitHub username input
│   │   │   └── Loading.jsx     # Loading animation
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   └── Results.jsx
│   │   ├── services/
│   │   │   └── api.js          # API client
│   │   ├── App.jsx
│   │   └── index.css
│   ├── package.json
│   └── tailwind.config.js
│
├── .env.example             # Environment variables template
├── docker-compose.yml       # Docker setup (optional)
└── docs/                    # Documentation
    └── API_SETUP.md
```

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js 16+
- GitHub API token
- OpenAI or Anthropic API key

### Installation

#### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Frontend Setup
```bash
cd frontend
npm install
```

### Configuration

Create a `.env` file in the backend directory:
```
GITHUB_API_TOKEN=your_github_token
AI_PROVIDER=openai  # or anthropic
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
FLASK_ENV=development
FLASK_DEBUG=True
```

### Running the App

**Terminal 1 - Backend:**
```bash
cd backend
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

Visit `http://localhost:3000` in your browser.

## License
MIT
