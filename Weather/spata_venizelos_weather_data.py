from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup

import calendar

import configparser

import logging

import os

import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_path() -> str or None:
    """
    Retrieves the executable path for ChromeDriver from the config.ini file.
    If the file doesn't exist, it prompts the user for the path, creates the file,
    and stores the path.

    Returns
    -------
    str: The path to the ChromeDriver executable (if found).
    None: If the path is not found in the config file and the user cancels the prompt.
    """

    config = configparser.ConfigParser()

    if not os.path.exists('config.ini'):
        while True:
            exe_path = input('Enter the executable path: ')
            if os.path.exists(exe_path):
                config['paths'] = {'chromedriver': exe_path}
                with open('config.ini', 'w') as configfile:
                    config.write(configfile)
                    break
            else:
                print("Invalid path. Please enter a valid path to the chromedriver executable.")

    config.read('config.ini')

    try:
        executable_path = config['paths']['chromedriver']
    except KeyError:
        logger.error(f"Error: 'chromedriver' path not found in config.ini")
        executable_path = None  # Or set a default path if desired

    return executable_path


def get_weather_data(year: int, month: int) -> tuple[int, list]:
    """
        Fetches weather data and the number of days for a given month and year from
        the provided URL using Selenium.

        Parameters
        ----------
        :param year: The year for which to retrieve data.
        :param month: The month for which to retrieve data.

        Returns
        -------
        data: A list containing the extracted weather data.
        days_in_month: The days for the specific date

        Raise
        -----
        :raise ValueError: If the ChromeDriver executable path is missing.
        """

    days_in_month = calendar.monthrange(year=year, month=month)

    executable_path = get_path()

    if not executable_path:
        raise ValueError('Error: Executable path is missing.')

    service = Service(executable_path=executable_path)

    options = Options()
    options.add_argument('start-maximized')
    options.add_argument('disable-infobars')
    options.add_argument('disable-search-engine-choice-screen')

    driver = webdriver.Chrome(service=service, options=options)

    url = f'https://www.wunderground.com/history/monthly/gr/spata/LGAV/date/{year}-{month}'

    driver.get(url)
    delay = 10
    data = []

    try:
        selector = ('#inner-content > div.region-content-main > div.row > div:nth-child(5) > div:nth-child(1) > div > '
                    'lib-city-history-observation > div > div.observation-table.ng-star-inserted')
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        print("Page is ready!")

        # Get the page source
        page_source = driver.page_source

        # Create a BeautifulSoup object
        soup = BeautifulSoup(page_source, 'html.parser')

        # Try different selectors if necessary
        outer_table = soup.find('div', class_='observation-table ng-star-inserted').find('table')
        if not outer_table:
            outer_table = soup.find('table', class_='days ng-star-inserted')  # Try a different selector
            if not outer_table:
                outer_table = soup.find('table', class_='ng-star-inserted')  # Try a more general selector

        if outer_table:
            # Extract data from the inner tables
            data = []
            for row in outer_table.find_all('tr'):
                cells = row.find_all('td')
                if cells:
                    row_data = []
                    for cell in cells:
                        inner_table = cell.find('table')
                        if inner_table:
                            inner_data = []
                            for inner_row in inner_table.find_all('tr'):
                                inner_cells = inner_row.find_all('td')
                                if inner_cells:
                                    inner_data.append([cell.text.strip() for cell in inner_cells])
                            row_data.append(inner_data)
                        else:
                            row_data.append(cell.text.strip())
                    data.append(row_data)

    except TimeoutException:
        logger.warning(f"Warning: 'Loading took too much")

    driver.quit()
    return int(days_in_month[1]), data[2:]


def create_dataframe(days_in_month: int, data: list):
    """
    Creates a pandas DataFrame from the extracted weather data.

    Parameters
    ----------
    :param days_in_month: Days in the specific month
    :param data: A list containing the extracted weather data.

    Returns
    -------
    df: A DataFrame containing weather data columns.
    """

    if not data:
        return None  # Handle a case where no data is found

    days = days_in_month + 1

    df = pd.DataFrame({'Time': data[:days],
                       'Temperature (°F)': data[days:2*days],
                       'Dew Point (°F)': data[2*days:3*days],
                       'Humidity (%)': data[3*days:4*days],
                       'Wind Speed (mph)': data[4*days:5*days],
                       'Pressure (in)': data[5*days:6*days],
                       'Precipitation (in)': data[6*days:7*days]
                       })

    return df


def save_to_csv(df: pd.DataFrame, filename: str):
    """
    Saves the DataFrame to a CSV file.

    Parameter
    ---------
    :param df: The DataFrame to save.
    :param filename: The name of the CSV file.
    """

    path = fr"C:\Users\SpaceYellow\Desktop\Python\Projects\Weather\Month_Data\{filename}.csv"

    if df is not None:
        df.to_csv(path, index=False)


def main():
    """
        Main function to get user input, build URL, and call helper functions.
        """

    year, month = int(input("Year: ")), int(input("Month: "))

    try:
        days, data = get_weather_data(year=year, month=month)
        df = create_dataframe(days_in_month=days, data=data)
        save_to_csv(df, f'spata_venizelos_{year}_{month}')
    except ValueError as e:
        print(f"Error: {e}"," \nPlease ensure the ChromeDriver executable path is set correctly.")


if __name__ == "__main__":
    main()
