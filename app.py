from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/get-price')
def get_price():
    symbol = request.args.get('symbol', '').upper()
    if not symbol:
        return jsonify({'error': 'Symbol is required'}), 400

    try:
        url = f'https://apipubaws.tcbs.com.vn/stock-insight/v1/instrument/detail?tickers={symbol}'
        response = requests.get(url, timeout=5)
        data = response.json()
        if 'data' not in data or not data['data']:
            raise ValueError("Invalid response from TCBS")

        last_price = data['data'][0].get('lastPrice', None)
        return jsonify({'symbol': symbol, 'price': last_price})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)