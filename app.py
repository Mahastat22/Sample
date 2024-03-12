#necessary libraries
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import re

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
@app.route('/tokens', methods=['POST'])
def scrape_data():   
    try:
        url = "https://coinmarketcap.com/cryptocurrency-category/"  
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table')
            if table:
                rows = table.find_all('tr')
                data = []
                for row in rows:
                    cols = row.find_all(['td', 'th'])
                    cols = [col.text.strip() for col in cols]
                    data.append(cols)
                result = [[row[1], row[4]] for row in data[1:13]]
                #print((result))
        df = pd.DataFrame(result, columns=['Name', 'Value'])
        df[['Money_Value', 'Percent_Value']] = df['Value'].apply(lambda x: pd.Series(money(x)))
        #print(df['Name', 'Money_Value'])
        return(df.iloc[:, [0, 2]].values.tolist())

    except requests.RequestException as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    app.run(debug=True)
