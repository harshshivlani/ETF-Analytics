#data manipulation
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#filter warnings for final presentation
import warnings
warnings.filterwarnings("ignore")
import edhec_risk_kit as erk
import yfinance as yf
import ipywidgets as widgets
from ipywidgets import interact, interact_manual
from datetime import date
import time
import datetime

#notebook formatting
from IPython.core.display import display, HTML

def drawdowns2020(data):
    return_series = pd.DataFrame(data.pct_change().dropna()['2020':])
    wealth_index = 1000*(1+return_series).cumprod()
    previous_peaks = wealth_index.cummax()
    drawdowns = (wealth_index - previous_peaks)/previous_peaks
    return drawdowns.min(axis=0)

def returns_heatmap(data, max_drawdowns, title, sortby='1-Day', reit='No', currencies='No', alok_secs='No', fg_data='No', style='Yes'):
    """
    
    """
    if reit=='Yes':
        df = pd.DataFrame(data = (data.pct_change(1).iloc[-1,:], data.pct_change(5).iloc[-1,:], data.pct_change(21).iloc[-1,:], data.pct_change(63).iloc[-1,:], data['2020':].iloc[-1,:]/data['2020':].iloc[0,:]-1, data['2020':].iloc[-1,:]/data['2020-03-23':].iloc[0,:]-1, data.pct_change(126).iloc[-1,:], data.pct_change(252).iloc[-1,:], max_drawdowns))
        df.index = ['1-Day', '1-Week', '1-Month', '3-Month', 'YTD', 'March-23 TD', '6-Month', '1-Year', 'Drawdowns']
        
    elif currencies=='Yes':
        df = pd.DataFrame(data = (data.pct_change(1).iloc[-1,:],  data.pct_change(5).iloc[-1,:], data.pct_change(21).iloc[-1,:], data.pct_change(42).iloc[-1,:], data.pct_change(63).iloc[-1,:], data['2020':].iloc[-1,:]/data['2020':].iloc[0,:]-1, data['2020':].iloc[-1,:]/data['2020-03-23':].iloc[0,:]-1, data.pct_change(126).iloc[-1,:], data.pct_change(252).iloc[-1,:], max_drawdowns))
        df.index = ['1-Day', '1-Week', '1-Month', '2-Month', '3-Month', 'YTD', 'March-23 TD', '6-Month', '1-Year', 'Drawdowns']
        
    elif alok_secs=='Yes':
        data = data.ffill()
        df = pd.DataFrame(data = (data.pct_change(1).iloc[-1,:],  data.pct_change(5).iloc[-1,:], data.pct_change(21).iloc[-1,:], data.pct_change(42).iloc[-1,:], data.pct_change(63).iloc[-1,:], data['2020':].iloc[-1,:]/data['2020-01-06':].iloc[0,:]-1, data['2020':].iloc[-1,:]/data['2020-03-23':].iloc[0,:]-1, max_drawdowns))
        df.index = ['1-Day', '1-Week', '1-Month', '2-Month', '3-Month', 'YTD', 'March-23 TD', 'Drawdowns']
    
    elif fg_data=='Yes':
        now = time.localtime()
        last = datetime.date(now.tm_year, now.tm_mon, 1) - datetime.timedelta(1)
        df = pd.DataFrame(data = (data.pct_change(1).iloc[-1,:],  data.pct_change(7).iloc[-1,:], data.pct_change(30).iloc[-1,:], data.iloc[-1,:]/data[last:].iloc[0,:]-1, data.pct_change(90).iloc[-1,:]))
        df.index = ['1-Day', '1-Week', '1-Month', 'MTD', '3-Month']
        
     
    else:
        df = pd.DataFrame(data = (data.pct_change(1).iloc[-1,:], data.pct_change(5).iloc[-1,:], data.pct_change(21).iloc[-1,:], data.pct_change(63).iloc[-1,:], data['2020':].iloc[-1,:]/data['2020':].iloc[0,:]-1, data['2020':].iloc[-1,:]/data['2020-03-23':].iloc[0,:]-1, data.pct_change(126).iloc[-1,:], data.pct_change(252).iloc[-1,:], data.pct_change(252*3).iloc[-1,:], max_drawdowns))
        df.index = ['1-Day', '1-Week', '1-Month', '3-Month', 'YTD', 'March-23 TD', '6-Month', '1-Year', '3-Year', 'Drawdowns']
        
        
    df_perf = (df.T*100).sort_values(by=sortby, ascending=False)
    df_perf.index.name = title
    if style=='Yes':
        df_perf = df_perf.round(2).style.format('{0:,.2f}%')\
                 .background_gradient(cmap='RdYlGn')\
                 .set_properties(**{'font-size': '10pt',})
    else:
        df_perf = df_perf.round(2)
    return df_perf

