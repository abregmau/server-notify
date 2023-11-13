import configparser
import os
import logging


class botConfig:
    def __init__(self, cfg_name):
        
        # Init config
        CFG_FL_NAME = cfg_name
        USER_CFG_SECTION = "GENERAL_USER_CONFIG"
        config = configparser.ConfigParser()

        if not os.path.exists(CFG_FL_NAME):
            print("No configuration file (user.cfg) found! See README.")
            exit()
        else:
            config.read(CFG_FL_NAME)
        
        loggingLevel = config.get(USER_CFG_SECTION, "LOGGING_LEVEL")
        if loggingLevel == "DEBUG":
            self.loggingLevel = logging.DEBUG
        elif loggingLevel == "INFO":
            self.loggingLevel = logging.INFO
        elif loggingLevel == "WARNING":
            self.loggingLevel = logging.WARNING
        elif loggingLevel == "ERROR":
            self.loggingLevel = logging.ERROR
        elif loggingLevel == "CRITICAL":
            self.loggingLevel = logging.CRITICAL
        else:
            self.loggingLevel == logging.WARNING

        self.telebotKey = config.get(USER_CFG_SECTION, "TELEBOT_KEY")
        self.allowedUserIds = config.get(USER_CFG_SECTION, "ALLOWED_TELEGRAM_IDS")