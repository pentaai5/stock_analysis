from StrategyTester import StrategyTester
import numpy as np
import pandas as pd
import plotly.graph_objects as go 
from plotly.subplots import make_subplots
from itertools import product
import sys



class RSIStrategyTester(StrategyTester):
    def __init__(self):
        self.cmd_line = "python RSIStrategyTester name='stock_name' start='YYYY-MM-DD' end='YYYY-MM-DD' long_only='True/False'"
        self.strategy_name = "RSI Strategy"
        

    def run_Strategy(self,window):
        self.data["Gain"] = np.where(self.data["Close"] - self.data["Close"].shift(1) > 0 ,
                                    self.data["Close"] - self.data["Close"].shift(1),0)
        self.data["Loss"] = np.where(self.data["Close"] - self.data["Close"].shift(1) < 0 ,
                                    self.data["Close"].shift(1) - self.data["Close"],0)
        self.data["Average_gain"] = self.data["Gain"].rolling(window).mean()
        self.data["Average_loss"] = self.data["Loss"].rolling(window).mean()
        self.data["MAR"] = self.data["Average_gain"] / self.data["Average_loss"]
        self.data["RSI"] = 100 - 100/(1 + self.data["MAR"])
        self.data["position"] = np.where( self.data["RSI"].shift(1) < 30 ,1 ,
                                        np.where(self.data["RSI"].shift(1) > 70,self.short,np.nan ))
        self.data["position"].ffill(inplace=True)
        self.data["Strategy_returns"] = self.data["daily_returns"]*self.data["position"]
        
        
        
    
    def plot_data_curve(self):
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace( go.Scatter(y=self.data["RSI"],x=self.data.index,name="RSI"),secondary_y=False)
        fig.add_trace( go.Scatter(y=self.data["position"],x=self.data.index,name="position"),secondary_y=True)
        fig.show(block=True)

        
    def optimise_Strategy(self,windowlist):
        self.result = pd.DataFrame(columns=["Window","Strategy_returns","daily_returns"])
        for window in windowlist:
            self.run_Strategy(window)
            df  = self.data[["Strategy_returns","daily_returns"]].cumsum().apply(np.exp)[-1:]
            if (len(df.index) == 1):
                self.result = pd.concat([self.result, 
                        pd.DataFrame([[window, df.iloc[0][0], df.iloc[0][1]]], 
                                    columns=["Window", "Strategy_returns", "daily_returns"])], 
                        ignore_index=True)


if __name__ == "__main__":
    s = RSIStrategyTester()
    s.parse_and_initialize(sys.argv)
    windowList = [i for i in range(5,100,10)]
    s.optimise_Strategy(windowList)
    s.result.sort_values(by=['Strategy_returns'],ascending=False,inplace=True)
    print(s.result.head())
    s.run_Strategy(s.result.iloc[0][0])
    s.plot_data_curve()
    s.plot_performance_stats()
