import json
import pandas as pd
from src.transform import create_dataframe, transform_dataframe
from src.load import load

def read_data_from_file(file_path):
    # Read the text file into a DataFrame
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def etl_process_from_file(file_path):
    # Read data from the text file
    data = read_data_from_file(file_path)
    # Create and clean a DataFrame from the data
    df = create_dataframe(data)
    # Transform the clean data
    final_df = transform_dataframe(df)
    #last will be load, but just return for now to display
    return final_df

def main():
    # List of test files
    test_files = [
        'data_business_us.txt',
        'data_entertainment_us.txt',
        'data_general_us.txt',
        'data_health_us.txt',
        'data_science_us.txt',
        'data_sports_us.txt',
        'data_technology_us.txt'
        #,'data_business_ca.txt',
        #'data_entertainment_ca.txt',
        #'data_general_ca.txt',
        #'data_health_ca.txt',
        #'data_science_ca.txt',
        #'data_sports_ca.txt',
        #'data_technology_ca.txt'
    ]

    for file_path in test_files:
        final_df = etl_process_from_file(file_path)
        #print(f"Data from file: {file_path}")
        #print(final_df)

        # Write the final DataFrame to a new text file with UTF-8 encoding
        output_file_path = file_path.replace('.txt', '_transformed.txt')
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(final_df.to_string())

if __name__ == "__main__":
    main()