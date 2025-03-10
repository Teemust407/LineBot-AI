from flask import Flask, request, jsonify
import datetime
import random
from face_detector import detect_face
from time_checker import get_message

app = Flask(__name__)

@app.route("/check-in", methods=["POST"])
def check_in():
    data = request.json
    user_name = data.get("name")
    image_url = data.get("image_url")
    check_in_time = datetime.datetime.now().strftime("%H:%M:%S")
    
    if detect_face(image_url):
        message = get_message()
        return jsonify({"user": user_name, "time": check_in_time, "message": message})
    else:
        return jsonify({"error": "ไม่พบใบหน้าในภาพ"}), 400

if __name__ == "__main__":
    app.run(debug=True)
