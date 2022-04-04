# reCAPTCHA_Solver
python reCAPTCHA solver

PRE-REQUISITES:
*Python 3
*pip install selenium
*pip install ffmpy
*apt-get install ffmpeg (doesn't work with pip install)
*pip install pydub
*pip install SpeechRecognition

*Recommended to use Linux as easier to install dependencies , but tested on windows and macOS and works fine!
*Chrome installed with chrome drive that supports the chrome version , for your OS of choice - https://chromedriver.chromium.org/downloads
*update variable "path" (line 112) with the path of your own chromedriver.exe (os.path.abspath("chromedriver.exe") did not work!)
*Enter CMD line argument of position [1] for target URL , or leave blank to run on test site provided

*if you get "-!-Audio did not download correctly-!-" , ffmpeg is not installed correctly! (tricky on windows , but apt-get install ffmpeg works fine on linux!!!)

*usage : python3 reCAPTCHA.py  - runs script with default test site supplied
	 python3 reCAPTCHA.py www.siteyouwanttotest.com  - runs script on www.siteyouwanttotest.com
  
* Demo https://www.youtube.com/watch?v=PHs3j61rC-I
