"""
Refactored main.py

Usage:
    1. Navigate to the parent directory in a terminal/console.
    2. Run: python -m greenblatt.main

This script orchestrates the following steps:
    1. Retrieves screening results from Magic Formula Investing, for various market cap thresholds.
    2. Parses the resulting HTML files, extracting unique tickers.
    3. Validates and processes each ticker (via yfinance).
    4. Generates a final CSV file containing the computed data (e.g., ROIC, Debt/Equity, etc.).

Requirements:
    - Valid login credentials (provided in get_screening_html_results.py).
    - A valid Chrome WebDriver path in get_screening_html_results.py.
    - The "monthly_magic_formula" directory structure must exist to store the generated files.

Notes:
    - TICKER_LIST_FILE: path to the CSV file storing combined, deduplicated tickers.
    - MARKET_CAPS: list of market capitalization thresholds to request in the Magic Formula screener.
"""

import logging
from final_table_creator import create_final_table
from tickers_csv_aggregator import aggregate_tickers_from_html
from screening_html_fetcher import fetch_screening_html
from ticker_processing_flow import ticker_processing_flow
from dotenv import load_dotenv
import os

load_dotenv()

# ------------------------------------------------------------------------------
# Global constants
# ------------------------------------------------------------------------------
TICKER_LIST_FILE = "./monthly_magic_formula/tickers.csv"
MARKET_CAPS = [
    250, 500, 1000, 1500, 2500, 5000, 10000,
    25000, 50000, 75000, 100000, 250000, 500000
]

USERNAME = os.getenv("MAGIC_FORMULA_USERNAME")
PASSWORD = os.getenv("MAGIC_FORMULA_PASSWORD")
# ------------------------------------------------------------------------------
# Configure logging
# ------------------------------------------------------------------------------
# You can configure the logging level to DEBUG for verbose output, INFO for standard usage, etc.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """
    Main entry point for the Greenblatt Magic Formula workflow.

    1) Scrape screening data for multiple market caps.
    2) Parse HTML files to generate a consolidated ticker list.
    3) Validate tickers and extract financial data from yfinance.
    4) Save the final table to a CSV file.
    """
    logger.info("Starting Magic Formula workflow...")

    # Step 1: Retrieve HTML results from Magic Formula screener
    logger.info("Scraping data from Magic Formula website...")
    fetch_screening_html(
        market_caps=MARKET_CAPS,
        # driver_path=DRIVER_PATH,
        username=USERNAME,
        password=PASSWORD,
    )
    logger.info("Scraping completed.")

    # Step 2: Parse HTML files to build a deduplicated CSV of tickers
    logger.info("Collecting tickers from HTML files...")
    aggregate_tickers_from_html(MARKET_CAPS, TICKER_LIST_FILE)
    logger.info("Ticker list created at %s", TICKER_LIST_FILE)

    # Step 3: Validate and process each ticker
    logger.info("Validating and processing tickers...")
    table = ticker_processing_flow(TICKER_LIST_FILE)
    logger.info("All tickers have been processed. Total valid tickers: %d", len(table))

    # Step 4: Create the final CSV results table
    logger.info("Generating final CSV output...")
    create_final_table(table)
    logger.info("Final CSV has been created in the 'monthly_magic_formula' folder.")

    logger.info("Magic Formula workflow completed successfully.")


if __name__ == "__main__":
    main()
