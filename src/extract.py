import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv('API_KEY')

def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def extract(category, country, page):
    url = (f'https://newsapi.org/v2/top-headlines?'
           f'country={country}&'
           f'category={category}&'
           f'sortBy=popularity&'
           f'pageSize=100&'
           f'page={page}&'
           f'apiKey={API_KEY}')
    data = fetch_data(url)
    return data