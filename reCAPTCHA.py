"""
SCRIPT: reCaptcha.py
AUTHOR: Tom Frisenda
PURPOSE: Automate reCAPTCHA by leveraging speech recognition library

PRE-REQUISITES:
*Chrome installed with chrome drive that supports the chrome version - https://chromedriver.chromium.org/downloads
*update driver code to the path of your own chromedriver (line 106)
*Enter CMD line argument of position [1] for target URL , or leave blank to run on test site

"""
# Standard python libraries
import sys
import time
import os
import random
import urllib
from urllib import request
import platform

# Additional Modules
from selenium import webdriver  # pip install selenium
from selenium.webdriver.chrome.options import Options
import ffmpy  # pip install ffmpy
import ffmpeg  # apt-get install ffmpeg (doesnt work with pip install)
import pydub  # pip install pydub
from pydub import AudioSegment
import speech_recognition as sr  # pip install SpeechRecognition
from google.cloud import speech  # pip install google-cloud-speech(back up)

# Modules for future improvement(s)
from selenium.webdriver.common.proxy import Proxy, ProxyType


"""Function to set up parameters for driver - option for chrome headless mode"""
def setup(path):
    options = webdriver.ChromeOptions()
    headless = input("Do you want to run Chrome in headless mode?").upper()
    if headless == "Y": # run headless on its own if used
        options.headless = True
        driver = webdriver.Chrome(options=options, executable_path=path)
        return driver
    else: # else use all available counter detection options
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument("--start-maximized")
        options.add_argument("--single-process")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--incognito")
        options.add_argument("disable-infobars")
        driver = webdriver.Chrome(options=options, executable_path=path)
    return driver


""" function to pause to wait for site to catch up , random number so pattern changes each time"""
def snooze():
    time.sleep(random.randint(1, 3))


""" function to switch frames and position based on the search conducted for the variable 'frames'"""
def changeFrame(frames, position=10):
    if position == 10:
        chrome_driver.switch_to.frame(frames)
    else:
        chrome_driver.switch_to.frame(frames[position])
    snooze()


"""Function to check for errors , as cannot raise SystemExit in try / except block"""
def failure_check(bool_check):
    if bool_check:
        print("-!-ERROR, QUITING-!-")
        sys.exit(0)
    else:
        print("---No errors at", time.strftime("%H:%M:%S"), "---")


""" function to grab audio source and download , then convert to .WAV"""
def audio_save(audio):
    # name for file when saved to PWD
    OS = platform.system()
    if OS == "Linux" or OS == "Linux2" or OS == "Darwin":
        filesys = "/"
    else:
        filesys = "\\"
    speech_file = filesys + "audio_sample.mp3"
    urllib.request.urlretrieve(audio, pwd + speech_file)
    sound = AudioSegment.from_mp3(pwd + speech_file)
    sound.export(pwd + filesys + "Sample_wav.wav", format="wav")
    print("---Audio successfully converted to .WAV")



"""Function to conver audio to text"""
def translate():
    r = sr.Recognizer()
    Wav_File = sr.AudioFile("Sample_wav.wav")
    with Wav_File as source:
        Final_audio = r.record(source)

    text = r.recognize_google(Final_audio)
    print("the captcha answer is:",text)
    return text


"""Set up parameters : target url , path to dependency 'chromedriver.exe' and driver options for increased undetectability."""
# !replace with path to your chrome drive! - path to chromedriver.exe
path = r"/home/kali/.config/google-chrome/chromedriver"
Error_check = False
pwd = os.getcwd()
print("your Current Working directiory is:", pwd)

chrome_driver = setup(path)


"""if no CMD line arguement is given , default tests are used"""
if len(sys.argv) < 2: # some test sites
    test = "https://www.google.com/recaptcha/api2/demo"
    # test = "https://patrickhlauke.github.io/recaptcha/"
    # test = "https://recaptcha-demo.appspot.com/recaptcha-v2-checkbox.php"
else:
    test = sys.argv[1]# command line argument for web address with reCAPTCHA


