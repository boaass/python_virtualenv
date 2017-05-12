# -*- coding:utf-8 -*-
import requests, termcolor
import os, sys, codecs, time, platform, random
import re, json, cookielib, lxml
from getpass import getpass
from bs4 import BeautifulSoup
from ConfigParser import ConfigParser
from enum import Enum
#
if sys.stdout.encoding != 'UTF-8':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout, 'strict')
if sys.stderr.encoding != 'UTF-8':
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr, 'strict')

class Logging:
    def __init__(self):
        pass

    flag = True

    @classmethod
    def error(cls, msg):
        if cls.flag:
            print "".join([termcolor.colored("ERROR", "red"), ": ", termcolor.colored(msg, "white")])

    @classmethod
    def warning(cls, msg):
        if cls.flag:
            print "".join([termcolor.colored("WARNING", "yellow"), ": ", termcolor.colored(msg, "white")])

    @classmethod
    def info(cls, msg):
        if cls.flag:
            print "".join([termcolor.colored("INFO", "magenta"), ": ", termcolor.colored(msg, "white")])

    @classmethod
    def debug(cls, msg):
        if cls.flag:
            print "".join([termcolor.colored("DEBUG", "magenta"), ": ", termcolor.colored(msg, "white")])

    @classmethod
    def success(cls, msg):
        if cls.flag:
            print "".join([termcolor.colored("SUCCESS", "green"), ": ", termcolor.colored(msg, "white")])


class AccountPasswordError(Exception):
    def __init__(self, msg="账号密码错误"):
        Logging.error(msg)


class AccountTypeError(Exception):
    def __init__(self, msg="账号类型错误"):
        Logging.error(msg)


class NetworkError(Exception):
    def __init__(self, msg="网络错误"):
        Logging.error(msg)

session = requests.Session()
session.cookies = cookielib.LWPCookieJar('cookies')
# noinspection PyBroadException
try:
    session.cookies.load(ignore_discard=True)
except Exception as e:
    Logging.debug(e.message)
    Logging.warning("cookies 加载失败 !!!")

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/"
}

# 判断登录状态
def isLogin():
    url = "https://www.zhihu.com/settings/profile"
    r = session.get(url, headers=header, allow_redirects=False, verify=False)
    status_code = r.status_code
    Logging.debug("======登录状态: {status_code}======".format(status_code=status_code))
    if status_code == 200:
        return True
    elif status_code == 301 or status_code == 302:
        # 未登录
        return False
    else:
        raise NetworkError()


# 读取本地账号信息
def read_account_info_from_config_file(config_file="account_info.ini"):
    cp = ConfigParser()
    if os.path.exists(config_file) and os.path.isfile(config_file):
        Logging.info("正在加载账号配置文件 ... ")
        cp.read(config_file)
        email = cp.get("info", ACCOUNT_TYPE.EMAIL_TYPE)
        phone_number = cp.get("info", ACCOUNT_TYPE.PHONE_TYPE)
        passward = cp.get("info", "password")
        if passward.strip() != "":
            if not "" == email.strip():
                return (email, passward)
            elif phone_number.strip() != "":
                return (phone_number, passward)
            else:
                pass
        Logging.info("本地无账号配置")
        return (None, None)

def save_account_info_to_config_file(form_data, config_file="account_info.ini"):
    cp = ConfigParser()
    cp.read(config_file)
    cp.set("info", ACCOUNT_TYPE.EMAIL_TYPE, form_data[ACCOUNT_TYPE.EMAIL_TYPE])
    cp.set("info", "password", form_data["password"])
    cp.set("cookies", "_xsrf", form_data["_xsrf"])
    try:
        cp.write(open(config_file,"w"))
    except Exception as e:
        Logging.warning(e.message)

# 获取_xsrf
def search_xsrf():
    url = "https://www.zhihu.com"
    response = session.get(url, headers=header, verify=False)
    Logging.debug("======_xsrf请求: %d======" % int(response.status_code))
    if int(response.status_code) != 200:
        raise NetworkError()

    soup = BeautifulSoup(response.text, "lxml")
    _xsrf_datas = soup.find_all(attrs={"name": "_xsrf"})
    if len(_xsrf_datas) == 0:
        Logging.info("_xsrf获取失败 !!!")
    else:
        return _xsrf_datas[0].get("value")


