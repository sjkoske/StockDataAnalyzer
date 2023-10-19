import pandas as pd
from datetime import datetime
from alpha_vantage.timeseries import TimeSeries
import pygal

# Dictionary to map integers to respective time series function names
time_series_dict = {
    1: "TIME_SERIES_INTRADAY",
    2: "TIME_SERIES_DAILY",
    3: "TIME_SERIES_WEEKLY",
    4: "TIME_SERIES_MONTHLY"
}

# Function to fetch data from Alpha Vantage API
# Uses the provided stock symbol, API key, and time series
def get_data(symbol, api_key, time_series):
    ts = TimeSeries(key=api_key, output_format='pandas')
    try:
        # Fetch data based on the chosen time series
        if time_series == 1:
            data, meta_data = ts.get_intraday(symbol=symbol, interval='60min', outputsize='full')
        elif time_series == 2:
            data, meta_data = ts.get_daily(symbol=symbol, outputsize='full')
        elif time_series == 3:
            data, meta_data = ts.get_weekly(symbol=symbol)
        elif time_series == 4:
            data, meta_data = ts.get_monthly(symbol=symbol)
    except ValueError as e:
        print(f"Error occurred: {e}")
        return None
    # Handle case where no data is avilable for the symbol
    if data.empty:
        print(f"No data available for symbol {symbol}")
        return None
    print('Data:', data)
    print('Meta data:', meta_data)
    return data

# Function to filter based on provided date range
def filter_by_date_range(data, start_date, end_date):
    data = data.sort_index(ascending=True)
    data.index = pd.to_datetime(data.index)
    return data.loc[start_date:end_date]

# Generic function to validate user input
def get_input(prompt, validation_func, error_message):
    while True:
        try:
            value = input(prompt)
            if validation_func(value):
                return value
            else:
                print(error_message)
        except ValueError:
            print("Incorrect value type\n")

# Validate stock symbol
def validate_stock_name(stock):
    return ((stock.isalpha() == True) & ((len(stock) > 0 ) & (len(stock) < 6)))

# Validate chart type
def validate_chart_type(chartType):
    return (chartType == "1" or chartType == "2")

# Validate date
def validate_time_series(timeSeries):
    return (timeSeries == "1" or timeSeries == "2" or timeSeries == "3" or timeSeries == "4")

# Validate date
def validate_date(date):
    try:
        datetime.strptime(date, '%Y-%m-%d')
        return True
    except ValueError:
        return False
    
# Validate date range
def validate_date_range(start_date, end_date):
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    return end >= start

# Function to plot the data
def plot_data(df, chart_type="line"):
    print(df.columns)
    
    # Create a line or bar chart based on user input
    if chart_type == "line":
        chart = pygal.Line(x_label_rotation=20, x_value_formatter=lambda dt: dt.strftime('%d-%m-%Y %H:%M:%S'))
    elif chart_type == "bar":
        chart = pygal.Bar()
    else:
        print("Unsupported chart type")
        return

    # Convert each column to numeric and drop non-numeric rows
    for col in ['1. open', '2. high', '3. low', '4. close']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        df = df.dropna(subset=[col])

        # Add data to chart
        chart.add(col, df[col].tolist())
    
    # Render chart in browser
    chart.render_in_browser()

# Main function to get user input and plot data
def main():
    # Get user inputs
    symbol = get_input("Enter the Stock Symbol you want to use (up to five letters):  ", validate_stock_name, "Input was not in the correct format, try again.\n")
    chart_type = get_input("Choose the chart type: \n1. Bar\n2. Line\n", validate_chart_type, "Please enter either 1 or 2.\n")
    
    # Map the chart_type input to the corresponding string
    chart_type_dict = {"1": "bar", "2": "line"}
    chart_type = chart_type_dict[chart_type]

    # Select the time series of the chart you wish to generate
    time_series = get_input("Select the time series of the chart you wish to generate: \n1. Intraday\n2. Daily\n3. Weekly\n4. Monthly\n", validate_time_series, "Please enter 1, 2, 3, or 4.\n")

    # Validate the start and end dates, ensuring the end date is after the start date
    while True:
        start_date = get_input("Enter StartDate (YYYY-MM-DD): ", validate_date, "Enter your date in the correct format (YYYY-MM-DD).\n ")
        end_date = get_input("Enter End Date (YYYY-MM-DD): ", validate_date, "Enter your date in the correct format (YYYY-MM-DD).\n ")
        if validate_date_range(start_date, end_date):
            break
        else:
            print("End date must be after start date. Please enter the dates again.\n")

    # Fetch data using the Alpha Vantage API
    data = get_data(symbol, "67ZV81HC5LKYSLBY", int(time_series))

    # If data is not None, filter it by the date range and plot it
    if data is not None:
        filtered_data = filter_by_date_range(data, start_date, end_date)
        plot_data(filtered_data, chart_type)

# Checks if script is run directly and calls the main function
if __name__ == "__main__":
    main()
