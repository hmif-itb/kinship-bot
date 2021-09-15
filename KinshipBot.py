from linebot.api import LineBotApi
from SpreadsheetService import SpreadsheetService
from MemeService import MemeService
from linebot.models.send_messages import TextSendMessage, ImageSendMessage
from ImageService import ImageService
from utils import text_contains
import time
import random
import os
import sys


CONFIG_KEYS = ['LINE_SECRET_TOKEN', 'LINE_ACCESS_TOKEN',
               'IMGBB_API_KEY', 'SPREADSHEET_SCRIPT_API', 'GROUP_ID_AUTO_REMINDER']


class KinshipBot:
    imgService = None
    lineBotService = None
    memeService = None
    spreadsheetService = None
    Config = dict()

    def __init__(self):
        print(sys.argv)
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
        print(self.Config)

    def setLineBot(self, lineBot: LineBotApi):
        self.lineBotService = lineBot

    def handleMessage(self, event, msg: str):
        payload = ("Nothing",)
        msg = msg.lower()
        if text_contains(msg, ['bagi', 'meme'], series=True, max_len=100):
            foundNumber = False
            for i in range(10, 0, -1):
                if (str(i) in msg):
                    self.reply(event, ("Text", ["Nih gue kasih " +
                                                str(i) + " meme, sabar yak, dicari duls"]))
                    payload = self.memeService.reply(i)
                    foundNumber = True
                    break
            if not(foundNumber):
                self.reply(event, ("Text", ["Bentar yak, nyari meme duls"]))
                payload = self.memeService.reply()
        elif text_contains(msg, ['hai', 'bot'], series=True, max_len=150):
            self.reply(event, ("ReplyText", "halo juga"))
        elif text_contains(msg, ['siapa', 'jodoh'], series=True, max_len=150):
            self.reply(event, ("ReplyText", "kotsar"))
        elif text_contains(msg, ['bagi', 'jokes', 'bapak'], series=True, max_len=150):
            self.reply(
                event, ("Image", ["https://jokesbapak2.herokuapp.com/v1/id/" + str(random.randint(1, 154))]))
        elif text_contains(msg, ['bagi', 'foto', 'nim'], series=True, max_len=150):
            splitMsg = msg.split(" ")
            try:
                idx = splitMsg.index("nim")
                if (idx+1 <= len(splitMsg)-1):
                    nim = int(splitMsg[idx+1])
                    self.reply(
                        event, ("Text", ["Bentar lagi diedit foto nim " + str(nim)]))
                    payload = self.spreadsheetService.getPhoto(nim)
            except ValueError:
                payload = ("Nothing",)
        elif text_contains(msg, ['siapa', 'ultah'], series=True, max_len=150):
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
                self.reply(event, ("Text", [result]))
            else:
                self.reply(event, ("Image", [result]))
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
                    time.sleep(0.5)
