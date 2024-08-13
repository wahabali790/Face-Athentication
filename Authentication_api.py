from flask import Flask, request, jsonify
import cv2
import face_recognition
import time

app = Flask(__name__)

###########################

User_image="cloudinary_image.png"
delay=3 #delay in second
threshold=0.6

###########################



def run_face_recognition():
    counter = 0
    messages = []
    while True:
        if counter >= 3:
            messages.append("You are not authentic person.")
            return messages

        # Open the default camera (index 0)
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            messages.append("Error: Could not open camera.")
            return messages

        # Capture frame-by-frame
        ret, frame = cap.read()

        # If the frame is read correctly, ret is True
        if not ret:
            messages.append("Error: Cannot receive frame.")
            return messages

        # Save the captured image
        cv2.imwrite('captured_image.jpg', frame)

        # Release the capture
        cap.release()

        # Load the captured image and detect faces
        picture_of_me = face_recognition.load_image_file("captured_image.jpg")
        face_locations = face_recognition.face_locations(picture_of_me)

        # If no face is detected, prompt the user to set their face in front of the camera
        if len(face_locations) == 0:
            messages.append("Please set your face position in front of the camera.")
            counter += 1  # Increment the counter if no face is detected
            time.sleep(delay)  # Wait for 5 seconds before retrying
            continue  # Restart the loop

        # If at least one face is detected, proceed with face recognition
        my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]

        unknown_picture = face_recognition.load_image_file(User_image)
        unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]

        # Compare face encodings
        results = face_recognition.compare_faces([my_face_encoding], unknown_face_encoding, tolerance=threshold)
        if results[0] == True:
            messages.append("Authentication successful")
            return messages
        else:
            messages.append("Authentication failed")
            counter += 1  # Increment the counter if authentication fails
            time.sleep(delay)  # Wait for 5 seconds before rerunning the code

@app.route('/authenticate', methods=['POST'])
def authenticate():
    messages = run_face_recognition()
    return jsonify({"messages": messages})

if __name__ == '__main__':
    app.run(debug=True,port=5005)
