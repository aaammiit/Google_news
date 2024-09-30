from django.shortcuts import render,redirect
import feedparser
import nltk
# from nltk.tokenize import word_tokenize
import threading
import schedule
import time
import tenacity
import smtplib
from dateutil import parser
from bs4 import BeautifulSoup
from urllib3 import request
import requests
import pandas as pd
from datetime import datetime,timedelta
import openpyxl
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
import os
import json
from django.contrib import messages

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = 'amistreetecom0101@gmail.com'
SMTP_PASSWORD = 'xmxj ztoo dfvw bxtm'
sender_email = 'amistreetecom0101@gmail.com'
Receiver_email='amitdwivedi06503@gmail.com'

subject = "News Alert"

def is_within_last_5_days(date):
    today = datetime.today()
    five_days_ago = today - timedelta(days=2)
    return five_days_ago.date() <= date <= today.date()

def serialize_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")

dt = datetime.now()
json_data = json.dumps(dt, default=serialize_datetime)

Record=[]
def Home(request):
    data=request.session.get('data')
    data={'data':data}
    return render(request,'index.html',data)


@tenacity.retry(wait=tenacity.wait_exponential(min=4, max=10), stop=tenacity.stop_after_attempt(3))
def Get_news(request):
        url_list=[
    'https://news.google.com/search?q=general%20counsel%20appoint%20when%3A1d&hl=en-IN&gl=IN&ceid=IN%3Aen',
    'https://news.google.com/search?q=chief%20compliance%20officer%20appoint%20when%3A1d&hl=en-IN&gl=IN&ceid=IN%3Aen',
    'https://news.google.com/search?q=chief%20risk%20officer%20appoint%20when%3A1d&hl=en-IN&gl=IN&ceid=IN%3Aen',
    'https://news.google.com/search?q=chief%20legal%20officer%20appoint%20when%3A1d&hl=en-IN&gl=IN&ceid=IN%3Aen',
    'https://news.google.com/search?q=chief%20sustainability%20officer%20appoint%20when%3A1d&hl=en-IN&gl=IN&ceid=IN%3Aen',
    'https://news.google.com/search?q=integrity%20and%20compliance%20officer%20appoint%20when%3A1d&hl=en-IN&gl=IN&ceid=IN%3Aen',
    'https://news.google.com/search?q=chief%20diversity%C2%A0officer%C2%A0appoint%20when%3A1d&hl=en-IN&gl=IN&ceid=IN%3Aen'
    ]
        
    
        for url in range(len(url_list)):
            today = datetime.today() 
            response = requests.get(url_list[url])
            soup = BeautifulSoup(response.content, 'html.parser')
            new_records=[]
            for article in soup.find_all('article'):
                title_tag = article.find_all('a')[1]
                if title_tag:
                    title = title_tag.get_text(strip=True)
                    relative_url = title_tag.get('href')
                    if relative_url and relative_url.startswith('./'):
                        url = 'https://news.google.com' + relative_url[1:]
                        urls=url
                    else:
                        urls=relative_url    
                date_tag = article.find('time')
                if date_tag:
                    date = date_tag.get('datetime')
                    date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d')
                    date=datetime.strptime(date, '%Y-%m-%d').date()
                    date_str = date.isoformat()
                    time_ago=date_tag.text 
                    
                record={
                    'tilte':title,
                    'link':urls,
                    'date':date_str,
                    'ago':time_ago
                } 
                if is_within_last_5_days(date): 
                    if record not in Record:
                        new_records.append(record)
            print('Done',len(new_records))  
            Record.extend(new_records)
            print(type(Record))
        sorted_list = sorted(Record, key=lambda x: x['date'], reverse=True)
        Record1 = sorted_list
        print(len(Record1))
        request.session['data']=Record1
        data={'data':Record1}
        return render(request,'All_news.html',data)

def update_news(request=None):
    global Record
    Get_news(request)
    

schedule.every(15).minutes.do(update_news)  # Run update_news every 5 minutes
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.daemon = True  # Set as daemon thread so it exits when main thread exits
scheduler_thread.start()

if __name__ == '__main__':
    run_scheduler()  # or whatever command you use to run your web server


    

def Send_file(request):
    data = request.session.get('data')
    data = {'data': data}

    # Create an Excel file
    wb = openpyxl.Workbook()
    ws = wb.active

    # Set the header row
    ws['A1'] = 'Title'
    ws['B1'] = 'Link'
    ws['C1'] = 'Date'

    # Iterate over the records and add them to the Excel file
    for i, record in enumerate(data['data']):  
        ws[f'A{i+2}'] = record['tilte']
        ws[f'B{i+2}'] = record['link']
        ws[f'C{i+2}'] = record['date']

    # Save the Excel file
    date_str = datetime.now().strftime("%B%d")
    current_time_str = datetime.now().strftime("%H%M%S")
    filename = f'{date_str}News_records{current_time_str}.xlsx'
    wb.save(filename)

    # Create the email message
    subject = "News Alerts"
    body = "Here The Top And Latest News Tilte Url And Links"  # Initialize the body as an empty string

    for record in data['data']:
        body += f"Title: {record['tilte']}, Link: {record['link']}\n"
    # Create a multipart message
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = Receiver_email
    msg['Date'] = formatdate(localtime=True)

    # Add the body to the message
    try:
        msg.attach(MIMEText(body, 'plain'))

        # Attach the Excel file
        attachment = open(f'{filename}', 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= news_records.xlsx")
        msg.attach(part)

        # Send the email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(sender_email, Receiver_email, msg.as_string())
        server.quit()
        print('done')
        messages.success(request, "File Successfully Sent in Your Email")
        
           
    except:
        print('err')

    return redirect('/')

def Search_News(request):
    News=[]
    if request.method=='POST':
        url=request.POST.get('url')
        time_period=request.POST.get('time_period')
        url=url
        time_period=time_period
        if url != 'nome' and time_period !='none':
            base_url=f'https://news.google.com/search?q={url}20when{time_period}&hl=en-IN&gl=IN&ceid=IN%3Aen'
            # print(base_url)
            response = requests.get(base_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            new_records=[]
            for article in soup.find_all('article'):
                title_tag = article.find_all('a')[1]
                if title_tag:
                    title = title_tag.get_text(strip=True)
                    relative_url = title_tag.get('href')
                    if relative_url and relative_url.startswith('./'):
                        url = 'https://news.google.com' + relative_url[1:]
                        urls=url
                    else:
                        urls=relative_url    
                    date_tag = article.find('time')
                    
                    if date_tag:
                        date = date_tag.get('datetime')
                        date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d')
                        date=datetime.strptime(date, '%Y-%m-%d').date()
                        date_str = date.isoformat()
                        time_ago=date_tag.text       
                    record={
                            'tilte':title,
                            'link':urls,
                            'date':date_str,
                            'ago':time_ago
                        } 
                    if record not in Record:
                        new_records.append(record)
            News.extend(new_records)
        else:
            print('url and time period select None')
    sorted_list = sorted(News, key=lambda x: x['date'], reverse=True)
    News = sorted_list

    print(len(News))
    if len(News) !=0:
       data={'data':News}
       return render(request,'news.html',data)
    else:
        msg={'msg':'Sorry, not any news to fetch.'}
        return render(request,'news.html',msg)
        

def Clear_news(request):
    request.session.clear()
    return redirect('/')


        
        
            