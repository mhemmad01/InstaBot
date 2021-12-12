import json
import requests
import time
import threading
import subprocess
import traceback
from abc import ABC, abstractmethod
from config import config


class VpnConnect():

    __instance = None

    def __init__(self):
        if VpnConnect.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            self.__ips = []
            self.__sess = None
            self.__normal_ip = None
            self.__HMAPath=config().HMAPath
            VpnConnect.__instance = self

    @staticmethod
    def getInstance():
        """ Static access method. """
        if VpnConnect.__instance == None:
            VpnConnect()
        return VpnConnect.__instance

    def synchronized(func):
        func.__lock__ = threading.Lock()
        def synced_func(*args, **kws):
            with func.__lock__:
                return func(*args, **kws)
        return synced_func

    def setHMAPath(self,HMAPath):
        self.__HMAPath=HMAPath

    def HMAConnect(self):
        self.__connected=True
        subprocess.call([self.__HMAPath, "-connect"])

    def HMADisconnect(self):
        self.__connected=False
        subprocess.call([self.__HMAPath, "-disconnect"])

    def HMAChaneIP(self):
        subprocess.call([self.__HMAPath, "-changeip"])

    def isConnected(self):
        return self.__connected

    def get_external_ip(self):
        try:
            while True:
                time.sleep(5)
                ip = json.loads(requests.get(url="http://ip.jsontest.com").text)["ip"]
                return ip
        except:
            print("Waiting for ip change...")
            time.sleep(5)
            pass

    def block_external_ip(self, current_ip):
        ip = self.get_external_ip()
        while current_ip == ip or self.__normal_ip == ip:
            if ip == self.__normal_ip:
                time.sleep(10)
                self.HMAConnect()
            print("Waiting for ip change...")
            ip = self.get_external_ip()
            if (ip in self.__ips):
                print("Same IP... changing...", ip, "in", self.__ips)
                time.sleep(10)
                self.HMAChaneIP()
                current_ip = self.block_external_ip(current_ip)
                continue
            time.sleep(5)
        print("Current IP: " + str(ip))
        return ip


    @synchronized
    def startAction(self, vpnmethod):
        current_ip = self.get_external_ip()
        self.__ips.append(current_ip)
        self.__normal_ip = current_ip
        print("Normal IP:", self.__normal_ip)
        self.HMAConnect()
        current_ip = self.block_external_ip(current_ip)
        self.__ips.append(current_ip)
        while not vpnmethod.stopCondition():
            try:
                __sess = requests.Session()
                #---------------Code----------------
                vpnmethod.method()
                time.sleep(vpnmethod.getSleepTime())
                #-----------------------------------
                self.HMAChaneIP()
                current_ip = self.block_external_ip(current_ip)
                self.__ips.append(current_ip)
            except Exception as e:
                print("Caught a general exception... changing IP.")
                traceback.print_exc()
                time.sleep(10)
                self.HMAChaneIP()
                current_ip = self.block_external_ip(current_ip)
                self.__ips.append(current_ip)
                continue
        self.HMADisconnect()


class vpnMethod(ABC):

    def __init__(self):
        self._sleepTime = 10
        self._StopCondition = False
        self._initFlag=True

    def setSleepTime(self, sleepTime):
        self._sleepTime= sleepTime

    def getSleepTime(self):
        return self._sleepTime

    def stopCondition(self):
        return self._StopCondition

    def stop(self):
       self._StopCondition=True

    @abstractmethod
    def method(self):
        pass



class CaptchaSlover():

    __API_KEY = 'c5c8ed078ce8a2c24c71fd829bb706bf'

    def setAPI_KEY(self, API_KEY):
        self.__API_KEY=API_KEY

    def solve_recaptcha(self, key, url):
        s = requests.Session()
        print("captcha key: " + key)
        captcha_id = s.post("http://2captcha.com/in.php?key={}&method=userrecaptcha&googlekey={}&pageurl={}".format(self.__API_KEY, key, url)).text.split('|')[1]
        recaptcha_answer = s.get("http://2captcha.com/res.php?key={}&action=get&id={}".format(self.__API_KEY, captcha_id)).text
        print("solving ref captcha...")
        while 'CAPCHA_NOT_READY' in recaptcha_answer:
            try:
                time.sleep(10)
                recaptcha_answer = s.get("http://2captcha.com/res.php?key={}&action=get&id={}".format(self.__API_KEY, captcha_id)).text
                print(recaptcha_answer)
            except:
                print("Exception while solving captcha, retrying...")
                continue
        recaptcha_answer = recaptcha_answer.split('|')[1]
        return recaptcha_answer

    def captcha_solver(self, key, url):
        captcha_solved = "ERROR_CAPTCHA_UNSOLVABLE"
        # try to solve captcha until success
        while captcha_solved == "ERROR_CAPTCHA_UNSOLVABLE":
            captcha_solved = self.solve_recaptcha(key, url)
        return captcha_solved

'''
Implemenation Example run method for "max" times:
    connection = VpnConnect.getInstance()
    class myMethod(vpnMethod):
        def __init__(self,max):
            vpnMethod.__init__(self)
            self._counter=0
            self._max=max

        def method(self):
            print("counter={}".format(self._counter))
            self._counter +=1
            if self._counter>=self._max:
                self._StopCondition=True

    method = myMethod(2)
    connection.startAction(method)

'''