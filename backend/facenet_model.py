from deepface import DeepFace
import numpy as np

def get_embedding(image_path):

    embedding = DeepFace.represent(
        img_path=image_path,
        model_name="Facenet"
    )

    return np.array(embedding[0]["embedding"])


def compare_faces(img1, img2):

    try:
        result = DeepFace.verify(
            img1,
            img2,
            model_name="Facenet"
        )

        return result["verified"]

    except:
        return False