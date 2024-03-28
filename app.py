from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

def number_to_words(num):
    num = int(num.replace('$', '').replace(',', ''))
    suffixes = ['', 'K', ' Million', ' Billion', ' Trillion', 'Q', 'Qu', 'S', 'Se', 'O', 'N', 'D']
    suffix_index = 0
    while num >= 1000 and suffix_index < len(suffixes)-1:
        suffix_index += 1
        num /= 1000.0
    return f"{num:.0f}{suffixes[suffix_index]}"

app = Flask(__name__)

def scrape_data():
    # Set up the WebDriver
    driver = webdriver.Chrome()  # Or specify the path to the ChromeDriver executable
    driver.get("https://coinmarketcap.com/cryptocurrency-category/")

    # Wait for the page to load
    time.sleep(5)

    # Find the table containing the data
    table = driver.find_element(By.XPATH, "//table[contains(@class, 'cmc-table')]")
    rows = table.find_elements(By.TAG_NAME, "tr")

    # Initialize lists to store data
    column_names = []
    data = []

    # Extract data from each row
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if cells:
            row_data = [cell.text for cell in cells]
            data.append(row_data)

    # Extract column names
    header_row = rows[0].find_elements(By.TAG_NAME, "th")
    column_names = [cell.text for cell in header_row]

    # Close the WebDriver
    driver.quit()

    # Create DataFrame
    df = pd.DataFrame(data, columns=column_names[0:])  # Skip the first column as it's usually an index
    filtered_df = df[df['Name'].isin(["E-commerce", "Ethereum Ecosystem", "Gaming", "Real Estate", "Generative AI", "Bitcoin Ecosystem", "Memes", "Video", "VR/AR", "DeFi Index", "Metaverse", "Cybersecurity"])]
    filtered1_df = filtered_df.iloc[:, [1,2, 4]]
    split_values = filtered1_df.iloc[:,2].str.split('\n', expand=True)
    filtered1_df['Market Cap'] = split_values[0]
    filtered1_df['Percent'] = split_values[1]
    filtered1_df['Market Cap'] = filtered1_df.iloc[:,2].apply(lambda x: pd.Series(number_to_words(x)))

    # Convert DataFrame to JSON
    json_data = filtered1_df.to_json(orient='records')
    return json_data

#df['Value (Words)'] = df['Value'].apply(lambda x: pd.Series(number_to_words(x)))

@app.route('/scrape', methods=['GET'])
def get_scraped_data():
    json_data = scrape_data()
    return jsonify(json_data)

if __name__ == '__main__':
    app.run(debug=True)


"""
from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

def number_to_words(num):
    num = int(num.replace('$', '').replace(',', ''))
    suffixes = ['', 'K', ' Million', ' Billion', ' Trillion', 'Q', 'Qu', 'S', 'Se', 'O', 'N', 'D']
    suffix_index = 0
    while num >= 1000 and suffix_index < len(suffixes)-1:
        suffix_index += 1
        num /= 1000.0
    return f"{num:.0f}{suffixes[suffix_index]}"

app = Flask(__name__)

def scrape_data():
    # Set up the WebDriver
    driver = webdriver.Chrome()  # Or specify the path to the ChromeDriver executable
    driver.get("https://coinmarketcap.com/cryptocurrency-category/")

    # Wait for the page to load
    time.sleep(5)

    # Find the table containing the data
    table = driver.find_element(By.XPATH, "//table[contains(@class, 'cmc-table')]")
    rows = table.find_elements(By.TAG_NAME, "tr")

    # Initialize lists to store data
    column_names = []
    data = []

    # Extract data from each row
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if cells:
            row_data = [cell.text for cell in cells]
            data.append(row_data)

    # Extract column names
    header_row = rows[0].find_elements(By.TAG_NAME, "th")
    column_names = [cell.text for cell in header_row]

    # Close the WebDriver
    driver.quit()

    # Create DataFrame
    df = pd.DataFrame(data, columns=column_names[0:])  # Skip the first column as it's usually an index
    filtered_df = df[df['Name'].isin(["E-commerce", "Ethereum Ecosystem", "Gaming", "Real Estate", "Generative AI", "Bitcoin Ecosystem", "Memes", "Video", "VR/AR", "DeFi Index", "Metaverse", "Cybersecurity"])]
    filtered1_df = filtered_df.iloc[:, [1,2, 4]]
    split_values = filtered1_df.iloc[:,2].str.split('\n', expand=True)
    filtered1_df['Market Cap'] = split_values[0]
    filtered1_df['Percent'] = split_values[1]
    filtered1_df['Market Cap'] = filtered1_df.iloc[:,2].apply(lambda x: pd.Series(number_to_words(x)))

    # Convert DataFrame to JSON
    json_data = filtered1_df.to_json(orient='records')
    return json_data

#df['Value (Words)'] = df['Value'].apply(lambda x: pd.Series(number_to_words(x)))

@app.route('/scrape', methods=['GET'])
def get_scraped_data():
    json_data = scrape_data()
    return jsonify(json_data)

if __name__ == '__main__':
    app.run(debug=True)
"""
"""
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import json

def money(value):
    pattern = re.compile(r'\$([\d,]+)(\d+\.\d+)%')
    match = pattern.match(value)
    if match:
        money_value = match.group(1)
        percent_value = match.group(2)
        return money_value, percent_value
    else:
        return 0
    
from flask import Flask, request, jsonify
application = Flask(__name__)
app=application
@app.route('/category', methods=['GET'])
def scrape_data():   
    try:
        url = "https://coinmarketcap.com/cryptocurrency-category/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'class': 'cmc-table'})
        headers = [header.text.strip() for header in table.find_all('th')]
        rows = []
        for row in table.find_all('tr')[1:]:  # Skip the first row (header row)
            rows.append([cell.text.strip() for cell in row.find_all('td')])
        df = pd.DataFrame(rows, columns=headers)
        filtered_df = df[df['Name'].isin(["e-Commerce", "Ethereum Ecosystem", "Gaming", "Real Estate", "Generative AI", "Bitcoin Ecosystem", "Memes", "Video", "VR/AR", "DeFi Index", "Metaverse", "Cybersecurity"])]
        filter_df = filtered_df[['Name', 'Avg. Price Change', "Market Cap"]]
        filter_df[['Money_Value', 'Percent_Value']] = filter_df['Market Cap'].apply(lambda x: pd.Series(money(x)))
        json_data = filter_df.to_json(orient='records')
        return(json_data)
    except requests.RequestException as e:
        print(f"Error: {e}")
if __name__ == '__main__':
    app.run(debug=True)
"""
