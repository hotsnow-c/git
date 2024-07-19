# This is a sample Python script.
import json
import time

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import random
import string
from getMail import get_verification_code,get_recaptcha_token,getOPT,random_account_password
from lumiChrome import LumiClient,lumi_info

chrome =None
#获取邮箱
all_email = None
with open('hotmail.txt','r') as f:
    all_email = f.readlines()
    all_email = [i.replace('\n','') for i in all_email]
#检测是否在acc_pwd.txt中
susccess_info = None
with open('acc_pwd.txt','r',encoding='utf8') as f:
    susccess_info = f.read()

new_all_email = []
for email in all_email:
    e_acc = email.split('----')[0]
    if e_acc not in susccess_info:
        new_all_email.append(email)


email_account = new_all_email[0].split('----')[0]
email_password =new_all_email[0].split('----')[1]
#删除已经使用的邮箱
new_all_email.pop(0)
print(email_account,email_password)
proxy_host = 'proxy.froxy.com'
proxy_port = 9010
proxyUserName = 'Dwt9ZkzgAoVF51pT'
proxyPassword = 'wifi;us;;;'
acc, pwd = random_account_password()

acc_list = 'jojo6574,a0912426336,2MAWYO3BT6U2NWPZ'.split(',')
if len(acc_list) > 2:
    acc = acc_list[0]
    pwd = acc_list[1]
    opt = acc_list[2]
    print('测试账号：', acc, pwd, opt)

def openLuMi():
    #brwoser_id = "8ba009cbbedf192f34817574c81c9454"
    lumi_info['proxyInfo']['port'] = proxy_port
    lumi_info['proxyInfo']['proxyUserName'] = proxyUserName
    lumi_info['proxyInfo']['proxyPassword'] = proxyPassword
    print(lumi_info['proxyInfo']['port'])
    print(lumi_info['proxyInfo']['proxyUserName'])
    print(lumi_info['proxyInfo']['proxyPassword'])
    # 初始化客户端
    client = LumiClient(port=50000,token="258a4107301a12383aabed96ced22b66")
    print(client)
    lumi_info['windowName'] = acc
    brwoser_id = client.browser_create(lumi_info).get("data").get("dirId")
    print(brwoser_id)

    # 打开浏览器
    rsp = client.browser_open(brwoser_id)
    if rsp.get("code") != 0:
        print("浏览器打开失败:",rsp)
        exit(0)

    # 获取selenium的连接信息
    debuggerAddress = rsp.get("data").get("http")
    driverPath = rsp.get("data").get("driver")
    print(f"浏览器打开成功,debuggerAddress:{debuggerAddress},driverPath:{driverPath}")

    # selenium 连接代码
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("debuggerAddress", debuggerAddress)

    chrome_service = Service(driverPath)
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return driver


chrome = openLuMi()