def data_sov():
    #Soveriegn Fixed Income ETFs
    data_sov = yf.download('SHY IEF TLT IEI EMB EMLC AGZ BWX IGOV TIP', progress=False)['Adj Close']
    data_sov.dropna(inplace=True)
    data_sov.columns = ['iShares Agency Bond ETF', 'SPDR International Treasury Bond ETF', 'USD Emerging Markets Bond ETF', 'EM Local Currency Bond ETF', '7-10 Year Treasury Bond ETF','3-7 Year Treasury Bond ETF', 'iShares International Treasury Bond ETF','1-3 Year Treasury Bond ETF', 'US TIPS Bond ETF','20+ Year Treasury Bond ETF']
    return data_sov

def data_corp():
    #Corporate Fixed Income ETFs -  IG & HY in Developed & EM
    data_corp = yf.download('AGG BND BNDX LQD HYG SHYG JNK FALN ANGL FPE HYXE HYXU HYEM EMHY', progress=False)['Adj Close']
    data_corp.dropna(inplace=True)
    data_corp.columns = ['Core US Aggregate Bond', 'ANGL Fallen Angel HY Bond', 'US Total Bond Market', 'Total International Bond', 
                'iShares EM High Yield','FALN Fallen Angels USD Bond', 'Preferred Securities', 'VanEck EM High Yield',
                'HYG US High Yield', 'US High Yield ex-Energy', 'Int High Yield', 'JNK US High Yield', 
                'US Investment Grade', '0-5Y US High Yield']
    return data_corp

def data_reit(ticker='No'):
    #Real Estate Investment Trust (REIT) ETFs
    data_reit = yf.download('VNQ VNQI SRVR INDS HOMZ REZ PPTY IFEU REM MORT SRET RFI FFR GQRE CHIR FFR WPS IFGL KBWY BBRE ROOF NETL SPG SRG SKT STOR', progress=False)['Adj Close']['2019':]
    data_reit.dropna(inplace=True)
    if ticker == 'Yes':
        data_reit.columns = data_reit.columns
    else:
        data_reit.columns = ['BetaBuilders', 'China RE', 'DM RE', 'Quality RE', 'ResidentialHOMZ', 'Europe RE', 'IGFL', 'Industrial RE',
                     'YieldEQ RE', 'MORT','NetLease RE', 'Divserified RE', 'MortgageREM', 'ResidentialREZ', 'Cohen RE',
                     'Small-Cap RE', 'TangerRetail', 'SimonRetail', 'SuperDividend', 'SeritageRetail', 'DataInfra RE',
                     'StoreRetail', 'VanguardUS', 'VanguardInt', 'DevelopedRE']
        
    return data_reit

def data_cur():
    #Currencies
    data_cur = yf.download('KRWUSD=X BRLUSD=X IDRUSD=X MXNUSD=X RUBUSD=X CADUSD=X JPYUSD=X EURUSD=X INRUSD=X TRYUSD=X NZDUSD=X GBPUSD=X DX-Y.NYB AUDUSD=X AUDJPY=X EURCHF=X TWDUSD=X THBUSD=X COPUSD=X CNYUSD=X CLPUSD=X ZARUSD=X HKDUSD=X CHFUSD=X SGDUSD=X',progress=False)['Adj Close']['2019':]
    data_cur.dropna(inplace=True)
    data_cur.columns = ['AUD/JPY', 'Australian Dollar', 'Brazilian Real', 'Canadian Dollar', 'Swiss Francs', 'Chilean Peso', 'Chinese Yuan',
                    'Colombian Peso', 'Dollar Index', 'EUR/CHF', 'Euro', 'British Pound', 'Hong Kong Dollar', 'Indonesian Rupiah',
                    'Indian Rupee', 'Japanese Yen', 'Korean Won', 'Mexican Peso', 'New Zealand Dollar', 'Russian Ruble',
                    'Singapore Dollar', 'Thai Baht', 'Turkish Lira', 'Taiwanese Dollar', 'South African Rand']
    return data_cur


