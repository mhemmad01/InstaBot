from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
from time import sleep
import urllib.request
import os
from config import *
from selenium.webdriver.common.by import By
from Constants import  Constants
import random
from selenium.webdriver.common.keys import Keys

class InstaBot:



    def __init__(self, instagramUsername=None, instagramPassword = None):
        self.__config = config()
        if((instagramUsername != None) and (instagramPassword != None)):
            self.setUsernamePassword(instagramUsername = instagramUsername,instagramPassword = instagramPassword)
        else:
            self.setUsernamePassword(instagramUsername = self.__config.instagramUsername,instagramPassword = self.__config.instagramPassword)

        self.driver = webdriver.Chrome(self.__config.ChromeDriverPath)
        self.logged_in = False
        self.followersLoaded=False
        self.followingLoaded=False

    def setUsernamePassword(self,instagramUsername=None, instagramPassword = None):
        if(instagramUsername != None):
            self.instagramUsername=instagramUsername
        if(instagramPassword != None):
            self.instagramPassword=instagramPassword

    def login(self):
        self.driver.get(self.__config.login_url)
        sleep(self.__config.PAGELOADING)
        usernameElement =  self.driver.find_element_by_xpath("//input[@name=\"username\"]")
        passwordElement = self.driver.find_element_by_xpath("//input[@name=\"password\"]")
        loginbuttonElement = self.driver.find_element_by_xpath('//button[@type="submit"]')

        usernameElement.send_keys(self.instagramUsername)
        passwordElement.send_keys(self.instagramPassword)
        loginbuttonElement.click()

        if not self.waitUrl(self.__config.login_url, max=10):
            return Constants.LoginError


        while(True):
            try:
                self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]") \
                    .click()
                sleep(self.__config.PAGELOADING)
            except:
              break

        return Constants.OK

    def AddPeopleFromSuggested(self, amount): #SUGGESTED_PEOPLE
        j=0
        try:
            while j<amount:
                self.driver.get(self.__config.SuggestedPeople)
                sleep(self.__config.PAGELOADING)
                followbuttons=self.driver.find_elements_by_xpath("//button[contains(text(), 'Follow')]")
                i=0
                for bt in followbuttons:
                    bt.click()
                    sleep(random.randint(1, 2))
                    i +=1
                    j +=1
                    if i >= self.__config.ACTIONSPERPART or j >= amount:
                        break
                sleep(random.randint(self.__config.PARTDELAYMIN, self.__config.PARTDELAYMAX))
        except:
            return Constants.FollowSuggestedError
        return  Constants.OK

    def UnfollowRandom(self, amount): #SUGGESTED_PEOPLE
        j=0
        try:
            while j<amount:
                self.driver.get(self.__config.nav_user_url.format(self.instagramUsername))
                sleep(self.__config.PAGELOADING)
                self.driver.find_element_by_xpath("//a[contains(@href,'/following')]").click()
                sleep(self.__config.PAGELOADING)
                unfollowbuttons=self.driver.find_elements_by_xpath("//button[contains(text(), 'Following')]")
                i=0
                for bt in unfollowbuttons:
                    bt.click()
                    sleep(random.randint(1, 2))
                    self.find_buttons("Unfollow")[0].click()
                    i +=1
                    j +=1
                    if i >= self.__config.ACTIONSPERPART or j >= amount:
                        break
                sleep(random.randint(self.__config.PARTDELAYMIN, self.__config.PARTDELAYMAX))
        except:
            return Constants.FollowSuggestedError
        return  Constants.OK

    def unfollowList(self,usersList, maxFollowers=-1,max=-1):
        i=0
        j=0
        for user in usersList:
            self.driver.get(self.__config.nav_user_url.format(user))
            sleep(self.__config.PAGELOADING)
            try:
                userFollowersTMP=str(self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span').text)
                for ch in userFollowersTMP:
                    if ch=="K" or ch=="k":
                        userFollowersTMP=userFollowersTMP.replace('k', '000')
                        userFollowersTMP=userFollowersTMP.replace('K', '000')
                    elif ch=="M" or ch=="m":
                        userFollowersTMP=userFollowersTMP.replace('m', '000000')
                        userFollowersTMP=userFollowersTMP.replace('M', '000000')
                userFollowersTMP=userFollowersTMP.replace(',', '')
                userFollowersTMP=userFollowersTMP.replace(' ', '')
                if userFollowersTMP.__contains__("."):
                    userFollowersTMP=userFollowersTMP.replace('.', '')
                    userFollowers=int(userFollowersTMP)/10
                else:
                    userFollowers=int(userFollowersTMP)
                if(maxFollowers!=-1 and userFollowers>maxFollowers):
                    continue
                elif max!=-1 and j>max:
                    break
                else:
                    try:
                        self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button')\
                        .click()
                    except:
                        self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[2]/button') \
                            .click()

                    try:
                        sleep(self.__config.PAGELOADING)
                        self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div/div[3]/button[1]").click()
                    except:
                        print("1: Cant Unfollow User: " + user)
                        pass
                    sleep(random.randint(self.__config.ACTIONDELAY, self.__config.ACTIONDELAY+2))
                    i+=1
                    j+=1
                    if i>10:
                        i=0
                        sleep(random.randint(self.__config.PARTDELAYMIN, self.__config.PARTDELAYMAX))
            except:
                print("2: Cant Follow User:{}".format(user))
        return  Constants.OK

    def followList(self,usersList, maxFollowers=-1,max=-1):
        following = self.GetFollowingList()
        toFollow = [user for user in usersList if user not in following]
        i=0
        j=0
        for user in toFollow:
            self.driver.get(self.__config.nav_user_url.format(user))
            sleep(self.__config.PAGELOADING)
            try:
                if(maxFollowers!=-1):
                    userFollowersTMP=str(self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span').text)
                    for ch in userFollowersTMP:
                        if ch=="K" or ch=="k":
                            userFollowersTMP=userFollowersTMP.replace('k', '000')
                            userFollowersTMP=userFollowersTMP.replace('K', '000')
                        elif ch=="M" or ch=="m":
                            userFollowersTMP=userFollowersTMP.replace('m', '000000')
                            userFollowersTMP=userFollowersTMP.replace('M', '000000')
                    userFollowersTMP=userFollowersTMP.replace(',', '')
                    userFollowersTMP=userFollowersTMP.replace(' ', '')
                    if userFollowersTMP.__contains__("."):
                        userFollowersTMP=userFollowersTMP.replace('.', '')
                        userFollowers=int(userFollowersTMP)/10
                    else:
                        userFollowers=int(userFollowersTMP)
                if(maxFollowers!=-1 and userFollowers>maxFollowers):
                    continue
                elif max!=-1 and j>max:
                    break
                else:
                    try:
                        self.driver.find_element_by_xpath("//button[contains(text(), 'Follow')]").click()
                    except:
                        self.driver.find_element_by_xpath("//button[contains(text(), 'Follow Back')]").click()
                    sleep(random.randint(self.__config.ACTIONDELAY, self.__config.ACTIONDELAY+2))
                    i+=1
                    j+=1
                    if i>10:
                        i=0
                        sleep(random.randint(self.__config.PARTDELAYMIN, self.__config.PARTDELAYMAX))
            except:
                print("2: Cant follow User:{}".format(user))

        return  Constants.OK

    def GetFollowingList(self,username=None, refresh=False):
        if(username==None and self.followingLoaded and not refresh):
            return self.followingList
        username = self.instagramUsername if username==None else username
        self.driver.get(self.__config.nav_user_url.format(username))
        sleep(self.__config.PAGELOADING)
        self.driver.find_element_by_xpath("//a[contains(@href,'/following')]").click()
        sleep(self.__config.PAGELOADING)
        sugs = self.driver.find_element_by_xpath('//a[contains(text(), Suggestions)]')
        self.driver.execute_script('arguments[0].scrollIntoView()', sugs)
        sleep(2)
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]")
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(1)
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        # close button
        self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div[1]/div/div[2]/button") \
            .click()
        if(username==None):
            self.followingList=names
            self.followingLoaded=True
        return names

    def GetFollowersList(self,username=None, refresh=False):
        if(username==None and self.followersLoaded and not refresh):
            return self.followersList
        usrname = self.instagramUsername if username==None else username
        self.driver.get(self.__config.nav_user_url.format(usrname))
        sleep(self.__config.PAGELOADING)
        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]").click()
        sleep(self.__config.PAGELOADING)
        sugs = self.driver.find_element_by_xpath('//a[contains(text(), Suggestions)]')
        self.driver.execute_script('arguments[0].scrollIntoView()', sugs)
        sleep(2)
        scroll_box = self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div[2]')
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(1)
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        # close button
        self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div[1]/div/div[2]/button") \
            .click()

        if(username==None):
            self.followersLoaded=True
            self.followersList = names
        return names

    def GetFollowingBackList(self):
        followers = self.GetFollowersList()
        following = self.GetFollowingList()
        following_back = [user for user in following if user in followers]
        return following_back

    def GetNotFollowingBackList(self):
        followers = self.GetFollowersList()
        following = self.GetFollowingList()
        not_following_back = [user for user in following if user not in followers]
        return not_following_back

    def GetFansList(self):
        followers = self.GetFollowersList()
        following = self.GetFollowingList()
        Fans = [user for user in followers if user not in following]
        return Fans

    def infinite_scroll(self):
        """
        Scrolls to the bottom of a users page to load all of their media
        Returns:
            bool: True if the bottom of the page has been reached, else false
        """

        SCROLL_PAUSE_TIME = 1

        self.last_height = self.driver.execute_script("return document.body.scrollHeight")

        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        sleep(SCROLL_PAUSE_TIME)

        print("Last Height: " + str(self.last_height))
        self.new_height = self.driver.execute_script("return document.body.scrollHeight")
        print("New Height: " + str(self.new_height))

        if self.new_height == self.last_height:
            return True

        self.last_height = self.new_height
        return False

    def waitUrl(self,url,max=-1):
        if(max==-1):
            while(self.driver.current_url.__eq__(url)):
                sleep(1)
            return True
        for _ in range(max):
            if(self.driver.current_url.__eq__(url)):
                sleep(1)
            else:
                return True
        return False

    def find_buttons(self, button_text):
        buttons = self.driver.find_elements_by_xpath("//*[text()='{}']".format(button_text))
        return buttons

    def likeLastestPost(self, amount):
        self.driver.get(self.__config.HOME)
        for i in range(0,int(amount)):
            print("i:"+str(i))
            sleep(2)
            try:
                if  i<7:
                    self.driver.find_element_by_xpath("/html/body/div[1]/section/main/section/div/div[2]/div/article[{0}]/div[3]/section[1]/span[1]/button".format(i)).click()
                else:
                    self.driver.find_element_by_xpath("/html/body/div[1]/section/main/section/div/div[2]/div/article[7]/div[3]/section[1]/span[1]/button").click()
            except:
                self.driver.execute_script("window.scroll(0,{0})".format(1000*i))
                print("err")

    def commentLastestPost(self, amount):
        self.driver.get(self.__config.HOME)
        for i in range(1,int(amount)):
            print("i:"+str(i))
            sleep(5)

            if  i<7:                              #/html/body/div[1]/section/main/section/div/div[2]/div/article[1]/div[3]/section[3]/div/form/textarea
                self.driver.find_element_by_xpath("/html/body/div[1]/section/main/section/div/div[2]/div/article[{0}]/div[3]/section[1]/span[1]/button".format(i)).click()
                jsScript_SendInput ='document.querySelector("#react-root > section > main > section > div > div:nth-child(2) > div > article:nth-child({0}) > div.eo2As > section.sH9wk._JgwE > div > form > textarea").click()'
                self.driver.execute_script(jsScript_SendInput.format(i,"Perfect!!"))
                jsScript_SendInput ='document.querySelector("#react-root > section > main > section > div > div:nth-child(2) > div > article:nth-child({0}) > div.eo2As > section.sH9wk._JgwE > div > form > textarea").value = "{1}"'
                self.driver.execute_script(jsScript_SendInput.format(i,"Perfect!!"))
                jsScript_SendInput ='document.querySelector("#react-root > section > main > section > div.cGcGK > div:nth-child(2) > div > article:nth-child({0}) > div.eo2As > section.sH9wk._JgwE > div > form > button").click()'
                self.driver.execute_script(jsScript_SendInput.format(i))
            else:
                self.driver.find_element_by_xpath("/html/body/div[1]/section/main/section/div/div[2]/div/article[7]/div[3]/section[1]/span[1]/button".format(i)).click()
                jsScript_SendInput ='document.querySelector("#react-root > section > main > section > div > div:nth-child(2) > div > article:nth-child({0}) > div.eo2As > section.sH9wk._JgwE > div > form > textarea").click()'
                self.driver.execute_script(jsScript_SendInput.format(7))
                jsScript_SendInput ='document.querySelector("#react-root > section > main > section > div > div:nth-child(2) > div > article:nth-child({0}) > div.eo2As > section.sH9wk._JgwE > div > form > textarea").value = "{1}"'
                self.driver.execute_script(jsScript_SendInput.format(7,"Perfect!!"))
                jsScript_SendInput ='document.querySelector("#react-root > section > main > section > div.cGcGK > div:nth-child(2) > div > article:nth-child({0}) > div.eo2As > section.sH9wk._JgwE > div > form > button").click()'
                self.driver.execute_script(jsScript_SendInput.format(7))
                #self.driver.find_element_by_xpath("/html/body/div[1]/section/main/section/div/div[2]/div/article[7]/div[3]/section[3]/div/form/button".format(i)).click()

    def likeUserPosts(self, user, amount, like=True):

        action = 'Like' if like else 'Unlike'

        self.driver.get(self.__config.nav_user_url.format(user))

        imgs = []
        imgs.extend(self.driver.find_elements_by_class_name('_9AhH0'))

        for img in imgs[:amount]:
            img.click()
            sleep(1)
            try:
                self.driver.find_element_by_xpath("//*[@aria-label='{}']".format(action)).click()
            except Exception as e:
                print(e)

            self.driver.find_element_by_xpath("/html/body/div[5]/div[3]/button").click()

    def viewFriendsStories(self,time):
        self.driver.get(self.__config.HOME)
        self.driver.find_element_by_xpath("/html/body/div[1]/section/main/section/div/div[1]/div/div/div/div/ul/li[8]/div/button").click()
        sleep(time)

    def signUp(self,random=True):
        self.driver.get(self.__config.SIGNUP)
        if random:
            pass

    def saveListToFile(self, list , filename):
        with open(filename, 'a') as filehandle:
            filehandle.writelines("%s\n" % place for place in list)

    def getListFromFile(self, filename):
        places = []
        with open(filename, 'r') as filehandle:
            filecontents = filehandle.readlines()
            for line in filecontents:
                current_place = line[:-1]
                places.append(current_place)
        return  places