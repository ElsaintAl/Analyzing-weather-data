import numpy as np


class ConverterToSIWeather:
    """
    A class for converting temperatures, wind speed and pressure from Imperial weather units to SI weather units.
    """

    def clean_temp(self, temp_str, len=10):
        """
        Strips leading/trailing whitespace, quotes, and brackets from a temperature string.

        Args:
            :param temp_str: A string representing the cell data.
            :param len: The string length of the cell data

        Returns:
            A cleaned string representing the temperature.
        """

        if len < 10:
            return temp_str.strip()[1:].replace(",", "").replace("'", "")

        return temp_str.strip()[1:-1].replace(",", "").replace("'", "")

    def to_celsius(self, temp):
        """
        Converts a list of Fahrenheit temperatures to Celsius.

        Args:
            :param temp: A list of Fahrenheit temperatures.

        Returns:
            A list of Celsius temperatures.
        """

        far = np.array(temp)
        cel = np.round(5 / 9 * (far - 32), decimals=2)
        return cel

    def to_float(self, s):
        """
        Converts a string representation of a temperature list to a list of floats.

        Args:
            :param s: A string representing a list of temperatures.

        Returns:
            A list of floats representing the converted temperatures.
        """
        return [float(item) for item in s.strip()[1:-1].replace(",", "").split()]

    def to_mps(self, mph):
        """
        Converts wind speed from miles per hour (mph) to meters per second (m/s).

        Args:
            :param mph: A list or array of wind speeds in miles per hour.

        Returns:
            :return mps: A list or array of wind speeds in meters per second.
        """
        mps = np.array(mph)

        return np.round(mps, 2)

    def to_hPc(self, inches):
        """
        Converts pressure from inches to hectoPascal (hPa).

        Args:
            :param inches: A list or array of pressures in inches.

        Returns:
            :returns: A list or array of pressures in hectoPascal.
        """
        hPc = np.array(inches)

        return np.round(hPc * 33.8639, 2)


# Example usage
"""
converter = TemperatureConverter()
temp_str = "['91', '82.7', '75']"
cleaned_temp = converter.clean_temp(temp_str)
float_temps = converter.to_float(cleaned_temp)
celsius_temps = converter.to_celsius(float_temps)

print(celsius_temps)
"""
