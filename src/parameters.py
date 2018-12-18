
import json

MAX_START_ARGUMENT = 3
INDICATOR_PID_PATH = "/tmp/aesirindicator.tmp"
CONF_FILE = "/home/firat/Desktop/AESIR_Screenshot/src/conf.json"
SOFTWARE_THREAD_CHECK_TIMEOUT = 6
SOFTWARE_UPDATER_TIMEOUT = 1
CONF_FILE_INSTANCE = json.loads(open("/home/firat/Desktop/AESIR_Screenshot/src/conf.json").read())