from utils import Message
import requests


class SpreadsheetService:
    spreadsheetScriptAPI = ""
    message = Message()

    def __init__(self, spreadsheetScriptAPI):
        self.spreadsheetScriptAPI = spreadsheetScriptAPI

    def checkUltah(self, delta=None):
        postData = dict()
        postData['action'] = 'getByDate'
        if (delta != None):
            postData['delta'] = int(delta)

        try:
            resp = requests.get(self.spreadsheetScriptAPI,
                                params=postData, verify=True)
            result = resp.json()
            return result
        except:
            return None

    def getDataByNIM(self, nim: int):
        postData = dict()
        postData['action'] = 'getByNIM'
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

    def getDataByPanggilan(self, panggilan: str):
        postData = dict()
        postData['action'] = 'getByPanggilan'
        postData['panggilan'] = panggilan

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
        return ("ReplyText", text)

    def getPhotoByNIM(self, nim: int):
        data = self.getDataByNIM(nim)
        if (data == None):
            return ("ReplyText", "Something went wrong")
        if (len(data.keys()) == 0):
            return ("ReplyText", self.message.NIMNotFound(nim))
        return ("UnprocessedImage", [data['Foto'], data['NIM'], data['Nama']])

    def replyData(self, panggilan):
        result = self.getDataByPanggilan(panggilan)
        if (result == None):
            return ("ReplyText", "Something went wrong")
        if (len(result['Result']) == 0):
            return ("ReplyText", self.message.PanggilanNotFound(panggilan))
        if (len(result['Result']) >= 40):
            return ("ReplyText", "Nama panggilan yang ditulis terlalu general")

        dateToName = dict()
        for i in result['Result']:
            if (i['Ultah'] in dateToName.keys()):
                dateToName[i['Ultah']] += "\n{} - {} ({})".format(
                    i['NIM'], i['Nama'], i['Panggilan'])
            else:
                dateToName[i['Ultah']] = "{}\n{} - {} ({})".format(
                    i['Ultah'], i['NIM'], i['Nama'], i['Panggilan'])

        msg = "Data nama panggilan '{}'\n".format(panggilan)
        i = 0
        for k in dateToName:
            if (i > 0):
                msg += "\n\n"
            msg += dateToName[k]
            i += 1
        return ("ReplyText", msg)
