from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route("/transcript", methods=["GET"])
def transcript():
    video_url = request.args.get("url")

    if not video_url:
        return jsonify({"error": "missing url"}), 400

    try:
        cmd = [
            "yt-dlp",

            # 🔵 IMPORTANT: force NO VIDEO LOGIC
            "--skip-download",
            "--no-playlist",

            # 🔵 subtitles only
            "--write-auto-sub",
            "--write-sub",
            "--sub-lang", "en,fr",

            # 🔵 stability flags
            "--no-warnings",
            "--quiet",

            # 🔵 cookies (si nécessaire)
            "--cookies", "cookies.txt",

            # 🔵 output
            "-o", "/tmp/video.%(ext)s",

            video_url
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            return jsonify({
                "error": "yt-dlp failed",
                "details": result.stderr
            }), 500

        # 🔵 récupérer fichier subtitle
        for file in os.listdir("/tmp"):
            if file.endswith(".vtt") or file.endswith(".srt"):
                with open(os.path.join("/tmp", file), "r", encoding="utf-8") as f:
                    content = f.read()

                return jsonify({
                    "videoId": video_url,
                    "transcript": content
                })

        return jsonify({"error": "no transcript found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
