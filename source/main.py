# main.py
import datetime

from fastapi import FastAPI
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import json
import re
from mysql import UsingMysql
from concurrent.futures import ThreadPoolExecutor
import requests
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
import base64

url = 'http://portal.dlut.edu.cn/'
chrome_opts=webdriver.ChromeOptions()
chrome_opts.add_argument("--headless")
chrome_opts.add_argument('--disable-gpu')
chrome_opts.add_argument("window-size=1024,768")
chrome_opts.add_argument('--no-sandbox')

app = FastAPI()


def add_cookies(cookiename,browser):   # broswer 加 cookies
    with open(cookiename, "r") as fp:
            cookies = json.load(fp)
            for cookie in cookies:
                cookie.pop('domain')  # 如果报domain无效的错误
                browser.add_cookie(cookie)


@app.get('/')
def index():
    return {'message': '你已经正确创建 FastApi 服务！'}

@app.get('/query/{uid}')
def query(uid:int):
    print(uid)
    return {'success': True, 'msg': uid}

@app.get('/api/login')
def get_Cookies(id:str,password:str):
    # 导入读取到的私钥数据, 生成 私钥对象, 返回类型为: <class 'Crypto.PublicKey.RSA.RsaKey'>

    #解密
    with open('private.pem', 'rb') as f:
        key = f.read()
        rsakey = RSA.importKey(key)  # 导入读取到的私钥
        cipher = Cipher_pkcs1_v1_5.new(rsakey)  # 生成对象
        # 将密文解密成明文，返回的是bytes类型，需要自己转成str,主要是对中文的处理
        text = cipher.decrypt(base64.b64decode(password), "ERROR")
        text=text.decode(encoding='utf-8')
    print(text.replace(' ',''))
    password=text.replace(' ','')
    browser = webdriver.Chrome(chrome_options=chrome_opts)
    browser.get(url)
    print("输入账号: ")

    print("输入密码: ")
    try:
        browser.find_element_by_xpath('/html/body/form[1]/div[2]/div/div[2]/div[2]/div[1]/input[1]').send_keys(id)
        # 输入密码
        browser.find_element_by_xpath('/html/body/form[1]/div[2]/div/div[2]/div[2]/div[1]/input[2]').send_keys(password)
        # click登录
        browser.find_element_by_xpath('/html/body/form[1]/div[2]/div/div[2]/div[2]/div[1]/span/input').click()
        cookies1=browser.get_cookies()
        browser.find_element_by_xpath('/html/body/div/div[2]/div/div/div/div[2]/div[3]/a').click()
        cookies = browser.get_cookies()

    except:
        print('账号密码输入错误')
        return ''



    with open(id+"cookies.txt", "w") as fp:
        json.dump(cookies, fp)
    with open(id+"cookies1.txt", "w") as fp:
        json.dump(cookies1, fp)

    with UsingMysql(log_time=True) as um:
        searchsql1 = 'select * from user as total where id=%s'
        searchparams = [id]
        um.cursor.execute(searchsql1, searchparams)
        data = um.cursor.fetchone()
        print(data)
        if (data):
            sql = "update user set id=%s,password=%s,cookie1=%s,cookie2=%s where id=%s"
            params = (id, password, str(cookies), str(cookies1), id)
        else:
            sql = "insert into user(id, password,cookie1,cookie2) values(%s, %s,%s,%s)"
            params = (id, password, str(cookies), str(cookies1))
        um.cursor.execute(sql, params)
    return 'success'

@app.get('/api/setmail')
def set_Mail(id:str,mail:str):
    with UsingMysql(log_time=True) as um:
        sql='update user set mail=%s where id=%s'
        params=(mail,id)
        um.cursor.execute(sql, params)


@app.get('/api/grades')
def find_Grade(find_course:str,id:str):
    browser = webdriver.Chrome(chrome_options=chrome_opts)
    browser.get('http://jxgl.dlut.edu.cn/student/for-std/program-completion-preview/')

    add_cookies(cookiename=id+'cookies.txt',browser=browser)

    browser.get('http://jxgl.dlut.edu.cn/student/for-std/program-completion-preview/')
    soup=BeautifulSoup(browser.page_source,'html.parser',from_encoding="gb18030")
    try:
        # find_course=input()
        course_list=soup.find('div',{"class":"tab-content"}).find_all(text=re.compile(find_course))
        if(len(course_list))==0:
            print('没找到课程')
        grades=[]
        dict={'success':True,'grades':grades}
        grade=''
        for i in course_list:
            course=i.find_parent().find_parent().get_text("  ")
            a1=course.split('  ')[0].replace('\n','')+course.split('  ')[5].replace('\n','')+'\n'
            x = re.findall(r'[0-9]+\.', a1)
            print(x)
            for i in x:
                a1 = a1.replace(i, '')
            print(course)
            grades.append(course)
            grade=grade+a1
        return grade

    except:
        print('没找到课程,可能被限流了')

