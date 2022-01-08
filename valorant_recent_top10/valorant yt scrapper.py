from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd

game_recent_url = 'https://www.youtube.com/channel/UCiMRGE8Sc6oxIGuu_JxFoHg/recent'
chrome_driver_path = 'C:\Program Files (x86)\chromedriver.exe'

def setup_driver(url,chrome_driver_path):

    serv = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=serv)
    driver.get(url)
    return driver


def get_n_recent_videos(url,driver_path,n):

    driver = setup_driver(url,driver_path)
    videos = driver.find_elements(By.TAG_NAME,'ytd-grid-video-renderer')
    data = []

    for i,video in zip(range(n),videos[:10]):

        temp_data = dict()

        temp_data['video_title'] = video.find_element(By.TAG_NAME,'h3').text
        temp_data['video_thumbnail'] = video.find_element(By.TAG_NAME,'img').get_attribute('src')
        temp_data['video_publisher'] = video.find_element(By.CLASS_NAME,'yt-formatted-string').text
        temp_data['video_length'] = video.find_element(By.TAG_NAME,'ytd-thumbnail-overlay-time-status-renderer').text
        temp_data['video_views'] = video.find_element(By.ID,'metadata-line').find_elements(By.TAG_NAME,'span')[0].text
        temp_data['video_time'] = video.find_element(By.ID,'metadata-line').find_elements(By.TAG_NAME,'span')[1].text

        data.append(temp_data)

    return data

number_of_videos = 10

recent_videos = get_n_recent_videos(game_recent_url,chrome_driver_path,number_of_videos)

videos_df = pd.DataFrame(recent_videos)

videos_df.to_csv(r'youtube-scarpper\top_recent_valorant_videos.csv',index = False)

