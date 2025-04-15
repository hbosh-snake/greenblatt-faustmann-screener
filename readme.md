## Introduction

This project is built upon the foundational concepts of value investing as articulated by two important thinkers: **Joel Greenblatt**, an American investor and academic, and **Martin Faustmann**, a German forester and economist. While their work originates in very different contexts—equities and forestry, respectively—both present methodologies for assessing long-term value, and this project merges these perspectives in a quantitative stock-screening tool.

### Who is Joel Greenblatt?

Joel Greenblatt introduced the **Magic Formula Investing** strategy in his book *The Little Book That Beats the Market*. The premise is simple: buying "good companies at good prices." Greenblatt’s Magic Formula ranks stocks based on two key metrics:

- **Earnings Yield** – a proxy for how "cheap" the stock is (e.g., EBIT / Enterprise Value).
- **Return on Capital (ROIC)** – a measure of how efficiently a company turns capital into profits.

Stocks with a high ranking in both are expected to outperform over the long term. This repository implements a scraper and analyzer based on these principles, automating the screening process from Greenblatt’s official website.

### Who is Faustmann, and why is he relevant?

Martin Faustmann developed a model in the 19th century to evaluate the value of forest land, balancing future yields against time and capital costs. His **Faustmann formula** is an early form of what we now call **net present value (NPV)**, adapted to assess recurring income from a capital asset over infinite cycles.

In this project, we draw inspiration from Faustmann’s logic to derive a custom **Faustmann Ratio**:

> `Faustmann = Market Cap / (Equity + Cash - Debt)`

This ratio attempts to reflect how much investors are paying per unit of “adjusted net worth,” adjusting for liquidity and leverage. A lower Faustmann ratio may suggest better value, echoing the timeless ideas of investing with a margin of safety.

> 📘 *Note: The inspiration to apply Faustmann’s forestry-based capital valuation to financial markets came from Mark Spitznagel’s book* **The Dao of Capital**, *which frames value investing as a strategy rooted in roundabout, long-term thinking.*

### What does this code do?

This Python-based system:

- **Scrapes** the Magic Formula Investing website to retrieve a list of candidate stocks based on various market cap thresholds.
- **Parses** and aggregates ticker data from the scraped HTML files into a structured CSV.
- **Validates** each ticker and queries financial data from Yahoo Finance via the `yfinance` API.
- **Computes** several financial metrics, including:
  - **Faustmann Ratio** (as described above),
  - **Return on Invested Capital (ROIC)**,
  - **Debt to Equity Ratio**,
  - **Price-to-Earnings (P/E)** ratio.
- **Outputs** a consolidated CSV file for further analysis or ranking.

Whether you're a value investor, a Python enthusiast, or just curious about financial automation, this project offers a reproducible, transparent tool to identify potentially undervalued stocks using well-established investment principles.

> ⚠️ *Disclaimer: This project is for educational and personal research purposes only. I do not claim ownership of the original ideas or intellectual properties of Joel Greenblatt or Mark Spitznagel. Nothing in this repository constitutes financial advice. Please do your own due diligence before making any investment decisions.*

# Greenblatt Magic Formula Project