def happ_login(acc,pwd,opt,proxy=None,addProxy=False):

    #chrome.get('https://lostark.mangot5.com/game/lostark/preSignup/artist/index')
    chrome.get('https://www.mangot5.com/Index/Billing/couponList')
    chrome.execute_script(f'document.querySelector("#oldPassword").value = "{acc}"')
    chrome.execute_script(f'document.querySelector("#newPassword").value = "{pwd}"')

    #re_token = ReCaptchaV2_create('https://www.mangot5.com/Index/Member/Login',"6LcZ2f0SAAAAAD0eUdEP0YdkRZLYrdf8rg2qjsdj")
    recaptcha_info1 = chrome.execute_script(
        'function findRecaptchaClients() { if (typeof (___grecaptcha_cfg) !== "undefined") { return Object.entries(___grecaptcha_cfg.clients).map(([cid, client]) => { const data = { id: cid, version: cid >= 10000 ? "V3" : "V2" }; const objects = Object.entries(client).filter(([_, value]) => value && typeof value === "object"); objects.forEach(([toplevelKey, toplevel]) => { const found = Object.entries(toplevel).find(([_, value]) => ( value && typeof value === "object" && "sitekey" in value && "size" in value )); if (typeof toplevel === "object" && toplevel instanceof HTMLElement && toplevel["tagName"] === "DIV"){ data.pageurl = toplevel.baseURI; } if (found) { const [sublevelKey, sublevel] = found; data.sitekey = sublevel.sitekey; const callbackKey = data.version === "V2" ? "callback" : "promise-callback"; const callback = sublevel[callbackKey]; if (!callback) { data.callback = null; data.function = null; } else { data.function = callback; const keys = [cid, toplevelKey, sublevelKey, callbackKey].map((key) => `["${key}"]`).join(""); data.callback = `___grecaptcha_cfg.clients${keys}`; } } }); return data; }); } return []; } return findRecaptchaClients()')
    print(type(recaptcha_info1))
    print(recaptcha_info1)
    recaptcha_info = recaptcha_info1[0]
    if recaptcha_info.get('sitekey') != None:
        print(recaptcha_info['pageurl'], recaptcha_info['sitekey'])
        re_token = get_recaptcha_token(recaptcha_info['pageurl'].replace('#step-3', ''), recaptcha_info['sitekey'],'123')
        chrome.execute_script(re_token)
        chrome.execute_script('document.querySelector("#submitBtn").click()')
        time.sleep(10)

    try:
        print('检测opt')
        if '驗證碼輸入區' == chrome.execute_script('return document.querySelector("#validCode").placeholder'):
            print('输入otp')
            otp_code = getOPT(opt)
            print(otp_code)
            chrome.execute_script(f'document.querySelector("#validCode").value ="{otp_code}"')
            chrome.execute_script('document.querySelector("#optForm > div:nth-child(3) > div > button").click()')
            print('otp输入成功')
            time.sleep(10)

        else:
            print('otp不存在')
    except:
        pass

    # happ_login(acc, pwd)
    # chrome.get('https://www.mangot5.com/Index/Security/OTP')
    # while True:
    #     try:
    #         print('判断所在页')
    #         # 找到所有的li标签
    #         # 使用 XPath 路径查找所有 li 标签
    #         li_elements = chrome.find_elements(By.XPATH, "//ul[@class='nav nav-tabs step-anchor']/li")
    #
    #         # 遍历所有 li 标签并判断 class 是否包含 "active"
    #         for i, li in enumerate(li_elements):
    #             class_name = li.get_attribute("class")
    #             if "active" in class_name:
    #                 index = i  # 索引从1开始
    #
    #                 print(li.text)
    #                 break
    #         # 打印结果
    #         if index != -1:
    #             print(f"The 'active' class is found in the {index} li element.")
    #         else:
    #             print("No 'li' element with 'active' class found.")
    #     except:
    #         print('判断错误!')
    #         pass
    #
    #     if index == 0:
    #         print('在您的行動裝置上，下載並安裝「Google Authenticator」APP。')
    #         chrome.execute_script('document.querySelector("#nextOTPbtn").click()')
    #     if index == 1:
    #         print('get otp')
    #         otp = chrome.execute_script(
    #             'return document.querySelector("#step-2 > div.secKey.alert.alert-info > span").innerHTML')
    #         with open('acc_pwd.txt', 'a') as f:
    #             f.write(f'{acc}----{pwd}----{otp}----{email_account}----{email_password}----{proxy_port}\n')
    #         chrome.execute_script('document.querySelector("#nextOTPbtn").click()')
    #     if index == 2:
    #         print('输入otp')
    #         otp_code = getOPT(otp)
    #         print(otp_code)
    #         chrome.execute_script(f'document.querySelector("#validCode").value ="{otp_code}"')
    #         chrome.execute_script('document.querySelector("#nextOTPbtn").click()')
    #
    #     if index == 3:
    #         print('otp绑定完成!')
    #         break
    #     time.sleep(3)

