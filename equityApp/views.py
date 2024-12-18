from django.shortcuts import render

# Create your views here.
# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Stock, Message
from .forms import MessageForm
from .forms import *

@login_required
def stock_list(request):
    stocks = Stock.objects.all()
    return render(request, 'stock_list.html', {'stocks': stocks})

from django.http import HttpResponse
from django.template.loader import render_to_string

@login_required
def get_messages(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)
    messages = stock.messages.all()
    html = render_to_string('messages_list.html', {'messages': messages})
    return HttpResponse(html)

@login_required
def stock_chat(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.stock = stock
            message.save()
            return redirect('stock_chat', stock_id=stock_id)
    else:
        form = MessageForm()
   
    return render(request, 'stock_chat.html', {'stock': stock, 'form': form})


# @login_required
# def stock_chat(request, stock_id):
#     stock = get_object_or_404(Stock, id=stock_id)
#     messages = stock.messages.all()
    
#     if request.method == 'POST':
#         form = MessageForm(request.POST)
#         if form.is_valid():
#             message = form.save(commit=False)
#             message.user = request.user
#             message.stock = stock
#             message.save()
#             return redirect('stock_chat', stock_id=stock_id)
#     else:
#         form = MessageForm()
    
#     return render(request, 'stock_chat.html', {'stock': stock, 'messages': messages, 'form': form})

def home(request):
    return render(request, 'home.html')
# from django.shortcuts import render


# from django.shortcuts import render
# from alpha_vantage.timeseries import TimeSeries
# import pandas as pd

# def visualise(request):
#     API_key = 'VTLCNKPV2GALGYKM'

#     # Initialize the TimeSeries object with the API key and pandas output format
#     ts = TimeSeries(key=API_key, output_format='pandas')

#     # Fetch the daily time series data for the 'MSFT' ticker
#     data, meta_data = ts.get_daily(symbol='MSFT', outputsize='full')

#     # Assuming today's date is July 20, 2024
#     end_date = pd.Timestamp.today()
#     start_date = end_date - pd.DateOffset(years=3)

#     # Filter the data to include only the last 5 years
#     filtered_data = data[(data.index >= start_date) & (data.index <= end_date)]

#     # Sort the data by date in ascending order
#     filtered_data.sort_index(inplace=True)

#     # Create lists for timestamps and closing prices
#     timestamps = filtered_data.index.strftime('%Y-%m-%d').tolist()
#     close_prices = filtered_data['4. close'].tolist()

#     return render(request, 'visualization.html', {'timestamps': timestamps, 'close_prices': close_prices})

from django.shortcuts import render
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import json
from .forms import KeywordForm

def visualise(request):
    context = {}
    if request.method == 'POST':
        form = KeywordForm(request.POST)
        if form.is_valid():
            keyword = form.cleaned_data['keyword']
            API_key = 'NOLCUHCZ5DDN5H58'

            # Initialize the TimeSeries object with the API key and pandas output format
            ts = TimeSeries(key=API_key, output_format='pandas')

            # Fetch the daily time series data for the 'MSFT' ticker
            data, meta_data = ts.get_daily(symbol=keyword, outputsize='full')

            # Assuming today's date is July 20, 2024
            end_date = pd.Timestamp.today()
            start_date = end_date - pd.DateOffset(years=7)

            # Filter the data to include only the last 5 years
            filtered_data = data[(data.index >= start_date) & (data.index <= end_date)]

            # Sort the data by date in ascending order
            filtered_data.sort_index(inplace=True)

            # Create lists for timestamps and closing prices
            timestamps = filtered_data.index.strftime('%Y-%m-%d').tolist()
            close_prices = filtered_data['4. close'].tolist()

            form = KeywordForm()
            context = {
                'timestamps': json.dumps(timestamps),
                'close_prices': json.dumps(close_prices),
                'form': form,
            }
        else:
            context['form'] = form
    else:
        form = KeywordForm()
        context['form'] = form

    return render(request, 'visualization.html', context)



import requests
from datetime import datetime, timedelta
from django.shortcuts import render
from django.http import HttpResponse
from .forms import KeywordForm

def news(request):
    if request.method == 'POST':
        form = KeywordForm(request.POST)
        if form.is_valid():
            company_name = form.cleaned_data['keyword']
        
            api_key = "e53ad7309613452c8320216716552a66"  # Replace with your actual API key

            base_url = "https://newsapi.org/v2/everything"

            # Calculate the date for one month ago
            one_month_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

            params = {
                'q': company_name,
                'from': one_month_ago,
                'sortBy': 'publishedAt',
                'apiKey': api_key,
                'language': 'en'
            }

            response = requests.get(base_url, params=params)

            if response.status_code == 200:
                news_data = response.json()
                articles = news_data.get('articles', [])
                
                form = KeywordForm()
                context = {
                    'company_name': company_name,
                    'articles': articles,
                    'form': form
                }
                
                return render(request, 'news.html', context)
            else:
                return HttpResponse(f"Error: Unable to fetch news. Status code: {response.status_code}")
    else:
        form = KeywordForm()

    return render(request, 'news.html', {'form': form})






from alpha_vantage.timeseries import TimeSeries
import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv
from django.shortcuts import render
from .forms import AlertForm
from .models import Alert

load_dotenv()

def get_alerts(request):
    if request.method == 'POST':
        form = AlertForm(request.POST)
        if form.is_valid():
            form.save()
            stock = form.cleaned_data['keyword']
            target_price = form.cleaned_data['price']
            email = form.cleaned_data['email']
            
            API_key = 'NOLCUHCZ5DDN5H58'
            last = Alert.objects.last()
            email = last.email

            try:
                # Initialize the TimeSeries object
                ts = TimeSeries(key=API_key, output_format='pandas')

                # Fetch intraday data for the stock with a 15-minute interval
                data, meta_data = ts.get_intraday(symbol=stock, interval='15min')

                # Get the most recent (current) price
                current_price = data['4. close'].iloc[0]

                if current_price > last.price:
                    c = str(current_price)
                    message = f"Your stock {stock} has reached a current price of {c}"
                    
                    # Create a new EmailMessage object
                    msg = EmailMessage()
                    msg['subject'] = 'Stock Alert'
                    msg['From'] = os.getenv('email')
                    msg['To'] = email
                    msg.set_content(message)

                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                        smtp.login(os.getenv('email'), os.getenv('password'))
                        smtp.send_message(msg)
                    
                    m = f"An alert email has been sent to {email} since {stock} reached the price of {c}."
                else:
                    p = str(target_price)
                    m = f"You will receive an email at {email} when {stock} reaches the price of {p}."
                
            except Exception as e:
                m = f"An error occurred: {e}"
            form = AlertForm()
            return render(request, 'alert.html', {'message': m, 'form': form})
    else:
        form = AlertForm()

    return render(request, 'alert.html', {'form': form})








# from alpha_vantage.timeseries import TimeSeries

# import smtplib
# import os
# from email.message import EmailMessage
# from dotenv import load_dotenv
# load_dotenv()


# msg = EmailMessage()
# msg['subject'] = 'Stock Alert'


# msg['From'] = os.getenv('email')

# #msg['To'] = 'cnithin650@gmail.com'

# def get_alerts(request):
#     if request.method == 'POST':
#         form = AlertForm(request.POST)
#         if form.is_valid():
#             form.save()
#             stock = form.cleaned_data['keyword']
#             price = form.cleaned_data['price']
#             email = form.cleaned_data['email']
#             # Your API key
            
#             API_key = 'Z3L9M5XB88ZBJSMO'
#             last = Alert.objects.last()
#             email =last.email
#             msg['To'] = email
#             # Initialize the TimeSeries object
#             ts = TimeSeries(key=API_key, output_format='pandas')

#             # Fetch intraday data for MSFT with a 15-minute interval
#             data, meta_data = ts.get_intraday(symbol=stock, interval='15min')

#             # Get the most recent (current) price
#             # The DataFrame index is in descending order, so the first row is the most recent
#             current_price = data['4. close'].iloc[0]
            
#             if current_price > last.price:
#                 c= str(current_price)
#                 message = f"Your stock has reached a current price of {c}"
#                 msg.set_content(message)
#                 with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
#                     smtp.login(os.getenv('email'),os.getenv('password'))
#                     smtp.send_message(msg)

#             p= str(price)
#             m =f"You will receive email at {email}, when stock reaches the price of {p}"
#             form = AlertForm()
#             return render(request,'alert.html',{'message':m,'form':form})
#     else:
#         form = AlertForm()
        
#     return render(request,'alert.html',{'form':form})
        
                


import pandas as pd
import numpy as np
from alpha_vantage.timeseries import TimeSeries
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

# Replace 'YOUR_API_KEY' with your actual Alpha Vantage API key
api_key = 'NOLCUHCZ5DDN5H58'



def linear(request):
    if request.method == 'POST':
        form = KeywordForm(request.POST)
        if form.is_valid():
            company_name = form.cleaned_data['keyword']
            # Fetch historical data
            symbol =company_name
            ts = TimeSeries(key=api_key, output_format='pandas')
            data, _ = ts.get_daily(symbol=symbol, outputsize='full')
            
            # Prepare the data
            data = data.sort_index(ascending=True)
            data['date'] = data.index
            data['date'] = pd.to_datetime(data['date'])
            data['days'] = (data['date'] - data['date'].min()).dt.days
            
            # Create features and target
            X = data[['days']]
            y = data['4. close']
            
            # Split the data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Train the model
            model = LinearRegression()
            model.fit(X_train, y_train)
            
            # Predict the price after 1 year
            last_date = data['date'].max()
            future_date = last_date + timedelta(days=365)
            days_in_future = (future_date - data['date'].min()).days
            
            future_price = model.predict([[days_in_future]])[0]
            
            # current_date = current_date.date()
            oneyear = future_date.date()
            #return future_price, last_date, future_date

            return render(request, 'linear.html', locals())
        # Make the prediction
        #predicted_price, current_date, future_date = future_price, last_date, future_date
    else:
        form = KeywordForm()
    return render(request, 'linear.html', locals())
    


            
            
from django.shortcuts import render
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import pandas as pd
import json
from .forms import KeywordForm

def market(request):
    context = {}
    if request.method == 'POST':
        form = KeywordForm(request.POST)
        if form.is_valid():
            keyword = form.cleaned_data['keyword']
            API_key = 'NOLCUHCZ5DDN5H58'

            # Initialize the TimeSeries and TechIndicators objects
            ts = TimeSeries(key=API_key, output_format='pandas')
            ti = TechIndicators(key=API_key, output_format='pandas')

            # Fetch the daily time series data
            data, meta_data = ts.get_daily(symbol=keyword, outputsize='full')

            # Calculate date range for the last 3 years
            end_date = pd.Timestamp.today()
            start_date = end_date - pd.DateOffset(years=3)

            # Filter the data to include only the last 3 years
            filtered_data = data[(data.index >= start_date) & (data.index <= end_date)]

            # Sort the data by date in ascending order
            filtered_data.sort_index(inplace=True)

            # Calculate moving averages
            try:
                ma50, _ = ti.get_sma(symbol=keyword, interval='daily', time_period=50, series_type='close')
                ma200, _ = ti.get_sma(symbol=keyword, interval='daily', time_period=200, series_type='close')
            except Exception as e:
                context['error'] = f"Error fetching moving averages: {e}"
                context['form'] = form
                return render(request, 'market.html', context)

            # Get the latest closing price
            latest_close = filtered_data['4. close'].iloc[-1]
            latest_ma50 = ma50['SMA'].iloc[-1] if not ma50.empty else None
            latest_ma200 = ma200['SMA'].iloc[-1] if not ma200.empty else None

            # Determine if bullish or bearish
            if latest_ma50 and latest_ma200:
                if latest_close > latest_ma50 and latest_ma50 > latest_ma200:
                    trend = 'bullish'
                elif latest_close < latest_ma50 and latest_ma50 < latest_ma200:
                    trend = 'bearish'
                else:
                    trend = 'neutral'
            else:
                trend = 'unable to determine'

            # Create lists for timestamps and closing prices
            timestamps = filtered_data.index.strftime('%Y-%m-%d').tolist()
            close_prices = filtered_data['4. close'].tolist()

            form = KeywordForm()
            context = {
                'timestamps': json.dumps(timestamps),
                'close_prices': json.dumps(close_prices),
                'form': form,
                'trend': trend
            }
        else:
            context['form'] = form
    else:
        form = KeywordForm()
        context['form'] = form

    return render(request, 'market.html', context)






import requests
from datetime import datetime
from django.shortcuts import render

# Function to convert 24-hour time to 12-hour time
def convert_to_12_hour(time_str):
    return datetime.strptime(time_str, "%H:%M").strftime("%I:%M %p")

def market_status(request):
    context = {}
    
    api_key = 'NOLCUHCZ5DDN5H58'
    url = f'https://www.alphavantage.co/query?function=MARKET_STATUS&apikey={api_key}'
            
    response = requests.get(url)
    data = response.json()

    market_status_data = data.get('markets', [])
    for market in market_status_data:
        market['local_open'] = convert_to_12_hour(market['local_open'])
        market['local_close'] = convert_to_12_hour(market['local_close'])

    context = {
        'market_status_data': market_status_data,
    }

    return render(request, 'market_status.html', context)



def analytics(request):
    return render(request, 'analytics.html')