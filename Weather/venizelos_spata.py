import os
import calendar

import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

from to_SI import si_dataframe
from date import DateGenerator


def main():
    filename = 'spata_venizelos_2024_1.csv'

    dg = DateGenerator(filename)
    multi_histogram(filename, dg)
#    temp_humidity_corr(filename)
#    month_temp_l_plot(filename, dg)


def create_df(filename):
    return si_dataframe(filename)


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
    :param filename: The cvs file name for data generation. The name format is
                     'spata_venizelos_"year_number"_"month_number".csv'
    :param date_generator: The date generator class.
    """

    h_temp, a_temp, l_temp = get_temp(filename)
    month, year = date_generator.get_month_year()
    dates = date_generator.get_dates()
    plt.style.use('classic')

    fig, ax = plt.subplots()
    ax.plot(dates, h_temp, c='r', alpha=0.5, label='High Temp')
    ax.plot(dates, l_temp, c='b', alpha=0.5, label='Low Temp')
    plt.fill_between(dates, h_temp, l_temp, facecolor='#21918c', alpha=0.1)

    # Format plot.
    plt.ylim(min(l_temp)-1, max(h_temp)+1)
    plt.grid(visible=True)
    plt.title(f'Daily high and lows temperatures for {get_month_name(month)} {year} in Spata', fontsize=24)
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


def multi_histogram(filename, date_generator):
    """
    Creates a histogram graph for the average temperature, humidity, pressure and dew point

    :param filename: The cvs file name for data generation. The name format is
                   'spata_venizelos_"year_number"_"month_number".csv'
    :param date_generator: The date generator class.
    """
    dg = date_generator
    month, year = dg.get_month_year()
    a_temp = get_temp(filename)[1]
    a_humi = get_humidity(filename)[1]

    a_pres = get_pressure(filename)[1]
    a_dew = get_dew_point(filename)[1]
    df = pd.DataFrame({'Temperature (°C)': a_temp[1:],
                       'Humidity (%)': a_humi[1:],
                       'Pressure (hPc)': a_pres[1:],
                       'Dew Point (°C)': a_dew[1:]})
    figure, axis = plt.subplots(2, 2)
    plt.suptitle(f'Distribution of weather parameters for {get_month_name(month)} {year} in Spata')
    colors = sns.color_palette("viridis")

    for ax in axis.flatten():  # Flatten the array to iterate over individual Axes objects
        if ax == axis[0, 0]:
            bin_width = 0.5
            sns.histplot(data=df, x='Temperature (°C)', kde=True, stat="probability", color=colors[2],
                         label="Probabilities", binwidth=bin_width, ax=ax)
            ax2 = ax.twinx()
            sns.kdeplot(data=df, x='Temperature (°C)', color="k", label="KDE density", ls=':', lw=2, ax=ax2)
            ax2.set_ylim(0, ax.get_ylim()[1] / bin_width)  # similar limits on the y-axis to align the plots
            ax2.yaxis.set_major_formatter(
                PercentFormatter(1 / bin_width))  # show an axis such that 1/bin_width corresponds to 100%
            ax2.set_ylabel(f'Probability for a bin width of {bin_width}')
            ax.legend(loc='upper left')
            ax2.legend(loc='upper right')

        if ax == axis[0, 1]:
            bin_width = 2
            sns.histplot(data=df, x='Humidity (%)', kde=True, stat="probability", color=colors[2],
                         label="Probabilities", binwidth=bin_width, ax=ax)
            ax2 = ax.twinx()
            sns.kdeplot(data=df, x='Humidity (%)', color="k", label="kde density", ls=':', lw=2, ax=ax2)
            ax2.set_ylim(0, ax.get_ylim()[1] / bin_width)  # similar limits on the y-axis to align the plots
            ax2.yaxis.set_major_formatter(
                PercentFormatter(1 / bin_width))  # show an axis such that 1/bin_width corresponds to 100%
            ax2.set_ylabel(f'Probability for a bin width of {bin_width}')
            ax.legend(loc='upper left')
            ax2.legend(loc='upper right')

        if ax == axis[1, 0]:
            # Get the bin edges
            bin_edges = sns.histplot(data=df, x='Pressure (hPc)', kde=True, stat="probability", color=colors[2],
                                     label="Probabilities", ax=ax).get_xticks()
            # Calculate the bin width
            bin_width = bin_edges[1] - bin_edges[0]

            ax2 = ax.twinx()
            sns.kdeplot(data=df, x='Pressure (hPc)', color="k", label="kde density", ls=':', lw=2, ax=ax2,
                        bw_adjust=0.5, bw_method=1)
            ax2.set_ylim(0, ax.get_ylim()[1] / bin_width)  # similir limits on the y-axis to align the plots
            ax2.yaxis.set_major_formatter(
                PercentFormatter(1 / bin_width))  # show axis such that 1/binwidth corresponds to 100%
            ax2.set_ylabel(f'Probability for a bin width of {round(bin_width, 2)}')
            ax.legend(loc='upper left')
            ax2.legend(loc='upper right')

        if ax == axis[1, 1]:
            bin_width = 1
            sns.histplot(data=df, x='Dew Point (°C)', kde=True, stat="probability", color=colors[2],
                         label="Probabilities", binwidth=bin_width, ax=ax)
            ax2 = ax.twinx()
            sns.kdeplot(data=df, x='Dew Point (°C)', color="k", label="kde density", ls=':', lw=2, ax=ax2)
            ax2.set_ylim(0, ax.get_ylim()[1] / bin_width)  # similar limits on the y-axis to align the plots
            ax2.yaxis.set_major_formatter(
                PercentFormatter(1 / bin_width))  # show an axis such that 1/bin_width corresponds to 100%
            ax2.set_ylabel(f'Probability for a bin width of {bin_width}')
            ax.legend(loc='upper left')
            ax2.legend(loc='upper right')
    plt.tight_layout()

    plt.show()


def precipitation_wind_speed_corr():
    pass


def temp_precipitation_dist():
    pass


def seasonal():
    pass


if __name__ == "__main__":
    main()
