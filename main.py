import json
import pandas as pd
from src.extract import extract
from src.transform import create_dataframe
from src.load import load

def etl_process(category, country):
    page = 1
    total = 1
    all_data = []  # List to store DataFrames

    while True:
        data = extract(category, country, page)
        if not data or 'articles' not in data:
            print("No data or articles found")
            break
        #Trasform and clean data to be stored in a database
        df = create_dataframe(data)
        #Add it to the list dataframes (since it does this one page at a time)
        all_data.append(df)
        if page == 1:
            total = data['totalResults']
            #print(f'${total} start')
        total -= len(data['articles'])
        #print(f'${total} ${page} ${len(data["articles"])}')
        if total <= 0 or len(data['articles']) == 0:
            break
        page += 1
    
    # Concatenate all DataFrames into a single DataFrame
    final_df = pd.concat(all_data, ignore_index=True)
    #final stage would be load, but we are just returning it to be displayed for now
    return final_df


def json_extract(category, country):
    page = 1
    total = 1
    all_data = []
    while True:
        data = extract(category, country, page)
        if not data or 'articles' not in data:
            print("No data or articles found")
            break
        all_data.extend(data['articles'])
        if page == 1:
            total = data['totalResults']
        total -= len(data['articles'])
        if total <= 0 or len(data['articles']) == 0:
            break
        page += 1

    return all_data
def main():
    '''
    categories = ['business', 'entertainment', 'general', 'health', 
                    'science', 'sports', 'technology']
    countries = ['us', 'ca']
    No country besides us has top headlines currently
    '''
    categories = ['business', 'entertainment', 'general', 'health', 
                    'science', 'sports', 'technology']
    countries = ['us']
    parameters = [{'category': category, 'country': country} for category in categories for country in countries]


    for param in parameters:
        category = param['category']
        country = param['country']
        #final_df = etl_process(category, country)
        json_data = json_extract(category, country)
        print(f"Data for category: {category}, country: {country}")
        print(json_data)

       # Write the final DataFrame to a text file with UTF-8 encoding
        with open(f'data_{category}_{country}.txt', 'w', encoding='utf-8') as f:
           json.dump(json_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()