import yfinance as yf

class DataDownLoader :

    def __init__(self, stock, start, end, source):
        self.stock_ = stock
        self.start_ = start
        self.end_ = end
        self.source_ = source
    
    def download_data(self) :
        try:
            data = yf.download(self.stock_, start=self.start_, end=self.end_)
            if data.empty:
                raise ValueError(f"No data found for {self.stock_}")
            return data
        except Exception as e:
            print(f"Failed to download data for {self.stock_}: {e}")
            return None