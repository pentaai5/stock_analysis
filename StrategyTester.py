from DataDownLoader import DataDownLoader
import pandas as pd
import numpy as np
import warnings
import plotly.graph_objects as go 
from plotly.subplots import make_subplots
warnings.filterwarnings('ignore')
pd.options.plotting.backend ="plotly"

class StrategyTester:
    
    def prepare_financial_data(self):
        self.data=DataDownLoader(self.context["name"],self.context["start"],self.context["end"],"yahoo").download_data()
        if self.data is None:
            raise ValueError(f"Failed to download data for {self.context['name']}. Please check the stock ticker or data source.")
        self.data["daily_returns"] = np.log(self.data["Close"] / self.data["Close"].shift(1))
    
    def plot_performance_stats(self):
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace( go.Scatter(y=self.data["daily_returns"].cumsum().apply(np.exp)*self.amount,
                                x=self.data.index,name="daily_returns"),secondary_y=False)
        fig.add_trace( go.Scatter(y=self.data["Strategy_returns"].cumsum().apply(np.exp)*self.amount,
                                x=self.data.index,name="Strategy_returns"),secondary_y=False)
        fig.add_trace( go.Scatter(y=self.data["position"],x=self.data.index,name="position"),secondary_y=True)
        fig.layout.update(title=self.strategy_name)
        fig.show(block=True)
    
    def get_attribute_value(self,parameter):
        lst = parameter.split("=")
        if (len(lst) != 2):
            raise BaseException(self.cmd_line)
        return (lst[0],lst[1])
        
    def parse_and_initialize(self,param_dictionary):
        self.context = {}
        for j,i in enumerate(param_dictionary):
            if j == 0 : continue
            param,value = self.get_attribute_value(i)
            self.context[param] = value
        if "amount" not in self.context :self.amount = 1
        else : self.amount = float(self.context["amount"])
        self.initialize()
    
    def verifyParams(self):
        mandatory_params = ["start","end","long_only","name"]
        if not all (k in self.context for k in mandatory_params):
            raise BaseException(self.cmd_line)

    def initialize(self):
        self.verifyParams()
        self.prepare_financial_data()
        self.short = 0 if self.context["long_only"] == "True" else -1
        
    def apply_transation_cost(self,tc):
        trades = self.data["position"].diff().fillna(0) != 0
        self.data["Strategy_returns"][trades] -= tc
