from StrategyTester import StrategyTester
import numpy as np
import pandas as pd
import plotly.graph_objects as go 
from plotly.subplots import make_subplots
from itertools import product
import sys
import warnings
warnings.filterwarnings('ignore')
pd.options.plotting.backend ="plotly"



class Momentum_TimeSeries_Tester(StrategyTester):
    def __init__(self):
        self.cmd_line = "python Momentum_TimeSeries_Tester name='stock_name' start='YYYY-MM-DD' end='YYYY-MM-DD' long_only='True/False'"
        self.strategy_name = "Momentum_TimeSeries Strategy"
        

    def run_Strategy(self,window,tc=0):
        self.data["position"] = np.where(self.data["daily_returns"].rolling(window).mean() >= 0 ,1 ,
                                        np.where(self.data["daily_returns"].rolling(window).mean() < 0 ,self.short,np.nan)
                                        )
        self.data["position"].ffill(inplace=True)
        self.data["Strategy_returns"] = self.data["daily_returns"]*self.data["position"].shift(1)
        if (tc != 0) :
            self.apply_transation_cost(tc)
        
        
        
    
    def plot_data_curve(self):
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace( go.Scatter(y=self.data["daily_returns"],x=self.data.index,name="daily_returns"),secondary_y=False)
        fig.add_trace( go.Scatter(y=self.data["Strategy_returns"],x=self.data.index,name="Strategy_returns"),secondary_y=False)
        fig.add_trace( go.Scatter(y=self.data["position"]*self.amount,x=self.data.index,name="position"),secondary_y=True)
        fig.show(block=True)

        
    def optimise_Strategy(self,windowlist,tcList):
        self.result = pd.DataFrame(columns=["Window","Transation_Cost","Strategy_returns","daily_returns"])
        for window,tc in product(windowlist,tcList):
            self.run_Strategy(window,tc)
            df  = self.data[["Strategy_returns","daily_returns"]].cumsum().apply(np.exp)[-1:]
            if (len(df.index) == 1):
                self.result = pd.concat([self.result, 
                        pd.DataFrame([[window, df.iloc[0][0], df.iloc[0][1]]], 
                                    columns=["Window", "Transation_Cost","Strategy_returns", "daily_returns"])], 
                        ignore_index=True)
    


if __name__ == "__main__":
    s = Momentum_TimeSeries_Tester()
    s.parse_and_initialize(sys.argv)
#     windowList = [i for i in range(1,10,1)]
#     tcList = [round(i,2) for i in np.arange(0.0,1.1,0.1)]
#     s.optimise_Strategy(windowList,tcList)
#     s.result.sort_values(by=['Strategy_returns'],ascending=False,inplace=True)
#     print(s.result.head())
#     s.run_Strategy(s.result.iloc[0][0],s.result.iloc[0][1])
    s.run_Strategy(6,0.1)
    s.plot_data_curve()
    s.plot_performance_stats()



