import subprocess
import time
from flask import Flask, Response

app = Flask(__name__)

# 📡 List of radio stations
RADIO_STATIONS = {

    "asianet_movies": "http://ktv.im:8080/44444/44444/81804",
    "surya_movies": "http://ktv.im:8080/44444/44444/81823",
    "surya_comedy": "http://ktv.im:8080/44444/44444/81825",
    "mazhavil_manorama": "http://ktv.im:8080/44444/44444/81837",
    "asianet_plus": "http://ktv.im:8080/44444/44444/81801",
    "media_one": "http://ktv.im:8080/44444/44444/81777",
"kairali_we":
"http://ktv.im:8080/44444/44444/81812",

}


# 🔄 Streaming function with error handling
def generate_stream(url):
    process = None
    while True:
        if process:
            process.kill()  # Stop old FFmpeg instance before restarting
        
        process = subprocess.Popen(
    [
        "ffmpeg", "-re", "-protocol_whitelist", "file,http,https,tcp,tls,crypto", 
        "-i", url, "-vn", "-ac", "2", "-b:a", "64k", "-buffer_size", "8192k", 
        "-c:a", "libmp3lame", "-f", "mp3", "-"
    ],
    stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=16384
)

        print(f"🎵 Streaming from: {url} (Mono, 40kbps)")

        try:
            for chunk in iter(lambda: process.stdout.read(8192), b""):
                yield chunk
        except GeneratorExit:
            process.kill()
            break
        except Exception as e:
            print(f"⚠️ Stream error: {e}")

        print("🔄 FFmpeg stopped, restarting stream...")
        time.sleep(5)  # Wait before restarting

# 🌍 API to stream selected station
@app.route("/<station_name>")
def stream(station_name):
    url = RADIO_STATIONS.get(station_name)
    if not url:
        return "⚠️ Station not found", 404
    
    return Response(generate_stream(url), mimetype="audio/mpeg")

# 🚀 Start Flask server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)