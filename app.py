from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/transcript", methods=["GET"])
def transcript():
    video_url = request.args.get("url")

    if not video_url:
        return jsonify({"error": "missing url"}), 400

    try:
        # extraire video id
        if "v=" in video_url:
        video_id = video_url.split("v=")[1].split("&")[0]

langs = ["en", "fr", "en-US"]

for lang in langs:
    url = f"https://www.youtube.com/api/timedtext?v={video_id}&lang={lang}"
    r = requests.get(url)

    if r.status_code == 200 and r.text.strip():
        return jsonify({
            "videoId": video_id,
            "lang": lang,
            "transcript": r.text
        })

return jsonify({"error": "no transcript found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
