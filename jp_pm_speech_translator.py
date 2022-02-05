##MAIN IMPORTER
import nagisa
import lxml.html as lh
import requests as rq
from selenium import webdriver
from deep_translator import GoogleTranslator
import time

path = os.environ["USERPROFILE"] + "/Desktop/jp_pm_speeches"                                                                                                             
if not os.path.exists(path):
    os.mkdir(path)
os.chdir(path)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome('chromedriver',options=chrome_options)
driver.get("https://www.benricho.org/moji_conv/13.html")


def get_wrds(txt):
    driver.find_element_by_name("before").clear()
    driver.find_element_by_name("before").click()
    driver.find_element_by_name("before").send_keys(txt)
    text = driver.find_element_by_name("after").get_attribute("value")

    sentences = text.split("\n")
    jp_tokenised_words = nagisa.extract(text, extract_postags=['英単語', '接頭辞', '形容詞', '名詞', '動詞', '助動詞', '副詞'])
    wrds = jp_tokenised_words.words
    eng = GoogleTranslator(source='auto', target='en').translate(text)
    return eng

yr_arr = []


u_main = rq.get("https://worldjpn.grips.ac.jp/documents/indices/pm/index.html")
doc_main = lh.fromstring(u_main.content)
tbl = doc_main.xpath("//p")





idx = 1
for t in tbl:
  arr = []
  yr = re.search(r"\d{4}[-]\d{4}", t.text_content())
  arr.append(yr.group())
  u = rq.get("https://worldjpn.grips.ac.jp/documents/indices/pm/" + str(idx) + ".html")
  doc = lh.fromstring(u.content)

  speeches = doc.xpath("//a/@href")



  for s in speeches:
    url_speech = "https:a//worldjpn.grips.ac.jp/documents/" + s[6:]
    u_speech = rq.get(url_speech)
    doc_speech = lh.fromstring(u_speech.content)
    p = doc_speech.xpath("//p")[1]
    while(True):
      try:
        translated = get_wrds(p)
        print(translated)
        arr.append(translated)
        break
      except:
        print("Waiting...")
        driver.quit()
        redo()
        time.sleep(20)
        continue
  yr_arr.append(arr)
  idx += 1
  if(idx == 3):
    break




for year in yr_arr:
  f = open(year + ".txt", "w")
  for speeches in year:
    f.write(speeches + "\n")
  f.close()
