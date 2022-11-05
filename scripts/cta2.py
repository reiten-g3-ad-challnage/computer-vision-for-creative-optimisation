import argparse
import cv2
import pandas as pd
import os
import glob

def detect_cta(game_id, path, logo):

    image = cv2.imread(path+"/end_frame.png")
    template = cv2.imread(logo)
    imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    templateGray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(imageGray, templateGray, cv2.TM_CCOEFF_NORMED)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(result)

    (startX, startY) = maxLoc
    endX = startX + template.shape[1]
    endY = startY + template.shape[0]
    cv2.rectangle(image, (startX, startY ), (endX, endY), (255, 0, 0), 3)
    cv2.imwrite(os.path.join("data/detected_cta",game_id+'detected_cta.jpg'), image)

    return game_id, startX, startY, template.shape[1], template.shape[1]


if __name__ == "__main__":

    path = "data/Challenge_Data/performance_data.csv"
    extracted_image_dir = "data/extracted_images"
    df = pd.read_csv(path)
    game_id_col = df['game_id']
    parent_dir = "data/Assets"
    count = 0
    data = []

    for i in range(len(game_id_col)):
        print("Processing asset " + game_id_col[i] + "index " + str(i))
        path = os.path.join(parent_dir, game_id_col[i])
        print('path '+str(path))
        extracted_im_path = os.path.join(extracted_image_dir, game_id_col[i])
        li = glob.glob(path+'/cta*')

        # li = path+'/cta.png'
        # print(li)
        
        for l in li:
            print(l)
            if os.path.exists(l):
                data.append(detect_cta(game_id_col[i], extracted_im_path, l))
        li = glob.glob(path+"/Cta*")
        #print(data)
        #print(li)

        for l in li:
            if os.path.exists(l):
                data.append(detect_cta(game_id_col[i], extracted_im_path, l))
        li = glob.glob(path+"/CTA*")

        for l in li:
            if os.path.exists(l):
                data.append(detect_cta(game_id_col[i],extracted_im_path, l))

    df = pd.DataFrame(data, columns=['game_id', 'startX', 'startY', 'height', 'width'])
    #print(data)
    df.to_csv("data/cta_data.csv")
    
