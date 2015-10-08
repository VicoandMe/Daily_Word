#! /usr/bin

from selenium.webdriver.remote.webdriver import WebDriver
import os, sys
import time
import urllib2
import cookielib
import string
import re

def DownLoad_jpg(url, name):
  try:
    cj = cookielib.CookieJar()
    cookie_support = urllib2.HTTPCookieProcessor(cj)
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)
    h = {
      'Referer' : url,
      'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0'
    }
    r = urllib2.urlopen(urllib2.Request(url,headers = h))
    data = r.read()
    with open("./daily-word/picture/" + name + ".jpg", "w+") as fp:
      fp.write(data)
  except:
     print "picture " + name + " download failed"

def DownLoad_mp3(url, name):
  try:
    cj = cookielib.CookieJar()
    cookie_support = urllib2.HTTPCookieProcessor(cj)
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)
    h = {
      'Referer' : url,
      'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0'
    }
    r = urllib2.urlopen(urllib2.Request(url,headers = h))
    data = r.read()
    with open("./daily-word/mp3/" + name + ".mp3", "w+") as fp:
      fp.write(data)
  except:
    print "mp3 " + name + " download failed"

def WriteWordList(word):
  with open("./daily-word/word_list.txt", "wb+") as fp1:
    sign = 0
    with open("./daily-word/word_list.txt", "r+") as fp2:
      for line in fp2.readline():
	line1 = line.split(' ')
        if line1[0] == word:
	  sign = 1
    if sign == 0:
      word = word.encode('utf-8')
      fp1.write(word)

def GetDailyWord():
  capabilities = {'loggingPrefs': {},'xwalkOptions': {'binary': '/usr/bin/xwalk','debugPort': '12450'}}
  driver = WebDriver('http://127.0.0.1:9515',desired_capabilities = capabilities,keep_alive=True)

  driver.get("http://cn.bing.com/dict/")

  word = driver.find_element_by_class_name('client_daily_word_en')
  word_text = word.text

  pronounce = driver.find_elements_by_class_name('client_daily_word_pn_pn')
  pronounce_text = []
  pronounce_text.append(pronounce[0].text)
  pronounce_text.append(pronounce[1].text)

  WriteWordList(word_text + " " + pronounce[0].text + " " + pronounce[1].text)
  audio = driver.find_elements_by_class_name('client_aud_o')
  audio1_onmouseover = audio[0].get_attribute('onmouseover')
  audio1_onclick = audio[0].get_attribute('onclick')
  DownLoad_mp3(audio[0].get_attribute("onclick").split('\'')[1], word_text + "_US")

  audio2_onmouseover = audio[1].get_attribute('onmouseover')
  audio2_onclick = audio[1].get_attribute('onclick')
  DownLoad_mp3(audio[1].get_attribute("onclick").split('\'')[1], word_text + "_UK")
  
  translate = driver.find_element_by_class_name('client_daily_word_zh')
  translate_text = translate.text

  picture1_src = driver.find_element_by_id("emb1").get_attribute('src')
  picture2_src = driver.find_element_by_id("emb2").get_attribute('src')
  picture3_src = driver.find_element_by_id("emb3").get_attribute('src')
  DownLoad_jpg(picture1_src, word_text + '1')
  DownLoad_jpg(picture2_src, word_text + '2')
  DownLoad_jpg(picture3_src, word_text + '3')

  html_src = "<head>\
<meta content=\"text/html; charset=utf-8\" http-equiv=\"content-type\" />\
<title>Daily word</title>\
<link rel=\"stylesheet\" type=\"text/css\" href=\"daily-word/daily.css\"></link>\
</head>\
<body>\
<div class=\"client_daily_word_content\">\
<div class=\"client_daily_words_bar\">\
  <div class=\"client_daily_word_en\">\
    <a id=\"word\" href=\"http://bing.com.cn/dict/search?q=" + word_text + "\"h=\"ID=Dictionary,5014.1\">" + word_text + "</a>\
  </div>\
  <div class=\"client_daily_word_pn\">\
    <div class=\"client_daily_word_pn_pn\" lang=\"en\">" + pronounce_text[0] + "</div>\
    <div class=\"client_daily_word_pn_audio\">\
      <div class=\"client_icon_container\">\
	<audio id=\"us_pronun\" src=./daily-word/mp3/" + word_text + "_US.mp3"+" controls=\"contrils\"></audio>\
	</a>\
      </div>\
    </div>\
  </div>\
  <div class=\"client_daily_word_pn\">\
    <div class=\"client_daily_word_pn_pn\" lang=\"en\">" + pronounce_text[1]+ "</div>\
    <div class=\"client_daily_word_pn_audio\">\
      <div class=\"client_icon_container\">\
	<audio id=\"us_pronun\" src=./daily-word/mp3/" + word_text + "_UK.mp3"+" controls=\"contrils\"></audio>\
	</a>\
      </div>\
    </div>\
  </div>\
  <div class=\"client_daily_word_zh\">" + translate_text + "</div>\
</div>\
<div class=\"client_daily_pic_bar\">\
  <a href=\"http://bing.com.cn/dict/search?q=" + word_text + "\"class=\"client_daily_pic_item\" target=\"_blank\" h=\"ID=Dictionary,5017.1\">\
    <img class=\"rms_img\" height=\"80\" id=\"emb1\" src=\"" + "./daily-word/picture/" + word_text + '1' + ".jpg" + "\" width = \"80\" />\
  </a>\
  <a href=\"http://bing.com.cn/dict/search?q=" + word_text + "\"class=\"client_daily_pic_item\" target=\"_blank\" h=\"ID=Dictionary,5017.1\">\
    <img class=\"rms_img\" height=\"80\" id=\"emb2\" src=\"" + "./daily-word/picture/" + word_text + '2' + ".jpg" + "\" width = \"80\" />\
  </a>\
  <a href=\"http://bing.com.cn/dict/search?q=" + word_text + "\"class=\"client_daily_pic_item\" target=\"_blank\" h=\"ID=Dictionary,5017.1\">\
    <img class=\"rms_img\" height=\"80\" id=\"emb3\" src=\"" + "./daily-word/picture/" + word_text + '3' + ".jpg" + "\" width = \"80\" />\
  </a>\
</div>\
</div>\
</div>\
<script src=\"daily-word/daily.js\"></script>\
</body>\
<html>\
"
  with open(word_text + ".html", "w+") as fp:
    html_src = html_src.encode('utf-8')
    fp.write(html_src)

if __name__ == '__main__':
  GetDailyWord()
