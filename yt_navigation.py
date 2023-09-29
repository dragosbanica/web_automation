from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import action
from threading import Thread
import logging
import time


def audio_record():
    import pyaudio
    import wave

    logging.info("Started the audio recording thread")
    filename= "audio_rec.wav"
    sound  = True

    #set the chunk size of 1024 samples
    CHUNK = 1024

    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 10
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index = 2,
                    frames_per_buffer=CHUNK)

    logging.info("Starting the audio recording")
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
     
    logging.info("Finished the audio recording")

    #stop and close stream
    stream.stop_stream()
    stream.close()

    #terminate pyaudio object
    p.terminate()

    #save audio file
    #open the file in 'write bytes' modes
    wf = wave.open(filename, 'wb')

    #set the channels
    wf.setnchannels(CHANNELS)

    #set the sample format
    wf.setsampwidth(p.get_sample_size(FORMAT))

    #set the sample rate
    wf.setframerate(RATE)

    # write the frames as bytes
    wf.writeframes(b''.join(frames))

    # close the file
    wf.close()

    logging.info("Closing the audio recording thread")


def screen_record():
    import cv2
    import numpy as np
    import pyautogui
    import pygetwindow as gw
    import sys

    logging.info("Started the screen recording thread")

    # the window name, e.g "notepad", "Chrome", etc.
    window_name = "chrome"

    # define the codec
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    # frames per second
    fps = 12.0
    # the time you want to record in seconds
    record_seconds = 10

    # search for the window, getting the first matched window with the title
    w = gw.getWindowsWithTitle(window_name)[0]
    # activate the window
    w.activate()

    # create the video write object
    out = cv2.VideoWriter("screen_rec.avi", fourcc, fps, tuple(w.size))

    logging.info("Starting the screen recording")
    
    for i in range(int(record_seconds * fps)):
        # make a screenshot
        img = pyautogui.screenshot(region=(w.left, w.top, w.width, w.height))
        # convert these pixels to a proper numpy array to work with OpenCV
        frame = np.array(img)
        # convert colors from BGR to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # write the frame
        out.write(frame)
        # show the frame
        #cv2.imshow("screenshot", frame)
        # if the user clicks q, it exits
        if cv2.waitKey(1) == ord("q"):
            break

    logging.info("Finished the screen recording")
    
    # make sure everything is closed when exited
    cv2.destroyAllWindows()
    out.release()

    logging.info("Closing the screen recording thread")

driver=webdriver.Chrome()

driver.get("https://www.youtube.com/")

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
logging.info("Opened youtube main page")

try:
    popup=WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='content']/div[2]/div[6]/div[1]/ytd-button-renderer[2]/yt-button-shape/button/yt-touch-feedback-shape/div"))
    )
    popup.click()
    logging.info("Clicked on the Cookies button")

except:
    logging.info("The element was not found or something else")
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
    logging.info("Clicked on a random video")
except:
    logging.info("The element was not found or something else")
    driver.quit()

srec=Thread(target=screen_record, daemon=True)
srec.start()

arec=Thread(target=audio_record, daemon=True)
arec.start()

time.sleep(11)

logging.info("Closing the browser")
driver.quit()
