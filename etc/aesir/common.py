
from parameters import CONF_FILE_INSTANCE
import os


from pathlib import Path


def returnIconPath(image_name):

    x= str(os.path.dirname(os.path.realpath(__file__))) + "/" + CONF_FILE_INSTANCE["icons"]["folder"] + "/" + \
           CONF_FILE_INSTANCE["icons"]["icons"][image_name]
    print(x)
    return x




class aesirPathManager:
    def __init__(self):
        pass

    def returnHomePath(self):
        return str(Path.home())

    def returnImageSavePath(self):

        directory = self.returnHomePath() + "/Aesir/"

        try:
            if not os.path.exists(directory):
                os.makedirs(directory)

            return directory
        except:
            return None

