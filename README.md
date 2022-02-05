# japanese-pm-speeches-project
This repository contains several programs written under the direction of JapanLab, a Japanese Studies initiative run out of the University of Texas. They are all designed to collect, organize, and preprocess a database of Japanese prime ministerial speeches. 

# pm_speech_grabber.py
This program is ordinarily distributed as an .exe, but only the raw .py file is provided here. It is a simple GUI application which functions as an "install wizard" for downloading the aforementioned speeches. It fetches them from the Tokyo University website, organizes each speech into separate folders for separate prime ministers, and packages everything into a folder placed on the user's desktop. 

# jp_pm_speech_translator.py
This program performs three principal functions. First, it grabs Japanese prime ministerial speeches from a Tokyo University database. Next  it opens a headless webdriver to convert the nineteenth-century Kanji into modern Kanji using a character conversion website found at benricho.org. Lastly, it dumps the speeches into text files organized by year.
