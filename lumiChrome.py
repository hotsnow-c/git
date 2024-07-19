from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from getMail import get_verification_code,get_recaptcha_token,getOPT,random_account_password
import string
#from lumi_api import LumiClient


import requests
import json
import time
import random

class LumiClient:
    '''
    :param port: api服务的端口号
    :param token: api服务的token
    '''

    def __init__(self, port: int, token: str) -> None:
        self.port = port
        self.host = "127.0.0.1"
        self.token = token
        self.url = f"http://{self.host}:{self.port}"

    def _build_headers(self):
        return {"Content-Type": "application/json", "token": self.token}

    def _post(self, path, data=None):
        return requests.post(self.url + path, json=data, headers=self._build_headers())

    def _get(self, path, data=None):
        return requests.get(self.url + path, params=data, headers=self._build_headers())

    '''
     健康检查,用于检查API服务是否正常运行,文档地址:https://lumibrowser.com/api/#/api_health
    '''

    def health(self):
        return self._get("/health").json()

    '''
    获取窗口列表,文档地址: https://lumibrowser.com/api/#/api_list
    :param dirId: 窗口id, 选填；如果填了就只查询这个窗口的信息
    :param page_index,page_size 分页参数,dirId 不填的时候有效
    :res 返回值参考文档
    '''

    def browser_list(self, dirId: str = "", page_index: int = 1, page_size: int = 15):
        return self._get("/browser/list", {"dirId": dirId, "page_index": page_index, "page_size": page_size}).json()

    '''
    创建窗口,文档地址: https://lumibrowser.com/api/#/api_create
    :param data: 创建窗口需要传的参数,参考文档说明
    :res 返回值参考文档
    '''

    def browser_create(self, data: dict = None):
        return self._post("/browser/create", data).json()

    '''
    修改窗口，文档地址: https://lumibrowser.com/api/#/api_mdf
    :param data: 创建窗口需要传的参数,参考文档说明
    :res 返回值参考文档
    '''

    def browser_mdf(self, data: dict):
        return self._post("/browser/mdf", data).json()

    '''
    删除窗口,文档地址:https://lumibrowser.com/api/#/api_delete
    :param data: 需要删除的窗口ID
    :res 返回值参考文档
    '''

    def browser_delete(self, data: dict):
        return self._post("/browser/delete", data).json()

    '''
    打开窗口,文档地址：https://lumibrowser.com/api/#/api_open
    :param dirId: 需要打开的窗口ID
    :res 返回值参考文档
    '''

    def browser_open(self, dirId: str):
        return self._post("/browser/open", {"dirId": dirId}).json()

    '''
    关闭窗口,文档地址:https://lumibrowser.com/api/#/api_close
    :param dirId: 需要关闭的窗口ID
    :res 返回值参考文档
    '''

    def browser_close(self, dirId: str):
        return self._post("/browser/close", {"dirId": dirId}).json()

    '''
    获取平台购买的静态IP,文档地址:https://lumibrowser.com/api/#/api_static_list
    :param page_index,page_size 分页参数
    :res 返回值参考文档
    '''

    def browser_static_ip_list(self, page_index: int = 1, page_size: int = 15):
        return self._get("/browser/static_list", {"page_index": page_index, "page_size": page_size}).json()

    '''
    获取已打开的浏览器,文档地址:https://lumibrowser.com/api/#/api_pid
    '''

    def browser_connection_info(self):
        return self._get("/browser/connection_info").json()


