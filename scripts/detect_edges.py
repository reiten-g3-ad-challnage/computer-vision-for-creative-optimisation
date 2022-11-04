import cv2
import pandas as pd
import os

path = "../data/performance_data.csv"
extracted_image_dir = "../data/extracted_images"
df = pd.read_csv(path)
game_id_col = df['game_id']
count = 0
data = []
for i in range(len(game_id_col)):
    try:
        print("Processing asset " + game_id_col[i] + "index " + str(i))
        path = os.path.join(extracted_image_dir, game_id_col[i])
        image = cv2.imread(path+"/start_frame.png")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        mid = cv2.Canny(blurred, 30, 150)
        count = cv2.countNonZero(mid)
        cv2.imwrite(os.path.join("../data/detected_edges",game_id_col[i]+'detected_edge.jpg'), mid)
        data.append((game_id_col[i], count))
    except:
        data.append((game_id_col[i], None))
        pass
df = pd.DataFrame(data, columns=['game_id', 'edges_pixel_count'])
df.to_csv("../data/edge_data.csv")

