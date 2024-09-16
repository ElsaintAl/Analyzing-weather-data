import calendar
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

from to_SI import new_si
from date import DateGenerator


def main():
    filename = 'spata_venizelos_2024_5.csv'
    dg = DateGenerator(filename)
    multi_histogram(filename)
#    temp_humidity_corr(filename)
#    month_temp_l_plot(filename, dg)


def create_df(filename):
    return new_si(filename)


def get_month_name(month_number):
    """Returns the name of the month corresponding to the given number."""
    return calendar.month_name[month_number]


def get_days(month, year):
    """Returns the days corresponding to the given month number."""
    return calendar.monthrange(year, month)[1]


def get_temp(filename):
    df = create_df(filename)
    h_temp, a_temp, l_temp = [], [], []

    for temp in df['Temperature (°C)'][1:]:
        h_temp.append(temp[0])
        a_temp.append(temp[1])
        l_temp.append(temp[2])

    return h_temp, a_temp, l_temp


def get_humidity(filename):
    df = create_df(filename)
    l_humi, a_humi, h_humi = [], [], []

    for temp in df['Humidity (%)'][1:]:
        h_humi.append(temp[0])
        a_humi.append(temp[1])
        l_humi.append(temp[2])
    return h_humi, a_humi, l_humi


def get_dew_point(filename):
    df = create_df(filename)
    l_dew, a_dew, h_dew = [], [], []

    for temp in df['Dew Point (°C)'][1:]:
        h_dew.append(temp[0])
        a_dew.append(temp[1])
        l_dew.append(temp[2])

    return h_dew, a_dew, l_dew


def get_pressure(filename):
    df = create_df(filename)
    l_pres, a_pres, h_pres = [], [], []

    for temp in df['Pressure (hPc)'][1:]:
        h_pres.append(temp[0])
        a_pres.append(temp[1])
        l_pres.append(temp[2])

    return h_pres, a_pres, l_pres


def month_temp_l_plot(filename, date_generator):
    """
    Generate the required data and plots the high vs. low temperatures for a specif month.
    :param filename: The cvs file.
    :param date_generator: The date generator class.
    """

    h_temp, a_temp, l_temp = get_temp(filename)
    month, year = date_generator.get_month_year()
    dates = date_generator.get_dates()
    plt.style.use('classic')

    fig, ax = plt.subplots()
    ax.plot(dates, h_temp, c='red', alpha=0.5)
    ax.plot(dates, l_temp, c='blue', alpha=0.5)
    plt.fill_between(dates, h_temp, l_temp, facecolor='blue', alpha=0.1)

    # Format plot.
    plt.grid(visible=True)
    plt.title(f'Daily high and lows temperatures, {get_month_name(month)} {year}', fontsize=24)
    plt.xlabel('', fontsize=16)
    fig.autofmt_xdate()
    plt.ylabel('Temperature (°C)', fontsize=16)
    plt.tick_params(axis='both', which='minor', labelsize=16, grid_alpha=0.5)
    plt.xticks(dates[4::5])

    plt.show()


def week_temp_l_plot(date):
    pass


def temp_humidity_corr(filename):
    """
        Generate the required data and plots the high vs. low temperatures for a specif month.
        :param filename: The cvs file.
        """

    h_temp, a_temp, l_temp = get_temp(filename)
    h_humi, a_humi, l_humi = get_humidity(filename)
    a_df = pd.DataFrame({'Average Temperature (°C)': a_temp,
                         'Average Humility (%)': a_humi})
    l_df = pd.DataFrame({'Low Temperature (°C)': a_temp,
                         'Low Humility (%)': a_humi})
    h_df = pd.DataFrame({'High Temperature (°C)': a_temp,
                         'High Humility (%)': a_humi})
#    sns.set(style="ticks", color_codes=True)
#    l_g = sns.pairplot(l_df)
#    a_g = sns.pairplot(a_df)
#    h_g = sns.pairplot(h_df)

    plt.hist(l_temp, bins=31, edgecolor='black')
    plt.xlabel('Temperature')
    plt.ylabel('Days')
    plt.title('High Temperature')

    plt.show()


def multi_histogram(filename):
    """
    Creates a histogram graph for the average temperature, humidity, pressure and dew point
    :param filename:
    """
    a_temp = get_temp(filename)[1]
    a_humi = get_humidity(filename)[1]
    a_pres = get_pressure(filename)[1]
    a_dew = get_dew_point(filename)[1]
    df = pd.DataFrame({'Temperature (°C)': a_temp[1:],
                       'Humidity (%)': a_humi[1:],
                       'Pressure (hPc)': a_pres[1:],
                       'Dew Point (°C)': a_dew[1:]})

    figure, axis = plt.subplots(2, 2)

    axis[0, 0].hist(df['Temperature (°C)'], bins=15, edgecolor='black')
    axis[0, 0].set_title("Temperature (°C)")

    axis[0, 1].hist(a_humi, bins=15, edgecolor='black')
    axis[0, 1].set_title("Humidity (%)")
    axis[1, 0].hist(a_pres, bins=15, edgecolor='black')
    axis[1, 0].set_title("Pressure (hPc)")

    axis[1, 1].hist(df['Dew Point (°C)'], bins=15, edgecolor='black')
    axis[1, 1].set_title("Dew Point (°C)")
    df['Dew Point (°C)'].plot.kde(zorder=2, color='C1')

    plt.show()


def precipitation_wind_speed_corr():
    pass


def temp_precipitation_dist():
    pass


def seasonal():
    pass


if __name__ == "__main__":
    main()
