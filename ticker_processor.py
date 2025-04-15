"""
ticker_processor.py

Retrieves financial data for the given ticker symbol using a Yahoo Finance wrapper,
calculates specific metrics (Faustmann, ROIC, P/E, etc.), and returns them in a
dictionary for further processing.

Typical Usage Example:
    from ticker_processor import process_ticker

    ticker_data = process_ticker("AAPL")
    if ticker_data:
        # Do something with the returned dictionary

Dependencies:
    - extract_financial_data_from_tickers.extract_data (function)
    - logging (standard library)

Author:
    Gizmo
"""

import logging
from typing import Dict, Any

# Adjust the import path to match your project’s folder structure
from financial_data_extractor import extract_data

# Configure a module-level logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def process_ticker(ticker: str) -> Dict[str, Any]:
    """
    Extracts and processes financial data for a given ticker symbol using Yahoo Finance data.

    This function relies on the `extract_data` function to fetch raw financial data
    (balance sheet, income statement) and calculates several key metrics, including:
      - Faustmann (market cap / (equity + cash - debt))
      - ROIC (net income TTM / (equity + debt))
      - Debt to Equity
      - P/E ratio
      - and others.

    Args:
        ticker (str): The stock ticker symbol to process.

    Returns:
        Dict[str, Any]: A dictionary containing relevant financial metrics and data for
                        the given ticker. An empty dictionary is returned if an exception
                        occurs during data extraction or processing.
    """
    try:
        (
            stock_name,
            equity,
            cash,
            debt,
            market_cap,
            faustmann,
            debt_to_equity,
            roic,
            price_earnings,
        ) = extract_data(ticker)
    except Exception as error:
        logger.exception("Error extracting data for ticker '%s': %s", ticker, error)
        return {}

    data = {
        "Ticker": ticker,
        "Stock name": stock_name,
        "Equity": equity,
        "Cash": cash,
        "Debt": debt,
        "Market cap": market_cap,
        "Faustmann": faustmann,
        "ROIC": roic,
        "Debt to equity": debt_to_equity,
        "P/E": price_earnings
    }

    logger.debug("Successfully processed ticker '%s': %s", ticker, data)
    return data