# 获取并解析验证码
def parse_captcha():
    # 下载验证码
    t = str(int(time.time() * 1000))
    url = "https://www.zhihu.com/captcha.gif?r={time}&type=login".format(time=t)
    response = session.get(url, headers=header, verify=False)
    Logging.debug("======验证码请求: %d======" % int(response.status_code))
    if response.status_code != 200:
        raise NetworkError("验证码请求失败")

    # 调用系统程序，打开验证码图片
    image_name = "".join(["verify", ".", response.headers["Content-Type"].split("/")[-1]])
    open(image_name, "wb").write(response.content)

    Logging.info("正在调用外部程序渲染验证码 ... ")
    if platform.system() == "Linux":
        Logging.info("Command: xdg-open %s &" % image_name)
        os.system("xdg-open %s &" % image_name)
    elif platform.system() == "Darwin":
        Logging.info("Command: open %s &" % image_name)
        os.system("open %s &" % image_name)
    elif platform.system() in ("SunOS", "FreeBSD", "Unix", "OpenBSD", "NetBSD"):
        os.system("open %s &" % image_name)
    elif platform.system() == "Windows":
        os.system("%s" % image_name)
    else:
        Logging.info("无法获取当前操作系统，请自行打开验证码 %s 文件，并输入验证码。" % os.path.join(os.getcwd(), image_name))

    # 提示用户输入验证码并获取
    sys.stdout.write(termcolor.colored("请输入验证码: ", "cyan"))
    captcha_code = raw_input()
    return captcha_code


# 自定义枚举
def enum(**enums):
    return type('Enum', (), enums)


ACCOUNT_TYPE = enum(PHONE_TYPE="phone_num", EMAIL_TYPE="email")


# 创建表单数据
def build_form_data(account, password):
    if re.match(r"^1\d{10}$", account):
        account_type = ACCOUNT_TYPE.PHONE_TYPE
    elif re.match(r"^\S+\@\S+\.\S+$", account):
        account_type = ACCOUNT_TYPE.EMAIL_TYPE
    else:
        raise AccountTypeError()
    form = {account_type: account, "password": password, "_xsrf": search_xsrf(), "captcha": parse_captcha()}
    return form


def upload_form(form):
    if ACCOUNT_TYPE.PHONE_TYPE in form:
        url = "https://www.zhihu.com/login/" + ACCOUNT_TYPE.PHONE_TYPE
    elif ACCOUNT_TYPE.EMAIL_TYPE in form:
        url = "https://www.zhihu.com/login/" + ACCOUNT_TYPE.EMAIL_TYPE
    else:
        raise ValueError("账号类型错误")

    response = session.post(url, data=form, headers=header)
    if int(response.status_code) != 200:
        raise NetworkError("表单数据上传失败 !!!")

    if response.headers["content-type"].lower() != "application/json":
        Logging.warning("无法解析服务器响应内容 !!!")
        return {
            "error": dict(code=-2, msg="parse error")}
    else:
        try:
            r_json = json.loads(response.content)
        except Exception as e:
            Logging.warning("json 解析失败 !!!")
            Logging.debug(e)
            Logging.debug(response.content)
            r_json = {}
        if r_json["r"] == 0:
            Logging.success(r_json["msg"])
            return dict(error=0)
        elif r_json["r"] == 1:
            Logging.warning(r_json["msg"])
            return dict(error=dict(code=int(r_json["errcode"]), msg=r_json["msg"], data=r_json["data"]))
        else:
            Logging.warn("表单上传出现未知错误: \n \t %s )" % (str(r_json)))
            return dict(error=dict(code=-1, message="unknown error"))


# 登录
def login():
    if isLogin():
        Logging.success("已经登录啦")
    else:
        Logging.info("未登录状态")
        config_file = "account_info.ini"
        (account, password) = read_account_info_from_config_file(config_file)
        if not account:
            sys.stdout.write("请输入登录账号: ")
            account = raw_input()
            password = getpass("请输入登录密码: ")
        form_data = build_form_data(account, password)
        result = upload_form(form_data)
        if result["error"] == 0:
            # 保存cookies
            session.cookies.save(ignore_discard=True)
            # 保存账号信息
            save_account_info_to_config_file(form_data=form_data)



if __name__ == '__main__':
    login()
