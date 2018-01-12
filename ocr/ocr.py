# 二值化算法
# def binarizing(img,threshold):
#     pixdata = img.load()
#     w, h = img.size
#     for y in range(h):
#         for x in range(w):
#             if pixdata[x, y] < threshold:
#                 pixdata[x, y] = 0
#             else:
#                 pixdata[x, y] = 255
#     return img
# #   图片截取
# #   问题
# imgQuestion = ImageGrab.grab((1420, 180, 1880, 250))
# imgQuestion.save('./imgQuestion.png')
# iQuestion = open("./imgQuestion.png","r")
# ###   选项一
# imgAnswerOne = ImageGrab.grab((1420, 330, 1880, 370))
# imgAnswerOne = imgAnswerOne.convert('L')
# imgAnswerOne = binarizing(imgAnswerOne, 220)
# imgAnswerOne.save('./imgAnswerOne.png')
# ###   选项二
# imgAnswerTwo = ImageGrab.grab((1420, 420, 1880, 460))
# imgAnswerTwo = imgAnswerTwo.convert('L')
# imgAnswerTwo = binarizing(imgAnswerTwo, 220)
# imgAnswerTwo.save('./imgAnswerTwo.png')
# ###   选项三
# imgAnswerThree = ImageGrab.grab((1420, 500, 1880, 540))
# imgAnswerThree = imgAnswerThree.convert('L')
# imgAnswerThree = binarizing(imgAnswerThree, 220)
# imgAnswerThree.save('./imgAnswerThree.png')
# #   图片识别
# #   问题
# question = pytesseract.image_to_string(imgQuestion, lang='chi_sim')
# question = question.replace(' ','').replace('\n','')
# question = question[question.find('.') + 1:question.find('?')]
# ###   选项一
# answerOne = pytesseract.image_to_string(imgAnswerOne, lang='chi_sim')
# answerOne = answerOne.replace(' ','').replace('\n','')
# answerOne = answerOne[answerOne.find('.') + 1:answerOne.find('?')]
# ###   选项二
# answerTwo = pytesseract.image_to_string(imgAnswerTwo, lang='chi_sim')
# answerTwo = answerTwo.replace(' ','').replace('\n','')
# answerTwo = answerTwo[answerTwo.find('.') + 1:answerTwo.find('?')]
# ###   选项三
# answerThree = pytesseract.image_to_string(imgAnswerThree, lang='chi_sim')
# answerThree = answerThree.replace(' ','').replace('\n','')
# answerThree = answerThree[answerThree.find('.') + 1:answerThree.find('?')]
# print('问题:' + question)
# print('选项一:' + answerOne)
# print('选项二:' + answerTwo)
# print('选项三:' + answerThree)