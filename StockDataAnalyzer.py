# Run 'pip install pandas datetime alpha_vantage pygal scikit-learn'
import pandas as pd
from datetime import datetime
from alpha_vantage.timeseries import TimeSeries
import pygal
from sklearn.preprocessing import MinMaxScaler


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
        if time_series == 1:
            data, _ = ts.get_intraday(symbol=symbol, interval='60min', outputsize='full')
        elif time_series == 2:
            data, _ = ts.get_daily(symbol=symbol, outputsize='full')
        elif time_series == 3:
            data, _ = ts.get_weekly(symbol=symbol)
        elif time_series == 4:
            data, _ = ts.get_monthly(symbol=symbol)
    except ValueError as e:
        print(f"Error occurred: {e}")
        return None

    if data.empty:
        print(f"No data available for symbol {symbol}")
        return None
    # For debug
    # print(data)
    return data

# Function to filter based on provided date range
def filter_by_date_range(data, start_date, end_date):
    # Convert the start and end dates to datetime objects without timezone localization
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Print the start and end dates (debug)
    # print(f"Start date: {start_date}")
    # print(f"End date: {end_date}")

    # Sort the DataFrame's index in ascending order
    data = data.sort_index()

    # Print the first and last timestamps in the DataFrame's index (debug)
    # print(f"First timestamp in data: {data.index[0]}")
    # print(f"Last timestamp in data: {data.index[-1]}")

    # Filter the data
    filtered_data = data.loc[start_date:end_date]

    # Print the filtered data (debug)
    # print("Filtered data:")
    # print(filtered_data)

    return filtered_data

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

def validate_yes_no(response):
    return response.lower() in ['yes', 'no', 'y', 'n']

# Function to plot the data
def plot_data(df, chart_type="line", normalize=False, time_series=None):
    rename_dict = {'1. open': 'Open', '2. high': 'High', '3. low': 'Low', '4. close': 'Close'}
    df.rename(columns=rename_dict, inplace=True)

    if normalize:
        scaler = MinMaxScaler()
        df[['Open', 'High', 'Low', 'Close']] = scaler.fit_transform(df[['Open', 'High', 'Low', 'Close']])

    # Create a line or bar chart based on user input
    if chart_type == "line":
        chart = pygal.Line(x_label_rotation=20, x_value_formatter=lambda dt: dt.strftime('%d-%m-%Y %H:%M:%S'))
    elif chart_type == "bar":
        chart = pygal.Bar(x_label_rotation=45)  # Rotate x-labels by 45 degrees
    else:
        print("Unsupported chart type")
        return

    # Add title and labels
    chart.title = 'Stock Data'
    chart.x_title = 'Date'
    chart.y_title = 'Value'

    # Change the date format to include time if time_series is 1 (intraday)
    if time_series == 1:
        chart.x_labels = map(lambda d: d.strftime('%Y-%m-%d %H:%M:%S'), df.index)
    else:
        chart.x_labels = map(lambda d: d.strftime('%Y-%m-%d'), df.index)

    # Convert each column to numeric and drop non-numeric rows
    for col in ['Open', 'High', 'Low', 'Close']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        df = df.dropna(subset=[col])

        # Add data to chart
        chart.add(col, df[col].tolist())
    
    # Render chart in browser
    chart.render_in_browser()

# Main function to get user input and plot data
def main():
    # Welcome message
    print("Welcome to the Stock Data Analyzer!")

    while True:
        # Prompt the user to enter the stock symbol
        symbol = get_input("Please enter the stock symbol (1-5 alphabets): ", validate_stock_name, "Invalid stock symbol. It should be 1-5 alphabets.")

        # Prompt the user to select the time series
        time_series = int(get_input("Please select the time series (1: Intraday, 2: Daily, 3: Weekly, 4: Monthly): ", validate_time_series, "Invalid choice. Please enter a number between 1 and 4."))

        # Fetch the data
        print("\nFetching stock data...\n")
        data = get_data(symbol, '67ZV81HC5LKYSLBY', time_series)

        # If the user chose the intraday option, inform them about the valid date range
        if time_series == 1:
            print(f"Data fetched from {data.index.min().date()} to {data.index.max().date()}. Please select a date range within this period.")

        # Prompt the user to enter the start and end dates
        start_date = get_input("Please enter the start date (YYYY-MM-DD): ", validate_date, "Invalid date. Please enter a date in the format YYYY-MM-DD.")
        end_date = get_input("Please enter the end date (YYYY-MM-DD): ", validate_date, "Invalid date. Please enter a date in the format YYYY-MM-DD.")
        while not validate_date_range(start_date, end_date):
            print("Invalid date range. The end date must be after the start date.")
            start_date = get_input("Please enter the start date (YYYY-MM-DD): ", validate_date, "Invalid date. Please enter a date in the format YYYY-MM-DD.")
            end_date = get_input("Please enter the end date (YYYY-MM-DD): ", validate_date, "Invalid date. Please enter a date in the format YYYY-MM-DD.")

        # Check if data is None
        if data is None:
            print("Failed to fetch data. Please check your inputs and try again.")
            return

        # Filter the data
        print("\nFiltering data...\n")
        filtered_data = filter_by_date_range(data, start_date, end_date)

        # Check if filtered data is empty
        if filtered_data.empty:
            print("No data available for the selected date range. Please try a different date range.")
            continue

        # Prompt the user to select the chart type
        chart_type = get_input("Please select the chart type (1: line, 2: bar): ", validate_chart_type, "Invalid choice. Please enter 1 for line or 2 for bar.")
        chart_type = "line" if chart_type == "1" else "bar"

        # Prompt the user to choose whether to normalize the data (for bar charts only)
        normalize = False
        if chart_type == "bar":
            normalize_str = get_input("Do you want to normalize the data to better visualize changes? (yes/no): ", validate_yes_no, "Invalid input. Please enter yes/no.")
            normalize = normalize_str.lower() in ["yes", "y"]

        # Plot the data
        print("\nPlotting data...\n")
        plot_data(filtered_data, chart_type, normalize, time_series)

        print("Done!")

        # Ask the user if they want to create another graph
        while True:
            another_graph_str = get_input("Do you want to create another graph? (yes/no): ", validate_yes_no, "Invalid input. Please enter yes/no.")
            another_graph = another_graph_str.lower()
            if another_graph in ["yes", "y"]:
                break
            elif another_graph in ["no", "n"]:
                return


# Checks if script is run directly and calls the main function
if __name__ == "__main__":
    main()
