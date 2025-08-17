import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import tkinter as tk
from tkinter import messagebox

# Define thresholds for fundamental analysis
thresholds = {
    'pe_ratio': 20,
    'roe': 15,
    'debt_to_equity': 1,
    'dividend_yield': 3
}

# Fetch stock price data
def get_stock_data(ticker, period="1mo", interval="1d"):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period, interval=interval)
    return data

# Fetch fundamental data
def get_fundamental_data(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    stock_data = {
        'symbol': ticker,
        'pe_ratio': info.get('trailingPE', None),
        'roe': info.get('returnOnEquity', None),
        'debt_to_equity': info.get('debtToEquity', None),
        'dividend_yield': info.get('dividendYield', None)
    }
    return stock_data

# Apply linear regression to predict next open price
def predict_next_price(data):
    data['Index'] = np.arange(len(data))
    X = data[['Index']].values
    y = data['Open'].values
    model = LinearRegression()
    model.fit(X, y)
    next_index = len(data)
    next_price = model.predict([[next_index]])
    return next_price[0]

# Evaluate fundamentals
def evaluate_fundamentals(stock_data):
    good_count = 0
    total_metrics = 4
    if stock_data['pe_ratio'] and stock_data['pe_ratio'] <= thresholds['pe_ratio']:
        good_count += 1
    if stock_data['roe'] and stock_data['roe'] >= thresholds['roe']:
        good_count += 1
    if stock_data['debt_to_equity'] and stock_data['debt_to_equity'] <= thresholds['debt_to_equity']:
        good_count += 1
    if stock_data['dividend_yield'] and stock_data['dividend_yield'] >= thresholds['dividend_yield']:
        good_count += 1

    if good_count == total_metrics:
        rating = "Good"
    elif good_count >= total_metrics / 2:
        rating = "Neutral"
    else:
        rating = "Bad"

    return rating

# Display results
def analyze_stock(ticker):
    data = get_stock_data(ticker)
    if data.empty:
        messagebox.showerror("Error", "No data found for the specified stock symbol.")
        return

    # Price Prediction
    next_price = predict_next_price(data)
    
    # Fundamental Analysis
    stock_data = get_fundamental_data(ticker)
    fundamental_rating = evaluate_fundamentals(stock_data)

    # Display Results
    result_text = f"Predicted Next Open Price: {next_price:.2f}\n"
    result_text += f"Fundamental Rating: {fundamental_rating}\n"
    result_text += f"P/E Ratio: {stock_data['pe_ratio']}\n"
    result_text += f"ROE: {stock_data['roe']}\n"
    result_text += f"Debt-to-Equity Ratio: {stock_data['debt_to_equity']}\n"
    result_text += f"Dividend Yield: {stock_data['dividend_yield']}"
    
    messagebox.showinfo("Stock Analysis Result", result_text)

# Tkinter UI setup
def submit_stock():
    ticker = stock_entry.get().upper() + ".NS"  # NSE stock symbol format
    analyze_stock(ticker)

# Set up Tkinter window
root = tk.Tk()
root.title("Stock Analysis with Prediction and Fundamentals")
root.geometry("500x300")

# Input for stock ticker
tk.Label(root, text="Enter Stock Symbol (e.g., TCS, RELIANCE):", font=("Arial", 12)).pack(pady=10)
stock_entry = tk.Entry(root, font=("Arial", 12))
stock_entry.pack(pady=5)

# Button to submit stock for analysis
submit_button = tk.Button(root, text="Analyze", command=submit_stock, font=("Arial", 12), bg="green", fg="white")
submit_button.pack(pady=20)

# Run Tkinter main loop
root.mainloop()
