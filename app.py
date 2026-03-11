from flask import Flask, send_from_directory, request, jsonify
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)

YOUR_EMAIL = "brawlstarsfreeze@gmail.com"
YOUR_APP_PASSWORD = "qpeg rnht qepb nxwn"

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/contact")
def contact():
    return send_from_directory(".", "contact.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(".", path)

@app.route("/send", methods=["POST"])
def send_email():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"success": False, "message": "Немає даних"}), 400

        name = data.get("name", "")
        email = data.get("email", "")
        subject = data.get("subject", "Нове повідомлення")
        message = data.get("message", "")

        text = f"""
Нове повідомлення з сайту

Ім'я: {name}
Email: {email}
Тема: {subject}

Повідомлення:
{message}
"""

        msg = MIMEText(text, "plain", "utf-8")
        msg["Subject"] = subject
        msg["From"] = YOUR_EMAIL
        msg["To"] = YOUR_EMAIL

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(YOUR_EMAIL, YOUR_APP_PASSWORD)
            server.send_message(msg)

        return jsonify({"success": True, "message": "Повідомлення надіслано!"})

    except Exception as e:
        print("EMAIL ERROR:", e)
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
