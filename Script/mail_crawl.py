import re
import requests
from bs4 import BeautifulSoup

response = requests.get('https://preview.owasp-juice.shop/')

soup = BeautifulSoup(response.text, 'html.parser')
email_regex = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
emails = re.findall(email_regex, str(soup))

print(emails)
