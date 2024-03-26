#necessary libraries
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
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
@app.route('/tokens', methods=['GET'])
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
        dd = df.iloc[:, [0, 2, 3]].values.tolist()
        json_data = []
        for sublist in dd:
            json_data.append({"Name": sublist[0], "Martketcap":sublist[1],"Percent": sublist[2]})

        #json_data1 = json.dumps(json_data)
        return json.dumps(json_data, indent=2)

    except requests.RequestException as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    app.run(debug=True)
"""
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
@app.route('/tokens', methods=['GET'])
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
        return(df.iloc[:, [0, 2, 3]].values.tolist())

    except requests.RequestException as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    app.run(debug=True)
"""

"""
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'
"""

