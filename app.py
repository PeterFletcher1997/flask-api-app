from flask import Flask, request
from import_files import format_json, success_email

post_url = "https://webhook.site/9a227568-3994-4c29-9006-0762865b808b"

app = Flask(__name__)

@app.route('/')
def homepage():
    return '<h1>main page</h2>'

@app.route('/webhook', methods=['POST'])
def receive_webhook():
    payload = request.json
    if request.method == 'POST':
        format_json(payload, post_url)
        try:
            success_email(payload)
        except Exception:
            raise Exception("Email was not sent due to error")


        return 'success', 200


if __name__ == "__main__":
    app.run(debug=True)