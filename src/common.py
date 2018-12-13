
from parameters import CONF_FILE_INSTANCE
import os

def returnIconPath(image_name):

    return os.getcwd() + "/" + CONF_FILE_INSTANCE["icons"]["folder"] + "/" + \
           CONF_FILE_INSTANCE["icons"]["icons"][image_name]

