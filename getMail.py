import imaplib
import email
import time

import requests
import json
#记得要import
#用于邮件解码

import os
import zipfile
import random
import string
def create_proxy_auth_extension(proxy_host, proxy_port, proxy_username, proxy_password, scheme='http', plugin_path=None):
    if plugin_path is None:
        plugin_path = 'proxy_auth_plugin.zip'

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
              singleProxy: {
                scheme: "%(scheme)s",
                host: "%(host)s",
                port: parseInt(%(port)d)
              },
              bypassList: ["localhost"]
            }
          };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%(username)s",
                password: "%(password)s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % {
        "host": proxy_host,
        "port": proxy_port,
        "username": proxy_username,
        "password": proxy_password,
        "scheme": scheme,
    }

    with zipfile.ZipFile(plugin_path, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    return plugin_path


# 邮件服务器信息
#IMAP_SERVER = 'imap-mail.outlook.com'
IMAP_SERVER = 'pop3.live.com'
#email_account =
#password =
proxies_none = {
    # 这个字典的key不可以乱写，必须是http和https
    # 如果你的只有http那就只写http代理，htpps也是相同的道理。
    # http代理
    "http": None,
    # https代理
    "https": None
}


def is_alpha_and_digit_combination(input_str):
    # 判断是否至少包含一个字母和一个数字，并且全为字母和数字的组合
    has_alpha = False
    has_digit = False

    for char in input_str:
        if char.isalpha():
            has_alpha = True
        elif char.isdigit():
            has_digit = True

        # 如果同时包含了字母和数字，则返回 True
        if has_alpha and has_digit:
            return True

    return False

def random_account_password():
    # 随机选择一个长度在8到10之间
    length = random.randint(8, 10)
    length2 = random.randint(8, 11)
    # 生成一个随机的账号，由字母和数字组成
    account = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
    #判断是否是纯数字或字母
    while is_alpha_and_digit_combination(account) == False:
        print('纯数字或字母')
        account = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

    password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length2))
    while is_alpha_and_digit_combination(password) == False:
        print('纯数字或字母')
        password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length2))
    return account,password


def get_verification_code(email_account,password):

    # 连接到IMAP服务器
    try:
        # 连接到IMAP服务器
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(email_account, password)

        # 选择收件箱
        mail.select('inbox')

        # 搜索所有邮件
        status, data = mail.search(None, 'ALL')
        if status == 'OK':
            print('邮箱登录成功！ ')
        else:
            print('登录失败！')
            return None
        print('邮件数量：',len(data))
        # 获取最新的一封邮件
        mail_ids = data[0].split()
        print('邮件数量：', len(mail_ids))
        latest_email_id = mail_ids[-1]

        # 获取邮件内容
        status, data = mail.fetch(latest_email_id, '(RFC822)')

        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)

        email_body = None  # 初始化 email_body 变量
        # 解析邮件内容
        # 解析multipart内容
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                for subpart in part.get_payload():
                    #print(subpart.get_content_type())
                    #print(subpart.get_payload())
                    if subpart.get_content_type() == 'text/html':
                        # 解码邮件头（如果需要）
                        charset = subpart.get_charset()
                        if charset is None:
                            charset = 'utf-8'  # 假设默认字符集为 utf-8
                        content = subpart.get_payload(decode=True).decode(charset, errors='replace')
                        if "認證碼" in content:
                            code = content.split('認證碼 :&nbsp;')[1].split('</strong></p>')[0]
                            return code
                        # 打印 HTML 内容
                        #print(content)

        return None

    except Exception as e:
        print(f'解析邮件时出错: {e}')
        return None

def ReCaptchaV2_create(weburl,websiteKey):

    url = "https://api.ez-captcha.com/createTask"

    payload = json.dumps({
        "clientKey": "985b3f98fa1c43dab3818caa1bc6ca03025159",
        "task": {
            "websiteURL": weburl,
            "websiteKey": websiteKey,
            "type": "ReCaptchaV2TaskProxyless",
            "isInvisible": False
        }
    })
    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False,proxies=proxies_none)
    print(response.text)
    if "taskId" in response.text:
        return response.json()['taskId']
    else:
        return False

