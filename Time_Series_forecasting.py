import pandas as pd 
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot  as plt
import warnings
warnings.filterwarnings('ignore')
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM,Input,Dense

stock_colors = {
        'TSLA': {'train': 'blue', 'test': 'darkblue', 'forecast': 'lightblue'},
        'BND': {'train': 'green', 'test': 'darkgreen', 'forecast': 'lightgreen'},
        'SPY': {'train': 'red', 'test': 'darkred', 'forecast': 'lightcoral'}
    }    
def LSTM():


    data = pd.read_csv('Time-Series-Forecasting-for-Portfolio-Management-Optimization/data/scaled_closing_price.csv', index_col=0)
    print("Successfully loaded scaled_closing_price.csv")

    assets = ['TSLA', 'BND', 'SPY']
    # Define stock_colors dictionary


    for col in assets:
        # Fit a new scaler for each stock
        scaler = MinMaxScaler(feature_range=(0,1))
        scaled_price = scaler.fit_transform(data[col].values.reshape(-1, 1))

        x,y=[],[]
        time_steps=60

        for i in range(len(scaled_price)-time_steps):
            x.append(scaled_price[i:i+time_steps,0])
            y.append(scaled_price[i+time_steps,0])

        x = np.array(x).reshape(np.array(x).shape[0],np.array(x).shape[1],1)
        train_size=int(len(x)*0.9)
        x_train,x_test=x[:train_size],x[train_size:]
        y_train,y_test=y[:train_size],y[train_size:]

        # Create and compile the model inside the loop for each stock
        model=Sequential()
        model.add(Input(shape=(time_steps,1)))
        model.add(LSTM(50,return_sequences=False))
        model.add(Dense(1))
        model.compile(optimizer='adam',loss='mean_squared_error')

        history=model.fit(x_train,np.array(y_train),epochs=20,batch_size=32,validation_data=(x_test,np.array(y_test).reshape(-1, 1)))
        y_pred=model.predict(x_test)

        # Inverse transform using the scaler fitted on the current stock's data
        y_pred_rescaled=scaler.inverse_transform(y_pred)

        # Reshape y_test for inverse_transform
        y_test_reshaped = np.array(y_test).reshape(-1, 1)
        y_test_rescaled=scaler.inverse_transform(y_test_reshaped)

        #plot
        plt.plot(np.arange(len(x_train)), scaler.inverse_transform(np.array(y_train).reshape(-1, 1)), label=f'{col} Train', color=stock_colors[col]['train'])
        plt.plot(np.arange(len(x_train), len(x_train) + len(x_test)), y_test_rescaled, label=f'{col} Test', color=stock_colors[col]['test'])
        plt.plot(np.arange(len(x_train), len(x_train) + len(x_test)), y_pred_rescaled, label=f'{col} Forecast', color=stock_colors[col]['forecast'], linestyle='--')


    plt.title("Forecast for the Three Stocks using LSTM")
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