def 注册():
    print('注册')
    # chrome.get('https://lostark.mangot5.com/game/lostark/preSignup/artist/index')
    chrome.get('https://www.mangot5.com/Index/Member/Register')

    input_action = False
    while True:
        time.sleep(2)
        # 初始化索引
        index = -1

        try:
            if 'https://lostark.mangot5.com/game/lostark/preSignup/artist/index' in chrome.current_url:
                chrome.execute_script('document.querySelector("#ARKcreg240620").click()')
                print('点击加入会员')
        except:
            pass

        try:
            print('判断所在页')
            # 找到所有的li标签
            # 使用 XPath 路径查找所有 li 标签
            li_elements = chrome.find_elements(By.XPATH, "//ul[@class='nav nav-tabs step-anchor']/li")

            # 遍历所有 li 标签并判断 class 是否包含 "active"
            for i, li in enumerate(li_elements):
                class_name = li.get_attribute("class")
                if "active" in class_name:
                    index = i  # 索引从1开始

                    print(li.text)
                    break
            # 打印结果
            if index != -1:
                print(f"The 'active' class is found in the {index} li element.")
            else:
                print("No 'li' element with 'active' class found.")

        except:
            pass

        try:
            if index == 0:
                mail_type = chrome.execute_script('return document.querySelector("#userEmail2Select").selectedIndex')
                print('设置邮箱页')
                print('mail_type: ', mail_type)
                if mail_type == 0:
                    print('邮箱类型: ' + 'gamil')
                elif mail_type == 1:
                    print('邮箱类型: ' + 'outlook')
                elif mail_type == 2:
                    print('邮箱类型: ' + 'hotmail')
                else:
                    print('邮箱类型：' + '未知邮箱类型')
                if mail_type != 2:
                    chrome.execute_script('document.querySelector("#userEmail2Select").selectedIndex = 2')
                    time.sleep(1)
                    mail = email_account.replace('@hotmail.com', '')
                    chrome.execute_script(f'document.querySelector("#userEmail1").value = "{mail}"')
                    time.sleep(5)
                    chrome.execute_script('document.querySelector("#nextOTPbtn").click()')
                    time.sleep(8)
        except:
            pass

        try:
            if index == 1:
                code = chrome.execute_script('return document.querySelector("#verificationCode").value')
                print('code: ', code)
                if code == "":
                    print('获取验证码！')
                    code = get_verification_code(email_account, email_password)
                    if code:
                        chrome.execute_script(f'document.querySelector("#verificationCode").value = "{code}"')
                        time.sleep(1)
                        chrome.execute_script('document.querySelector("#nextOTPbtn").click()')
                    else:
                        print('获取验证码失败！')
                else:
                    print('验证码存在！')
        except:
            pass

        try:
            if input_action == True:
                print('输入过一次信息：', email_account, email_password, acc, pwd)
                print('请输入谷歌验证！')
            if index == 2 and input_action == False:
                button = chrome.execute_script('return document.querySelector("#nextOTPbtn").innerText')
                print('button: ', button)
                if button == "輸入完成":
                    input_action = True

                    print(acc, pwd)
                    chrome.execute_script(f'document.querySelector("#userID").value = "{acc}"')
                    chrome.execute_script(f'document.querySelector("#password").value = "{pwd}"')
                    chrome.execute_script(f'document.querySelector("#password2").value = "{pwd}"')
                    chrome.execute_script(
                        'document.querySelector("#Register > div:nth-child(9)").querySelector("#checkbox").checked = true')
                    chrome.execute_script(
                        'document.querySelector("#Register > div:nth-child(10)").querySelector("#checkbox").checked = true')
                    recaptcha_info1 = chrome.execute_script(
                        'function findRecaptchaClients() { if (typeof (___grecaptcha_cfg) !== "undefined") { return Object.entries(___grecaptcha_cfg.clients).map(([cid, client]) => { const data = { id: cid, version: cid >= 10000 ? "V3" : "V2" }; const objects = Object.entries(client).filter(([_, value]) => value && typeof value === "object"); objects.forEach(([toplevelKey, toplevel]) => { const found = Object.entries(toplevel).find(([_, value]) => ( value && typeof value === "object" && "sitekey" in value && "size" in value )); if (typeof toplevel === "object" && toplevel instanceof HTMLElement && toplevel["tagName"] === "DIV"){ data.pageurl = toplevel.baseURI; } if (found) { const [sublevelKey, sublevel] = found; data.sitekey = sublevel.sitekey; const callbackKey = data.version === "V2" ? "callback" : "promise-callback"; const callback = sublevel[callbackKey]; if (!callback) { data.callback = null; data.function = null; } else { data.function = callback; const keys = [cid, toplevelKey, sublevelKey, callbackKey].map((key) => `["${key}"]`).join(""); data.callback = `___grecaptcha_cfg.clients${keys}`; } } }); return data; }); } return []; } return findRecaptchaClients()')
                    print(type(recaptcha_info1))
                    print(recaptcha_info1)
                    recaptcha_info = recaptcha_info1[0]
                    if recaptcha_info.get('sitekey') != None:
                        print(recaptcha_info['pageurl'], recaptcha_info['sitekey'])
                        re_token = get_recaptcha_token(recaptcha_info['pageurl'].replace('#step-3', ''),
                                                       recaptcha_info['sitekey'], '123')
                        chrome.execute_script(re_token)
                        time.sleep(5)


        except Exception as e:
            print(e)

        try:
            if index == 3:
                print('请输入谷歌验证3！')
                recaptcha_info1 = chrome.execute_script(
                    'function findRecaptchaClients() { if (typeof (___grecaptcha_cfg) !== "undefined") { return Object.entries(___grecaptcha_cfg.clients).map(([cid, client]) => { const data = { id: cid, version: cid >= 10000 ? "V3" : "V2" }; const objects = Object.entries(client).filter(([_, value]) => value && typeof value === "object"); objects.forEach(([toplevelKey, toplevel]) => { const found = Object.entries(toplevel).find(([_, value]) => ( value && typeof value === "object" && "sitekey" in value && "size" in value )); if (typeof toplevel === "object" && toplevel instanceof HTMLElement && toplevel["tagName"] === "DIV"){ data.pageurl = toplevel.baseURI; } if (found) { const [sublevelKey, sublevel] = found; data.sitekey = sublevel.sitekey; const callbackKey = data.version === "V2" ? "callback" : "promise-callback"; const callback = sublevel[callbackKey]; if (!callback) { data.callback = null; data.function = null; } else { data.function = callback; const keys = [cid, toplevelKey, sublevelKey, callbackKey].map((key) => `["${key}"]`).join(""); data.callback = `___grecaptcha_cfg.clients${keys}`; } } }); return data; }); } return []; } return findRecaptchaClients()')
                print(type(recaptcha_info1))
                print(recaptcha_info1)
                recaptcha_info = recaptcha_info1[0]
                if recaptcha_info.get('sitekey') != None:
                    print(recaptcha_info['pageurl'], recaptcha_info['sitekey'])
                    re_token = get_recaptcha_token(recaptcha_info['pageurl'].replace('#step-3', ''),
                                                   recaptcha_info['sitekey'], '123')
                    chrome.execute_script(re_token.replace('g-recaptcha-response', 'g-recaptcha-response-1'))
                    chrome.execute_script('document.querySelector("#submitForm").click()')
                    time.sleep(5)

        except:
            pass

        try:
            if index == 4:
                print('注册完成！')
                # 结果写入文件
                with open('acc_pwd.txt', 'a') as f:
                    f.write(f'{acc}----{pwd}---- ----{email_account}----{email_password}----{proxy_port}\n')
                with open('hotmail.txt', 'w', encoding='utf8') as f:
                    txt = '\n'.join(new_all_email)
                    f.write(txt)
                break
                # 登录地址 https://www.mangot5.com/Index/Member/Login?ref=/Index
                # 设定opt  https://www.mangot5.com/Index/Security/OTP
                # 手机设定  https://www.mangot5.com/Index/Member/VerifySms
        except:
            pass




