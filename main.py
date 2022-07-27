import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import pandas_datareader as pdr
import streamlit as st
import plotly.express as px
################################



@st.cache
def fred_data_yoy(index_name):
  data = pdr.DataReader(index_name,'fred')
  data_yoy = data.pct_change(12).mul(100).round(2).dropna()
  fig , ax = plt.subplots(figsize= (20,10))
  plt.bar(x=data_yoy.index ,height = data_yoy[index_name], color ='maroon' ,width = 20)
  plt.xticks(rotation = 90,fontsize =20)
  plt.yticks(fontsize =20)
  return fig ,ax
NYSE_csv = 'nasdaq_screener.csv'
index_csv = 'World Index.csv'
NYSE = pd.read_csv(NYSE_csv)
major_index = pd.read_csv(index_csv)
nyse_symbol = NYSE['Symbol']
nyse_sector = NYSE['Sector'].unique()
major_index_symbol = major_index['Symbol']

fred_serie = pd.read_html('https://www.ivo-welch.info/professional/fredcsv.html')
fred_table = pd.DataFrame(fred_serie[0]).iloc[:,[0,3]]

st.image('TECH STOCK WARRIOR.png')
st.title('This application is made from Streamlit')
with st.sidebar:
   serie = st.selectbox('Select Macro Economic Indicator of your choice. (For first Macro tab)' , fred_table.iloc[:,1])   
   index= st.multiselect('Select Index to see Year To Date performance. (For Index tab)', major_index_symbol,default=['^IXIC'])
   stock = st.multiselect('Select Stock from the sector above. (For Stock tab)', NYSE['Symbol'],default=['MSFT' , 'GOOG','SNOW'])

stock_data = yf.download(stock , start= '2022-01-01')
correlation = stock_data['Close'].pct_change().dropna().corr()

index_data = yf.download(index , start='2022-01-01')['Close']
index_ytd =  index_data.div(index_data.iloc[0]).mul(100)

fred = fred_table[fred_table.iloc[:,1]==serie].iloc[:,0]
data = pdr.DataReader(fred,'fred',start = '2018-01-01')
yoy = data.pct_change(12).mul(100).round(2).dropna()

ind = ['^IXIC' , '^DJI' , '^GSPC']
met = yf.download(ind,start='2022-02-02')['Close'].round(2)
pct = round(met.pct_change()*100,2)
with open('style.css') as f:
  st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html= True)
  
st.header('Major index')
col1 ,col2 ,col3 = st.columns(3)
col1.metric(pct.columns[0],met.iloc[-1][0],pct.iloc[-1][0])
col2.metric(pct.columns[1],met.iloc[-1][1],pct.iloc[-1][1])
col3.metric(pct.columns[2],met.iloc[-1][2],pct.iloc[-1][2])



tab1, tab2, tab3 = st.tabs(["Macro", "Index", "Stock"])
with tab1:
  st.header('Macro Econonics Data')
  st.write('Year Over Year percentage change')
  fig = px.bar(yoy, y = fred, title = serie[1:] )
  st.plotly_chart(fig)

with tab2:
  st.header('Index Perfomance YTD')
  st.write('Please select index from sidebar tab')
  fig = px.line(index_ytd)
  st.plotly_chart(fig)

with tab3:
  st.header('This tab show how each stock correlated to each other')
  st.write('Please select stock from sidebar tab.')
  fig = px.imshow(correlation )
  st.plotly_chart(fig)


