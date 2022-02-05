##MAIN IMPORTER
import lxml.html as lh
import requests as rq
import re
import time
import os
import tkinter as tk
from tkinter import ttk
from threading import *

progress = 0
progress_total = 1


def runner():
  path = os.environ["USERPROFILE"] + "/Desktop/jp_pm_speeches"                                                                                                             #create the amendments folder
  if not os.path.exists(path):
      os.mkdir(path)
  os.chdir(path)

  u_main = rq.get("https://worldjpn.grips.ac.jp/documents/indices/pm/index.html")
  doc_main = lh.fromstring(u_main.content)



  tbl = doc_main.xpath("//p")

  #tbl.insert(0, first)
  global progress_total
  progress_total = len(tbl)

  idx = 0
  global progress

  for element in tbl:
    progress += 1
    t = element.text_content()
    html_idx = doc_main.xpath("//p//a/@href")[idx].split(".")[0]

    print(t, html_idx)

    if (t.rindex("）") + 1 != len(t)):
      continue

    u = rq.get("https://worldjpn.grips.ac.jp/documents/indices/pm/" + str(html_idx) + ".html")
    doc = lh.fromstring(u.content)
    path = os.environ["USERPROFILE"] + "/Desktop/jp_pm_speeches/" + t[1:]
    if not os.path.exists(path):
      os.mkdir(path)
    os.chdir(path)



    speeches = doc.xpath("//a/@href")
    speeches_title = doc.xpath("//a")


    indx = 0
    t_idx = 2
    for s in speeches:
      file_title = speeches_title[indx].text_content() + ".txt"
      if(os.path.exists(path + "/" + file_title)):
        f = open(speeches_title[indx].text_content() + "_" + str(t_idx) + ".txt", "w", encoding='utf-8')
        t_idx += 1
      else:
        f = open(speeches_title[indx].text_content() + ".txt", "w", encoding='utf-8')
      url_speech = "https://worldjpn.grips.ac.jp/documents/" + s[6:]
      u_speech = rq.get(url_speech)
      doc_speech = lh.fromstring(u_speech.content)
      p = doc_speech.xpath("//p")[1:]
      full = ""
      for line in p:
        full += line.text_content() + "\n"
      f.write(full)
      indx += 1

    os.chdir(os.environ["USERPROFILE"] + "/Desktop/jp_pm_speeches/")
    idx += 1




class app(tk.Tk):
  def __init__(self, *args, **kwargs):
    tk.Tk.__init__(self, *args, **kwargs)
    container = tk.Frame(self)
    container.pack(side="top", fill = "both", expand = True)

    self.p = 0

    container.grid_rowconfigure(0, weight = 1)
    container.grid_columnconfigure(0, weight = 1)

    self.frames = {}

    for f in (Start, Page1, Page2):
      frame = f(container, self)
      self.frames[f] = frame
      frame.grid(row = 0, column = 0, sticky = "nsew")

    self.show_frame(Start)

  def show_frame(self, cont):
    frame = self.frames[cont]
    frame.tkraise()

class Start(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    controller.geometry("350x100")
    button = ttk.Button(self, text="Click to start", command = lambda : self.handle_click(controller))
    #button.bind("<Button-1>", self.handle_click(controller))
    button.place(relx = 0.5, rely = 0.5, anchor = 'center')


  def handle_click(self, cntrl):
    t1 = Thread(target=runner)
    t1.start()
    cntrl.show_frame(Page1)

class Page2(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    label = ttk.Label(self, text="Download completed. You may exit.", font=4)
    label.place(relx=0.5, rely=0.5, anchor='center')

class Page1(tk.Frame):
  def __init__(self, parent, controller):
    self.c = controller
    tk.Frame.__init__(self, parent)
    controller.geometry("350x100")
    label = ttk.Label(self, text = "Downloading", font=4)
    label.place(relx = 0.5, rely = 0.5, anchor = 'center')
    t2 = Thread(target=self.prep)
    t2.start()




  def prep(self):
    self.p = 0
    while(True):
      self.p = self.update(self.p)
      time.sleep(1)

  def update(self, var):
    if(var < 4):
      var += 1
    else:
      var = 0
    txt = "Downloading"
    if(var == 1):
      txt += "."
    elif(var == 2):
      txt += ".."
    else:
      txt += "..."
    global progress
    global progress_total
    label = ttk.Label(self, text=txt, font=4)
    label.place(relx=0.5, rely=0.5, anchor='center')
    p = progress / progress_total * 100
    if(p > 99):
      self.c.show_frame(Page2)
    num = "%.2f" % p
    pcnt = ttk.Label(self, text=num + "%", font=4)
    pcnt.place(relx=0.5, rely=0.7, anchor='center')
    return var

def main():
  a = app()
  a.mainloop()


main()

