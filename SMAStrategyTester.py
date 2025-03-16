from StrategyTester import StrategyTester
import numpy as np
import pandas as pd
import plotly.graph_objects as go 
from plotly.subplots import make_subplots
from itertools import product
import sys



class SMAStrategyTester(StrategyTester):
    def __init__(self):
        self.cmd_line = "python SMAStrategyTester name='stock_name' start='YYYY-MM-DD' end='YYYY-MM-DD' long_only='True/False'"
        self.strategy_name = "Simple Moving Average"
        

    def run_Strategy(self,SMA1,SMA2):
        self.data["SMA1"] = self.data["Close"].rolling(SMA1).mean()
        self.data["SMA2"] = self.data["Close"].rolling(SMA2).mean()
        self.data["position"] = np.where((self.data['SMA1'].shift(2) < self.data['SMA2'].shift(2)) &
                                        (self.data['SMA1'].shift(1) > self.data['SMA2'].shift(1)),1,
                            np.where((self.data['SMA1'].shift(2) > self.data['SMA2'].shift(2)) &
                                        (self.data['SMA1'].shift(1) < self.data['SMA2'].shift(1)),self.short,np.nan
                                    ) 
                            )
        self.data["position"].ffill(inplace=True)
        self.data["Strategy_returns"] = self.data["daily_returns"]*self.data["position"]
    
    def plot_sma_curve(self):
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace( go.Scatter(y=self.data["SMA1"],x=self.data.index,name="SMA1"),secondary_y=False)
        fig.add_trace( go.Scatter(y=self.data["SMA2"],x=self.data.index,name="SMA2"),secondary_y=False)
        fig.add_trace( go.Scatter(y=self.data["position"],x=self.data.index,name="position"),secondary_y=True)
        fig.show(block=True)

        
    def optimise_Strategy(self,sma1list,sma2list):
        self.result = pd.DataFrame(columns=["SMA1","SMA2","Strategy_returns","daily_returns"])
        for sma1,sma2 in product(sma1list,sma2list):
            if sma2 <= sma1 :
                continue
            self.run_Strategy(sma1,sma2)
            df  = self.data[["Strategy_returns","daily_returns"]].cumsum().apply(np.exp)[-1:]
            if (len(df.index) == 1):
                self.result = pd.concat([self.result, 
                        pd.DataFrame([[sma1,sma2, df.iloc[0][0], df.iloc[0][1]]], 
                                    columns=["SMA1","SMA2", "Strategy_returns", "daily_returns"])], 
                        ignore_index=True)

if __name__ == "__main__":
    s = SMAStrategyTester()
    s.parse_and_initialize(sys.argv)
    sma1list = [i for i in range(1,100,10)]
    sma2list = [i for i in range(50,300,20)]
    s.optimise_Strategy(sma1list,sma2list)
    s.result.sort_values(by=['Strategy_returns'],ascending=False,inplace=True)
    print(s.result.head())
    s.run_Strategy(s.result.iloc[0][0],s.result.iloc[0][1])
    s.plot_sma_curve()
    s.plot_performance_stats()