#ReCaptchaV2_create('https://www.mangot5.com/Index/Member/Login',"6LcZ2f0SAAAAAD0eUdEP0YdkRZLYrdf8rg2qjsdj")

def get_task_result(taskId):
    url = "https://api.ez-captcha.com/getTaskResult"

    payload = json.dumps({
        "clientKey": "985b3f98fa1c43dab3818caa1bc6ca03025159",
        "taskId": taskId
    })
    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False,proxies=proxies_none)
    print(response.text)
    if "gRecaptchaResponse" in response.text:
        return response.json()['solution']['gRecaptchaResponse']
    else:
        return False


def get_recaptcha_token(weburl,websiteKey,token):
    js_code = """
            (function (response) {
                try {
                    const ele = document.getElementById("g-recaptcha-response");
                    console.log("Element found:", ele);
                    if (ele) {
                        ele.style.display = "block";
                        ele.innerText = response;
                        ele.text = response;
                    } else {
                        console.log("Element not found");
                    }
                    const base = Object.values(___grecaptcha_cfg.clients)[0];
                    for (let k0 of Object.keys(base)) {
                        for (let k1 of Object.keys(base[k0])) {
                            if (base[k0][k1] && base[k0][k1].callback && typeof base[k0][k1].callback === "function") {
                                console.log("Callback function found and executed");
                                base[k0][k1].callback(response);
                            }
                        }
                    }
                } catch (error) {
                    console.log("Error occurred:", error);
                }
            })("tooc");
            """
    recaptcha_token = None
    taskid = None
    while token != recaptcha_token:
        #获取任务id
        if taskid == None or taskid == False:
            taskid = ReCaptchaV2_create(weburl=weburl, websiteKey=websiteKey)
        if taskid != False:
            time.sleep(2)
            #获取token
            print(taskid)
            recaptcha_token = get_task_result(taskid)
            if recaptcha_token != False:
                cc = js_code.replace('tooc',recaptcha_token)
                #print(cc)
                #pyperclip.copy(cc)
                #置粘贴板

                break

        else:
            print('taskid 获取失败！')


    return cc

def getOPT(otp_code):
    # header = '''
    #     Accept: application/json, text/javascript, */*; q=0.01
    #     Accept-Encoding: gzip, deflate, br, zstd
    #     Accept-Language: zh-CN,zh;q=0.9
    #     Priority: u=1, i
    #     Referer: https://2fa.run/
    #     Sec-Ch-Ua: "Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"
    #     Sec-Ch-Ua-Mobile: ?0
    #     Sec-Ch-Ua-Platform: "Windows"
    #     Sec-Fetch-Dest: empty
    #     Sec-Fetch-Mode: cors
    #     Sec-Fetch-Site: same-origin
    #     User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36
    #     X-Requested-With: XMLHttpRequest
    # '''
    # response = requests.request("GET", "https://2fa.run/app/2fa.php?secret=code".replace('code',otp_code), headers=header, verify=False,proxies={})
    # print(response.text)
    # if "true" in response.text:
    #     return response.json()['newCode']
    # else:
    #     return False
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Priority': 'u=1, i',
        'Referer': 'https://2fa.run/',
        'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    # 禁用 SSL 警告

    url = f"https://2fa.run/app/2fa.php?secret={otp_code}"
    print(url)
    # try:
    response = requests.get(url, headers=headers, verify=False,proxies=None)
    response.raise_for_status()  # 检查请求是否成功
    if response.status_code == 200:
        print(response.text)
        if "true" in response.text:
            return response.json().get('newCode')
    else:
        return False
    # except requests.RequestException as e:
    #     print(f"Request failed: {e}")
    #     return False

def get_phone():
    pass

def get_phone_code(token):
    pass
