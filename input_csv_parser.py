"""
Module: input_csv_parser.py

This module provides functionality to parse a CSV file containing stock tickers,
returning them as a list of strings. Each line of the input CSV is expected
to contain one ticker symbol.
"""

import csv
import logging
from typing import List

# Configure a module-level logger
logger = logging.getLogger(__name__)

def get_tickers(file_path: str) -> List[str]:
    """
    Parse a CSV file containing a list of stock tickers, one per row,
    and return them as a list of strings.

    :param file_path: The path to the CSV file containing the ticker symbols.
    :return: A list of ticker symbols read from the file. If the file cannot
             be read, an empty list is returned.
    """
    tickers = []

    # Attempt to open and read the CSV file
    try:
        with open(file_path, "r", newline="") as csvfile:
            reader = csv.reader(csvfile)

            # Enumerate each row so that we can log the line number for debugging
            for row_number, row in enumerate(reader, start=1):
                # Ensure the row has at least one element
                if row:
                    ticker = row[0].strip()
                    if ticker:
                        tickers.append(ticker)
                    else:
                        logger.warning(
                            f"Empty ticker encountered on line {row_number} in '{file_path}'. Skipping."
                        )
                else:
                    logger.warning(
                        f"No data found on line {row_number} in '{file_path}'. Skipping."
                    )

        logger.info(
            f"Successfully parsed {len(tickers)} tickers from file '{file_path}'."
        )

    except FileNotFoundError as e:
        logger.error(f"File not found: '{file_path}'. Error: {e}")
    except OSError as e:
        logger.error(f"OS error occurred while reading '{file_path}': {e}")
    except Exception as e:
        logger.error(f"Unexpected error while reading '{file_path}': {e}")

    # Return the list of parsed tickers (possibly empty in case of errors)
    return tickers
