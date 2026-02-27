from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Currency API! Use /convert?from=USD&to=PKR&amount=10"

@app.route('/convert', methods=['GET'])
def convert():
    from_curr = request.args.get('from', 'USD').upper()
    to_curr = request.args.get('to', 'PKR').upper()
    amount = float(request.args.get('amount', 1))

    # Free API for exchange rates
    url = f"https://api.exchangerate-api.com/v4/latest/{from_curr}"
    
    try:
        response = requests.get(url)
        data = response.json()
        rate = data['rates'][to_curr]
        converted_amount = amount * rate

        return jsonify({
            "status": "success",
            "from": from_curr,
            "to": to_curr,
            "amount": amount,
            "rate": rate,
            "result": round(converted_amount, 2)
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
