import requests
import configparser
import sys

from datetime import datetime
from requests.auth import HTTPBasicAuth

def exit_w_error(message):
    errFile = open("ErrorLog.txt", "a")
    errFile.write(str(datetime.now())+' '+message+'\n')
    errFile.close()
    sys.exit(1)

class TogglConfig(object):
    """Loads Toggl info"""

    def __init__(self, cfg_path):
        config = configparser.ConfigParser()
        config.read(cfg_path)

        if "Toggl Info" in config and "ApiToken" in config["Toggl Info"]:
            self.API_TOKEN = config["Toggl Info"]["ApiToken"]
        else:
            exit_w_error("Missing ApiToken")

        if "Toggl Info" in config and "PID" in config["Toggl Info"]:
            self.PID = config["Toggl Info"]["PID"]
        else:
            exit_w_error("Missing Project ID")

        if "Settings" in config and "DefaultDescription" in config["Settings"]:
            self.DEFAULT_DESCRIPTION = config["Settings"]["DefaultDescription"]
        else:
            self.DEFAULT_DESCRIPTION = "Clicking Circles to the Beat!"

        if "Settings" in config and "SongAsDescription" in config["Settings"] \
          and config["Settings"]["SongAsDescription"] == "0":
            self.SONG_AS_DESCRIPTION = False
        else:
            self.SONG_AS_DESCRIPTION = True

class TogglAPI(object):
    """A wrapper for Toggl Api"""

    def __init__(self, api_token):
        self.api_token = api_token

    def _make_url(self, section):
        url = 'https://www.toggl.com/api/v8/{}'.format(section)
        return url

    def _make_auth(self):
        return HTTPBasicAuth(self.api_token, 'api_token')

    ## Time Entry functions
    def _start_time_entry(self, description='', tags=[], pid=0, program_name=''):
        url = self._make_url(section='time_entries/start')
        data = '[(["time_entry":[(["description":"{0}","tags":{1},"pid":{2},"created_with":"{3}"])]])]'.format(description, [], pid, program_name)
        data = data.replace("[([","{")
        data = data.replace("])]","}")
        r = requests.post(url, headers={'content-type': 'application/json'}, 
          data=data, auth=self._make_auth())
        return r.json()

    def _stop_time_entry(self, tid=0):
        url = self._make_url('time_entries/{}/stop'.format(tid))
        r = requests.put(url, headers={'content-type': 'application/json'}, 
          auth=self._make_auth())
        return r.json()