def openChrome(proxy=None,addProxy=False):



    print('123')
    #chrome.get('https://lostark.mangot5.com/game/lostark/preSignup/artist/index')
    chrome.get('https://www.mangot5.com/Index/Member/Register')

    input_action = False
    while True:
        time.sleep(2)
        # 初始化索引
        index = -1

        try:
            if 'https://lostark.mangot5.com/game/lostark/preSignup/artist/index' in chrome.current_url:
                chrome.execute_script('document.querySelector("#ARKcreg240620").click()')
                print('点击加入会员')
        except:
            pass

        try:
            print('判断所在页')
            # 找到所有的li标签
            # 使用 XPath 路径查找所有 li 标签
            li_elements = chrome.find_elements(By.XPATH, "//ul[@class='nav nav-tabs step-anchor']/li")

            # 遍历所有 li 标签并判断 class 是否包含 "active"
            for i, li in enumerate(li_elements):
                class_name = li.get_attribute("class")
                if "active" in class_name:
                    index = i   # 索引从1开始

                    print(li.text)
                    break
            # 打印结果
            if index != -1:
                print(f"The 'active' class is found in the {index} li element.")
            else:
                print("No 'li' element with 'active' class found.")

        except:
            pass

        try:
            if index == 0:
                mail_type = chrome.execute_script('return document.querySelector("#userEmail2Select").selectedIndex')
                print('设置邮箱页')
                print('mail_type: ' ,mail_type)
                if mail_type == 0:
                    print('邮箱类型: ' + 'gamil')
                elif mail_type == 1:
                    print('邮箱类型: ' + 'outlook')
                elif mail_type == 2:
                    print('邮箱类型: ' + 'hotmail')
                else:
                    print('邮箱类型：' + '未知邮箱类型')
                if mail_type != 2:
                    chrome.execute_script('document.querySelector("#userEmail2Select").selectedIndex = 2')
                    time.sleep(1)
                    mail = email_account.replace('@hotmail.com','')
                    chrome.execute_script(f'document.querySelector("#userEmail1").value = "{mail}"')
                    time.sleep(5)
                    chrome.execute_script('document.querySelector("#nextOTPbtn").click()')
                    time.sleep(8)
        except:
            pass

        try:
            if index == 1:
                code = chrome.execute_script('return document.querySelector("#verificationCode").value')
                print('code: ',code)
                if code == "":
                    print('获取验证码！')
                    code = get_verification_code(email_account,email_password)
                    if code:
                        chrome.execute_script(f'document.querySelector("#verificationCode").value = "{code}"')
                        time.sleep(1)
                        chrome.execute_script('document.querySelector("#nextOTPbtn").click()')
                    else:
                        print('获取验证码失败！')
                else:
                    print('验证码存在！')
        except:
            pass

        try:
            if input_action == True:
                print('输入过一次信息：',email_account,email_password,acc,pwd)
                print('请输入谷歌验证！')
            if index == 2 and input_action == False:
                button = chrome.execute_script('return document.querySelector("#nextOTPbtn").innerText')
                print('button: ',button)
                if button == "輸入完成":
                    input_action = True

                    print(acc,pwd)
                    chrome.execute_script(f'document.querySelector("#userID").value = "{acc}"')
                    chrome.execute_script(f'document.querySelector("#password").value = "{pwd}"')
                    chrome.execute_script(f'document.querySelector("#password2").value = "{pwd}"')
                    chrome.execute_script('document.querySelector("#Register > div:nth-child(9)").querySelector("#checkbox").checked = true')
                    chrome.execute_script('document.querySelector("#Register > div:nth-child(10)").querySelector("#checkbox").checked = true')
                    recaptcha_info1 = chrome.execute_script(
                        'function findRecaptchaClients() { if (typeof (___grecaptcha_cfg) !== "undefined") { return Object.entries(___grecaptcha_cfg.clients).map(([cid, client]) => { const data = { id: cid, version: cid >= 10000 ? "V3" : "V2" }; const objects = Object.entries(client).filter(([_, value]) => value && typeof value === "object"); objects.forEach(([toplevelKey, toplevel]) => { const found = Object.entries(toplevel).find(([_, value]) => ( value && typeof value === "object" && "sitekey" in value && "size" in value )); if (typeof toplevel === "object" && toplevel instanceof HTMLElement && toplevel["tagName"] === "DIV"){ data.pageurl = toplevel.baseURI; } if (found) { const [sublevelKey, sublevel] = found; data.sitekey = sublevel.sitekey; const callbackKey = data.version === "V2" ? "callback" : "promise-callback"; const callback = sublevel[callbackKey]; if (!callback) { data.callback = null; data.function = null; } else { data.function = callback; const keys = [cid, toplevelKey, sublevelKey, callbackKey].map((key) => `["${key}"]`).join(""); data.callback = `___grecaptcha_cfg.clients${keys}`; } } }); return data; }); } return []; } return findRecaptchaClients()')
                    print(type(recaptcha_info1))
                    print(recaptcha_info1)
                    recaptcha_info = recaptcha_info1[0]
                    if recaptcha_info.get('sitekey') != None:
                        print(recaptcha_info['pageurl'], recaptcha_info['sitekey'])
                        re_token = get_recaptcha_token(recaptcha_info['pageurl'].replace('#step-3', ''),
                                                      recaptcha_info['sitekey'],'123')
                        chrome.execute_script(re_token)
                        time.sleep(5)


        except Exception as e:
            print(e)

        try:
            if index == 3:
                print('请输入谷歌验证3！')
                recaptcha_info1 = chrome.execute_script(
                    'function findRecaptchaClients() { if (typeof (___grecaptcha_cfg) !== "undefined") { return Object.entries(___grecaptcha_cfg.clients).map(([cid, client]) => { const data = { id: cid, version: cid >= 10000 ? "V3" : "V2" }; const objects = Object.entries(client).filter(([_, value]) => value && typeof value === "object"); objects.forEach(([toplevelKey, toplevel]) => { const found = Object.entries(toplevel).find(([_, value]) => ( value && typeof value === "object" && "sitekey" in value && "size" in value )); if (typeof toplevel === "object" && toplevel instanceof HTMLElement && toplevel["tagName"] === "DIV"){ data.pageurl = toplevel.baseURI; } if (found) { const [sublevelKey, sublevel] = found; data.sitekey = sublevel.sitekey; const callbackKey = data.version === "V2" ? "callback" : "promise-callback"; const callback = sublevel[callbackKey]; if (!callback) { data.callback = null; data.function = null; } else { data.function = callback; const keys = [cid, toplevelKey, sublevelKey, callbackKey].map((key) => `["${key}"]`).join(""); data.callback = `___grecaptcha_cfg.clients${keys}`; } } }); return data; }); } return []; } return findRecaptchaClients()')
                print(type(recaptcha_info1))
                print(recaptcha_info1)
                recaptcha_info = recaptcha_info1[0]
                if recaptcha_info.get('sitekey') != None:
                    print(recaptcha_info['pageurl'], recaptcha_info['sitekey'])
                    re_token = get_recaptcha_token(recaptcha_info['pageurl'].replace('#step-3', ''),
                                                   recaptcha_info['sitekey'], '123')
                    chrome.execute_script(re_token.replace('g-recaptcha-response','g-recaptcha-response-1'))
                    chrome.execute_script('document.querySelector("#submitForm").click()')
                    time.sleep(5)

        except:
            pass

        try:
            if index == 4:
                print('注册完成！')
                #结果写入文件
                with open('acc_pwd.txt','a') as f:
                    f.write(f'{acc}----{pwd}---- ----{email_account}----{email_password}----{proxy_port}\n')
                with open('hotmail.txt', 'w',encoding='utf8') as f:
                    txt = '\n'.join(new_all_email)
                    f.write(txt)
                break
                #登录地址 https://www.mangot5.com/Index/Member/Login?ref=/Index
                #设定opt  https://www.mangot5.com/Index/Security/OTP
                #手机设定  https://www.mangot5.com/Index/Member/VerifySms
        except :
            pass

    happ_login(acc,pwd)
    chrome.get('https://www.mangot5.com/Index/Security/OTP')
    while True:
        try:
            print('判断所在页')
            # 找到所有的li标签
            # 使用 XPath 路径查找所有 li 标签
            li_elements = chrome.find_elements(By.XPATH, "//ul[@class='nav nav-tabs step-anchor']/li")

            # 遍历所有 li 标签并判断 class 是否包含 "active"
            for i, li in enumerate(li_elements):
                class_name = li.get_attribute("class")
                if "active" in class_name:
                    index = i   # 索引从1开始

                    print(li.text)
                    break
            # 打印结果
            if index != -1:
                print(f"The 'active' class is found in the {index} li element.")
            else:
                print("No 'li' element with 'active' class found.")
        except:
            print('判断错误!')
            pass

        if index == 0:
            print('在您的行動裝置上，下載並安裝「Google Authenticator」APP。')
            chrome.execute_script('document.querySelector("#nextOTPbtn").click()')
        if index == 1:
            print('get otp')
            otp = chrome.execute_script('return document.querySelector("#step-2 > div.secKey.alert.alert-info > span").innerHTML')
            with open('acc_pwd.txt', 'a') as f:
                f.write(f'{acc}----{pwd}----{otp}----{email_account}----{email_password}----{proxy_port}\n')
            chrome.execute_script('document.querySelector("#nextOTPbtn").click()')
        if index == 2:
            print('输入otp')
            otp_code = getOPT(otp)
            print(otp_code)
            chrome.execute_script(f'document.querySelector("#validCode").value ="{otp_code}"')
            chrome.execute_script('document.querySelector("#nextOTPbtn").click()')


        if index == 3:
            print('otp绑定完成!')
            break
        time.sleep(3)
    #chrome.get('https://www.mangot5.com/Index/Member/Login?gname=lostark&ref=/Index/Billing/couponList')
    chrome.get('https://www.mangot5.com/Index/Billing/couponList')
    chrome.execute_script('document.querySelector("#couponSerial").value = "來自團隊滿滿的感謝"')

#随机生成8到10位的账号



# 测试函数
print(random_account_password())

def get_mail_hotmail(email,passwd):
    print('get_hotmail')
    code = "123"
    return code

def bond_2fa():
    pass
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    happ_login(acc,pwd,'otp')
    #openChrome()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
