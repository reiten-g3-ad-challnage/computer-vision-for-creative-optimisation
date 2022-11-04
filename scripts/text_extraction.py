import pandas as pd
import matplotlib.pyplot as plt
import pytesseract
import cv2
import os

class extract_text:

    def __init__(self):
        pass

    def text_to_df(self, pic_paths , writeout: bool=True, writeout_every: int=50, file_name: str='output.png')-> pd.Series:
        output_df = pd.DataFrame(columns=['pic_path', 'text'])

        output_df['pic_path'] = pic_paths

        for i, pic in enumerate(pic_paths):
            text = ''
            if os.path.exists(pic):
                try:
                    text = pytesseract.image_to_string(pic, timeout= 5) # Timeout after 5 seconds
                except RuntimeError as timeout_error:
                    pass
            text = self.clean_text(text)

            output_df.loc[i, 'text'] = text

            if writeout and (i+1)%writeout_every ==0:
                output_df.to_csv('../data/text_'+file_name[:-4]+'.csv', index=False)

        if writeout:
            output_df.to_csv('../data/text_'+file_name[:-4]+'.csv', index=False)

        return output_df['text']

    def clean_text(self, text:str)->str:
        output = text.replace('\x0c', '').replace('\x0b', '').replace('\n\n','\n')

        return output