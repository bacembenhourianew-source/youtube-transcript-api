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
        # yt-dlp command
        cmd = [
    "yt-dlp",
    "--write-auto-sub",
    "--sub-lang", "en,fr",
    "--skip-download",
    "--no-warnings",
    "--quiet",
    "-o", "/tmp/video",
    video_url
]

        result = subprocess.run(cmd, capture_output=True, text=True)

        # ❗ gestion erreur yt-dlp
        if result.returncode != 0:
            return jsonify({
                "error": "yt-dlp failed",
                "details": result.stderr
            }), 500

        # chercher fichier généré
        for file in os.listdir("/tmp"):
            if file.endswith(".vtt"):
                with open(os.path.join("/tmp", file), "r", encoding="utf-8") as f:
                    content = f.read()

                return jsonify({
                    "transcript": content
                })

        return jsonify({"error": "no transcript found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
