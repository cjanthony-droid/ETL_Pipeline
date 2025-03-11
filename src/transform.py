import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import WhitespaceTokenizer
from nltk.tokenize import TreebankWordTokenizer
from nltk.tag import pos_tag

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

#tokenizer = WhitespaceTokenizer()
tokenizer = TreebankWordTokenizer()

def create_dataframe(data):
    if data and 'articles' in data:
        df = pd.json_normalize(data['articles'])
        df = df.drop(columns=['urlToImage', 'content'])
        df['title'] = df['title'].apply(lambda x: x.split('- ')[0].strip() if isinstance(x, str) else x)
        return df
    else:
        print("No data available to create DataFrame")
        return pd.DataFrame()

def filter_words(text):
    if text is None:
        return ""
    # Tokenize the text
    words = tokenizer.tokenize(text)
    # Tag the words with part of speech
    tagged_words = pos_tag(words)
    # Filter out non-nouns, non-adjectives, non-verbs, non-adverbs
    filtered_words = [word for word, pos in tagged_words if pos.startswith('N') or pos.startswith('J') or pos.startswith('V') or pos.startswith('R')]
    return ' '.join(filtered_words)

def transform_dataframe(df):
    df.columns = df.columns.str.strip()
    #data is a dataframe with source:json, author: string, title: string, description: string, url:string, publishedAt: ISO 8601 date and time format
    #we want to create a data frome that can be sent to database easily
    #to clean, drop stuff from source or split it, title and description have to be cleaned, date should just be date no time
    #source will just be a string, 
    print(','.join(df.columns.tolist()))    # Drop 'source' column or split it if needed
    if 'source.id' in df.columns and 'source.name' in df.columns:
        df['source.id'] = df['source.id'].fillna(df['source.name'])

    
    # Clean 'title' and 'description' columns
    if 'title' in df.columns:
        df['title'] = df['title'].apply(filter_words)
    if 'description' in df.columns:
        df['description'] = df['description'].apply(filter_words)
    
    # Convert 'publishedAt' to date only
    if 'publishedAt' in df.columns:
        df['publishedAt'] = pd.to_datetime(df['publishedAt']).dt.date
    
    
    return df