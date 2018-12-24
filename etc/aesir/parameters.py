
import json
import os
MAX_START_ARGUMENT = 3
INDICATOR_PID_PATH = "/tmp/aesirindicator.tmp"

CONF_FILE_PATH = os.path.dirname(__file__) + "/confs/conf.json"
ICON_PATH = os.path.dirname(__file__) + "/icons"

CONF_FILE_INSTANCE = json.loads(open(CONF_FILE_PATH).read())


SOFTWARE_THREAD_CHECK_TIMEOUT = 6
SOFTWARE_UPDATER_TIMEOUT = 1