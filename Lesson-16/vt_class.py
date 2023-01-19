import base64
import datetime
import json
import os

import requests
import validators

class VT():


    def __init__(self):
        self._db_path = 'vt_database.json'
        self._db = {}   # Need an explanation how to store the information
        #                 url_id : {      "url" : str,
        #                                 "reputation" : float,
        #                                 "last_analysis_date" : datetime, //in UTC
        #                                 "last_analysis_stats": {
        #                                                   "harmless": 77,
        #                                                   "malicious": 0,
        #                                                   "suspicious": 0,
        #                                                   "undetected": 13,
        #                                                   "timeout": 0
        #                                                   }
        #                           }

        self._rescan_period_days = 178 # 178 = 6 month

        with open (os.environ['VT_KEY'], 'r') as fh:
            self._vt_api_key = fh.read()

        self._base_vt_url = "https://www.virustotal.com/api/v3/urls"
        self._base_vt_url_analysis = "https://www.virustotal.com/api/v3/analyses"
        self._base_vt_url_user_quota = "https://www.virustotal.com/api/v3/users"
        self._headers = {
                            "accept": "application/json",
                            "content-type": "application/x-www-form-urlencoded",
                            "x-apikey": self._vt_api_key
                            }
        self._



    def _load_scan_db(self):
        """
        Loads file with previous scanned URLs from database.
        If file does not exist returns ???
        """
        with open(self._db_path, 'r') as fh:
            self._db = json.load(fh)

    def _save_scanned_db(self):
        """
        Stores the updated database of scanned URLs into file
        """
        with open(self._db_path, 'w') as fh:
            json.dump(self._db,fh)

    @staticmethod
    def _get_base64_encoded_url_id(url:str) -> str:
        """
        Encoding URL string into urlsafe string , which will be provided as ID for a scan to
        VirusTotal's API
        """
        return base64.urlsafe_b64encode('https://edulabs.co.il'.encode()).decode().strip('=')

    def _is_rescan_period_expired(self) -> bool:
        """
        Checks if time period between scans has expired
        """
        if (datetime.datetime.utcnow() - self._db["last_analysis_date"]).days> self._rescan_period_days:
            return True
        return False

    def _scan_urls(self, url_list :[str]):
        """
        Sends SCAN request to VirusTotal API and updates database.
        """
        pass

    @staticmethod
    def _response_handler(response):
        if response.status_code == 404:
            raise Exception(f"404 - NotFoundError = The requested resource was not found.")
        if response.status_code>=400:
            response_json = json.loads(response.text)
            raise Exception(f"Error: {response.status_code}\n"
                            f"Error code: {response_json['error']['code']}\n"
                            f"VirusTotal message: {response_json['error']['message']}\n")

    def _get_users_request_quota(self):
        url_users = os.path.join(self._base_vt_url_user_quota,self._vt_api_key)
        response = requests.get(url_users,headers=self._headers)
        self._response_handler(response=response)


    def _get_url_analysis_from_vt(self,url_id:str):
        url = os.path.join(self._base_vt_url,url_id)
        response = requests.get(url,headers=self._headers)

        # Add validation regarding the response
        # according to errors from VT https://developers.virustotal.com/reference/errors



        response_json = json.loads(response.text)
        self._db[url_id]["reputation"] = response_json["data"]["attributes"]["reputation"]

        # Getting timestamp data
        last_analysis_date_timestamp = response_json["data"]["attributes"]["last_analysis_date"]
        self._db[url_id]["last_analysis_date"] = datetime.datetime.fromtimestamp(last_analysis_date_timestamp)

        self._db[url_id]["last_analysis_date"] = response_json["data"]["attributes"]["last_analysis_stats"]

    def get_url_reputation(self, url_list:[str]):

        # Check if URL is valid
        # Get url_id (encoded base64)
        # If url_id exist and date of last scan not exceeds the _rescan_period -> return reputation
        #       > url_id not exist -> Get a URL analysis report from VirusTotal API
        #           >> Analysis exist and last scan not exceeds the _rescan_period -> return reputation
        #           >> Analysis exist but last scan exceeds the _rescan_period ->
        #                   >>> Request headers from url -> check if last update of URL is different from Last update from analysis
        #                           >>>> If not different -> return value of analysis
        #                           >>>> If different -> request to Scan
        #           >> Analysis not exists -> request to Scan
        # If url_id exist and date of last scan exceeds the _rescan_period ->
        #       >  Request headers from url -> check if last update of URL is different from Last update from analysis
        #                           >>>> If not different -> return value of reputation from database
        #                           >>>> If different -> request (Analysis or Scan and then Analysis)?
        pass

if __name__ == '__main__':
    my_vt = VT()


