import configparser

class config:
    __config_file_path = "./config.ini"

    def __init__(self):

        path = self.__config_file_path.split('.')
        assert(path[len(path)-1] == 'ini')
        self.__config = configparser.ConfigParser()
        self.__config.read(self.__config_file_path)

        self.login_url =        self.__config['IG_URLS']['LOGIN']
        self.nav_user_url =     self.__config['IG_URLS']['NAV_USER']
        self.get_tag_url =      self.__config['IG_URLS']['SEARCH_TAGS']
        self.SuggestedPeople =  self.__config['IG_URLS']['SUGGESTED_PEOPLE']
        self.HOME =             self.__config['IG_URLS']['HOME']
        self.SIGNUP =           self.__config['IG_URLS']['SIGNUP']

        self.instagramUsername = self.__config['IG_AUTH']['USERNAME']
        self.instagramPassword = self.__config['IG_AUTH']['PASSWORD']

        self.ChromeDriverPath=  self.__config['ENVIRONMENT']['CHROMEDRIVER_PATH']
        self.HMAPath =          self.__config['ENVIRONMENT']['HMAPATH']

        self.PAGELOADING =      int(self.__config['IG_DELAYS']['PAGELOADING'])
        self.ACTIONDELAY =      int(self.__config['IG_DELAYS']['ACTIONDELAY'])
        self.ACTIONSPERPART =   int(self.__config['IG_DELAYS']['ACTIONSPERPART'])
        self.PARTDELAYMIN =     int(self.__config['IG_DELAYS']['PARTDELAYMIN'])
        self.PARTDELAYMAX =     int(self.__config['IG_DELAYS']['PARTDELAYMAX'])

