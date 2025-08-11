import pandas as pd 
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot  as plt
import warnings
warnings.filterwarnings('ignore')
def load():
    try:        
        data = pd.read_csv('data/time_serious.csv', header=[0, 1], parse_dates=[0], index_col=0)

        Price=data['Close']
        returns=Price.pct_change().dropna()
        train_size=int(len(data)*0.8)
        train,test=data.iloc[:train_size],data.iloc[train_size:]
        
        return train,test
    except Exception as e:
        print(f'load First the Notebook/transferable.ipynb the file is excuted there {e}')
def Arima(train, test):
    assets = ['TSLA', 'BND', 'SPY']
    
    # Create a single plot figure
    plt.figure(figsize=(14, 7))
    
    # Define a color palette for the stocks to ensure each has a distinct set of colors
    stock_colors = {
        'TSLA': {'train': 'blue', 'test': 'darkblue', 'forecast': 'lightblue'},
        'BND': {'train': 'green', 'test': 'darkgreen', 'forecast': 'lightgreen'},
        'SPY': {'train': 'red', 'test': 'darkred', 'forecast': 'lightcoral'}
    }
    
    for col in assets:
        # Fit the ARIMA model for each stock
        model = ARIMA(train[('Close', col)], order=(1, 1, 1))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=len(test))
        
        # Plot the data for the current stock with its specific colors
        plt.plot(train.index, train[('Close', col)], label=f'{col} Train', color=stock_colors[col]['train'])
        plt.plot(test.index, test[('Close', col)], label=f'{col} Test', color=stock_colors[col]['test'])
        plt.plot(test.index, forecast, label=f'{col} Forecast', color=stock_colors[col]['forecast'], linestyle='--')
    
    plt.title("Forecast for the Three Stocks using ARIMA")
    plt.xlabel("Date")
    plt.ylabel("Close Price")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
if __name__ == '__main__':
    train,test=load()
    Arima(train,test)