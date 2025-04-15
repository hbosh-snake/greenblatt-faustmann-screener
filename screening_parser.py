"""
screening_parser.py

This module is responsible for parsing the HTML files obtained from the Magic Formula
website's screening results. It extracts and returns a list of stock tickers found
within the HTML content.

Usage Example:
    from screening_parser import parse_screening_html

    file_path = "monthly_magic_formula/tickers_from_html/stock_screening_results_250.html"
    tickers = parse_screening_html(file_path)
    print(tickers)
"""

import logging
from typing import List
from bs4 import BeautifulSoup

# Set up a logger for this module
logger = logging.getLogger(__name__)


def parse_screening_html(file_path: str) -> List[str]:
    """
    Parses an HTML file containing Magic Formula screening results and extracts stock tickers.

    The HTML is expected to have a <table> element with the class 'screeningdata', where
    each row in the table body corresponds to one stock. The stock ticker is typically located
    in the second <td> cell of each row.

    :param file_path: The path to the HTML file to parse.
    :return: A list of extracted stock tickers (may be empty if no table or tickers are found).
    """
    logger.info("Parsing screening results from HTML file: %s", file_path)
    tickers: List[str] = []

    try:
        # Read the HTML content from the file
        with open(file_path, "r", encoding="utf-8") as file:
            html_content = file.read()
    except FileNotFoundError:
        logger.error("File not found: %s", file_path)
        return []
    except OSError as e:
        logger.error("Error reading file %s: %s", file_path, e)
        return []

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Find the table containing the stock tickers
    table = soup.find("table", {"class": "screeningdata"})
    if not table:
        logger.warning("No table with class 'screeningdata' found in file: %s", file_path)
        return []

    # Check if the table has a body
    tbody = table.find("tbody")
    if not tbody:
        logger.warning("No <tbody> found within the table in file: %s", file_path)
        return []

    # Extract tickers from each row in the table body
    rows = tbody.find_all("tr")
    for row in rows:
        cells = row.find_all("td")
        # Ensure the row has at least two columns before accessing cells[1]
        if len(cells) > 1:
            ticker_text = cells[1].get_text(strip=True)
            if ticker_text:
                tickers.append(ticker_text)

    logger.info("Extracted %d tickers from file: %s", len(tickers), file_path)
    return tickers