lumi_info = {
"windowName": "窗口1",                                  # 窗口名称, str类型，非必传
    "coreVersion": "125",                                   # 内核版本，枚举值：117，109, str类型，非必传，默认125
    "os": "Windows",                                        # 操作系统, 枚举值：Windows、macOS、Linux、IOS、Android, str类型，非必传，默认Windows
    "osVersion": "10",                                      # 操作系统版本, Windows的枚举值：11、10、8、7; macOS和Linux的枚举值：ALL，Android的枚举值：13,12,11,10,9；IOS的枚举值：17.0,16.6,16.5,16.4,16.3,16.2,16.1,16.0,15.7,15.6,15.5,15.4,15.3,15.2,15.1,15.0,14.7,14.6,14.5,14.4,14.3,14.2,14.1,14.0；str类型，非必传，默认11
    # "cookie": [],                                           # cookie, List类型，非必传
    # "platformUrl": "http://dww.com/",                       # 业务平台URL，str类型，非必传
    # "platformUserName": "xxx",                              # 平台账号，str类型，非必传
    # "platformPassword": "xxx",                              # 平台密码，str类型，非必传
    # "efa":"777777",                                            # efa，str类型，非必传
    # "defaultOpenUrl": ["https://www.facebook.com"],         # 存储浏览器标签页，List类型，非必传
    "windowRemark": "窗口1",                                         # 窗口备注, str类型，非必传
    "proxyInfo": {
            "proxyMethod": "import",                                # 代理方式，枚举值：直连：noproxy，自定义：import，str类型，非必传，默认为noproxy
            "proxyType": "rotate",                                   # 代理类型, 枚举值：static：静态IP，rotate: 动态IP，str类型，非必传
            "proxyNetwork": "resi",                                  # 代理网络, 枚举值：resi：住宅IP，mobile: 手机IP，dc: 机房IP，ipv6: IPv6，str类型，非必传
            "billMethod": "bandwidth",                                    # 计费方式,枚举值：month:包月，bandwidth:流量，str类型，非必传
            "ipType": "IPV4",                                        # 网络协议, 枚举值：IPV4, IPV6，str类型，非必传
            "protocol": "SOCKS5",                                    # 代理协议，枚举值：HTTP, HTTPS, SOCKS5，str类型，非必传
            #"country": "us",                                         # 国家代码，str类型，非必传
            "host": "proxy.froxy.com",                                  # 代理主机，str类型，非必传
            "port": "10002",                                         # 代理端口，str类型，非必传
            #"proxyUserName": "z84y4su7fqm7ze7dowfhn2h",                               # 代理账号，str类型，非必传
            #"proxyUserName": "g8nmn6zo3oytgyrjq7inw45",                               # 代理账号，str类型，非必传
            "proxyUserName": "4nd0fvdschbg2sx7endqtp4",                               # 代理账号，str类型，非必传
            "proxyPassword": "RNW78Fm5",                               # 代理密码，str类型，非必传
            "proxyTime": "2",                                       # ip时长，单位：分钟，枚举值：10，30，60，90，str类型，非必传
            "refreshUrl": "http://refresh-hk.lumibrowser.com"       # 刷新URL，str类型，非必传
    },
    "fingerInfo": {
            "isLanguageBaseIp": False,                               # 浏览器语言类型，跟随IP匹配：True，自定义：false，布尔类型，非必传, 默认True
            "language": "zh-TW",                                    # 浏览器语言类型为自定义时指定的语言值，str类型，非必传，见附录-语言列表
            "isDisplayLanguageBaseIp": False,                        # 界面语言类型，跟随IP匹配：True，自定义：false，布尔类型，非必传, 默认True
            "displayLanguage": "zh-TW",                             # 界面语言类型为自定义时指定的语言值，str类型，非必传，见附录-界面语言列表
            "isTimeZone": True,                                     # 时区类型，跟随IP匹配：True，自定义：false，布尔类型，非必传, 默认True
            "timeZone": "GMT-12:00 Etc/GMT+12",                     # 时区类型为自定义时指定的时区值, str类型，非必传，见附录-时区列表
            "position": 0,                                          # 地理位置提示类型，询问: 0，允许：1，禁用：2，int类型, 非必传, 默认1
            "isPositionBaseIp": True,                               # 地理位置类型，跟随IP匹配：True，自定义：false，布尔类型，非必传, 默认True
            "longitude": "376",                                     # 经度值，isPositionBaseIp为false时设置, str类型, 非必传
            "latitude": "165",                                      # 纬度值， isPositionBaseIp为false时设置, str类型, 非必传
            "precisionPos": "600",                                  # 精度值(米)， isPositionBaseIp为false时设置, str类型, 非必传
            "forbidAudio": True,                                    # 网页是否打开声音，开启：True，关闭：false，布尔类型，非必传, 默认True
            "forbidImage": True ,                                    # 网页是否加载图片，加载：True，禁止：false，布尔类型，非必传, 默认True
            "forbidMedia": False,                                    # 网页是否播放视频，允许：True，禁止：false，布尔类型，非必传, 默认True
            "syncTab": True,                                        # 是否同步标签页，True：是，false：否，布尔类型，非必传, 默认True
            "syncCookie": True,                                     # 是否同步Cookie，True：是，false：否， 布尔类型，非必传, 默认True
            "forbidSavePassword": True,                                # 网页是否弹出保存密码提示，True：是，false：否，布尔类型，非必传, 默认false
            "stopOpenNet": True,                                    # 网络不通是否停止打开窗口，True：是，false：否，布尔类型，非必传, 默认false
            "stopOpenIP": False,                                     # 出口IP发生变化是否停止打开窗口，True：是，false：否，布尔类型，非必传, 默认false
            "stopOpenPosition": True,                               # 出口IP对应国家/地区发生变化是否停止打开窗口，True：是，false：否，布尔类型，非必传, 默认false
            "syncIndexedDb": True,                                  # 是否同步IndexedDB，True：是，false：否，布尔类型，非必传, 默认True
            "syncLocalStorage": True,                               # 是否同步Local Storage，True：是，false：否，布尔类型，非必传, 默认True
            "syncBookmark": True,                                   # 是否同步书签，True：是，false：否，布尔类型，非必传, 默认True
            "syncPassword": True,                                   # 是否同步已保存的用户名密码，True：是，false：否，布尔类型，非必传, 默认True
            "syncHistory": True,                                    # 是否同步历史记录，True：是，false：否，布尔类型，非必传, 默认false
            "syncExtensions": True,                                 # 是否同步扩展应用数据，True：是，false：否，布尔类型，非必传, 默认True
            "clearCacheFile": True,                                 # 启动浏览器前是否删除缓存文件，True：是，false：否，布尔类型，非必传, 默认false
            "clearCookie": True,                                    # 启动浏览器前是否删除Cookie，True：是，false：否，布尔类型，非必传, 默认false
            "clearHistory": True,                                   # 启动浏览器前删除历史记录，True：是，false：否，布尔类型，非必传, 默认false
            "randomFingerprint": True,                              # 启动浏览时是否随机生成指纹，True：是，false：否，布尔类型，非必传, 默认false
            "useGpu": True,                                         # 使用硬件加速模式，True：是，false：否，布尔类型，非必传, 默认True
            "webRTC": 2,                                             # webrtc 替换: 0，真实：1，禁止：2，int类型, 非必传, 默认2
            "ignoreHttpsError": True,                                   # 是否忽略https证书错误，True：是，false：否，布尔类型，非必传, 默认false
            "openWidth": "1000",                                        # 窗口尺寸，宽度, str类型，非必传，默认 1000
            "openHeight": "1000",                                   # 窗口尺寸，高度, str类型，非必传，默认 1000
            "resolutionType": True,                                     # 分辨率，True: 自定义, false: 真实，布尔类型，非必传, 默认false
            "resolutionX": "",                                          # 自定义分辨率时，分辨率宽度值, str类型，见附录-分辨率列表，非必传
            "resolutionY": "",                                          # 自定义分辨率时，分辨率高度值, str类型，见附录-分辨率列表，非必传
            "fontType": True,                                       # 字体指纹，随机：True，真实：false，布尔类型，非必传, 默认True
            "canvas": True,                                         # canvas，随机：True，真实：false，布尔类型，非必传, 默认True
            "webGL": True,                                          # webGL图像， 随机：True，真实：false，布尔类型，非必传, 默认True
            "webGLInfo": True,                                      # webGLInfo开关，自定义：True，真实：false，布尔类型，非必传, 默认True
            "webGLManufacturer": "",                                # webGLInfo为自定义时指定的webGL厂商值, str类型，非必传
            "webGLRender": "",                                      # webGLInfo为自定义时指定的webGL渲染值, str类型，非必传
            "webGpu": "webgl",                                      # webGpu，基于webgl匹配：webgl，真实：real，禁用：block，str类型，非必传，默认值：webgl
            "audioContext": True,                                   # audioContext值，随机：True，真实：false，布尔类型，非必传, 默认True
            "speechVoices": True,                                   # Speech Voices，随机：True，真实：false，布尔类型，非必传, 默认True
            "doNotTrack": True,                                     # doNotTrack，True：开启，false：关闭，布尔类型，非必传, 默认True
            "clientRects": True,                                    # ClientRects，随机：True，真实：false，布尔类型，非必传, 默认True
            "deviceInfo": True,                                     # 媒体设备，随机：True，真实：false，布尔类型，非必传, 默认True
            "deviceNameSwitch": True,                               # 设备名称，随机：True，真实：false，布尔类型，非必传, 默认True
            "macInfo": True,                                        # MAC地址，自定义：True，真实：false，布尔类型，非必传, 默认True
            "portScanProtect": True,                                    # 端口扫描保护, false: 关闭, True: 开启，布尔类型，非必传, 默认True
            "portScanList": "",                                     # 端口扫描保护开启时的白名单，英文逗号分隔，str类型，非必传
            "disableSsl": True,                                         # ssl指纹设置, True: 开启, false: 关闭, 布尔类型，非必传, 默认false
            "disableSslList": [],                                   # ssl特性值列表，List格式类型，非必传
            "hardwareConcurrent": "4",                               # 硬件并发数, str类型，非必传
            "deviceMemory": "8"                                      # 设备内存, str类型，非必传
    }

}

