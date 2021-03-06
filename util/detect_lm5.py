import cv2
import mediapipe as mp


def midpoint(p1, p2):
    coords = (p1.x + p2.x) / 2.0, (p1.y + p2.y) / 2.0
    return coords


def relative_coord(shape, coord):
    x = coord[0]
    y = coord[1]
    relative_x = round(x * shape[1], 2)
    relative_y = round(y * shape[0], 2)
    return relative_x, relative_y


def generate5keypoints(img):
    mp_face_mesh = mp.solutions.face_mesh
    with mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=2,
            min_detection_confidence=0.5) as face_mesh:
        # annotated_image = image.copy()
        results = face_mesh.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        if results.multi_face_landmarks is None or len(results.multi_face_landmarks) > 1:
            return None
        else:

            for face in results.multi_face_landmarks:
                shape = img.shape

                leftEye = relative_coord(shape, midpoint(face.landmark[33], face.landmark[133]))
                rightEye = relative_coord(shape, midpoint(face.landmark[362], face.landmark[263]))
                noseTip = relative_coord(shape, (face.landmark[1].x, face.landmark[1].y))
                mouthLeft = relative_coord(shape, (face.landmark[57].x, face.landmark[57].y))
                mouthRight = relative_coord(shape, (face.landmark[287].x, face.landmark[287].y))

                features = [leftEye, rightEye, noseTip, mouthLeft, mouthRight]
                return features
