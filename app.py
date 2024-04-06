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

    return books_list['d']['Loans'], True

# Route to display books
@app.route('/')
def display_books():
    books, success = get_books()
    if not success:
        return render_template('error.html', message=books)  # Assume you have an error.html template for errors
    
    return render_template('books.html', books=books)  # Assume you have a books.html template to display the books

if __name__ == '__main__':
    app.run(debug=True)
