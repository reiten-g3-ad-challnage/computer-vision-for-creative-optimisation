import pandas as pd
import os
from deepface import DeepFace
import cv2

def emotions_feature_extratctor():
    path = "/home/henok_desalegn/data/Challenge_Data/performance_data.csv"
    df = pd.read_csv(path)
    game_id_col = df['game_id']
    parent_dir = "/home/henok_desalegn/data/extracted_images"
    start_frame_data = pd.DataFrame(columns=['game_id','emotion','gender','race'])

   
    for i in range(len(game_id_col)):
        f = os.path.join(parent_dir, game_id_col[i],)
        f = f+'/start_frame.png'
        try:
            if os.path.isfile(f):
                image = cv2.imread(f)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
                faces = faceCascade.detectMultiScale(
                    gray,
                    scaleFactor=1.3,
                    minNeighbors=3,
                    minSize=(30, 30)
                )
                if len(faces) != 0:
                    face_analysis = DeepFace.analyze(img_path = f, enforce_detection=False)
                    start_frame_data.loc[len(start_frame_data.index)] = [game_id_col[i],face_analysis['dominant_emotion'],face_analysis['gender'],face_analysis['dominant_race']]
                else:
                    start_frame_data.loc[len(start_frame_data.index)] = [game_id_col[i],'None','None','None']
        except Exception:
            pass
    start_frame_data.to_csv("../data/emotions_extracted_data.csv",index=False)