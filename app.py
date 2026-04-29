from flask import Flask, request, jsonify
import requests
from urllib.parse import urlparse, parse_qs

app = Flask(__name__)

@app.route("/transcript", methods=["GET"])
def transcript():
    video_url = request.args.get("url")

    if not video_url:
        return jsonify({"error": "missing url"}), 400

    try:
        # 🔵 extraction robuste du video_id
        parsed = urlparse(video_url)
        video_id = parse_qs(parsed.query).get("v", [None])[0]

        if not video_id:
            return jsonify({"error": "invalid youtube url"}), 400

        # 🔵 langues à tester
        langs = ["en", "fr", "en-US"]

        # 🔵 tentative récupération transcript
        for lang in langs:
            url = f"https://www.youtube.com/api/timedtext?v={video_id}&lang={lang}"
            r = requests.get(url)

            if r.status_code == 200 and r.text.strip():
                return jsonify({
                    "videoId": video_id,
                    "lang": lang,
                    "transcript": r.text
                })

        return jsonify({
            "error": "no transcript found",
            "videoId": video_id
        }), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🔵 obligatoire pour Render
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
