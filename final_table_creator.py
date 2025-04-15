"""
final_table_creator.py

This module provides functionality to create and export a final CSV table
from a given data structure (list of dictionaries or a pandas DataFrame).
"""

import logging
import os
from datetime import datetime
import pandas as pd

# Configure logger for this module
logger = logging.getLogger(__name__)


def create_final_table(table, output_dir: str = "monthly_magic_formula") -> str:
    """
    Create a final CSV table from the input data structure.

    :param table: A list of dictionaries or a pandas DataFrame representing
                  the rows of the final CSV file.
    :param output_dir: Directory where the resulting CSV file will be saved.
                       Defaults to "monthly_magic_formula".
    :return: The absolute path to the created CSV file.
    :raises ValueError: If 'table' is not a DataFrame or list of dictionaries.
    :raises OSError: If the CSV file could not be written.
    """
    # Ensure output directory exists; create if it doesn’t
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # Build the output file name based on current month and year
    current_month_year = datetime.now().strftime("%Y_%B")
    output_file_name = f"Greenblatt_{current_month_year}.csv"
    output_file_path = os.path.join(output_dir, output_file_name)

    # Convert table to a DataFrame if necessary
    if isinstance(table, pd.DataFrame):
        df = table
    elif isinstance(table, list):
        df = pd.DataFrame(table)
    else:
        message = "Input 'table' must be a DataFrame or list of dictionaries."
        logger.error(message)
        raise ValueError(message)

    try:
        # Write DataFrame to CSV
        df.to_csv(output_file_path, index=False)
        logger.info(f"Final table successfully created at {output_file_path}")
        return os.path.abspath(output_file_path)
    except OSError as e:
        logger.error(f"Error writing the final table to CSV: {e}")
        raise
