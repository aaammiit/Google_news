# nltk.download('punkt')
# keywords = "sport,ai,india,russia,china"
# Record = []

# @tenacity.retry(wait=tenacity.wait_exponential(min=4, max=10), stop=tenacity.stop_after_attempt(3))
# def fetch_feed(url):
#     feed = feedparser.parse(url)
#     return feed

# def Index(request):
    
#     try:
#         # feed = fetch_feed('https://news.google.com/rss')
#         feed = fetch_feed(f"https://news.google.com/rss/search?q=india")

#         # feed=fetch_feed('https://news.google.com/rss/search?q=business&hl=en-US&gl=US&ceid=US:en&when=1h')
#     except tenacity.RetryError as e:
#         print(f"Failed to fetch feed after {e.last_attempt.attempt_number} attempts: {e.last_attempt.exception}")
#         return render(request, 'error.html', {'error': 'Failed to fetch feed'})

#     entries = feed.entries
#     today = datetime.today() 
#     new_records = []  # List to store new news items
#     for entry in entries[:30]:  # Show only the latest 30 headlines
#         title = entry.title.lower()  # Convert title to lowercase for case-insensitive search
#         # if any(keyword.lower() in title for keyword in keywords):
#             # print(entry.published)  # Check if any keyword is in the title
#         record = {
#                     'title': entry.title,
#                     'link': entry.link,
#                     'date': parser.parse(entry.published), 
#                 }
#         if record not in Record:
#             if record['date'].date() == today.date(): 
#                 # print(record['date']) # Check if the news item is not already in the Record list and its date matches today's date
#                 new_records.append(record)
#       # Add the news item to the new_records list

#     if new_records:  # Check if there are new news items
#         body = ""  # Initialize an empty string to store the email body
#         for record in new_records:
#             body += f"Title: {record['title']}\nLink: {record['link']}\nDate: {record['date']}\n\n"  # Concatenate each news item to the body
#         msg = f"Subject: {subject}\n\n{body}"  # Create the email message
#         msg = msg.encode('utf-8')  # Encode the message as bytes
#         server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
#         server.starttls()
#         server.login(SMTP_USERNAME, SMTP_PASSWORD)
#         server.sendmail(sender_email, Receiver_email, msg)  # Send the email
#         server.quit()
#         print("News sent successfully")
#         Record.extend(new_records)  # Update the Record list with the new news items
#     else:
#         print('No new News Sent')   
#         data = {'data': Record[::-1]}  # Return the Record list directly
#         return render(request, 'index.html', data)

#     Record1 = Record[::-1]
#     data = {'data': Record1}
#     return render(request, 'index.html', data)

# def update_news(request=None):
#     global Record
#     Index(request)
# #     # You can also save the records to a database or file here

# schedule.every(30).minutes.do(update_news)  # Run update_news every 5 minutes
# def run_scheduler():
#     while True:
#         schedule.run_pending()
#         time.sleep(1)

# scheduler_thread = threading.Thread(target=run_scheduler)
# scheduler_thread.daemon = True  # Set as daemon thread so it exits when main thread exits
# scheduler_thread.start()

# if __name__ == '__main__':
#     run_scheduler()  # or whatever command you use to run your web server


# def Home(request):

#     return render(request,'index.html')

# import requests
# from bs4 import BeautifulSoup
# from datetime import datetime, timedelta

# def Home(request):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
#     }
#     new_records = []
#     url = "https://news.google.com/q?hl=en-US&gl=US&ceid=US:en&q=india"
#     response = requests.get(url, headers=headers)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     today = datetime.today() 
#     news_list = []
    
#     for article in soup.find_all('article'):
#         a_tags = article.find_all('a')
#         if len(a_tags) > 1:
#             title_tag = a_tags[1]
#             title = title_tag.text
#         else:
#             title = "Unknown title"
#         print(title) # If no title is found, use a default value

#         link = article.find('a')['href']
#         date_str = article.find('time')['datetime']
#         date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
#         record={
#                 'title': title,
#                 'link': link,
#                 'date': date.strftime('%Y-%m-%d %H:%M:%S')
#             }
#         if record not in Record:
#             if date > datetime.now() - timedelta(hours=12):
#                 new_records.append(record)
#     if new_records:  # Check if there are new news items
#         body = ""  # Initialize an empty string to store the email body
#         for records in new_records:
#             body += f"Title: {records['title']}\nLink: {records['link']}\nDate: {records['date']}\n\n"  # Concatenate each news item to the body
#         msg = f"Subject: {subject}\n\n{body}"  # Create the email message
#         msg = msg.encode('utf-8')  # Encode the message as bytes
#         server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
#         server.starttls()
#         server.login(SMTP_USERNAME, SMTP_PASSWORD)
#         server.sendmail(sender_email, Receiver_email, msg)  # Send the email
#         server.quit()
#         print("News sent successfully")
#         Record.extend(new_records)  # Update the Record list with the new news items
#     else:
#         print('No new News Sent')   
#         data = {'data': Record[::-1]}  # Return the Record list directly
#         return render(request, 'index.html', data)
#     Record1 = Record[::-1]
#     data={'data':Record1}
#     return render(request,'index.html',data)

# def update_news(request=None):
#     global Record
#     Home(request)

# schedule.every(30).minutes.do(update_news)  # Run update_news every 5 minutes
# def run_scheduler():
#     while True:
#         schedule.run_pending()
#         time.sleep(1)

# scheduler_thread = threading.Thread(target=run_scheduler)
# scheduler_thread.daemon = True  # Set as daemon thread so it exits when main thread exits
# scheduler_thread.start()

# if __name__ == '__main__':
#     run_scheduler()  # or whatever command you use to run your web server


# 
# url_list=[
#     'https://news.google.com/search?q=chief%20compliance%20officer%20appoint%20when%3A7d&hl=en-IN&gl=IN&ceid=IN%3Aen',
#     'https://news.google.com/search?q=general%20counsel%20appoint%20when%3A7d&hl=en-IN&gl=IN&ceid=IN%3Aen',
#     'https://news.google.com/search?q=chief%20risk%20officer%20appoint%20when%3A7d&hl=en-IN&gl=IN&ceid=IN%3Aen',
#     'https://news.google.com/search?q=chief%20legal%20officer%20appoint%20when%3A7d&hl=en-IN&gl=IN&ceid=IN%3Aen',
#     'https://news.google.com/search?q=chief%20sustainability%20officer%20appoint%20when%3A7d&hl=en-IN&gl=IN&ceid=IN%3Aen',
#     'https://news.google.com/search?q=integrity%20and%20compliance%20officer%20appoint%20when%3A7d&hl=en-IN&gl=IN&ceid=IN%3Aen',
#     'https://news.google.com/search?q=chief%20diversity%C2%A0officer%C2%A0appoint%20when%3A7d&hl=en-IN&gl=IN&ceid=IN%3Aen'
# ]