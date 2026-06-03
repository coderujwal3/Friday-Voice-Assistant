import os
import cv2
import numpy as np
from insightface.app import FaceAnalysis

app = FaceAnalysis()
app.prepare(ctx_id=0)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

embedding_path = os.path.join(
    BASE_DIR,
    "face_db",
    "ujwal.npy"
)

known_embedding = np.load(embedding_path)

# known_embedding = np.load(
#     "face_db/ujwal.npy"
# )


def authenticate():
    authenticated = False
    count = 0  # number of frames used to verify user
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Camera could not be opened.")
        cap.release()
        return False

    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            print("Failed to read frame from camera.")
            count += 1
            if count >= 4:
                break
            continue

        faces = app.get(frame)
        count += 1

        for face in faces:
            bbox = face.bbox.astype(int)
            current_embedding = face.embedding
            similarity = np.dot(
                known_embedding,
                current_embedding
            ) / (
                np.linalg.norm(known_embedding)
                * np.linalg.norm(current_embedding)
            )

            if similarity > 0.60:
                color = (0, 255, 0)
                text = f"Authenticated {similarity:.2f}"
                authenticated = True
            else:
                color = (0, 0, 255)
                text = f"Unauthorized {similarity:.2f}"

            cv2.rectangle(
                frame,
                (bbox[0], bbox[1]),
                (bbox[2], bbox[3]),
                color,
                2
            )
            cv2.putText(
                frame,
                text,
                (bbox[0], bbox[1]-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color,
                2
            )

        cv2.imshow("Authentication", frame)

        if cv2.waitKey(1) == 27:
            break

        if count >= 4:
            break

    cap.release()
    cv2.destroyAllWindows()
    return authenticated

if __name__ == "__main__":
    authenticate()