def data_comd():
    #Soveriegn Fixed Income ETFs
    data_comd = yf.download('COMT GSG DBC USO CL=F HG=F COPX GC=F GLD GDX PA=F PALL PPLT SI=F SIL ICLN TAN W=F ZC=F NG=F', progress=False)['Adj Close']
    data_comd.dropna(inplace=True)
    data_comd.columns = ['Crude Oil WTI','COMT', 'Copper Miners', 'DB CMTY Fund', 'Gold Futures', 'Gold Miners',
                     'Gold ETF', 'GSCI ETF', 'Copper Futures', 'Clean Energy', 'NatGas Futures',
                     'Palladium Futures', 'Physical Palladium ETF', 'Physical Platinum ETF', 'Silver Futures', 'Silver ETF', 
                     'Solar ETF', 'USO Oil ETF', 'Wheat Futures', 'Corn Futures']
    return data_comd


def heatmap_fixed_income(days=1, Ticker='No', figsize=(12,6)):
    data_sov1 = yf.download('SHY IEF TLT IEI EMB EMLC AGZ BWX IGOV TIP', progress=False)['Adj Close']
    data_sov1.dropna(inplace=True)
    data_corp1 = yf.download('AGG BND BNDX LQD HYG SHYG JNK FALN ANGL FPE HYXE HYXU HYEM EMHY')['Adj Close']
    data_corp1.dropna(inplace=True)
    sov_rets = pd.DataFrame(data_sov1.pct_change(days).iloc[-1,:])
    corp_rets = pd.DataFrame(data_corp1.pct_change(days).iloc[-1,:])
    rets = (sov_rets.append(corp_rets))
    rets.columns = ['Return']
    if Ticker == 'Yes':
        rets.index = rets.index
    else:
        rets.index = ['Agency', 'Int-Govt', 'EM Govt', 'EM LCL', '7-10Y UST', '3-7Y UST', 'Int-Govt1', '1-3Y UST',
              'US TIPS', '20Y+ UST', 'Agg Bonds', 'ANGL', 'Total Bonds', 'Int-Bonds', 'EM HY', 'FALN', 'Preferred',
              'HY EM', 'HYG', 'HYXE', 'Int-HY', 'JNK', 'US IG', 'SHYG']
    rets = rets.sort_values('Return', ascending=False)
    symbols = (np.asarray(list(rets.index))).reshape(4,6)
    pct_rets = (np.asarray(rets['Return'].values)).reshape(4,6)
    rows = [1,1,1,1,1,1,2,2,2,2,2,2,3,3,3,3,3,3,4,4,4,4,4,4]
    cols = [1,2,3,4,5,6,1,2,3,4,5,6,1,2,3,4,5,6,1,2,3,4,5,6]
    rets['Rows'] = rows
    rets['Cols'] = cols
    result = rets.pivot(index = 'Rows', columns = 'Cols', values = 'Return')
    labels = (np.asarray(["{0} \n {1:.2%}".format(symb,value)
                     for symb, value in zip(symbols.flatten(), pct_rets.flatten())])).reshape(4,6)
    fig, ax = plt.subplots(figsize=(12,6))
    title = 'Fixed Income ETFs Heatmap'
    plt.title(title, fontsize=15)
    ttl = ax.title
    ttl.set_position([0.5,1.05])
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis('off')
    sns.heatmap(result, annot=labels, fmt="", cmap = 'RdYlGn', linewidth=0.30, ax=ax, square=True, annot_kws={"size": 12})
    plt.show()

