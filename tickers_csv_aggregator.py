"""
tickers_csv_aggregator.py

This module aggregates stock tickers from multiple HTML screening result files
into a single CSV file. It reads each HTML file (named by market cap), extracts
the tickers, combines them into a sorted unique list, and then saves them to
the specified CSV output path.

Usage:
    from tickers_csv_aggregator import aggregate_tickers_from_html
    ...
    market_caps = [250, 500, 1000]  # or any list of numeric values
    output_csv_path = "./monthly_magic_formula/tickers.csv"
    aggregate_tickers_from_html(market_caps, output_csv_path)

Dependencies:
    - get_tickers_from_screening.py
    - Python standard libraries: csv, logging
"""

import logging
import csv
from screening_parser import parse_screening_html

# Configure the logger. In a larger project, you'll typically set up logging once,
# in your main entry point, and simply retrieve the logger here.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)


def aggregate_tickers_from_html(market_caps, output_csv_path):
    """
    Aggregate stock tickers from multiple HTML screening result files and store
    them in a CSV file at output_csv_path.

    Args:
        market_caps (list of int): A list of market cap values used to name the
            HTML files. For each value in market_caps, an HTML file
            'stock_screening_results_<value>.html' is expected to exist under
            './monthly_magic_formula/tickers_from_html/'.
        output_csv_path (str): Path to the CSV file where the combined tickers
            should be saved.

    Returns:
        None. (A CSV file is created/written to output_csv_path)

    The function:
        1. Iterates through each market cap in market_caps.
        2. Builds the expected HTML filename for each market cap.
        3. Extracts tickers from that file using tickers_from_screening_results.
        4. Collects and de-duplicates all extracted tickers.
        5. Writes the final, sorted list of unique tickers to output_csv_path.
    """
    # Aggregate all extracted tickers in a single list
    logger.info("Starting aggregation of tickers from HTML files.")
    logger.debug("Market caps to process: %s", market_caps)

    all_tickers = []
    for cap in market_caps:
        file_path = f"./monthly_magic_formula/tickers_from_html/stock_screening_results_{cap}.html"
        logger.debug("Reading tickers from %s", file_path)

        extracted_tickers = parse_screening_html(file_path)
        if extracted_tickers:
            logger.info("Retrieved %d tickers from %s", len(extracted_tickers), file_path)
        else:
            logger.warning("No tickers found or unable to read file: %s", file_path)

        all_tickers.extend(extracted_tickers)

    # Convert list to a set to remove duplicates, then back to a list
    unique_tickers = sorted(set(all_tickers))
    logger.info("Total unique tickers found: %d", len(unique_tickers))

    # Write the final list of unique tickers to CSV
    try:
        with open(output_csv_path, "w", newline="", encoding="utf-8") as csv_file:
            csv_writer = csv.writer(csv_file)
            for ticker in unique_tickers:
                csv_writer.writerow([ticker])
        logger.info("Wrote unique tickers to CSV at %s", output_csv_path)
    except Exception as e:
        logger.error("Error writing tickers to CSV: %s", e, exc_info=True)
        raise
