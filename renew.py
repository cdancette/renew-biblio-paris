import os
import requests
import json
from dotenv import load_dotenv

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

# Check if login was successful
if login_response.status_code == 200:
    print("Login successful")
else:
    print("Login failed")
    exit()



# 2. Get list of books
books_url = 'https://bibliotheques.paris.fr/default/Portal/Services/UserAccountService.svc/ListLoans?serviceCode=SYRACUSE&userUniqueIdentifier='
books_response = session.get(books_url)
books_list = books_response.json()

# Filter books to renew
print("List of all books", [loan['Title'] for loan in books_list['d']['Loans']])
loans_to_renew = [loan for loan in books_list['d']['Loans'] if loan['State'] == "A rendre bientôt"]

# 3. Renew books
renew_url = 'https://bibliotheques.paris.fr/default/Portal/Services/UserAccountService.svc/RenewLoans'
renew_headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Content-Type': 'application/json',
    'Referer': 'https://bibliotheques.paris.fr/account.aspx',
    'X-Requested-With': 'XMLHttpRequest',
}
renew_data = json.dumps({"loans": loans_to_renew, "userUniqueIdentifier": ""})


if len(loans_to_renew) == 0:
    print("No books to renew")
    exit()
print("Books to renew", [loan['Title'] for loan in loans_to_renew])

renew_response = session.post(renew_url, headers=renew_headers, data=renew_data)

# Check and print the renewal response
renew_result = renew_response.json()
# print(json.dumps(renew_result, indent=4))
print("Success, number of books renewed", len(renew_result['d']['Successes']))