def heatmap_reit(days=1, Ticker='No', figsize=(12,6)):
    reit = yf.download('VNQ VNQI SRVR INDS HOMZ REZ PPTY IFEU REM MORT SRET RFI FFR GQRE CHIR FFR WPS IFGL KBWY BBRE ROOF NETL SPG SRG SKT STOR', progress=False)['Adj Close']['2019':]
    reit.dropna(inplace=True)
    if Ticker == 'Yes':
        reit.columns = reit.columns
    else:
        reit.columns = ['BetaBuilders', 'China RE', 'DM RE', 'Quality RE', 'ResidentialHOMZ', 'Europe RE', 'IGFL', 'Industrial RE',
                     'YieldEQ RE', 'MORT','NetLease RE', 'Divserified RE', 'MortgageREM', 'ResidentialREZ', 'Cohen RE',
                     'Small-Cap RE', 'TangerRetail', 'SimonRetail', 'SuperDividend', 'SeritageRetail', 'DataInfra RE',
                     'StoreRetail', 'VanguardUS', 'VanguardInt', 'DevelopedRE']
    rets = pd.DataFrame(reit.pct_change(days).iloc[-1,:])
    rets.columns = ['Return']
    rets = rets.sort_values('Return', ascending=False)
    symbols = (np.asarray(list(rets.index))).reshape(5,5)
    pct_rets = (np.asarray(rets['Return'].values)).reshape(5,5)
    rows = [1,1,1,1,1,2,2,2,2,2,3,3,3,3,3,4,4,4,4,4,5,5,5,5,5]
    cols = [1,2,3,4,5,1,2,3,4,5,1,2,3,4,5,1,2,3,4,5,1,2,3,4,5]
    rets['Rows'] = rows
    rets['Cols'] = cols
    result = rets.pivot(index = 'Rows', columns = 'Cols', values = 'Return')
    labels = (np.asarray(["{0} \n {1:.2%}".format(symb,value)
                     for symb, value in zip(symbols.flatten(), pct_rets.flatten())])).reshape(5,5)
    fig, ax = plt.subplots(figsize=figsize)
    title = 'REIT ETFs Heatmap'
    plt.title(title, fontsize=15)
    ttl = ax.title
    ttl.set_position([0.5,1.05])
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis('off')
    sns.heatmap(result, annot=labels, fmt="", cmap = 'RdYlGn', linewidth=0.30, ax=ax, annot_kws={"size": 12})
    plt.show()
    

def heatmap_commodities(days=1, Ticker='No', figsize=(12,6)):
    comd = yf.download('COMT GSG DBC USO CL=F HG=F COPX GC=F GLD GDX PA=F PALL PPLT SI=F SIL ICLN TAN W=F ZC=F NG=F', progress=False)['Adj Close']
    comd.dropna(inplace=True)
    if Ticker == 'Yes':
        comd.columns = comd.columns
    else:
        comd.columns = ['Crude Oil WTI', 'COMT', 'Copper Miners', 'DB CMTY Fund', 'Gold Futures', 'Gold Miners',
                     'Gold ETF', 'GSCI ETF', 'Copper Futures', 'Clean Energy', 'NatGas Futures',
                     'Palladium Futures', 'Physical Palladium ETF', 'Physical Platinum ETF', 'Silver Futures', 'Silver ETF', 
                     'Solar ETF', 'USO Oil ETF', 'Wheat Futures', 'Corn Futures']
    rets = pd.DataFrame(comd.pct_change(days).iloc[-1,:])
    rets.columns = ['Return']
    rets = rets.sort_values('Return', ascending=False)
    symbols = (np.asarray(list(rets.index))).reshape(4,5)
    pct_rets = (np.asarray(rets['Return'].values)).reshape(4,5)
    rows = [1,1,1,1,1,2,2,2,2,2,3,3,3,3,3,4,4,4,4,4]
    cols = [1,2,3,4,5,1,2,3,4,5,1,2,3,4,5,1,2,3,4,5]
    rets['Rows'] = rows
    rets['Cols'] = cols
    result = rets.pivot(index = 'Rows', columns = 'Cols', values = 'Return')
    labels = (np.asarray(["{0} \n {1:.2%}".format(symb,value)
                     for symb, value in zip(symbols.flatten(), pct_rets.flatten())])).reshape(4,5)
    fig, ax = plt.subplots(figsize=figsize)
    title = 'Commodities ETF/Futures Heatmap'
    plt.title(title, fontsize=15)
    ttl = ax.title
    ttl.set_position([0.5,1.05])
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis('off')
    sns.heatmap(result, annot=labels, fmt="", cmap = 'RdYlGn', linewidth=0.30, ax=ax, annot_kws={"size": 12})
    plt.show()
    
