from utils import Message
import requests


class SpreadsheetService:
    spreadsheetScriptAPI = ""
    message = Message()

    def __init__(self, spreadsheetScriptAPI):
        self.spreadsheetScriptAPI = spreadsheetScriptAPI

    def checkUltah(self, delta=None):
        postData = dict()
        postData['targetSheet'] = "ALL"
        if (delta != None):
            postData['delta'] = int(delta)

        try:
            resp = requests.get(self.spreadsheetScriptAPI,
                                params=postData, verify=True)
            result = resp.json()
            return result
        except:
            return None

    def getData(self, nim: int):
        postData = dict()
        postData['action'] = 'data'
        postData['nim'] = nim

        try:
            resp = requests.get(self.spreadsheetScriptAPI,
                                params=postData, verify=True)
            result = resp.json()
            if 'error' in result.keys():
                return dict()
            return result
        except:
            return None

    def reply(self, delta=None):
        orang = self.checkUltah(delta)
        if (len(orang["Result"]) == 0):
            return ("Text", [self.message.NoBirthday()])
        text = "Ulang tahun " + orang["Date"] + "\n"
        i = 0
        for o in orang["Result"]:
            if (i > 0):
                text += "\n"
            text += "{} - {}".format(o["NIM"], o["Nama"])
            i += 1
        return ("Text", [text])

    def getPhoto(self, nim: int):
        data = self.getData(nim)
        if (data == None):
            return ("ReplyText", "Something went wrong")
        if (len(data.keys()) == 0):
            return ("ReplyText", self.message.NIMNotFound(nim))
        return ("UnprocessedImage", [data['Foto'], data['NIM'], data['Nama']])
