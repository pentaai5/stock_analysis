# Strategies in Python

## Introduction
This project provides a collection of trading strategy testers implemented in Python. It includes multiple strategies for technical analysis, such as moving averages, Bollinger Bands, RSI, and momentum-based indicators. The goal is to test and evaluate different trading strategies using historical market data.

## Features
- Backtesting framework for multiple trading strategies.
- Includes Exponential Moving Average (EMA), Simple Moving Average (SMA), Bollinger Bands, RSI, VWAP, and Momentum-based strategies.
- Supports downloading historical market data.
- Modular implementation to extend and customize strategies.

## Technologies Used
- Python 3.x
- Pandas (for data manipulation)
- NumPy (for numerical computations)
- Matplotlib (for visualization)
- yfinance (for data fetching)
- Other common Python libraries

## Project Structure
```
Strategies_in_python-main/
│── StrategyTester.py               # Main script for strategy testing
│── DataDownLoader.py               # Downloads historical market data
│── ExponentialMovingAverage.py     # Implements EMA strategy
│── SMAStrategyTester.py            # Tests SMA strategy
│── BollingerBandTester.py          # Implements Bollinger Bands strategy
│── RSIStrategyTester.py            # Tests RSI strategy
│── Momentum_TimeSeries_Tester.py   # Tests momentum-based strategies
│── VWAPStratergyTester.py          # Implements VWAP strategy
│── .vscode/settings.json           # VS Code workspace settings (optional)
│── __pycache__/                     # Compiled Python files (ignore)
```

## Running the Strategy Tester
Run a specific strategy tester script using:
```bash
python StrategyTester.py name='STOCK_TICKER' start='YYYY-MM-DD' end='YYYY-MM-DD' long_only='True/False'
```
Replace `StrategyTester.py` with the relevant script name, such as BollingerBandTester.py.

An example command would be
```bash
python BollingerBandTester.py name='6758.T' start='2024-01-01' end='2025-01-01' long_only='False'
```


