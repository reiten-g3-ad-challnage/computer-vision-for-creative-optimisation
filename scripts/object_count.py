import pandas as pd
import os
import cv2
import numpy as np

def count_objects():
    path = "/home/henok_desalegn/data/Challenge_Data/performance_data.csv"
    df = pd.read_csv(path)
    game_id_col = df['game_id']
    parent_dir = "/home/henok_desalegn/data/extracted_images"
    data = pd.DataFrame(columns=['game_id','object_count'])
    for i in range(len(game_id_col)):
        f = path = os.path.join(parent_dir, game_id_col[i],)
        f = f+'/start_frame.png'
        try:
            if os.path.isfile(f):
                img = cv2.imread(f)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                _, thresh = cv2.threshold(img, 225, 255, cv2.THRESH_BINARY_INV)
                kernal = np.ones((2, 2), np.uint8)
                dilation = cv2.dilate(thresh, kernal, iterations=2)
                contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                data.loc[len(data.index)] = [game_id_col[i],len(contours)]
        except Exception:
            pass
    data.to_csv("../data/object_count_data.csv",index=False)