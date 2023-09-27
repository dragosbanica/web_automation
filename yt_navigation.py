from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import action

driver=webdriver.Chrome()

driver.get("https://www.youtube.com/")


try:
    popup=WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='content']/div[2]/div[6]/div[1]/ytd-button-renderer[2]/yt-button-shape/button/yt-touch-feedback-shape/div"))
    )
    popup.click()

except:
    driver.quit()
"""
#moving cursor on a video

action=webdriver.ActionChains(driver)
WebDriverWait(driver, 10)
element=driver.find_element(By.XPATH, "//*[@id='contents']/ytd-rich-item-renderer[3]")
action.move_to_element(element)
action.perform()

"""

try:
    video_play=WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='inline-preview-player']/div[18]/div[1]"))
    )
    video_play.click()

except:
    driver.quit()

#import screen_record
#import audio_record

#driver.quit()
