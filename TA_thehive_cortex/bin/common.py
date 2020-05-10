import sys
import ta_thehive_cortex_declare_lib
import json
import splunklib.client as client
import logging

class Settings(object):

    def __init__(self, client, logger = None):
        self.logger = logger
        # get settings
        query = {"output_mode":"json"}
        self.__thehive_settings = json.loads(client.get("TA_thehive_cortex_settings/thehive", owner="nobody", app="TA_thehive_cortex",**query).body.read())["entry"][0]["content"]
        self.__cortex_settings = json.loads(client.get("TA_thehive_cortex_settings/cortex", owner="nobody", app="TA_thehive_cortex",**query).body.read())["entry"][0]["content"]
        self.__logging_settings = json.loads(client.get("TA_thehive_cortex_settings/logging", owner="nobody", app="TA_thehive_cortex",**query).body.read())["entry"][0]["content"]
        self.__storage_passwords = client.storage_passwords
        for s in self.__storage_passwords:
            # Get the TheHive API key
            if "thehive_api_key" in s['clear_password']:
                self.__thehive_settings['thehive_api_key'] = str(json.loads(s["clear_password"])["thehive_api_key"])

            # Get the Cortex API key
            if "cortex_api_key" in s['clear_password']:
                self.__cortex_settings['cortex_api_key'] = str(json.loads(s["clear_password"])["cortex_api_key"])

        # Checks before configure
        # TheHive
        cortex_information_required = ["thehive_protocol","thehive_host","thehive_port","thehive_api_key"]
        for i in cortex_information_required:
            if not i in self.__thehive_settings:
                self.logger.warning("[10-FIELD MISSING] TheHive: No \""+i+"\" setting set in \"Configuration\", please configure your Cortex instance under \"Configuration\"")

        # Cortex
        cortex_information_required = ["cortex_protocol","cortex_host","cortex_port","cortex_api_key"]
        for i in cortex_information_required:
            if not i in self.__cortex_settings:
                self.logger.warning("[10-FIELD MISSING] Cortex: No \""+i+"\" setting set in \"Configuration\", please configure your Cortex instance under \"Configuration\"")

        if int(self.getSetting("logging","debug")) == 1:
            logger.setLevel(logging.DEBUG)
            logger.debug("LEVEL changed to DEBUG according to the configuration")

   
    def getTheHiveURL(self):
        """ This function returns the URL of the TheHive instance """
        return self.__thehive_settings["thehive_protocol"]+"://"+self.__thehive_settings["thehive_host"]+":"+self.__thehive_settings["thehive_port"]

    def getTheHiveApiKey(self):
        """ This function returns the API key of the TheHive instance """
        return self.__thehive_settings["thehive_api_key"]

    def getTheHiveCasesMax(self):
        """ This function returns the maximum number of jobs to return of the TheHive instance """
        return self.__thehive_settings["thehive_cases_max"]

    def getTheHiveCasesSort(self):
        """ This function returns the sort key to use for jobs of the TheHive instance """
        return self.__thehive_settings["thehive_cases_sort"]

    def getCortexURL(self):
        """ This function returns the URL of the Cortex instance """
        return self.__cortex_settings["cortex_protocol"]+"://"+self.__cortex_settings["cortex_host"]+":"+self.__cortex_settings["cortex_port"]

    def getCortexApiKey(self):
        """ This function returns the API key of the Cortex instance """
        return self.__cortex_settings["cortex_api_key"]

    def getCortexJobsMax(self):
        """ This function returns the maximum number of jobs to return of the Cortex instance """
        return self.__cortex_settings["cortex_jobs_max"]

    def getCortexJobsSort(self):
        """ This function returns the sort key to use for jobs of the Cortex instance """
        return self.__cortex_settings["cortex_jobs_sort"]

    def getSetting(self, page, key):
        """ This function returns the settings for the concerned page and key """

        result = None
        settings = None
        if (page == "thehive"):
            settings = self.__thehive_settings
        elif (page == "cortex"):
            settings = self.__cortex_settings
        elif (page == "logging"):
            settings = self.__logging_settings
        try:
            result = settings[key]
        except Exception as e:
            self.logger.error("This settings \""+key+"\" doesn't exist for the page "+page)

        return result
