### Project Architecture

blackStone/

│
├── app/                     # UI layer
│   ├── streamlit_app.py
│   ├── api_client.py
│
├── backend/                 # Core logic (never changes)
│   ├── api/                 # FastAPI endpoints
│   ├── services/            # Business logic
│   ├── agents/              # Automation agents
│   ├── analysis/            # Financial calculations
│   ├── rag/                 # Retrieval system
│
├── data_engine/             # Data collection
│   ├── collectors/          # APIs (yfinance etc.)
│   ├── scrapers/            # web scraping
│   ├── pipelines/           # cleaning + processing
│
├── database/
│   ├── models/              # schema
│   ├── db_manager.py
│
├── config/
│   ├── settings.py
│
├── utils/
│
└── main.py