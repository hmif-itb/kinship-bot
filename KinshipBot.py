from linebot.api import LineBotApi
from SpreadsheetService import SpreadsheetService
from MemeService import MemeService
from linebot.models.send_messages import TextSendMessage, ImageSendMessage
from ImageService import ImageService
from utils import Message, text_contains
import time
import random
import os
import sys


CONFIG_KEYS = ['LINE_SECRET_TOKEN', 'LINE_ACCESS_TOKEN',
               'IMGBB_API_KEY', 'SPREADSHEET_SCRIPT_API']


class KinshipBot:
    imgService = None
    lineBotService = None
    memeService = None
    spreadsheetService = None
    Config = dict()
    message = Message()

    def __init__(self):
        if ('--dev' in sys.argv):
            with open('.env', 'r') as envfile:
                envs = envfile.read()
                for env in envs.split('\n'):
                    keypair = env.split('=')
                    self.Config[keypair[0]] = keypair[1]
            for key in CONFIG_KEYS:
                if (key not in self.Config):
                    raise Exception('{} not found in .env'.format(key))
        else:
            for key in CONFIG_KEYS:
                self.Config[key] = os.environ[key]
        self.imgService = ImageService(self.Config['IMGBB_API_KEY'])
        self.memeService = MemeService()
        self.spreadsheetService = SpreadsheetService(
            self.Config['SPREADSHEET_SCRIPT_API'])

    def setLineBot(self, lineBot: LineBotApi):
        self.lineBotService = lineBot

    def handleMessage(self, event, msg: str):
        payload = ("Nothing",)
        msg = msg.lower()
        if (not('bot' in msg) or 'http' in msg or 'https' in msg):
            return
        if ('help' in msg):
            payload = ("ReplyText", "Apa yang bisa dibantu?\nFoto: 'bot bagi foto nim xxx' atau 'bagi foto nim xxx dong bot'\n\nCek ultah: 'bot, siapa yang ultah hari ini?'\nSupported keyword: hari ini, besok, kemarin, lusa, lusa kemarin, x hari lagi, x hari lalu, minggu depan, minggu lalu\n\nSearch by nama panggilan: 'bot, bagi data dengan nama xxx' atau 'bagi data dengan nama xxx dong bot'\n\nKalau mau meme: 'bot, bagi meme dong' atau 'bagi meme ya bot'\n\nKalau mau dad jokes: 'bot, bagi jokes bapak2' atau 'bagi jokes bapak bapak dong bot'\n\nHal-hal umum seperti: 'hai bot', 'gws bot', 'thank you bot' juga akan gue balas\n\nKalau mau tau cari jodoh: 'bot siapa jodoh gue?' atau 'siapa jodoh kosar bot?'\n\nTanya pendapat ke bot: 'bot, apakah ...'")
        elif text_contains(msg, ['bagi', 'meme'], series=True, max_len=100):
            payload = self.memeService.reply()
            #foundNumber = False
            # for i in range(5, 0, -1):
            # if (str(i) in msg):
            #self.reply(event, ("Text", [self.message.MemeWait(i)]))
            #payload = self.memeService.reply(i)
            #foundNumber = True
            # break
            # if not(foundNumber):
            #self.reply(event, ("Text", [self.message.MemeWait()]))
            #payload = self.memeService.reply()

        elif text_contains(msg, ['bagi', 'data', 'nama'], series=True, max_len=150):
            splitMsg = msg.split(" ")
            try:
                idx = splitMsg.index("nama")
                if (idx+1 <= len(splitMsg)-1):
                    pg = splitMsg[idx+1]
                    # self.reply(
                    #    event, ("Text", [self.message.FindWait()]))
                    payload = self.spreadsheetService.replyData(pg)
            except ValueError:
                payload = ("Nothing",)
        elif text_contains(msg, ['siapa', 'jodoh'], series=True, max_len=150):
            self.reply(event, ("ReplyText", self.message.NamaOrang()))
        elif text_contains(msg, ['bagi', 'jokes', 'bapak'], series=True, max_len=150) or text_contains(msg, ['bagi', 'jokes', 'bapak2'], series=True, max_len=150):
            self.reply(
                event, ("ReplyImage", "https://jokesbapak2.herokuapp.com/v1/id/" + str(random.randint(1, 154))))
        elif text_contains(msg, ['bagi', 'foto', 'nim'], series=True, max_len=150):
            splitMsg = msg.split(" ")
            try:
                idx = splitMsg.index("nim")
                if (idx+1 <= len(splitMsg)-1):
                    nim = int(splitMsg[idx+1])
                    # self.reply(
                    #    event, ("Text", [self.message.EditWait(nim)]))
                    payload = self.spreadsheetService.getPhotoByNIM(nim)
            except ValueError:
                payload = ("Nothing",)
        elif text_contains(msg, ['siapa', 'ultah'], series=True, max_len=150):
            #self.reply(event, ("Text", [self.message.FindWait()]))
            if text_contains(msg, ['besok'], series=True, max_len=150):
                payload = self.spreadsheetService.reply(1)
            elif text_contains(msg, ['lusa', 'kemarin'], series=True, max_len=150):
                payload = self.spreadsheetService.reply(-2)
            elif text_contains(msg, ['lusa'], series=True, max_len=150):
                payload = self.spreadsheetService.reply(2)
            elif text_contains(msg, ['minggu', 'depan'], series=True, max_len=150):
                payload = self.spreadsheetService.reply(7)
            elif text_contains(msg, ['minggu', 'lalu'], series=True, max_len=150):
                payload = self.spreadsheetService.reply(-7)
            elif text_contains(msg, ['hari', 'lalu'], series=True, max_len=150):
                splitMsg = msg.split(" ")
                try:
                    idx = splitMsg.index("hari")
                    if (idx >= 1):
                        hari = int(splitMsg[idx-1])
                        payload = self.spreadsheetService.reply(hari * -1)
                except ValueError:
                    payload = ("Nothing",)
            elif text_contains(msg, ['hari', 'lagi'], series=True, max_len=150):
                splitMsg = msg.split(" ")
                try:
                    idx = splitMsg.index("hari")
                    if (idx >= 1):
                        hari = int(splitMsg[idx-1])
                        payload = self.spreadsheetService.reply(hari)
                except ValueError:
                    payload = ("Nothing",)
            elif text_contains(msg, ['kemarin'], series=True, max_len=150):
                payload = self.spreadsheetService.reply(-1)
            else:
                payload = self.spreadsheetService.reply()
        elif text_contains(msg, ['apakah'], series=True, max_len=150):
            self.reply(event, ("ReplyText", self.message.YesOrNo()))
        elif ('hai' in msg or 'halo' in msg or 'hi' in msg):
            self.reply(event, ("ReplyText", self.message.Hai()))
        elif ('gws' in msg or 'get well soon' in msg):
            self.reply(event, ("ReplyText", self.message.Thankyou()))
        elif ('makasih' in msg
              or 'thx' in msg
              or 'thanks' in msg
              or 'thank you' in msg
              or 'terima kasih' in msg
              or 'terimakasih' in msg):
            self.reply(event, ("ReplyText", self.message.Welcome()))

        self.reply(event, payload)

    def reply(self, event, data: tuple):
        if (data[0] == "Nothing"):
            return

        if (len(data) != 2):
            raise Exception("payload should be length of 2")

        if (data[0] == "ReplyImage"):
            self.lineBotService.reply_message(
                event.reply_token,
                ImageSendMessage(data[1], data[1])
            )
        elif (data[0] == "UnprocessedImage"):
            rawOutput = None
            if (len(data[1][0]) <= 4):
                rawOutput = self.imgService.getUnknownPhoto()
            else:
                rawOutput = self.imgService.getPhoto(data[1][0])
            output = self.imgService.resize(rawOutput,)
            edited = self.imgService.editPhoto(
                output, str(data[1][1]), data[1][2])
            result = self.imgService.upload(edited)
            if (result.startswith("Error:")):
                self.reply(event, ("ReplyText", result))
            else:
                self.reply(event, ("ReplyImage", result))
        elif (data[0] == "ReplyText"):
            self.lineBotService.reply_message(
                event.reply_token, TextSendMessage(text=data[1]))
        elif (data[0] == "Text" or data[0] == "Image"):
            sourceType = event.source.type
            sourceId = ""
            if (sourceType == "user"):
                sourceId = event.source.user_id
            elif (sourceType == "group"):
                sourceId = event.source.group_id

            sendItem = []
            if (data[0] == "Text"):
                for item in data[1]:
                    sendItem.append(TextSendMessage(text=item))
            elif (data[0] == "Image"):
                for item in data[1]:
                    sendItem.append(ImageSendMessage(item, item))

            if (sourceId != "" and len(sendItem) != 0):
                for msgQueue in sendItem:
                    self.lineBotService.push_message(sourceId, msgQueue)
                    time.sleep(0.75)
