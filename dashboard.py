import streamlit as st, yfinance as yf
import plotly.express as px
import datetime

st.title('Interactive Stock Dashboard')
ticker = st.sidebar.text_input('Ticker Symbol')
start_date = st.sidebar.date_input('From')
end_date = st.sidebar.date_input('To')
st.sidebar.caption('Tools used: Python, Streamlit, Yahoo Finance api, News api')
home = st.sidebar.link_button("Main Page", "https://keadon-ch.github.io")

st.write("This is a simple interactive stock dashboard showing price movements of a desired US-Based ticker. Select your desired date range and press enter, then the data will populate. There are also two tabs to select from for additional information. The News tab displays the top 5 recent articles written about the company, and the price movement tab gives a more in-depth view of pricing data in table format. Enjoy!")

if not ticker:
    st.error('Please enter a ticker symbol e.g. AMZN')
    
elif start_date >= datetime.date.today():
    st.error('Please select a start date before the current date.')
elif end_date <= start_date:
    st.error('End date must be after the start date.')

else:

    ticker_obj = yf.Ticker(ticker)
    data = yf.download(ticker, start = start_date, end = end_date)
    current_price = data["Close"].iloc[-1]
    price_format = f"${current_price}"
    company_name = ticker_obj.info.get("shortName") #Extracting relevant data from yahoo finance such as current price, name, etc 

    st.header('Current Price:')
    st.subheader(price_format)
    fig = px.line(data, x = data.index, y = data['Adj Close'], title = company_name)
    st.plotly_chart(fig) # Displaying the current price and the price chart

    pricing_data, news = st.tabs(["Price Movement", "News"])

    with pricing_data:
        st.header("Price Movements")
        p_data = data
        p_data['% change'] = data['Adj Close'] / data['Adj Close'].shift(1) - 1
        p_data.dropna(inplace = True)
        st.write(p_data) # Extracting the price movements data from Yfinance to provide the user with more insight
        annual = p_data['% change'].mean()*252*100
        st.write('Annual return is %', annual) 

    from newsapi.newsapi_client import NewsApiClient 
    with news:
        st.header(f'{ticker} News')
        newsapi = NewsApiClient(api_key="3d26a96332d14db39ab5e87c219e639b")

        query = f"q={ticker}"
        response = newsapi.get_everything(ticker, language='en')      

        if response['status'] == "ok":
            articles = response['articles']
        for i in range(min(5, len(articles))):#Limit to 5 articles
            st.subheader(f'Article {i+1}')
            st.write(articles[i]['title'])
            st.write(articles[i]['description'])#Display description
            published_date = articles[i]['publishedAt']
            formatted_date = datetime.datetime.strptime(published_date, "%Y-%m-%dT%H:%M:%SZ").strftime("%d %b %Y, %H:%M")  
            st.write(f"Published: {formatted_date}")

st.caption('© 2024 Keadon Harrison. All rights reserved.')