"""open target url"""
print("----Attempting to Open Webpage----")
try:
    chrome_driver.get(test)# open website supplied at command line or default test
    print("----Webpage opened successfully----" \
          , "\nopened:", chrome_driver.title \
          , "\nat: " + str(test))
except:
    print("Opening website unsuccessful , please check the URL and try again")
    Error_check = True
failure_check(Error_check)# check to see if any errors occured
snooze() # sleep for a random value so behaviour changes each run


"""Locate and interact with captcha initiation button"""
search = chrome_driver.find_element_by_tag_name("iframe") # search for first iframe
changeFrame(search)# switch to first iframe

try:  # Find "I am not a robot" element and  use action 'click'
    chrome_driver.find_element_by_class_name("recaptcha-checkbox-border").click()
    print("---successfully initiated captcha---")
except (RuntimeError, TypeError, NameError):
    print("-!-Captcha did not initiate...quiting-!-")
    Error_check = True
failure_check(Error_check)
chrome_driver.switch_to.default_content()# Switch back to default frame before searching for another
snooze()


"""Locate and interact with audio reCAPTCHA initiation button"""
search = chrome_driver.find_element_by_xpath("/html/body/div[2]/div[4]").find_elements_by_tag_name("iframe")# find iframe element border by searching with xpath
changeFrame(search, 0)# switch to new captcha frame
snooze()
try:  # Find recaptcha audio button inside selected frame , and click it
    chrome_driver.find_element_by_id("recaptcha-audio-button").click()
    print("---successfully switched to audio reCAPTCHA---")
except (RuntimeError, TypeError, NameError): # causes error if audio button not found
    print("-!-audio reCAPTCHA did not initiate...quiting-!-")
    Error_check = True
failure_check(Error_check)
chrome_driver.switch_to.default_content()
search = chrome_driver.find_elements_by_tag_name("iframe")
changeFrame(search, -1)
snooze()


"""check if suspected automated activited error occurs"""
try: # search for "try again later" element , if displayed , bot is detected 
    element_check = chrome_driver.find_element_by_xpath("/html/body/div/div/div[1]/div[1]/div").is_displayed()
    if element_check:# if this element exists ,the bot has been detected - so quit
        print("-!!!-Bot detected , try switching location on VPN or use a proxy-!!!-" \
              , "                  -!-quiting-!-", sep="\n")
        Error_check = True
except: # if the try statement continued , the bot detection element does not exist
    print("---Web driver has not been detected!---")
failure_check(Error_check)


"""Locate and interact with play and download audio reCAPTCHA initiation button"""
chrome_driver.switch_to.default_content()
search = chrome_driver.find_elements_by_tag_name("iframe")
changeFrame(search, -1)
snooze()
try:  # Find play and download button interact with .click() and save audio source to download later
    chrome_driver.find_element_by_xpath('//*[@id=":2"]').click()
    audioDownload = chrome_driver.find_element_by_id("audio-source").get_attribute("src")
    print("---Audio successfully found", "---audio source ---", audioDownload, sep="\n")
    try:  # try and extract audio from link
        audio_save(audioDownload)
        print("---Audio successfully saved to:", pwd, "...---")
    except: # else error , quit when failure_check runs
        print("-!-Audio did not download correctly-!-")
        Error_check = True
except:
    print("-!-Audio source not found-!-")
    Error_check = True
failure_check(Error_check)
snooze()


"""invoke speech recognition function to translate .WAV file to text """
text = translate()


"""Located text box and enter reCAPTCHA answer stored in text"""
snooze()
try:# search for text box and try to interact with it
    textbox = chrome_driver.find_element_by_xpath('//*[@id="audio-response"]') # find element
    textbox.send_keys(text) # pass the element the answer stored in text
    chrome_driver.find_element_by_xpath('//*[@id="recaptcha-verify-button"]').click() # find 'verify ' button and click
    print("---Text box found and answer entered!---")
except:
    print("---Failure entering answer---")
    Error_check = True
failure_check(Error_check)
chrome_driver.switch_to.default_content()
chrome_driver.find_element_by_xpath('//*[@id="recaptcha-demo-submit"]').click()
print("---Authentication successfully passed!---")