#token1 ='03AFcWeA6k_KZ9ZGMywclO7ZaBu0aVGvUobnnmeuXkcvKu8ufUk-C0rpRvfhPXf_F34kw28PRLvq4COJfDvIM3_f3rQ4YiP_e26ym82mMCiyUTZkOiji31mWc2SeF-8v6Kqrgw_2I7Kr03DyZfNE8TzVeklssDbaBXQGkQSc4BxFnixyy-ld2fnFSv3C4QoCB-BOB4-UfjKi7wsolOQunrm4asUvnR6seb_roTsotGOi0djNBKN2KA307cHqd7Ln5RJyCC6BVwhkxR3-_9gRtUl2f4Yl554n_4kId3u41MmfsbdInz7GYA9dtF_ZLNzg5OZvopX5VmQoVG6VXhE-YCpD8xHB7f5l0tPXChn-q1X4ehAF673JH-chVIwWOoolhm7mqh_NEtiUajQoXzRgHkDEiynM0eyRUPBuaqaLCNJTMdzS6__eq_AbArueSK5wW9uIaKSKNyLJHLIiYSIfynFv6vnBe3FqNHoxbKm2MgO787BCrPQl-jLFEUZlUDuNWOxPmcPTT9huwMxufOInIZ7wEne3oLJ9a3K3v1AQp9hMwMO0Zxm3mVhdctoUy2bJANi06GaasmcblcwVXioaG5tdKHa21AhnPz4-miOpYwu00WrL5SkULld36MHL5SP_jxkbfUOD2Fbvsrl5hN5dKJ8BHr-hr5iL8_gFTB-4s7x0OdJPFLpOpsOF5Nr0IvKoa6hTgTcE6UYr7M83MktBCS-1CgCi0KgpldV69qg9Q_n-Cx9AUDWFgS8ajcbYOG_pB2oz-E18iGgsXdHPDRAKe-Er0pb_h9GvQfm1rEw3D8nXVrIC7CDxNqQRVoCEMuYCKnBaXH08xFR8JHvgWmxYEf32gErgG2mJD2v91OIwauzAEJFAZY_vm2H7MN5wu2eIyOs-uoRVfOuep8BEXKWVMyj06qiy6eip3leOik87yCNIC_EFblpen03i8JrQQVn3yoH1L3s0w50qBPldqMN4j3qvmQq_NZN9xoZoIr21Y9ot5J28nA5R5KOxtJHTpLjIbFAv-5foaGurWH9d_Lzzpw9hgaO3pyi3ZhZp11BJ2J2nD89NQQ71VPhZOwrGO2XDkbHhuVufGfTESM0jzaIUqMVeAHb_HhuD4zlyJwnpcBVmNRjjhlzilG6hoNe_LZB9ovj5svnFz6l-b0nOXoV-sf3e5G-nS81pizhiCzJZDTL9Q8f3hMu4JMweqeip9Je3tNIb_sxTdSto2v1C0w0R39ABlWMJhPN6iN4Okqc8RpG3fy3d5Kf3Jc0DfH7nQBo44z747IoK671Ji8crFkU1-P7VTUD-3lMFrv4AhhJNKybRP0X_AspRLO7WLet2j-0yUkDdXswmt-dQBw5NE8GeBXwfy7NXlwuZZYkJSnPmXtxN_h_r9YTf3YUod5Bm0_Jmqx4YJHwwRtlH2kKPoLsJub-tO-ANj27iXkvVGx8-9qnp9Bh2wrnFkFma-FqHW0U0_wG_mMkKKNKWKwV5yuXSV31jyha2y-KYSaamW2JM_8s6HNL9u72FYy8dr3BTvX1cZpbPvPeMbZcdlrHt6tTjAxU7qcpgt4d7uexoM0xWrUVmRwUs7z48rcXa6qh33vOI6--f92S4NQxw_TLBBure0uqGXopTNt7_kdMx2CQTJFF8lgXEE2aELkCrf9fUtUT2d8kOEXsW6w68K7dLEhJUjdjc1jOtZLqJbQGQ'
#get_recaptcha_token('https://www.mangot5.com/Index/Member/Login',"6LcZ2f0SAAAAAD0eUdEP0YdkRZLYrdf8rg2qjsdj",token1)
#获取验证码
#verification_code = get_verification_code() # 6b50bf66-5f2e-4737-8e30-7f6a06951c47
# if verification_code:
#     print(f'验证码是: {verification_code}')
# else:
#     print('未找到验证码')




