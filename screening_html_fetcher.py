# screening_html_fetcher.py
"""
Module for automating the fetching of stock-screening HTML pages from
Magic Formula Investing. It logs into the website, inputs specified market
cap values, and retrieves the resulting HTML content.

Usage Example:
    from screening_html_fetcher import fetch_screening_html

    MARKET_CAPS = [250, 500, 1000]
    DRIVER_PATH = r"/path/to/chromedriver"
    USERNAME = "myuser@example.com"
    PASSWORD = "mypassword"
    OUTPUT_DIR = "./monthly_magic_formula/tickers_from_html"

    fetch_screening_html(
        market_caps=MARKET_CAPS,
        driver_path=DRIVER_PATH,
        username=USERNAME,
        password=PASSWORD,
        output_directory=OUTPUT_DIR
    )

Ensure you have ChromeDriver installed and Selenium properly set up in your environment.
"""

import logging
import time
import sys
from pathlib import Path
from typing import List, Optional

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException
)
from webdriver_manager.chrome import ChromeDriverManager

# -------------------------------------------------------------------------
# LOGGING CONFIGURATION
# -------------------------------------------------------------------------
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # or INFO, depending on verbosity desired

# You can configure more complex logging (e.g., file handlers, formatters) as needed.
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
logger.addHandler(console_handler)


# -------------------------------------------------------------------------
# MAIN FUNCTIONS
# -------------------------------------------------------------------------
def init_webdriver() -> webdriver.Chrome:
    """
    Initialize a Chrome WebDriver with certain default options.

    Args:
        driver_path (str): The filesystem path to the ChromeDriver executable.

    Returns:
        webdriver.Chrome: An instance of the Chrome WebDriver.
    """
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--disable-search-engine-choice-screen")

    logger.debug("Initializing WebDriver.")
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    return driver


def login_to_magic_formula_investing(
    driver: webdriver.Chrome,
    username: str,
    password: str
) -> None:
    """
    Log into the Magic Formula Investing website using the provided credentials.

    Args:
        driver (webdriver.Chrome): The active Selenium WebDriver.
        username (str): The email/username for login.
        password (str): The password for login.

    Raises:
        SystemExit: If login fails or the page does not navigate to the expected URL.
    """
    login_url = "https://www.magicformulainvesting.com/Account/LogOn"
    driver.get(login_url)
    logger.info("Navigated to login page.")

    try:
        username_field = driver.find_element(By.ID, "Email")
        password_field = driver.find_element(By.ID, "Password")
    except NoSuchElementException as e:
        logger.error("Login form fields not found on the page.")
        raise SystemExit("Cannot proceed without a valid login form.") from e

    username_field.send_keys(username)
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    logger.debug("Submitted login form.")

    # Wait for the Stock Screening page to load
    try:
        WebDriverWait(driver, 20).until(
            EC.url_contains("/Screening/StockScreening")
        )
        logger.info("Successfully logged in and navigated to Stock Screening page.")
    except TimeoutException:
        logger.error("Login page took too long to load or navigation failed.")
        raise SystemExit("Login failed or page load timeout.")


def fetch_single_screening_html(
    driver: webdriver.Chrome,
    market_cap: int
) -> Optional[str]:
    """
    For a given market cap, interact with the screening form and retrieve the resulting HTML.

    Args:
        driver (webdriver.Chrome): The active Selenium WebDriver.
        market_cap (int): The minimum market cap to input in the screening form.

    Returns:
        Optional[str]: The page source HTML if successful, or None if any step times out.
    """
    try:
        # Wait for the market cap input to appear
        market_cap_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "MinimumMarketCap"))
        )
        market_cap_field.clear()
        market_cap_field.send_keys(str(market_cap))
        logger.debug("Entered Minimum Market Cap: %s", market_cap)

        # Select the radio button for 50 stocks (value="false")
        number_of_stocks_radio = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@id='Select30' and @value='false']"))
        )
        number_of_stocks_radio.click()
        logger.debug("Selected Number of Stocks radio button.")

        # Click "Get Stocks" button
        get_stocks_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input.button[value='Get Stocks']"))
        )
        get_stocks_button.click()
        logger.debug("Clicked 'Get Stocks' button.")

        # Wait for results page to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(2)  # Additional delay for page content to render fully

        logger.info("Fetched HTML for market cap %s successfully.", market_cap)
        return driver.page_source

    except TimeoutException as e:
        logger.error("Timeout while fetching screening results for market cap %s: %s", market_cap, e)
        return None


def save_html_to_file(html_content: str, filepath: Path) -> None:
    """
    Save the provided HTML content to the specified file.

    Args:
        html_content (str): The HTML content to be saved.
        filepath (Path): Filesystem path where the HTML file will be written.
    """
    try:
        with filepath.open(mode="w", encoding="utf-8") as f:
            f.write(html_content)
        logger.info("Saved HTML to %s", filepath)
    except Exception as e:
        logger.error("Error writing HTML to %s: %s", filepath, e)


def fetch_screening_html(
    market_caps: List[int],
    # driver_path: str,
    username: str,
    password: str,
    output_directory: str = "./monthly_magic_formula/tickers_from_html"
) -> None:
    """
    Main entry point for fetching screening HTML pages for multiple market caps
    from Magic Formula Investing. Logs into the website, iterates through the
    provided market caps, and saves HTML files locally.

    Args:
        market_caps (List[int]): A list of market cap values to screen.
        username (str): Magic Formula Investing username or email.
        password (str): Magic Formula Investing password.
        output_directory (str, optional): Directory to store the resulting HTML files.
            Defaults to "./monthly_magic_formula/tickers_from_html".

    Usage Example:
        fetch_screening_html(
            market_caps=[250, 500, 1000],
            driver_path="C:/path/to/chromedriver.exe",
            username="user@example.com",
            password="supersecret",
            output_directory="./output_html"
        )
    """
    driver = init_webdriver()
    output_dir_path = Path(output_directory)
    output_dir_path.mkdir(parents=True, exist_ok=True)

    try:
        # Login
        login_to_magic_formula_investing(driver, username, password)

        # For each market cap, fetch the HTML and save it
        for cap in market_caps:
            # Navigate to the screening page fresh each time
            screening_url = "https://www.magicformulainvesting.com/Screening/StockScreening"
            driver.get(screening_url)

            # Wait a bit for page to load
            time.sleep(2)

            html_content = fetch_single_screening_html(driver, cap)
            if html_content:
                filename = f"stock_screening_results_{cap}.html"
                save_html_to_file(html_content, output_dir_path / filename)
            else:
                logger.warning("No HTML returned for market cap %s. Skipping save step.", cap)

            # Sleep between iterations to allow the website to reset
            time.sleep(2)

    except SystemExit as e:
        logger.error("SystemExit encountered during the process: %s", e)
        # Could handle or just re-raise
        raise
    finally:
        logger.debug("Closing WebDriver.")
        driver.quit()
