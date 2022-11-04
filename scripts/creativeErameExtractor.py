from typing import Tuple
from time import sleep
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from os import path
import pyautogui
import pandas as pd 
import os


class CreativeFrameExtractor:
    '''
    Class responsible for Extracting Creative Start and End Frames.
    It requires a chrome webdriver compatible with selenium to be
    installed/included in the run environment path.
    '''

    def __init__(self, preview_url: str,  
                 save_location: str = '',
                 browser_edges: Tuple[float, float] = (70, 1039)) -> None:
        
        self.preview_url = preview_url
        self.browser_edges = browser_edges
        self.save_location = save_location
        self.engagement_type = "tap"
        self.seconds = []
        self.opt = Options()
        self.opt.add_argument("--hide-scrollbars")
        self.opt.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        # Browser Logs
        self.capabilities = DesiredCapabilities.CHROME
        self.capabilities["goog:loggingPrefs"] = {"browser": "ALL"}

    def is_status_complete(self, passed_driver) -> bool:
        '''
        Function to check status of the AD-Unit and its completion.
        '''
        # Retrieve logs from browser
        logs = passed_driver.get_log("browser")

        for log in logs:
            # Select logs coming from AD-Unit
            if log["source"] == "console-api":
                # Extract message from log
                message = log["message"]

                if '"GAME CREATED"' in message or '"DROPPED"' in message:
                    # Start Recording Game
                    print("Starting Recording AD-UNIT...")
                    print(log)
                    return False

                if '"START"' in message:
                    # Engaged
                    print("AD-UNIT Engaged...")
                    print(log)
                    return False

                if '"GAME COMPLETE"' in message:
                    # Stop Recording Game
                    print("Stopped Recording AD-UNIT...")
                    print(log)
                    return True

        return True
    
   

    def _imitate_engagement(self, ad_size: Tuple[float, float]) -> None:
        '''
        Function to imitate a given engagement type.
        '''
        center = (ad_size[0]/2, self.browser_edges[0] + (ad_size[1]/2))

        if self.engagement_type == "tap":
            pyautogui.moveTo(center[0], center[1], duration=1)
            pyautogui.leftClick()

        elif self.engagement_type == "swipe right":
            pyautogui.moveTo(center[0], center[1], duration=1)
            pyautogui.dragRel(center[0], 0, duration=1)

        elif self.engagement_type == "swipe left":
            pyautogui.moveTo(center[0], center[1], duration=1)
            pyautogui.dragRel(-center[0], 0, duration=1)

        elif self.engagement_type == "tap and hold":
            pyautogui.moveTo(center[0], center[1], duration=1)
            pyautogui.click()

        elif self.engagement_type == "scrub":
            pyautogui.moveTo(center[0] - (1/2 * center[0]),
                             center[1] - (2/3 * center[1]), duration=0.2)
            pyautogui.dragRel(center[0], 0, duration=0.2)
            pyautogui.dragRel(-center[0], (1/3 * center[1]), duration=0.2)
            pyautogui.dragRel(center[0], 0, duration=0.2)
            pyautogui.dragRel(-center[0], (1/3 * center[1]), duration=0.2)
            pyautogui.dragRel(center[0], 0, duration=0.2)
            

    def generate_frames(self) -> None:
        '''
        Function to generate creative start and end frames.
        '''
        # Initialize Selenium WebDriver
        driver = webdriver.Chrome(
            options=self.opt, desired_capabilities=self.capabilities, )
        # Maximize WebDriver's Window to Maximum Size
        driver.maximize_window()

        try:
            # Load AD-Unit through Selenium
            driver.get(self.preview_url)

            # Locate AD-Unit Element from Browser
            canvas = driver.find_element(By.TAG_NAME, "canvas")

            # Capture Start Frame
            canvas.screenshot(
                os.path.join(self.save_location, 'start_frame.png'))
            print('Start Frame captured')

            ad_size = (canvas.size.get("width"), canvas.size.get("height"))
            
            self._imitate_engagement(ad_size)
            t1 = datetime.now()

            WebDriverWait(driver, 30).until(self.is_status_complete)

            sleep(20)
            t2 = datetime.now()

            delta = t2 - t1
            canvas.screenshot(os.path.join(self.save_location,'end_frame.png'))
            print('End Frame Captured')
            sec = delta.total_seconds()
            self.seconds.append(sec)
            driver.close()

        except TimeoutException:
            print("TimeOut Exception Fired")
            print("AD-Unit Status Console Logs did not Complete. Engagement Failed.")
            self.seconds.append(0)
            driver.close()

        except NoSuchElementException:
            self.seconds.append(0)
            print(f"AD-Unit Failed to Load: {self.preview_url}")
            driver.close()
    
    def save(self, df):
        df['video_length'] = self.seconds
        df.to_csv("video_length.csv")

if __name__ == "__main__":
    path = "../data/performance_data.csv"
    df = pd.read_csv(path)
    game_id_col = df['game_id']
    preview_link = df['preview_link']
    parent_dir = "../data/extracted_images"
    for i in range(len(game_id_col)):
        print("Processing asset " + game_id_col[i] + "index " + str(i))
        path = os.path.join(parent_dir, game_id_col[i])
        if not os.path.isdir(path):
            os.mkdir(path)
        extract = CreativeFrameExtractor(preview_link[i],path)
        extract.generate_frames()
    extract.save(df['game_id'])

