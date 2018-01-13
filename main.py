import urllib, urllib.request, sys, json, time, base64, re
from bs4 import BeautifulSoup
import pytesseract
import requests
from PIL import (Image, ImageGrab)

def main():
    while input("答题框出现后按Enter键开始识别(0 退出) : ") != '0':
        start = time.time()
        #   图片截取
        imgQuestion = ImageGrab.grab((1400, 180, 1880, 570))
        imgQuestion.save('./imgQuestion.png')
        imgQuestion = open('./imgQuestion.png','rb')
        #   图片转换成BS64
        imgData = imgQuestion.read()
        imgData = base64.b64encode(imgData)
        #  请求头设置
        headers = {
            "Accept":"*/*",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.9",
            "Connection":"keep-alive",
            "Content-Length":"136759",
            "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie":"BIDUPSID=710816008E09C3C82D05F3988AE2110D; PSTM=1508120444; __cfduid=d34ac0c26a112cae942bd33658d0c6b951508832212; BAIDUID=2AF897AE37304AFB84FC151F591E6305:FG=1; MCITY=-2911%3A257%3A; H_WISE_SIDS=114749_120991_116792_114746_121431_121253_100099_120762_120126_121146_120010_118881_118873_118840_118836_118793_107312_121255_121535_121215_117586_117330_117244_117435_120597_121563_121044_120944_121362_121272_117558_114820_121309_120851_121464_120035_116408_121359_121134_110085_116860_119783_120813_100460; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; Hm_lvt_fdad4351b2e90e0f489d7fbfc47c8acf=1515722101; H_PS_PSSID=1436_24886_21092_22074; BDUSS=ldUWklBNUZ5LTBlZVlXbm80NHFhVmYwME5iZn4yYnBCeVVtUkJzRnNJQnN4MzlhQUFBQUFBJCQAAAAAAAAAAAEAAADnIsAUz8S5rNPTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGw6WFpsOlhaW; BDSFRCVID=hW-sJeC62xS7nyRASaVFbapLY22_jarTH6aoaN3MOEl5_f9Hu4snEG0Pqx8g0Ku-S28FogKK3gOTH4jP; H_BDCLCKID_SF=tR-JoK8ytCt3fP36q4Jq5bLtqxby26n8KeJeaJ5nJDon8lTp55oNeh0T5f5KbU7ktHOgahr4QpP-HJ7w3MODy5-_XUcftfJd26v3Kl0MLpbtbb0xynoDhPvQKxnMBMPe52OnaIb_LIFabK-RDTAaD5PW5ptXK-QJbCKX3b7Ef-3pV-O_bf--Dxt75aj25M_OLNTz3JjMBUTHHx5RbPTxy5K_hUKeWf39aDDOKpb8KqrxHqQHQT3myRvbbN3i-4jy2nRHWb3cWKOJ8UbSj-6me6jLeHAJJT-jf5vfL5rtaP5qqPbp-PR5q4tHeUR93RJZ5mAqot5EJ4OaMljv-fkb-4_QXbuHb53OWK7naIQqab5ceJrs5tOOM4CiK-oT0nJ43bRTKnLy5KJvfJ_xjMn-hP-UyNbMWh37JIQTVDL5fILKMD8r-PvE-PnH-fv0hRQXHD7yWCvOJKn5OR5JLn7nDn-Y3fbC25vBJKF8aqRmLUAVORbFQMrIQTJyyGCHJ6FOJn4foIv5b-0_HRRGbJbM-ttfKgT22jPLMmJeaJ5nJDoSORF4jqONhpt4Lf5KbU7ktjAJXpvJQpP-HJ7GehQvy--9hPbwbMjD5mOGKl0MLPjlbb0xynoDD50g5xnMBMPe52OnaIb_LIFahIPlDjK5ePtjhpobetjK2CntsJOOaCvRffJRy4oTj6Db0NJXhljCLK6aBJoq-pRZhCo3M4QK3MvB-fnKWjJuB2TQ_x7DflnhM-OkQft20b_beMtjBbLLLbuOKJ7jWhk5ep72y5O805TLDNADJ6DefK7QW-5eHJoHjJbGq4bohjPJ3gceBtQmJJrObK38MxoNVnjKQ45HKMA4DG5datoHQg-q3R7qBDOY8p51jqntefk0jhbX0x-jLT6OVn0MW-KVVI_9Q4nJyUnybPnnBT3BLnQ2QJ8BJC0aMKoP; PSINO=6; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; seccode=480dc44b8347347eb8fae9af2c0efdbc; Hm_lpvt_fdad4351b2e90e0f489d7fbfc47c8acf=1515734923",
            "Host":"ai.baidu.com",
            "Origin":"http://ai.baidu.com",
            "Referer":"http://ai.baidu.com/tech/ocr/general",
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            "X-Requested-With":"XMLHttpRequest"
        }
        #   请求百度接口
        baiduRd = requests.post('http://ai.baidu.com/aidemo', headers=headers, data={"type":"commontext", "image": "data:image/png;base64," + str(imgData.decode()), "image_url": ""})
        baiduResultJson = baiduRd.json()
        baiduJsonLen = len(baiduResultJson['data']['words_result'])
        words_result = baiduResultJson['data']['words_result']
        ###   问题组合
        question = ''
        count = 0
        while (baiduJsonLen - 3 > 0 and count < baiduJsonLen - 3):
            question += words_result[count]["words"]
            count = count + 1
        ##  搜索答案，百度搜索
        baiduR = requests.get('http://www.baidu.com/s?wd=' + question).text
        baiduResult = BeautifulSoup(baiduR, 'html.parser')
        baiduRegOne = re.compile("(?=" + words_result[-3]["words"] + ")")
        baiduRegTwo = re.compile("(?=" + words_result[-2]["words"] + ")")
        baiduRegThree = re.compile("(?=" + words_result[-1]["words"] + ")")
        if words_result[-3]["words"]:
            baiduLengthOne = len(baiduRegOne.findall(str(baiduResult)))
        else:
            baiduLengthOne = '0'
        if words_result[-2]["words"]:
            baiduLengthTwo = len(baiduRegTwo.findall(str(baiduResult)))
        else:
            baiduLengthTwo = '0'
        if words_result[-1]["words"]:
            baiduLengthThree = len(baiduRegThree.findall(str(baiduResult)))
        else:
            baiduLengthThree = '0'
        print('问题:' + question)
        print('选项一:' + words_result[-3]["words"])
        print('选项二:' + words_result[-2]["words"])
        print('选项三:' + words_result[-1]["words"])
        print("百度搜索：")
        if baiduLengthOne > baiduLengthTwo and baiduLengthOne > baiduLengthThree:
            print("选项一：" + '\33[91m' + words_result[-3]["words"] + '====指数：' + str(baiduLengthOne) + '\033[0m')
        else:
            print("选项一：" + words_result[-3]["words"] + '====指数：' + str(baiduLengthOne))
        if baiduLengthTwo > baiduLengthOne and baiduLengthTwo > baiduLengthThree:
            print("选项二：" + '\33[91m' + words_result[-2]["words"] + '====指数：' + str(baiduLengthTwo) + '\033[0m')
        else:
            print("选项二：" + words_result[-2]["words"] + '====指数：' + str(baiduLengthTwo))
        if baiduLengthThree > baiduLengthTwo and baiduLengthThree > baiduLengthOne:
            print("选项三：" + '\33[91m' + words_result[-1]["words"] + '====指数：' + str(baiduLengthThree) + '\033[0m')
        else:
            print("选项三：" + words_result[-1]["words"] + '====指数：' + str(baiduLengthThree))
        
        ###答题结束
        end = time.time()
        print('总共用时：' + str( end - start ) + '秒')

if __name__ == '__main__':
    main()