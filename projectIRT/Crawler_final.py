import requests
# import csv
# import os
# from bs4 import BeautifulSoup
# import re
# import spacy 
# import pandas as pd
# import numpy as np
# from spacy.lang.en import English
# import random
# nlp = English()
# nlp.max_length = 2000000
# from spacy.lang.en.stop_words import STOP_WORDS

def get_search_results(query, num_results=20):
    api_key = '3d1dcaaaf45cb1d0a6d44ce7f0b037ea1e88b60b040b23cff802bcb933fabf1e' 
    # query = input("enter you query")
    # results = get_search_results(query, api_key)
# save to csv
    ''' getting the craw using the serp API and getting the Title and Link'''
    url = 'https://serpapi.com/search'
    params = {
        'q': query,
        'api_key': api_key,
        'engine': 'google',
        'num': num_results,
    }

    response = requests.get(url, params=params)
    data = response.json()

    results = []
    for result in data.get('organic_results', []):
        title = result.get('title')
        link = result.get('link')
        if title and link:
            results.append((title, link))
    
    return results

# Usage