@app.get('/api/exams')
def getExam(id:str):
    browser=webdriver.Chrome(chrome_options=chrome_opts)
    exam_url = 'http://jxgl.dlut.edu.cn/student/for-std/exam-arrange'
    browser.get(exam_url)
    add_cookies(id+'cookies.txt',browser)

    browser.get(exam_url)
    exams=browser.find_elements_by_xpath('/html/body/div/div[2]/div[1]/table/tbody/tr')  # 考试列表
    time.sleep(10)
    print(exams)
    exams_list=[]  # 最终返回
    info=[]
    for i in range(1,len(exams)+1):
        exam_xpath='/html/body/div/div[2]/div[1]/table/tbody/tr[' + str(i) + ']'
        e_name=browser.find_element_by_xpath(exam_xpath+'/td[1]').text

        e_time=browser.find_element_by_xpath(exam_xpath+'/td[2]').text

        e_room=browser.find_element_by_xpath(exam_xpath+'/td[3]').text
        e_location=browser.find_element_by_xpath(exam_xpath+'/td[4]').text
        e_school=browser.find_element_by_xpath(exam_xpath+'/td[5]').text
        exam={"e_name":e_name,
              "e_time":e_time,
              "e_room":e_room,
              "e_location":e_location,
              "e_school":e_school
              }
        info.append(exam)
        print(exam)
        exams_list.append(exam)
    # 获得邮件地址
    mail=''
    with UsingMysql(log_time=True) as um:
        searchsql1 = 'select mail from user as email where id=%s'
        searchparams = [id]
        um.cursor.execute(searchsql1, searchparams)
        data = um.cursor.fetchone()
        print(data)
    mail=data['mail']
    browser.quit()
    times = []
    email=[]
    exams_list1=''
    for i in exams_list:
        e_time = i['e_time'].split(' ')[0]
        year = e_time.split(' ')[0].split('-')[0]
        month = e_time.split(' ')[0].split('-')[1]
        day = e_time.split(' ')[0].split('-')[2]
        scheduled_time = datetime.datetime(int(year), int(month), int(day) - 1, 8, 00, 00)
        times.append(scheduled_time)
        email.append(mail)
        exams_list1=exams_list1+i['e_name'] + ' ' + i['e_time'] + ' ' + i['e_room'] + ' ' + i['e_location']+'\n'

    # 多线程处理邮件
    with ThreadPoolExecutor(len(email)) as pool:
        results = pool.map(mails, times,info,email)
       # send_mail(exams_list)
    return exams_list1


def mails(scheduled_time,info,mail):
    while True:
        now = datetime.datetime.now().replace(microsecond=0)
        print(now)
        if now > scheduled_time:
            print('过期考试')

            # 由于目前没有考试，所以测试不方便，故使用过期的考试进行测试
            info = info['e_name'] + '  ' + info['e_time'] + '  ' + info['e_room'] + '  ' + info['e_location']
            print(info)
            infos = '明天你有一门考试哦\n' + str(info)
            url = 'https://api.dzzui.com/api/mail?Host=smtp.163.com&Username=a2561952525@163.com&Password=ZRCNUIVFZJIKVBLG&Port=465&SMTPSecure=ssl&addAddress=' + mail + '&title=你明天有一门考试哦&text=' + infos
            print(url)
            req = requests.get(url)
            print(req)
            break  # 不写break的话，也可以增加scheduled_time的值。如果都不写，会遇到重复运行的问题

        #前一天发送邮件提醒考试！
        if now == scheduled_time:  # 等于前一天
            print('发送邮件')
            info = info['e_name'] + '  ' + info['e_time'] + '  ' + info['e_room'] + '  ' + info['e_location']
            print(info)
            infos = '明天你有一门考试哦\n' + str(info)
            url = 'https://api.dzzui.com/api/mail?Host=smtp.163.com&Username=a2561952525@163.com&Password=ZRCNUIVFZJIKVBLG&Port=465&SMTPSecure=ssl&addAddress=' + mail + '&title=你明天有一门考试哦&text=' + infos
            print(url)
            req = requests.get(url)
            print(req)

            break