def heatmap_fx(days=1, Ticker='No', figsize=(12,6)):
    cur = yf.download('KRWUSD=X  BRLUSD=X  IDRUSD=X  MXNUSD=X  RUBUSD=X  CADUSD=X  JPYUSD=X  EURUSD=X  INRUSD=X  TRYUSD=X  NZDUSD=X  GBPUSD=X  DX-Y.NYB  AUDUSD=X  AUDJPY=X  EURCHF=X', progress=False)['Adj Close']['2017':]
    cur.dropna(inplace=True)
    if Ticker == 'Yes':
        cur.columns = cur.columns
    else:
        cur.columns = ['Aussie Yen', 'Australian Dollar', 'Brazilian Real', 'Canadian Dollar', 'Dollar Index', 'EUR/CHF',
                    'Euro', 'British Pound', 'Indonesian Rupiah', 'Indian Rupee', 'Japanese Yen', 'South Korean Won',
                    'Mexican Peso', 'New Zealand Dollar', 'Russian Ruble', 'Turkish Lira']
    
    rets = pd.DataFrame(cur.pct_change(days).iloc[-1,:])
    rets.columns = ['Return']
    rets = rets.sort_values('Return', ascending=False)
    symbols = (np.asarray(list(rets.index))).reshape(4,4)
    pct_rets = (np.asarray(rets['Return'].values)).reshape(4,4)
    rows = [1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4]
    cols = [1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4]
    rets['Rows'] = rows
    rets['Cols'] = cols
    result = rets.pivot(index = 'Rows', columns = 'Cols', values = 'Return')
    labels = (np.asarray(["{0} \n {1:.2%}".format(symb,value)
                     for symb, value in zip(symbols.flatten(), pct_rets.flatten())])).reshape(4,4)
    fig, ax = plt.subplots(figsize=figsize)
    title = 'REIT ETFs Heatmap'
    plt.title(title, fontsize=15)
    ttl = ax.title
    ttl.set_position([0.5,1.05])
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis('off')
    sns.heatmap(result, annot=labels, fmt="", cmap = 'RdYlGn', linewidth=0.30, ax=ax, annot_kws={"size": 12})
    plt.show()
    
    
def heatmap(rets, title='Cross Asset ETFs Heatmap', figsize=(15,10), annot_size=12, n_rows=10, n_cols=8):
    rets.columns = ['Return']
    rets = rets.sort_values('Return', ascending=False)
    symbols = (np.asarray(list(rets.index))).reshape(n_rows,n_cols)
    pct_rets = (np.asarray(rets['Return'].values)).reshape(n_rows,n_cols)
    rows =[]
    for i in range(1,n_rows+1):
        rows += list(np.repeat(i,n_cols))

    cols = list(list(np.arange(1,n_cols+1))*n_rows)
    rets['Rows'] = rows
    rets['Cols'] = cols
    
    result = rets.pivot(index = 'Rows', columns = 'Cols', values = 'Return')
    labels = (np.asarray(["{0} \n {1:.2%}".format(symb,value)
                     for symb, value in zip(symbols.flatten(), pct_rets.flatten())])).reshape(n_rows,n_cols)
    fig, ax = plt.subplots(figsize=figsize)
    plt.title(title, fontsize=15)
    ttl = ax.title
    ttl.set_position([0.5,1.05])
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis('off')
    return sns.heatmap(result, annot=labels, fmt="", cmap = 'RdYlGn', linewidth=0.30, ax=ax, annot_kws={"size": annot_size})
    
    
