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
        else:
            return jsonify({"error": "invalid youtube url"}), 400

        # YouTube captions API (FREE + no bot block)
        url = f"https://www.youtube.com/api/timedtext?v={video_id}&lang=en"

        r = requests.get(url)

        if r.status_code != 200 or not r.text.strip():
            return jsonify({"error": "no transcript found"}), 404

        return jsonify({
            "videoId": video_id,
            "transcript": r.text
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
