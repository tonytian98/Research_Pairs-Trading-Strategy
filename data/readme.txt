StockPool  contains 944 U.S. Stock data from 2013-12-1 to 2019-12-30 in dictionary form (dict[StockName]=StockData)

FinalPairs  contains 463 pairs information after pair selection, in the form of DataFrame

selectedpairs  contains the randomly drawed 20 pairs used in the study, in the form of DataFrame

selectedpairs_LSTM  contains selectedpairs.pkl plus the forecasted value from LSTM model, mse on the validation set, and best parameters for each pair

selectedpairs_ARIMA contains selectedpairs.pkl plus the forecasted value from ARIMA model, mse on the validation set, and best parameters for each pair

selectedpairs_para contains the (sn,sp,lp,ln) parameters for each pair

LSTM_result contains the results (rate of returns, etc.)after the strategy is implemented using LSTM forecasting

ARIMA_result contains the results (rate of returns, etc.)after the strategy is implemented using ARIMA forecasting