def alok_heatmap():
    alok_data = yf.download("CADUSD=X EURUSD=X GBPUSD=X USDINR=X USDSGD=X ACWI URTH ^NDX ^NSEI ^GSPC BZ=F DBC GLD GC=F PALL USO O9P.SI ANGL EDV EMB EMHY EMLC FPE GOVT HYEM HYG JNK LQD SHYG TLT TMF VWOB ZROZ ABR A17U.SI AV.L J85.SI J91U.SI MERY.PA ME8U.SI RGL.L VNQ VNQI 8697.T AAPL ABT ADBE AHCO AIEQ AIIQ AMD AMZN B3SA3.SA BABA BB BBJP BOX CLX CMG CRWD CTXS DBX DOCU DPZ ERUS EWT EWZ FXI GILD GOOG HD JD LSE.L MA MFA MOEX.ME MSFT NDAQ NEM NFLX NLOK NTES NVDA PTON PYPL PZZA QQQ S68.SI SHOP SMG SNY SPY SQ TDOC TMO TWLO TWOU TWTR V WORK X.TO ZM PD MKC NKE LQDA.L UST.PA PSHZF VTWO IWM", start='2019-12-31',end=date.today())['Adj Close']
    
    alok_data = alok_data.rename(columns = {'^NSEI':'NIFTY50', 'BZ=F':'Crude', 'A17U.SI':'AREIT', 'AV.L':'AV', 'J85.SI':'CDREIT',
                                            'J91U.SI':'EREIT','S68.SI':'SGX', 'X.TO':'TMX Group', 'CADUSD=X':'CADUSD','ME8U.SI':'MINT',
                                            'EURUSD=X':'EURUSD', 'GBPUSD=X':'GBPUSD', 'USDINR=X':'USDINR', 'USDSGD=X':'USDSGD',
                                            '^NDX':'NASDAQ', 'URTH':'MSCI Wrld', '^GSPC':'S&P500', 'GC=F': 'GOLD', 'O9P.SI':'AHYG'})
    alok_data = alok_data.ffill().asfreq('B').dropna()
    alok_data1 = pd.DataFrame(data = (alok_data.iloc[-1,:],alok_data.pct_change().iloc[-1,:])).T
    alok_data1.columns = ['Price', 'Chg (%)']
    alok_data2 = alok_data1.style.format({'Chg (%)': "{:.2%}", 'Price': "{:.2f}"})
    alok_map = returns_heatmap(alok_data, drawdowns2020(alok_data), title='Securities', alok_secs='Yes', style='No')
    prices = pd.DataFrame(alok_data1['Price'])
    prices.index.name = 'Securities'
    final = prices.merge(alok_map, on='Securities').sort_values(by='1-Day', ascending=False).style.format('{0:,.2f}%', subset=list(alok_map.columns))\
                     .format('{0:,.2f}', subset=['Price'])\
                     .background_gradient(cmap='RdYlGn', subset=list(alok_map.columns))\
                     .set_properties(**{'font-size': '10pt',})
    return (final, alok_data1, alok_data)
    

def cross_asset_data():
    """
    """
    data_sov = yf.download('SHY IEF TLT IEI EMB EMLC AGZ BWX TIP', progress=False)['Adj Close']['2019':]
    data_sov.dropna(inplace=True)
    data_corp = yf.download('AGG BND BNDX LQD HYG SHYG JNK FALN ANGL FPE HYXE HYXU HYEM EMHY', progress=False)['Adj Close']['2019':]
    data_corp.dropna(inplace=True)
    data_reit = yf.download('VNQ VNQI SRVR INDS HOMZ REZ IFEU REM MORT SRET RFI FFR GQRE CHIR FFR WPS PPTY IFGL KBWY ROOF NETL SPG SKT STOR', progress=False)['Adj Close']['2019':]
    data_reit.dropna(inplace=True)
    data_cur = yf.download('KRWUSD=X  BRLUSD=X  IDRUSD=X  MXNUSD=X  RUBUSD=X  CADUSD=X  JPYUSD=X  EURUSD=X  INRUSD=X  TRYUSD=X  NZDUSD=X  GBPUSD=X  DX-Y.NYB  AUDUSD=X  AUDJPY=X  EURCHF=X', progress=False)['Adj Close']['2019':].iloc[:-1,:]
    data_cur.dropna(inplace=True)
    data_comd = yf.download('COMT USO CL=F HG=F COPX GC=F GLD GDX PA=F PALL PPLT SI=F SIL ICLN TAN W=F ZC=F NG=F', progress=False)['Adj Close']['2019':]
    data_comd.dropna(inplace=True)
    
    all_data = data_sov.merge(data_corp, on='Date').merge(data_reit, on='Date').merge(data_cur, on='Date').merge(data_comd, on='Date')
    return all_data
    
    
def cross_asset_heatmap(data, n_rows, n_cols, days=1, figsize=(15,10), annot_size=12, title='Cross Asset ETFs Heatmap'):
    """
    """
    rets = pd.DataFrame(data.pct_change(days).iloc[-1,:])
    return heatmap(rets, n_rows=n_rows, n_cols=n_cols, figsize=figsize, annot_size=annot_size, title=title)






