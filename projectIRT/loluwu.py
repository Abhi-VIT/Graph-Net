import requests
import csv
import os
from bs4 import BeautifulSoup
import re
import spacy 
import pandas as pd
import numpy as np
from spacy.lang.en import English
import random
from summarizer import summarize_text
nlp = English()
nlp.max_length = 2000000
from spacy.lang.en.stop_words import STOP_WORDS

def get_search_results(query, api_key, num_results=20):
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

def save_to_csv(results, filename=r'C:\Users\abhis\Downloads\Information Retrieval Project\results.csv'):
    ''' converting the results intot the title and csv file with title and Link as a two columns'''
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Link'])  # Header
        writer.writerows(results)
    return print(f'Saved {len(results)} results to {filename}')

def save_clean_text(url, file_path):
    ''' to clean the text from the url and export it into the 
    txt file
    '''
    try:
        # Fetch content from URL
        response = requests.get(url)
        response.raise_for_status()

        # Parse and clean HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        for script_or_style in soup(['script', 'style']):
            script_or_style.decompose()
        clean_text = soup.get_text(separator=' ', strip=True)

        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Save text to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(clean_text)

        print(f"Text data saved to {file_path}")

    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
    except Exception as e:
        print(f"Error saving file: {e}")
def clean_text(text):
    text=re.sub('[,.\n?|<>:"/\\*+-123456789;]','',text)
    text=text.lower()
    return text

def get_ultimate_summary(query):
    
    api_key = '3d1dcaaaf45cb1d0a6d44ce7f0b037ea1e88b60b040b23cff802bcb933fabf1e' 
    results = get_search_results(query, api_key)

    #Getting the dataFrame
    data = pd.DataFrame(results)

    # for i in range(len(data[1])):
    #     text1 = data[1][i]
    #     text1 = clean_text(text1)
    #     data[1][i] = text1

    docs = []
    for j in range(len(data[0])):
        url = data[1][j]

        response: requests.Response = requests.get(url)
        # response = str(response)

        if response.status_code != 200:
            continue
        
        html_parsed = BeautifulSoup(response.text, features="html.parser")
        doc = html_parsed.body.text
        doc = nlp(doc)
        
        t = summarize_text(doc)
        return t

    # for i in range(len(data.Link)):
    #     num = random.randint(1,1000000)
    #     url = data.Link[i]
    #     file_path = rf'C:\Users\abhis\Downloads\Information Retrieval Project\documents\{data.Title[i]}\example{num}.txt'
    #     if not os.path.exists(file_path):
    #             # Create directories if they don't exist
    #             os.makedirs(os.path.dirname(file_path), exist_ok=True)
    #             # Create the file
    #             with open(file_path, 'w') as file:
    #                 file.write("")
    #     save_clean_text(url,file_path)
    #     response = requests.get(url)
    #     response = str(response)
    #     if response == '<Response [403]>' or response == '<Response [460]>' or response == '<Response [405]>':
    #         continue
    #     else:
    #         if not os.path.exists(file_path):
    #             # Create directories if they don't exist
    #             os.makedirs(os.path.dirname(file_path), exist_ok=True)
    #             # Create the file
    #             with open(file_path, 'w') as file:
    #                 file.write("")  # Creates an empty file

            
    #         file = open(file_path, encoding='utf-8')
    #         text = file.read()
    #         my_doc = nlp(text)
        
    #     # Create list of word tokens
    #         token_list = []
    #         for token in my_doc:
    #             token_list.append(token.text)
            
    #         # Create list of word tokens after removing stopwords
    #         filtered_sentence =[] 
            
    #         for word in token_list:
    #             lexeme = nlp.vocab[word]
    #             if lexeme.is_stop == False:
    #                 filtered_sentence.append(word) 
    #         # print(token_list)
    #         # print(' '.join(filtered_sentence))
    #         with open(rf'C:\Users\abhis\Downloads\Information Retrieval Project\documents\{data.Title[i]}\example{num}.txt', 'w', encoding='utf-8') as f:
    #                     f.write(' '.join(filtered_sentence))
