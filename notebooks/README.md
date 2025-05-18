# MoonLight Energy Solutions - Solar Challenge Week 1


## Environment Setup

To set up the development environment for this project, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Fentahun022/solar-challenge-week1.git
    cd solar-challenge-week1
    ```

2.  **Create and activate a virtual environment:**
    Using `venv`:

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    

3.  **Install dependencies:**
  
    pip install -r requirements.txt
 

## Project Structure

├── .github/
│   └── workflows/
│       └── ci.yml
├── .gitignore
├── data/                  
├── notebooks/             # For EDA Jupyter notebooks
│   ├── __init__.py
│   └── README.md          # Explaining contents or purpose of notebooks
├── src/                   # For reusable Python modules/scripts
│   ├── __init__.py
│   └── utils.py           # Example utility functions
├── tests/                 # For unit tests
│   ├── __init__.py
├── scripts/               # For standalone helper scripts (data fetching, etc.)
│   ├── __init__.py
│   └── README.md
├── app/                   # (For Bonus Task) Streamlit application
│   ├── __init__.py
│   ├── main.py
│   └── utils.py
├── README.md
└── requirements.txt