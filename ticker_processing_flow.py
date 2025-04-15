"""
ticker_processing_flow.py

This module provides a flow to read a list of ticker symbols from a CSV file,
validate each ticker's data availability, and if valid, extract key financial
data. The processed data is then returned as a list of dictionaries.
"""

import logging
from ticker_validator import check_ticker_validity
from input_csv_parser import get_tickers
from ticker_processor import process_ticker

# Configure logging at the module level
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def ticker_processing_flow(tickers_csv_path: str) -> list:
    """
    Executes a comprehensive flow for processing tickers from a CSV file:
      1. Reads the ticker list from the specified CSV file.
      2. Validates each ticker to ensure financial data can be retrieved.
      3. For valid tickers, fetches and processes key financial data.
      4. Returns a collection of processed financial data records.

    Parameters
    ----------
    tickers_csv_path : str
        The file path to the CSV file containing a list of ticker symbols,
        one symbol per row.

    Returns
    -------
    list
        A list of dictionaries, where each dictionary contains the processed
        financial data for a valid ticker. If a ticker fails validation,
        it will not appear in the returned list.
    """

    # List to accumulate valid, processed ticker data
    processed_data = []

    # Get all tickers from the CSV
    all_tickers = get_tickers(tickers_csv_path)

    # Iterate over each ticker symbol
    for ticker in all_tickers:
        # Check if the ticker is valid (e.g., has available balance sheet data)
        if check_ticker_validity(ticker):
            # If valid, process the ticker to extract financial metrics
            data = process_ticker(ticker)
            processed_data.append(data)
            logger.info("Successfully processed ticker: %s", ticker)
        else:
            # If invalid, log a warning
            logger.warning("Skipping invalid ticker or missing data: %s", ticker)

    return processed_data
