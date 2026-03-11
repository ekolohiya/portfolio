from flask import Flask, send_from_directory, request, jsonify
import smtplib
from email.mime.text import MIMEText

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
    data = request.get_json()

    name = data["name"]
    email = data["email"]
    subject = data["subject"]
    message = data["message"]

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

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(YOUR_EMAIL, YOUR_APP_PASSWORD)
    server.send_message(msg)
    server.quit()

    return jsonify({"success": True, "message": "Повідомлення надіслано!"})


app.run(debug=True)