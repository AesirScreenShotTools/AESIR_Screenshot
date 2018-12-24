import json  # json parsellemek icin kullanılan phyton kütüphanesidir.

from parameters import CONF_FILE_INSTANCE


class confReader:


    def getConfigFileContext(self):
        try:
            print(self.conf_file_path)
            self.conf_file = open(self.conf_file_path).read()
            return json.loads(self.conf_file)
        except IOError:
            print("Configuration file not found.")
            return None
        except ValueError:
            print("Configuration file corrupted")
            return None

    def parseJson(self, data):

        return json.loads(data)


    def getJsonValue(self, token):
        context = self.getConfigFileContext()
        return context[token]


    def fileToJsonData(self, data):
        try:
            json_data = json.loads(data)
            return json_data
        except:
            return None

    def __init__(self, configuration_file_path):
        self.conf_file_path = configuration_file_path;
        CONF_FILE_INSTANCE = self.getConfigFileContext()
