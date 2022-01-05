# i大工Lite
## 适用于DLUT学生
## 🎈本项目采用unity引擎编写前端UI，采用FastAPI库编写后端✨
主要用于安卓平台，也可用于PC

**主要代码为c#和python** 🤩

**教务处查成绩** ~~十 分 稳 定~~ **(不是)**

**因此获取教务处api，精简前端，为查成绩提供极简通道**

## 🎈项目结构
### 📲[戳我下载👉安卓包下载 v0.1.0👈戳我下载](https://github.com/iUshio/DLUT-OPENSOURCE/releases/tag/v0.1.0)
### opensource文件为unity源文件
### source为服务器后端文件，需自主配置参数

## 🎈功能如下
### 1.成绩查询📑✅
支持模糊搜索，对指定名字的课程成绩进行查询
### 2.考试查询✏✅
快速查询本学期的考试安排，显示详细的时间和地点
### 3.邮件提醒📩✅
支持注册用户对应邮件，在考试前会进行邮件提醒

## 🎈本项目也公开查询成绩接口：
**授权接口** http://116.62.15.29:8000/api/login
**参数**
***id*** 学号
***password*** 教务密码，需使用RSA加密，密钥见文件

**查询成绩接口** http://116.62.15.29:8000/api/exams
**参数**
***id*** 学号
（仅已授权的用户可用）

**考试提醒服务注册接口** http://116.62.15.29:8000/api/email
**参数**
***id*** 学号
***mail*** 邮箱
（仅已授权的用户可用）

## 🎈完成人员
fionajoyo ***~~无 双 剑 击~~ 🤺 菲奥娜😍***

Anchor 

iUshio
