from flask import Flask, request
from import_files import return_json, success_email

post_url = "https://webhook.site/9a227568-3994-4c29-9006-0762865b808b"

app = Flask(__name__)

@app.route('/')
def homepage():
    return '<h1>main page</h2>'

@app.route('/webhook', methods=['POST'])
def receive_webhook():
    payload = request.json
    if request.method == 'POST':
        return_json(payload, post_url)
        success_email(payload)

        return 'success', 200


if __name__ == "__main__":
    app.run(debug=True)