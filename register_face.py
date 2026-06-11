import cv2
import numpy as np
from insightface.app import FaceAnalysis
import os

def register_face(name):
    app = FaceAnalysis()
    app.prepare(ctx_id=0)

    os.makedirs("face_db", exist_ok=True)

    cap = cv2.VideoCapture(0)

    print("Press S to register")

    while True:
        ret, frame = cap.read()

        faces = app.get(frame)

        for face in faces:
            bbox = face.bbox.astype(int)

            cv2.rectangle(
                frame,
                (bbox[0], bbox[1]),
                (bbox[2], bbox[3]),
                (0, 255, 0),
                2
            )

        cv2.imshow("Register Face", frame)

        key = cv2.waitKey(1)

        if key == ord("s"):

            if len(faces) != 1:
                print("Exactly one face required")
                continue

            embedding = faces[0].embedding

            np.save(
                f"face_db/{name}.npy",
                embedding
            )

            print("Face Registered Successfully")
            break

        elif key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    return