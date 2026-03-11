from flask import Flask, send_from_directory, request, jsonify
import os
import requests

app = Flask(__name__)

RESEND_API_KEY = os.environ.get("RESEND_API_KEY")
TO_EMAIL = os.environ.get("TO_EMAIL")

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
        data = request.get_json(silent=True)

        if not data:
            return jsonify({"success": False, "message": "Немає даних"}), 400

        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        subject = data.get("subject", "").strip()
        message = data.get("message", "").strip()

        if not name or not email or not subject or not message:
            return jsonify({"success": False, "message": "Заповніть усі поля"}), 400

        if not RESEND_API_KEY or not TO_EMAIL:
            return jsonify({"success": False, "message": "Не налаштовані змінні середовища"}), 500

        html = f"""
        <h2>Нове повідомлення з сайту</h2>
        <p><b>Ім'я:</b> {name}</p>
        <p><b>Email:</b> {email}</p>
        <p><b>Тема:</b> {subject}</p>
        <p><b>Повідомлення:</b><br>{message}</p>
        """

        response = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "from": "onboarding@resend.dev",
                "to": [TO_EMAIL],
                "subject": f"Повідомлення з сайту: {subject}",
                "html": html,
                "reply_to": email
            },
            timeout=20
        )

        if response.status_code not in (200, 201):
            return jsonify({
                "success": False,
                "message": f"Помилка Resend: {response.text}"
            }), 500

        return jsonify({"success": True, "message": "Повідомлення надіслано!"})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
