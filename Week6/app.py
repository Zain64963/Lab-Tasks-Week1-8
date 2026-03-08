from flask import Flask, render_template, request
import cv2
import dlib
import numpy as np
import os

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")


def calculate_distance(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))


def personality_prediction(eye, nose, mouth, jaw):

    if eye > 70:
        return "Extrovert Personality"

    elif jaw > 140:
        return "Leader Personality"

    elif nose > 60:
        return "Creative Personality"

    else:
        return "Analytical Personality"


@app.route("/", methods=["GET", "POST"])
def index():

    result = None
    image_path = None

    if request.method == "POST":

        file = request.files["image"]

        if file:

            path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(path)

            image_path = path

            img = cv2.imread(path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            faces = detector(gray)

            for face in faces:

                landmarks = predictor(gray, face)

                points = []

                for i in range(68):
                    x = landmarks.part(i).x
                    y = landmarks.part(i).y

                    points.append((x, y))

                    cv2.circle(img, (x, y), 2, (0,255,0), -1)

                eye_distance = calculate_distance(points[36], points[45])

                nose_length = calculate_distance(points[27], points[33])

                mouth_width = calculate_distance(points[48], points[54])

                jaw_width = calculate_distance(points[0], points[16])

                personality = personality_prediction(
                    eye_distance,
                    nose_length,
                    mouth_width,
                    jaw_width
                )

                result = {
                    "eye": round(eye_distance,2),
                    "nose": round(nose_length,2),
                    "mouth": round(mouth_width,2),
                    "jaw": round(jaw_width,2),
                    "personality": personality
                }

            cv2.imwrite(path, img)

    return render_template(
        "index.html",
        result=result,
        image_path=image_path
    )


if __name__ == "__main__":
    app.run(debug=True)