def random_fenbianlv():
    # 分辨率列表
    fenbianlv = [
        (1600, 1200),
        (1920, 1080),
        (1920, 1200),
        (2048, 1152),
        (2304, 1440),
        (2560, 1440),
        (2560, 1600),
        (2880, 1800),
    ]
    x,y = random.choice(fenbianlv)
    return str(x),str(y)



#随机窗口大小
def random_window():
    openWidth_mini = 1024
    openHeight_mini = 800
    openWidth_max = 1800
    openHeight_max = 1240
    openWidth = random.randint(openWidth_mini,openWidth_max)
    openHeight = random.randint(openHeight_mini,openHeight_max)
    return str(openWidth),str(openHeight)

lumi_info['resolutionX'],lumi_info['resolutionY'] = random_fenbianlv()
lumi_info['openWidth'],lumi_info['openHeight'] = random_window()
print(lumi_info['openWidth'],lumi_info['openHeight'])
print(lumi_info['resolutionX'],lumi_info['resolutionY'])
if __name__ == "__main__":
    print('main')
    #brwoser_id = "8ba009cbbedf192f34817574c81c9454"

    acclist = [
        #"mu7966597,8jyw4la1iu,ZQZYTM5GEMHKO3PR,112233,阿曼,0,全局脚本",
        #"mei331153,36t2pk9xof,2T7QEGPM5RFH3MG7,112233,阿曼,0,全局脚本",
        #"Wovzgert0809,9fy7zf4hdr,NTHPJMVHWQID3GQM,112233,阿曼,0,全局脚本",
        #"shi714619,8fcyzphgfu,WLBVVAEKV3NU7WRI,112233,阿曼,0,全局脚本",
         "han8088471,1ugch1xgmn,ESVQPKIOLWA5SUAO,112233,阿曼,0,全局脚本",
        # "gy4397960,0siy2wacaa,GLSEHSO3DLSGMDVF,112233,阿曼,0,全局脚本",
        # "9573knalbgv,0uad9pgbei,SP5KZ4SNL2HXKIDP,112233,阿曼,0,全局脚本",
        # "2181cwpt,8e3yec2gta,3JERARNODXK2RKGA,112233,阿曼,0,全局脚本",
        # "Rihpckqc0416,749rboqh7q,YFFHF6WLWUXZHV7T,112233,阿曼,0,全局脚本",
        # "Otxiv23163,9n7dc3irlg,2BKW76OLP525H34L,112233,阿曼,0,全局脚本",

    ]
    for i in range(len(acclist)):
        lumi_info['windowName'] = acclist[i]
        lumi_info['proxyInfo']['port'] = '1000'+str(i+5)
        print(lumi_info['windowName'])
        print(lumi_info['proxyInfo']['port'])

        # 初始化客户端
        client = LumiClient(port=50000,token="258a4107301a12383aabed96ced22b66")

        print(client)
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

        #driver.get('https://www.mangot5.com/Index/Member/Login?gname=lostark&ref=/Index/Billing/couponList')
        driver.get('https://www.mangot5.com/Index/Member/VerifySms')

        #print(driver.title)
        chrome = driver
        print('123')
        # chrome.get('https://lostark.mangot5.com/game/lostark/preSignup/artist/index')
        chrome.get('https://www.mangot5.com/Index/Billing/couponList')
        acc = acclist[i].split(',')[0]
        pwd = acclist[i].split(',')[1].split(',')[0]
        chrome.execute_script(f'document.querySelector("#oldPassword").value = "{acc}"')
        chrome.execute_script(f'document.querySelector("#newPassword").value = "{pwd}"')

        # re_token = ReCaptchaV2_create('https://www.mangot5.com/Index/Member/Login',"6LcZ2f0SAAAAAD0eUdEP0YdkRZLYrdf8rg2qjsdj")
        #來自團隊滿滿的感謝
        recaptcha_info1 = chrome.execute_script(
            'function findRecaptchaClients() { if (typeof (___grecaptcha_cfg) !== "undefined") { return Object.entries(___grecaptcha_cfg.clients).map(([cid, client]) => { const data = { id: cid, version: cid >= 10000 ? "V3" : "V2" }; const objects = Object.entries(client).filter(([_, value]) => value && typeof value === "object"); objects.forEach(([toplevelKey, toplevel]) => { const found = Object.entries(toplevel).find(([_, value]) => ( value && typeof value === "object" && "sitekey" in value && "size" in value )); if (typeof toplevel === "object" && toplevel instanceof HTMLElement && toplevel["tagName"] === "DIV"){ data.pageurl = toplevel.baseURI; } if (found) { const [sublevelKey, sublevel] = found; data.sitekey = sublevel.sitekey; const callbackKey = data.version === "V2" ? "callback" : "promise-callback"; const callback = sublevel[callbackKey]; if (!callback) { data.callback = null; data.function = null; } else { data.function = callback; const keys = [cid, toplevelKey, sublevelKey, callbackKey].map((key) => `["${key}"]`).join(""); data.callback = `___grecaptcha_cfg.clients${keys}`; } } }); return data; }); } return []; } return findRecaptchaClients()')
        print(type(recaptcha_info1))
        print(recaptcha_info1)
        recaptcha_info = recaptcha_info1[0]
        if recaptcha_info.get('sitekey') != None:
            print(recaptcha_info['pageurl'], recaptcha_info['sitekey'])
            re_token = get_recaptcha_token(recaptcha_info['pageurl'].replace('#step-3', ''), recaptcha_info['sitekey'],
                                           '123')
            chrome.execute_script(re_token)
            chrome.execute_script('document.querySelector("#submitBtn").click()')
            time.sleep(10)
