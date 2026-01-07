from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv 
from groq import Groq

app = Flask(__name__)
CORS(app)
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route("/", methods=["GET"])
def health():
    return {"status": "Groq AI server running"}

@app.route("/test", methods=["GET"])
def test_ai():
    chat = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": "Reply only with OK"}],
        temperature=0
    )
    return {"reply": chat.choices[0].message.content}

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

Hech qanday izoh YO‘Q.
Yahshilab o'ylanib keyin aniq javob ber.

Matn:
{text}
"""

        chat = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a strict exam answer extractor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        answer = chat.choices[0].message.content.strip()

        return jsonify({"answer": answer})

    except Exception as e:
        print("AI ERROR:", e)
        return jsonify({"error": "Groq AI error"}), 500

@app.route("/ai-image", methods=["POST"])
def analyze_image():
    try:
        data = request.json
        image_b64 = data.get("image_base64", "")
        if not image_b64:
            return jsonify({"error": "Image yo‘q"}), 400

        prompt = (
            "This is an exam question image. "
            "Answer strictly in ONE line. "
            "Format exactly: \"<raqam>-javob — <to‘liq javob>\". "
            "No explanations."
        )

        chat = client.chat.completions.create(
            model="models/llama-3.2-vision-preview",
            messages=[
                {
                    "role": "admin",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_b64}"
                            }
                        }
                    ],
                }
            ],
            temperature=0
        )

        answer = chat.choices[0].message.content.strip()
        return jsonify({"answer": answer})

    except Exception as e:
        print("VISION ERROR:", e)
        return jsonify({"error": "Vision AI error"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
