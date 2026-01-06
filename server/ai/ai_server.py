from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

client = genai.Client(api_key = os.getenv("GEMINI_API_KEY"))
@app.route("/ai", methods=["POST"])
def analyze_text():
    try:
        data = request.json
        text = data.get("text", "").strip()

        if not text:
            return jsonify({"error": "Text yo‘q"}), 400

        prompt = f"""
Quyidagi matn test savolidir.
Variantlar raqam bilan berilgan.

Faqat bitta qatorda javob qaytar.
Format QATTIQ:
"<raqam>-javob — <to‘liq javob matni>"

Hech qanday izoh, tushuntirish, qo‘shimcha gap YO‘Q.

Matn:
{text}
"""

        res = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "temperature": 0,
                "response_mime_type": "application/json"
            }
        )
        try:
            result = res.parsed
            if not result:
                result = json.loads(res.text)
        except Exception:
            result = {"answer": res.text.strip()}

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": "AI bilan bog‘lanishda xatolik"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
