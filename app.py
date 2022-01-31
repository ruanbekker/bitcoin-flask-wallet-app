from flask import Flask, render_template
import requests
import time
import os

password = os.environ['BTC_PASSWORD']

app = Flask(__name__)

@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    date = time.strftime("%Y-%m-%d %H:%S %Z", time.localtime(date))
    return date

def fetch_transactions():
    headers = {'Content-Type': 'text/plain'}
    payload = {'jsonrpc': '1.0', 'id': 'flask', 'method': 'listtransactions', 'params': []}
    response = requests.post('http://127.0.0.1:18332/wallet/main', auth=('bitcoin', password), headers=headers, json=payload).json()
    return response['result']

@app.route('/')
def main():
    return 'hello'

@app.route('/listtransactions')
def listtransactions():
    transactions = fetch_transactions()
    return render_template('table.html', title='Recent Transactions', transactions=transactions)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009)
