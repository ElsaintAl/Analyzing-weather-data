from converter import ConverterToSIWeather

import argparse
import pandas as pd
import logging
import os


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def read_weather_data(file: str) -> pd.DataFrame or None:
    """
        Reads weather data from a CSV file into a pandas DataFrame.

        :arg file: The path to the CSV file.

        :returns pd.DataFrame: The weather data DataFrame, or None if an error occurs.
        """

    try:
        df = pd.read_csv(filepath_or_buffer=f'Month_Data/{file}')
        return df
    except (FileNotFoundError, pd.errors.ParserError) as e:
        logger.error(f"Error reading file '{file}': {e}")
        return None


def create_new_column_name(old_column_name: str, new_unit: str) -> str:
    """
    Creates a new column name based on the old column name and the new unit.

    :arg old_column_name: The original column name.
    :arg new_unit: The new unit.

    :returns str: The new column name.
    """
    old_column_name = old_column_name.split(" (")
    return f"{old_column_name[0]} ({new_unit})"


def convert_unit(df: pd.DataFrame, column_name: str, new_unit: str):
    """
    Converts a column in a DataFrame to SI units.

    :arg df: The DataFrame contains the data.
    :arg column_name: The name of the column to convert.
    :arg new_unit: The new unit.

    Returns:
        pd.DataFrame: The DataFrame with the converted column.
    """

    converter = ConverterToSIWeather()
    if column_name == 'Humidity (%)':
        new_column_name = column_name
        df[new_column_name] = df[column_name]
    else:
        new_column_name = create_new_column_name(column_name, new_unit)
        df[new_column_name] = df[column_name]

    df[new_column_name] = [converter.clean_temp(x) for x in df[column_name]]
    df.loc[1:, new_column_name] = df[new_column_name][1:].apply(converter.to_float)

    if column_name in ['Temperature (°F)', 'Dew Point (°F)']:
        df[new_column_name] = df[new_column_name][1:].apply(converter.to_celsius)
        df.loc[0, new_column_name] = df[column_name][0]
    elif column_name == 'Wind Speed (mph)':
        df[new_column_name] = df[new_column_name][1:].apply(converter.to_mps)
        df.loc[0, new_column_name] = df[column_name][0]
    elif column_name in ['Precipitation (in)', 'Pressure (in)']:
        df[new_column_name] = df[new_column_name][1:].apply(converter.to_mps)
        df.loc[0, new_column_name] = df[column_name][0]
    elif column_name == 'Humidity (%)':
        df.loc[0, new_column_name] = df[column_name][0]
        return df
    else:
        raise ValueError(f"Unsupported unit for column: {column_name}")
    return df


def create_output_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a new DataFrame containing the desired weather data columns in SI units.

    :arg df: The converted weather data DataFrame.

    :returns pd.DataFrame: The output DataFrame with selected columns in SI units.
    """

    return df[['Time', 'Temperature (°C)', 'Dew Point (°C)', 'Humidity (%)',
               'Wind Speed (mps)', 'Pressure (hPc)', 'Precipitation (hPc)']]


def si_dataframe(file: str, overwrite: bool = False) -> pd.DataFrame or None:
    """
        Reads weather data, converts units to SI, and creates an output DataFrame.

        :arg file: The path to the CSV file.
        :arg overwrite: Whether to overwrite the output file if it exists.

        :returns pd.DataFrame: The output DataFrame with weather data in SI units,
                               or None if an error occurs.
        """

    df = read_weather_data(file)
    if df is None:
        return None

    column_conversions = [
        ('Temperature (°F)', '°C'),
        ('Dew Point (°F)', '°C'),
        ('Humidity (%)', '%'),
        ('Wind Speed (mph)', 'mps'),
        ('Pressure (in)', 'hPc'),
        ('Precipitation (in)', 'hPc'),
    ]

    for col_name, new_unit in column_conversions:
        convert_unit(df, col_name, new_unit)

    converted_df = create_output_dataframe(df)

    # Check if the output file exists
    output_file = "SI_" + file
    path = fr'C:\Users\SpaceYellow\Desktop\Python\Projects\Weather\SI_Month_Data\{output_file}'

    if os.path.exists(path):
        if overwrite:
            converted_df.to_csv(path, index=False)
            print(f"Saved converted data to {path}.")
    else:
        converted_df.to_csv(path, index=False)
        print(f"Saved converted data to {path}.")

    return converted_df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert weather data to SI units.")
    parser.add_argument("file", help="The input CSV file")
    parser.add_argument("-o", "--overwrite", action="store_true",
                        help="Overwrite the output file if it exists")
    args = parser.parse_args()

    si_dataframe(args.file, args.overwrite)