This repository contains a Python-based solution to:
1. **Scrape stock screening data** from the [Magic Formula Investing website](https://www.magicformulainvesting.com/).
2. **Aggregate** the resulting tickers into a CSV list.
3. **Validate** the tickers and fetch fundamental data (using [yfinance](https://pypi.org/project/yfinance/)).
4. **Compute** metrics such as **Faustmann**, **ROIC**, **Debt to Equity**, and **P/E**.
5. **Generate** a final CSV table with all collected and processed information.

## Table of Contents

- [Project Overview](#project-overview)
- [Setup and Installation](#setup-and-installation)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Detailed Modules Explanation](#detailed-modules-explanation)
  - [1. `scrapper.py`](#1-scrapperpy)
  - [2. `screening_parser.py`](#2-screening_parserpy)
  - [3. `aggregator.py`](#3-aggregatorpy)
  - [4. `input_csv_reader.py`](#4-input_csv_readerpy)
  - [5. `validator.py`](#5-validatorpy)
  - [6. `data_extractor.py`](#6-data_extractorpy)
  - [7. `ticker_processor.py`](#7-ticker_processorpy)
  - [8. `final_table_creator.py`](#8-final_table_creatorpy)
  - [9. `main.py`](#9-mainpy)
- [Logging and Debugging](#logging-and-debugging)
- [Contributing](#contributing)
- [License](#license)

---

## Project Overview

This project aims to **automate** the process of retrieving and calculating relevant financial data for a list of tickers obtained from the Magic Formula Investing website. The main goals are:

- Scrape data behind a login screen using Selenium.
- Create a consolidated, validated, and deduplicated **list of tickers**.
- Use **yfinance** to fetch and compute fundamental metrics.
- Provide an **output CSV** that includes all relevant metrics for a quick overview.

---

## Setup and Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/hbosh-snake/greenblatt-faustmann-screener.git
   cd greenblatt_magic_formula
   ```

2. **Create and activate a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   Make sure that your `requirements.txt` includes the necessary libraries, such as:
   - `selenium`
   - `beautifulsoup4`
   - `yfinance`
   - `pandas`

4. **Download the correct WebDriver** for your browser (Chrome is used in this example):
   - Place it in a known path or update the `scrapper.py` with the correct driver path.

---

## Project Structure

Below is a simplified view of the main files and their relationships:

```
greenblatt_magic_formula/
│
├── greenblatt/
│   ├── __init__.py
│   ├── scrapper.py               # Logs in and downloads HTML from Magic Formula site
│   ├── screening_parser.py       # Parses the downloaded HTML to extract tickers
│   ├── aggregator.py             # Aggregates all parsed tickers into a single CSV
│   ├── input_csv_reader.py       # Reads tickers from a user-provided CSV
│   ├── validator.py              # Checks if tickers are valid / fetchable
│   ├── data_extractor.py         # Uses yfinance to fetch data & compute metrics
│   ├── ticker_processor.py       # Orchestrates extraction & structure of each ticker’s data
│   ├── final_table_creator.py    # Creates the final CSV with all data
│   └── main.py                   # Main entry point for running the entire workflow
│
├── monthly_magic_formula/
│   └── tickers_from_html/        # Folder where HTML files from the Magic Formula site are saved
│
├── requirements.txt
└── README.md                     # This file
```

---

## Usage

1. **Configure** any user-specific parameters inside `scrapper.py`, such as:
   - `username` and `password`
   - `driver_path` (path to your ChromeDriver or another supported WebDriver)

2. **Run** the main script:
   ```bash
   python -m greenblatt.main
   ```
   What it does:
   - Logs into [magicformulainvesting.com](https://www.magicformulainvesting.com/) for **each** specified market cap threshold.
   - Saves the HTML results into `monthly_magic_formula/tickers_from_html/`.
   - Aggregates and deduplicates tickers, writing them to `monthly_magic_formula/tickers.csv`.
   - Validates these tickers and uses `yfinance` to extract fundamental data.
   - Creates a final CSV file named `Greenblatt_<YEAR>_<MONTH>.csv` in the `monthly_magic_formula/` directory.

3. **Review** the resulting CSV to analyze or visualize the metrics.

---

## Detailed Modules Explanation

### 1. `scrapper.py`
- **Purpose**: Logs into the Magic Formula Investing website, retrieves the screened tickers for various market cap thresholds, and saves the resulting HTML to disk.
- **Key Function**:
  - `get_data_from_screener(market_caps: list) -> None`:
    - Logs in using Selenium.
    - Iterates over `market_caps`.
    - For each market cap, inputs the value, clicks “Get Stocks,” and saves the resulting HTML page into `monthly_magic_formula/tickers_from_html/`.

### 2. `screening_parser.py`
- **Purpose**: Parses the local HTML files to extract the ticker symbols.
- **Key Function**:
  - `tickers_from_screening_results(file_path: str) -> list[str]`:
    - Uses BeautifulSoup to find the table of stock tickers in the HTML.
    - Returns a list of all extracted tickers.

### 3. `aggregator.py`
- **Purpose**: Collects tickers from **all** HTML files saved by the scrapper, creates a **unique** aggregated set, and writes them into a CSV.
- **Key Function**:
  - `iterate_html_files(market_caps: list, ticker_list_file: str) -> None`:
    - Iterates over each HTML file corresponding to a market cap.
    - Calls `screening_parser.py` to retrieve tickers.
    - Deduplicates them into a set.
    - Writes them to the specified CSV file (e.g., `monthly_magic_formula/tickers.csv`).

### 4. `input_csv_reader.py`
- **Purpose**: Reads a CSV file (one ticker per line) and returns a list of tickers.
- **Key Function**:
  - `get_tickers(file: str) -> list[str]`:
    - Given a CSV path, returns the list of tickers in that file.

### 5. `validator.py`
- **Purpose**: Checks if each ticker is valid by attempting to fetch its **balance sheet** from yfinance. If the data exists, we assume the ticker is valid.
- **Key Functions**:
  - `check_tickers(ticker: str) -> bool`:
    - Returns `True` if the ticker’s quarterly balance sheet can be accessed, `False` otherwise.
  - `validate_and_process_ticker(tickers_list: str) -> list[dict]`:
    - Reads all tickers from the CSV using `input_csv_reader.py`.
    - For each valid ticker, processes it (using `ticker_processor.py`) and accumulates the data in a list of dictionaries.

### 6. `data_extractor.py`
- **Purpose**: Uses **yfinance** to retrieve financial statements and basic stats for a single ticker, computing relevant metrics. 
- **Key Function**:
  - `extract_data(ticker: str) -> tuple`:
    - Retrieves the ticker object from yfinance.
    - Fetches **balance sheet** and **income statement** data.
    - Extracts `equity`, `cash`, `debt` (both long-term and current), `net_income_ttm`, etc.
    - Computes derived metrics like:
      - **Faustmann** (`market_cap / (equity + cash – debt)`)
      - **ROIC**
      - **Debt to Equity**
      - **Price/Earnings**
    - Returns these metrics in a tuple.

### 7. `ticker_processor.py`
- **Purpose**: Integrates `data_extractor.py` to structure the ticker’s extracted data into a neat dictionary.
- **Key Function**:
  - `process_ticker(ticker: str) -> dict`:
    - Calls `extract_data` from `data_extractor.py`.
    - Packages the returned values into a dictionary with keys like `"Ticker"`, `"Equity"`, `"Debt"`, `"ROIC"`, etc.
    - Returns that dictionary, which can be appended to a table or further used in data frames.

### 8. `final_table_creator.py`
- **Purpose**: Converts the final list of processed ticker dictionaries into a Pandas DataFrame and saves it to a CSV file.
- **Key Function**:
  - `create_table(table: list[dict]) -> None`:
    - Takes a list of dictionaries (each representing a single ticker’s data).
    - Creates a DataFrame and outputs a timestamped CSV (e.g., `Greenblatt_2025_March.csv`).

### 9. `main.py`
- **Purpose**: The main entry point orchestrating all the modules. 
- **Key Steps**:
  1. **Scrape** the Magic Formula site for multiple market caps (`scrapper.py`).
  2. **Aggregate** the resulting tickers into `monthly_magic_formula/tickers.csv` (`aggregator.py`).
  3. **Validate** tickers, compute metrics, and build a data structure (`validator.py` + `ticker_processor.py`).
  4. **Create** a final CSV table with all the data (`final_table_creator.py`).

Run it as:
```bash
python -m main
```

---

## Logging and Debugging

- **Logging**:  
  Each module has been refactored to include print statements or logging calls (depending on your preference) that provide **step-by-step information** about what the script is doing. 
- **Debugging**:
  - If there’s an error logging into the site, Selenium should print messages to the console.
  - If some tickers are invalid or data is missing, an informative message is printed out.
  - Ensure you review console output to see which tickers were skipped or if there were any connection issues.

---

## License

This project is open-source; feel free to adapt it to your own needs.

---