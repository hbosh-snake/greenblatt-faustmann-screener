"""
ticker_validator.py

This module provides functionality to validate a given stock ticker by attempting
to retrieve its quarterly balance sheet data using yfinance. If the data is
retrieved successfully, the ticker is considered valid.
"""

import logging
import yfinance as yf

# Configure module-level logger. Adjust the configuration to match your project's
# logging preferences (handlers, formatting, etc.).
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def check_ticker_validity(ticker: str) -> bool:
    """
    Checks whether a given ticker can be considered valid by retrieving its
    quarterly balance sheet data via yfinance. A lack of required fields or
    other exceptions indicates that the ticker is invalid.

    Parameters
    ----------
    ticker : str
        The stock ticker symbol (e.g., "AAPL").

    Returns
    -------
    bool
        True if data is successfully retrieved and the expected fields are present;
        False otherwise.
    """
    try:
        stock = yf.Ticker(ticker)
        balance_sheet = stock.quarterly_balance_sheet.T
        equity = balance_sheet.iloc[0]["Stockholders Equity"]  # Key field check
        logger.debug(f"Ticker '{ticker}' valid. Equity: {equity}")
        return True

    except (IndexError, KeyError) as e:
        logger.error(
            "Ticker '%s' is missing the expected fields in its balance sheet. "
            "Details: %s", ticker, e
        )
        return False

    except Exception as e:
        logger.exception(
            "An unexpected error occurred while validating ticker '%s': %s",
            ticker, e
        )
        return False
