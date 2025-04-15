"""
financial_data_extractor.py

Module to retrieve and compute various financial metrics for a given ticker using yfinance.
Logs key steps for easier debugging and provides extensive docstrings for clarity.
"""

import logging
import yfinance as yf
from typing import Optional, Tuple

# Configure the module-level logger
logger = logging.getLogger(__name__)


def extract_data(ticker: str) -> Optional[Tuple[str, int, int, int, int, float, float, float, float]]:
    """
    Retrieve and compute financial data for a given stock ticker using Yahoo Finance.

    This function fetches the quarterly balance sheet, quarterly income statement,
    and additional company info to compute several key metrics:
        - Stock name
        - Equity
        - Cash
        - Debt
        - Market cap
        - Faustmann ratio
        - Debt-to-equity ratio
        - ROIC
        - Price/Earnings ratio

    If data is unavailable or any critical metric calculation fails, returns None.

    Args:
        ticker (str): The stock ticker symbol.

    Returns:
        Optional[Tuple[str, int, int, int, int, float, float, float, float]]:
            A tuple containing the following data in order:
                1. stock_name      (str)
                2. equity          (int)
                3. cash            (int)
                4. debt            (int)
                5. market_cap      (int)
                6. faustmann       (float)
                7. debt_to_equity  (float)
                8. roic            (float)
                9. price_earnings  (float)

            Returns None if a critical part of the data is missing or an error occurs.
    """

    def safe_int_access(df, row_idx: int, column_name: str) -> int:
        """
        Safely retrieve and convert a value from a DataFrame to int.
        Returns 0 if data is missing or conversion fails.
        """
        try:
            return int(df.iloc[row_idx][column_name])
        except (KeyError, IndexError, TypeError, ValueError):
            return 0

    try:
        logger.debug(f"Starting data extraction for ticker: {ticker}")
        stock = yf.Ticker(ticker)

        # Check if the required data is present
        if stock.quarterly_balance_sheet is None or stock.quarterly_incomestmt is None:
            logger.warning(f"No financial data available for ticker {ticker}. Skipping extraction.")
            return None

        balance_sheet = stock.quarterly_balance_sheet.T
        income_statement = stock.quarterly_incomestmt.T

        # Basic data extractions
        equity = safe_int_access(balance_sheet, 0, "Stockholders Equity")
        cash = safe_int_access(balance_sheet, 0, "Cash And Cash Equivalents")
        long_term_debt = safe_int_access(balance_sheet, 0, "Long Term Debt")
        current_debt = safe_int_access(balance_sheet, 0, "Current Debt")
        debt = long_term_debt + current_debt

        # Additional metadata
        stock_info = stock.info or {}
        market_cap = stock_info.get("marketCap", 0)
        stock_name = stock_info.get("longName", "N/A")

        # Compute Faustmann ratio: market_cap / (equity + cash - debt)
        denominator = (equity + cash - debt)
        faustmann = round(market_cap / denominator, 3) if denominator else 0.0

        # Retrieve net incomes from the past four quarters
        net_incomes = [
            safe_int_access(income_statement, i, "Net Income") for i in range(4)
        ]
        net_income_ttm = sum(net_incomes)

        # Compute debt-to-equity
        debt_to_equity = round(debt / equity, 3) if equity else 0.0

        # Compute ROIC: net_income_ttm / (equity + debt)
        roic = round(net_income_ttm / (equity + debt), 3) if (equity + debt) else 0.0

        # Compute Price/Earnings
        price = stock_info.get("currentPrice", 0)
        eps = stock_info.get("trailingEps", 0)
        price_earnings = round(price / eps, 2) if eps else 0.0

        logger.debug(
            f"Extraction for {ticker} complete. "
            f"Equity: {equity}, Cash: {cash}, Debt: {debt}, MarketCap: {market_cap}, "
            f"Faustmann: {faustmann}, D/E: {debt_to_equity}, ROIC: {roic}, P/E: {price_earnings}"
        )

        return (
            stock_name,
            equity,
            cash,
            debt,
            market_cap,
            faustmann,
            debt_to_equity,
            roic,
            price_earnings,
        )

    except Exception as e:
        logger.exception(f"Error extracting financial data for {ticker}: {e}")
        return None
