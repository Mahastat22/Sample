#necessary libraries
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

from flask import Flask, request, jsonify
application = Flask(__name__)
app=application
@app.route('/categories', methods=['POST'])
def scrape_data():
    url = "https://coinmarketcap.com/cryptocurrency-category/"  

    try:
        # request to the URL
        response = requests.get(url)

        # Check if the request is successful or not
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            # Find the table in of the webpage
            table = soup.find('table')
            #table extraction
            if table:
                rows = table.find_all('tr')
                data = []
                for row in rows:
                    cols = row.find_all(['td', 'th'])
                    cols = [col.text.strip() for col in cols]
                    data.append(cols)
                result = [[row[1], row[4]] for row in data[1:13]]
                return(jsonify(result))
                #for row in result:
                    #print(row)
    
    except requests.RequestException as e:
        # Handle exceptions (connection errors or timeouts)
        print(f"Error: {e}")

if __name__ == '__main__':
    app.run(debug=True)
