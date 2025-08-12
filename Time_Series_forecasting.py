import pandas as pd 
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot  as plt
import warnings
warnings.filterwarnings('ignore')
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM,Dense,Input

stock_colors = {
        'TSLA': {'train': 'blue', 'test': 'darkblue', 'forecast': 'lightblue'},
        'BND': {'train': 'green', 'test': 'darkgreen', 'forecast': 'lightgreen'},
        'SPY': {'train': 'red', 'test': 'darkred', 'forecast': 'lightcoral'}
    }    
def LSTM():
    data = pd.read_csv('data/scaled_closing_price.csv', index_col=0)
    scaler = MinMaxScaler(feature_range=(0,1))

    scaled_price=scaler.fit_transform(data)
    x,y=[],[]
    time_steps=60
    
    for i in range(len(scaled_price)-time_steps):
        x.append(scaled_price[i:i+time_steps,0])
        y.append(scaled_price[i+time_steps,0])

    x=x.shape(x.shape[0],x.shape[1],1)
    train_size=int(len(x)*0.9)
    x_train,x_test=x[:train_size],x[train_size:]
    y_train,y_test=y[:train_size],y[train_size:]
    model=Sequential()
    model.add(Input(shape=(time_steps,1)))
    model.add(LSTM(50,return_sequences=False))
    model.add(Dense(1))
    model.compile(optimizer='adam',loss='mean_squared_error')
    assets = ['TSLA', 'BND', 'SPY']
    for col in assets:
        history=model.fit(x_train[col],y_train[col],epochs=100,batch_size=32,validation_data=(x_test[col],y_test[col]))
        y_pred=history.predict(x_test[col])
        y_pred_rescaled=scaler.inverse_transform(y_pred)
        y_test_rescaled=scaler.inverse_transform(y_test)

    #plot
        # Fit the ARIMA model for each stock
        
        # Plot the data for the current stock with its specific colors
        plt.plot(x_train.index, y_train, label=f'{col} Train', color=stock_colors[col]['train'])
        plt.plot(x_test.index, y_test_rescaled, label=f'{col} Test', color=stock_colors[col]['test'])
        plt.plot(x_test.index, y_pred_rescaled, label=f'{col} Forecast', color=stock_colors[col]['forecast'], linestyle='--')
    
    plt.title("Forecast for the Three Stocks using ARIMA")
    plt.xlabel("Date")
    plt.ylabel("Close Price")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def Arima():
    try:
        data = pd.read_csv('data/scaled_closing_price.csv', index_col=0)
        train_size=int(len(data)*0.9)
        train,test=data.iloc[:train_size],data.iloc[train_size:]
        
        return train,test
    except Exception as e:
        print(f'load First the Notebook/transferable.ipynb the file is excuted there {e}')
    assets = ['TSLA', 'BND', 'SPY']
    
    # Create a single plot figure
    plt.figure(figsize=(14, 7))
    
    # Define a color palette for the stocks to ensure each has a distinct set of colors
    
    
    for col in assets:
        # Fit the ARIMA model for each stock
        model = ARIMA(train[(col)], order=(1, 1, 1))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=len(test))
        
        # Plot the data for the current stock with its specific colors
        plt.plot(train.index, train[( col)], label=f'{col} Train', color=stock_colors[col]['train'])
        plt.plot(test.index, test[( col)], label=f'{col} Test', color=stock_colors[col]['test'])
        plt.plot(test.index, forecast, label=f'{col} Forecast', color=stock_colors[col]['forecast'], linestyle='--')
    
    plt.title("Forecast for the Three Stocks using ARIMA")
    plt.xlabel("Date")
    plt.ylabel("Close Price")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
   LSTM()
