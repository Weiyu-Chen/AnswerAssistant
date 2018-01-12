import urllib, urllib.request, sys, json, time, base64
from bs4 import BeautifulSoup
import pytesseract
import requests
from PIL import (Image, ImageGrab)
import re

# 二值化算法
def binarizing(img,threshold):
    pixdata = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            if pixdata[x, y] < threshold:
                pixdata[x, y] = 0
            else:
                pixdata[x, y] = 255
    return img

def main():
    while input("答题框出现后按任意键开始识别(0 退出) : ") != '0':
        start = time.time()
        #   图片截取
        #   问题
        imgQuestion = ImageGrab.grab((1420, 180, 1880, 250))
        imgQuestion.save('./imgQuestion.png')
        iQuestion = Image.open("./imgQuestion.png")
        ###   选项一
        imgAnswerOne = ImageGrab.grab((1420, 330, 1880, 370))
        imgAnswerOne = imgAnswerOne.convert('L')
        imgAnswerOne = binarizing(imgAnswerOne, 220)
        imgAnswerOne.save('./imgAnswerOne.png')
        ###   选项二
        imgAnswerTwo = ImageGrab.grab((1420, 420, 1880, 460))
        imgAnswerTwo = imgAnswerTwo.convert('L')
        imgAnswerTwo = binarizing(imgAnswerTwo, 220)
        imgAnswerTwo.save('./imgAnswerTwo.png')
        ###   选项三
        imgAnswerThree = ImageGrab.grab((1420, 500, 1880, 540))
        imgAnswerThree = imgAnswerThree.convert('L')
        imgAnswerThree = binarizing(imgAnswerThree, 220)
        imgAnswerThree.save('./imgAnswerThree.png')
        #   图片识别
        #   问题
        question = pytesseract.image_to_string(imgQuestion, lang='chi_sim')
        question = question.replace(' ','').replace('\n','')
        question = question[question.find('.') + 1:question.find('?')]
        ###   选项一
        answerOne = pytesseract.image_to_string(imgAnswerOne, lang='chi_sim')
        answerOne = answerOne.replace(' ','').replace('\n','')
        answerOne = answerOne[answerOne.find('.') + 1:answerOne.find('?')]
        ###   选项二
        answerTwo = pytesseract.image_to_string(imgAnswerTwo, lang='chi_sim')
        answerTwo = answerTwo.replace(' ','').replace('\n','')
        answerTwo = answerTwo[answerTwo.find('.') + 1:answerTwo.find('?')]
        ###   选项三
        answerThree = pytesseract.image_to_string(imgAnswerThree, lang='chi_sim')
        answerThree = answerThree.replace(' ','').replace('\n','')
        answerThree = answerThree[answerThree.find('.') + 1:answerThree.find('?')]
        print('问题:' + question)
        print('选项一:' + answerOne)
        print('选项二:' + answerTwo)
        print('选项三:' + answerThree)
        ###   搜索答案，悟空问答
        wukongR = requests.get(url='https://www.wukong.com/wenda/web/search/brow/?search_text=' + urllib.parse.quote(question) + '&count=10')
        if wukongResult["data"]["feed_question"][0]['ans_list']:
            wukongResult = wukongResult["data"]["feed_question"][0]['ans_list'][0]['abstract_text']
        else:
            wukongResult = '无答案'
        print('悟空问答：' + wukongResult)
        ###   搜索答案，百度搜索
        baiduR = requests.get('http://www.baidu.com/s?wd=' + '巴西的官方语言').text
        baiduResult = BeautifulSoup(baiduR, 'html.parser')
        baiduRegOne = re.compile("(?=" + answerOne + ")")
        baiduRegTwo = re.compile("(?=" + answerTwo + ")")
        baiduRegThree = re.compile("(?=" + answerThree + ")")
        if answerOne:
            baiduLengthOne = len(baiduRegOne.findall(str(baiduResult)))
        else:
            baiduLengthOne = '0'
        if answerTwo:
            baiduLengthTwo = len(baiduRegTwo.findall(str(baiduResult)))
        else:
            baiduLengthTwo = '0'
        if answerThree:
            baiduLengthThree = len(baiduRegThree.findall(str(baiduResult)))
        else:
            baiduLengthThree = '0'
        print("百度搜索：")
        print("选项一：" + baiduLengthOne)
        print("选项二：" + baiduLengthTwo)
        print("选项三：" + baiduLengthThree)
        ###答题结束
        end = time.time()
        print('总共用时：' + str( end - start ) + '秒')

if __name__ == '__main__':
    main()