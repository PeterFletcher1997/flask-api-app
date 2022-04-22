from flask import Flask, request
from import_files import format_json, success_email
from enviro_variables import SEND_URL

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def receive_webhook():
    payload = request.json
    if request.method == 'POST':
        format_json(payload, SEND_URL)
        try:
            success_email(payload)
        except Exception:
            raise Exception("Email was not sent due to error")

        return 'success', 200


if __name__ == "__main__":
    app.run(debug=True)
