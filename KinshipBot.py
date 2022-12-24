from MagicConchShellService import MagicConchShellService
from linebot.api import LineBotApi
from SpreadsheetService import SpreadsheetService
from MemeService import MemeService
from linebot.models.send_messages import TextSendMessage, ImageSendMessage
from ImageService import ImageService
from utils import Message, text_contains
from random import randint
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
    mcsService = MagicConchShellService()

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
        msg = msg.replace("bot,", "bot ")
        msg = msg.replace("bot?", "bot ")
        msgSplit = msg.split(" ")
        if (not('bot' in msgSplit) or 'http' in msgSplit or 'https' in msgSplit):
            return
        if ('help' in msgSplit):
            payload = ("ReplyText", "Apa yang bisa dibantu?\nFoto: 'bot bagi foto nim xxx' atau 'bagi foto nim xxx dong bot'\n\nCek ultah: 'bot, siapa yang ultah hari ini?'\nSupported keyword: hari ini, besok, kemarin, lusa, lusa kemarin, x hari lagi, x hari lalu, minggu depan, minggu lalu\n\nCek ultah dalam range: 'bot, cek ultah x hari lagi'\nSupported Keyword: x hari lagi, x hari lalu\n\nSearch by nama panggilan: 'bot, bagi data dengan nama xxx' atau 'bagi data dengan nama xxx dong bot'\n\nKalau mau meme: 'bot, bagi meme dong' atau 'bagi meme ya bot'\n\nKalau mau dad jokes: 'bot, bagi jokes bapak2' atau 'bagi jokes bapak bapak dong bot'\n\nHal-hal umum seperti: 'hai bot', 'gws bot', 'thank you bot' juga akan gue balas\n\nKalau mau tanya siapa: 'bot siapa jodoh gue?' atau 'siapa jodoh kosar bot?'\n\nTanya pendapat ke bot: 'bot, apakah ...'\n\nButuh quote? 'bot, bagi quote dong'\n\nKalau mau this/that? 'bot pilih ... atau ... (atau ...)'\n\nMinta bot ngerating: 'bot, kasih rating buat ... dong'\n\nKalau mau generate random number: 'dari ... sampai ... berapa ...'\n\nDeskripsi random: 'bot, deskripsikan ...'\n\nMinta pendapat: 'bot, apa pendapat bot tentang ...?")
        elif text_contains(msg, ['bagi', 'meme'], max_len=100):
            payload = self.memeService.reply()
            # foundNumber = False
            # for i in range(5, 0, -1):
            # if (str(i) in msgSplit):
            # self.reply(event, ("Text", [self.message.MemeWait(i)]))
            # payload = self.memeService.reply(i)
            # foundNumber = True
            # break
            # if not(foundNumber):
            # self.reply(event, ("Text", [self.message.MemeWait()]))
            # payload = self.memeService.reply()

        elif text_contains(msg, ['bagi', 'data', 'nama']):
            splitMsg = msgSplit.copy()
            try:
                idx = splitMsg.index("nama")
                if (idx+1 <= len(splitMsg)-1):
                    pg = splitMsg[idx+1]
                    # self.reply(
                    #    event, ("Text", [self.message.FindWait()]))
                    payload = self.spreadsheetService.replyData(pg)
            except ValueError:
                payload = ("Nothing",)
        elif (text_contains(msg, ['bagi', 'quote'])
              or text_contains(msg, ['bagi', 'kata', 'bijak'])
              or text_contains(msg, ['bagi', 'kata2', 'bijak'])):
            x = randint(1, 10)
            if (x % 2 == 0):
                self.reply(event, ("ReplyText", self.message.AnimeQuote()))
            else:
                self.reply(event, ("ReplyText", self.message.Quote()))
        elif text_contains(msg, ['bagi', 'jokes', 'bapak']) or text_contains(msg, ['bagi', 'jokes', 'bapak2']):
            self.reply(
                event, ("ReplyImage", "https://jokesbapak2.herokuapp.com/v1/id/" + str(random.randint(1, 154))))
        elif text_contains(msg, ['bagi', 'foto', 'nim']):
            splitMsg = msgSplit.copy()
            try:
                idx = splitMsg.index("nim")
                if (idx+1 <= len(splitMsg)-1):
                    nim = int(splitMsg[idx+1])
                    # self.reply(
                    #    event, ("Text", [self.message.EditWait(nim)]))
                    payload = self.spreadsheetService.getPhotoByNIM(nim)
            except ValueError:
                payload = ("Nothing",)
        elif text_contains(msg, ['cek', 'ultah']) or text_contains(msg, ['check', 'ultah']):
            if text_contains(msg, ['hari', 'lalu']):
                splitMsg = msgSplit.copy()
                try:
                    idx = splitMsg.index("hari")
                    if (idx >= 1):
                        hari = int(splitMsg[idx-1])
                        payload = self.spreadsheetService.replyUltahInRange(
                            hari * -1)
                except ValueError:
                    payload = ("Nothing",)
            elif text_contains(msg, ['hari', 'lagi']):
                splitMsg = msgSplit.copy()
                try:
                    idx = splitMsg.index("hari")
                    if (idx >= 1):
                        hari = int(splitMsg[idx-1])
                        payload = self.spreadsheetService.replyUltahInRange(
                            hari)
                except ValueError:
                    payload = ("Nothing",)
        elif text_contains(msg, ['siapa', 'ultah']):
            #self.reply(event, ("Text", [self.message.FindWait()]))
            if text_contains(msg, ['besok']):
                payload = self.spreadsheetService.reply(1)
            elif text_contains(msg, ['lusa', 'kemarin']):
                payload = self.spreadsheetService.reply(-2)
            elif text_contains(msg, ['lusa']):
                payload = self.spreadsheetService.reply(2)
            elif text_contains(msg, ['minggu', 'depan']):
                payload = self.spreadsheetService.reply(7)
            elif text_contains(msg, ['minggu', 'lalu']):
                payload = self.spreadsheetService.reply(-7)
            elif text_contains(msg, ['hari', 'lalu']):
                splitMsg = msgSplit.copy()
                try:
                    idx = splitMsg.index("hari")
                    if (idx >= 1):
                        hari = int(splitMsg[idx-1])
                        payload = self.spreadsheetService.reply(hari * -1)
                except ValueError:
                    payload = ("Nothing",)
            elif text_contains(msg, ['hari', 'lagi']):
                splitMsg = msgSplit.copy()
                try:
                    idx = splitMsg.index("hari")
                    if (idx >= 1):
                        hari = int(splitMsg[idx-1])
                        payload = self.spreadsheetService.reply(hari)
                except ValueError:
                    payload = ("Nothing",)
            elif text_contains(msg, ['kemarin']):
                payload = self.spreadsheetService.reply(-1)
            else:
                payload = self.spreadsheetService.reply()
        else:
            payload = self.mcsService.handleMessage(event, msg)

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
