import pandas as pd
from converter import ConverterToSIWeather


def new_si(file):
    converter = ConverterToSIWeather()

    # Read CSV (assuming 'eleusis_2024_8.csv' exists)
    df = pd.read_csv(f'Month_Data/{file}')
    #    if len(df['Time'])  >
    #    df = df.drop(32)

    df['Temperature (°C)'] = df['Temperature (°F)']
    df['Temperature (°C)'] = [converter.clean_temp(x, ) for x in df['Temperature (°C)']]
    df.loc[1:, 'Temperature (°C)'] = df['Temperature (°C)'][1:].apply(converter.to_float)
    df.loc[1:, 'Temperature (°C)'] = df['Temperature (°C)'][1:].apply(converter.to_celsius)

    df['Dew Point (°C)'] = [converter.clean_temp(x, ) for x in df['Dew Point (°F)']]
    df.loc[1:, 'Dew Point (°C)'] = df['Dew Point (°C)'][1:].apply(converter.to_float)
    df.loc[1:, 'Dew Point (°C)'] = df['Dew Point (°C)'][1:].apply(converter.to_celsius)

    df['Humidity (%)'] = [converter.clean_temp(x, ) for x in df['Humidity (%)']]
    df.loc[1:, 'Humidity (%)'] = df['Humidity (%)'][1:].apply(converter.to_float)

    df['Wind Speed (mps)'] = [converter.clean_temp(x, ) for x in df['Wind Speed (mph)']]
    df.loc[1:, 'Wind Speed (mps)'] = df['Wind Speed (mps)'][1:].apply(converter.to_float)
    df.loc[1:, 'Wind Speed (mps)'] = df['Wind Speed (mps)'][1:].apply(converter.to_mps)

    df['Precipitation (hPc)'] = [converter.clean_temp(x, ) for x in df['Precipitation (in)']]
    df.loc[1:, 'Precipitation (hPc)'] = df['Precipitation (hPc)'][1:].apply(converter.to_float)
    df.loc[1:, 'Precipitation (hPc)'] = df['Precipitation (hPc)'][1:].apply(converter.to_mps)

    df['Pressure (hPc)'] = [converter.clean_temp(x, ) for x in df['Pressure (in)']]
    df.loc[1:, 'Pressure (hPc)'] = df['Pressure (hPc)'][1:].apply(converter.to_float)
    df.loc[1:, 'Pressure (hPc)'] = df['Pressure (hPc)'][1:].apply(converter.to_mps)

    df_con = pd.DataFrame(data=df[['Time', 'Temperature (°C)', 'Dew Point (°C)', 'Humidity (%)',
                                   'Wind Speed (mps)', 'Pressure (hPc)', 'Precipitation (hPc)']])
#    path = fr'C:\Users\SpaceYellow\Desktop\Python\Projects\Weather\SI_Month_Data\SI_{file}.csv'
#    df_con.to_csv(path, index=False)

    return df_con


# new_si('spata_venizelos_2024_1.csv')
