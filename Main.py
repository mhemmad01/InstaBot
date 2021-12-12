from InstaBot import InstaBot
from vpn import *
from time import  sleep

def Main():

    #bot.AddPeopleFromSuggested(3)
    #bot.UnfollowRandom(3)
    #following = bot.GetFollowersList()
    #followers = bot.GetFollowingList()
    #not_following_back = bot.GetNotFollowingBackList()
    #bot.followList(bot.GetFansList())
    #bot.followList(["kheir_abeed21"])

    '''
    connection = VpnConnect.getInstance()
    class myMethod(vpnMethod):
        def __init__(self,max):
            vpnMethod.__init__(self)


        def method(self):
            bot = InstaBot()
            bot.login()
            bot.viewFriendsStories(10)
            self.stop()

    method = myMethod(2)
    connection.startAction(method)


    bot = InstaBot()
    bot.login()
    following=bot.GetFollowingList(username="filmygyan")
    followers=bot.GetFollowersList(username="aditisharma8865")
    bot.saveListToFile(followers,"follower.txt")
    bot.saveListToFile(following,"follower.txt")

    saved =bot.getListFromFile("followers.txt")
    i=0
    for usr in saved:
        print("{0} : {1}".format(i,usr))
        i+=1


    bot = InstaBot()
    bot.login()
    targetList= ['Clickus_dm','_shirshivuk','Yonicohen_dolead','tagshark','digi_tili','_shivuki_']
    for usr in targetList:
        try:
            print("Getting followers for ther user: " + usr)
            followers=bot.GetFollowersList(username=usr)
            bot.saveListToFile(followers,"targetlist.txt")
        except:
            print("Error in user: " + usr)
            traceback.print_stack()

    saved = bot.getListFromFile("targetList.txt")
    i=0
    for usr in saved:
        print("{0} : {1}".format(i,usr))
        i+=1

    bot = InstaBot()
    saved = bot.getListFromFile("targetList.txt")
    for i in range (1,400):
        print("{0} : {1}".format(i,saved[5*(i-1):5*i]))
    '''

    bot = InstaBot()
    bot.login()
    input("press enter to contiue")

data_list=[ ["Mhemmad" , "207723099", 20, 0 , 0], ["3" , "rere", 20, 1 , 0], ["2" , "3r3", 50, 1 , 2]]


def getInfo1(data, age1, age2, sex):
    myList = []
    for i in range(len(data)):
        if data[i][2]<=age2 and  data[i][2]>=age1 and data[i][3]==sex and data[i][4]==2:
            myList.append(data[i][1])
    return len(myList),myList


age1= input("age 1?")
age2= input("age 2?")
sex= input("sex?")
count, myList = getInfo1(data_list, int(age1), int(age2), int(sex))
print(count, end=": ")
for i in myList:
    print(i, end=" ")



def getInfo(data, age1, age2):
    listMale = []
    listFemale = []
    for i in range(len(data)):
        if data[i][2]<=age2 and  data[i][2]>=age1 and data[i][3]==0 and data[i][4]==0:
            listMale.append(data[i][1])
        if data[i][2]<=age2 and  data[i][2]>=age1 and data[i][3]==1 and data[i][4]==0:
            listFemale.append(data[i][1])
    return listFemale, listMale


age1= input("age 1?")
age2= input("age 2?")
listFemale, listMale = getInfo(data_list, int(age1), int(age2))

print(len(listFemale), end=": ")
for i in listFemale:
    print(i, end=" ")

print(len(listMale), end=": ")
for i in listMale:
    print(i, end=" ")

if __name__ == "__main__":


    pass
    # Main()
