from flask import Flask, render_template
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Function to log in and retrieve book list
def get_books():
    load_dotenv()

    # Start a session
    session = requests.Session()

    # 1. Login
    login_url = 'https://bibliotheques.paris.fr/default/Portal/Recherche/logon.svc/logon'
    login_headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'https://bibliotheques.paris.fr/Default/',
        'X-Requested-With': 'XMLHttpRequest',
    }
    login_data = {
        'username': os.getenv('USERNAME'),
        'password': os.getenv('PASSWORD'),
        'rememberMe': 'false',
    }
    login_response = session.post(login_url, headers=login_headers, data=login_data)

    # Exit if login fails
    if login_response.status_code != 200:
        return "Login failed", False

    # 2. Get list of books
    books_url = 'https://bibliotheques.paris.fr/default/Portal/Services/UserAccountService.svc/ListLoans?serviceCode=SYRACUSE&userUniqueIdentifier='
    books_response = session.get(books_url)
    books_list = books_response.json()
    # parse dates
    for book in books_list['d']['Loans']:
        book['WhenBack'] = parse_dotnet_date(book['WhenBack'])


    return books_list['d']['Loans'], True


from datetime import datetime, timedelta, timezone
import re

def parse_dotnet_date(date_str):
    """
    Parses a .NET JSON date format "/Date(1714773600000+0200)/" to a Python datetime object.
    """
    match = re.search(r'/Date\((\d+)([+-]\d{4})\)/', date_str)
    if not match:
        raise ValueError("Invalid date format")

    # Extract milliseconds and timezone offset from the matched groups
    milliseconds, tz_offset_str = match.groups()
    milliseconds = int(milliseconds)

    # The timezone offset is in HHMM format. Convert it to a timedelta object
    tz_offset = int(tz_offset_str[:3]) * 60 + int(tz_offset_str[3:])  # Convert to total minutes
    tz_delta = timedelta(minutes=tz_offset)

    # Convert milliseconds to seconds and create a datetime object in UTC
    date = datetime.utcfromtimestamp(milliseconds / 1000)

    # Apply the timezone offset to get the correct datetime
    date = date.replace(tzinfo=timezone.utc) + tz_delta
    return date.astimezone(timezone.utc)  # Return as UTC datetime object

# Example usage
# date_str = "/Date(1714773600000+0200)/"
# parsed_date = parse_dotnet_date(date_str)
# print(parsed_date)



# Route to display books
@app.route('/')
def display_books():
    books, success = get_books()
    if not success:
        return render_template('error.html', message=books)
    
    return render_template('books.html', books=books)

if __name__ == '__main__':
    app.run(debug=True)
