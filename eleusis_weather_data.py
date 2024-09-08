import pandas
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup

import calendar

import pandas as pd


def get_weather_data(year: int, month: int):
    """
        Fetches weather data and the number of days for a given month and year from
        the provided URL using Selenium.

        Args:
            :param year: The year for which to retrieve data.
            :param month: The month for which to retrieve data.

        Returns:
            :param data: A list containing the extracted weather data.
            :param days_in_month: The days for the specific date
        """

    days_in_month = calendar.monthrange(year=year, month=month)

    executable_path = ('C:/Users/SpaceYellow/Desktop/Output/Selenium/'
                       'chromedriver-win64/chromedriver.exe')
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
        print("Loading took too much")

    driver.quit()
    return int(days_in_month[1]), data[2:]


def create_dataframe(days_in_month: int, data: list):
    """
    Creates a pandas DataFrame from the extracted weather data.

    Args:
        :param days_in_month: Days in the specific month
        :param data: A list containing the extracted weather data.

    Returns:
        :param df: A DataFrame containing weather data columns.
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


def save_to_csv(df: pandas.DataFrame, filename: str):
    """
    Saves the DataFrame to a CSV file.

    Args:
        :param df: The DataFrame to save.
        :param filename: The name of the CSV file.
    """
    path = fr"C:\Users\SpaceYellow\Desktop\Python\Projects\Weather\{filename}.csv"

    if df is not None:
        df.to_csv(path, index=False)


def main():
    """
        Main function to get user input, build URL, and call helper functions.
        """

    year, month = int(input("Year: ")), int(input("Month: "))

    days, data = get_weather_data(year=year, month=month)
    df = create_dataframe(days_in_month=days, data=data)
    save_to_csv(df, f'eleusis_{year}_{month}')


if __name__ == "__main__":
    main()
