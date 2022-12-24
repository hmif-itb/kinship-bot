
from utils import Message, text_contains
from random import randint
import bs4
import requests
from googletrans import Translator


class MagicConchShellService:
    message = Message()

    def handleMessage(self, event, msg: str):
        payload = ("Nothing",)
        msgSplit = msg.split(" ")
        if (text_contains(msg, ['siapa'])
                or text_contains(msg, ['siapakah'])):
            payload = ("ReplyText", self.message.NamaOrang())

        elif text_contains(msg, ['apakah']):
            payload = ("ReplyText", self.message.YesOrNo())

        elif text_contains(msg, ['kasih', 'rating']):
            payload = ("ReplyText", self.message.Rating())

        elif text_contains(msg, ['berapa']):
            splitMsg = msgSplit.copy()
            fromNumber = 0
            toNumber = 10
            try:
                idx = splitMsg.index("dari")
                if (idx+1 <= len(splitMsg)-1):
                    fromNumber = int(splitMsg[idx+1])

            except ValueError:
                pass

            try:
                idx = splitMsg.index("sampai")
                if (idx+1 <= len(splitMsg)-1):
                    toNumber = int(splitMsg[idx+1])

            except ValueError:
                pass

            if (fromNumber == toNumber):
                payload = (
                    "ReplyText", "jadi, dari berapa sampai berapa nih? fix " + str(fromNumber) + ", dong?")
            elif (fromNumber > toNumber):
                swapNumber = toNumber
                toNumber = fromNumber
                fromNumber = swapNumber
            payload = ("ReplyText", str(randint(fromNumber, toNumber)))

        elif (text_contains(msg, ['pilih'])):
            splitMsg = msgSplit.copy()
            startIdx = None
            try:
                idx = splitMsg.index("pilih")
                if (idx+1 <= len(splitMsg)-1):
                    startIdx = idx+1
            except ValueError:
                startIdx = None
                payload = ("Nothing",)

            if (startIdx != None):
                choicesSentence = " ".join(splitMsg[startIdx:])
                choicesSentence = choicesSentence.replace(" atau ", "/")
                choicesSentence = choicesSentence.replace(" ato ", "/")
                choicesSentence = choicesSentence.replace(" or ", "/")
                choices = choicesSentence.split("/")
                choices = list(filter(lambda x: len(x) > 0, choices))
                if len(choices) >= 2:
                    choice = choices[randint(0, len(choices)-1)]
                    payload = ("ReplyText", choice.strip())
                elif len(choices) == 1:
                    payload = (
                        "ReplyText", self.message.OneChoice())
            # splitMsg = msg.split(" ")
            # startMsg1Idx = None
            # endMsg1Idx = None
            # startMsg2Idx = None

            # middleIdx = None
            # try:
            #     idx = splitMsg.index("pilih")
            #     if (idx+1 <= len(splitMsg)-1):
            #         startMsg1Idx = idx+1
            # except ValueError:
            #     startMsg1Idx = None
            #     payload = ("Nothing",)

            # if text_contains(msg, ['atau']):
            #     try:
            #         middleIdx = splitMsg.index("atau")
            #     except ValueError:
            #         middleIdx = None
            #         payload = ("Nothing",)

            # if (middleIdx != None):
            #     if ((middleIdx >= 1) and (splitMsg[middleIdx-1] != "pilih") and (middleIdx+1 <= len(splitMsg) - 1)):
            #         endMsg1Idx = middleIdx-1
            #         startMsg2Idx = middleIdx+1

            # if (startMsg1Idx != None and startMsg2Idx != None and endMsg1Idx != None):
            #     firstChoice = " ".join(splitMsg[startMsg1Idx:endMsg1Idx+1])
            #     secondChoice = " ".join(splitMsg[startMsg2Idx:len(splitMsg)])
            #     choice = randint(1, 6)
            #     if (choice % 2 == 0):
            #         payload = ("ReplyText", firstChoice)
            #     else:
            #         payload = ("ReplyText", secondChoice)
        elif text_contains(msg, ['monitor', 'bot']):
            payload = ("ReplyText", 'monitor')
        elif text_contains(msg, ['deskripsikan']):
            payload = ("ReplyText", self.translate(self.getRandomAdjective()))
        elif text_contains(msg, ['apa', 'pendapatmu', 'tentang']) or text_contains(msg, ['apa', 'pendapat', 'tentang']):
            payload = ("ReplyText", self.translate(
                " ".join([self.getRandomNoun(), self.getRandomAdjective()])))
        elif ('hai' in msgSplit or 'halo' in msgSplit or 'hi' in msgSplit):
            payload = ("ReplyText", self.message.Hai())

        elif ('gws' in msgSplit or 'get well soon' in msgSplit):
            payload = ("ReplyText", self.message.Thankyou())

        elif ('makasih' in msgSplit
              or 'thx' in msgSplit
              or 'thanks' in msgSplit
              or 'thank you' in msgSplit
              or 'terima kasih' in msgSplit
              or 'terimakasih' in msgSplit):
            payload = ("ReplyText", self.message.Welcome())

        return payload

    def getRandomAdjective(self):
        resp = requests.get("https://randomword.com/adjective")
        soup = bs4.BeautifulSoup(resp.content, 'html.parser')
        word = soup.find_all(id="random_word")[0].get_text()
        return word

    def getRandomNoun(self):
        resp = requests.get("https://randomword.com/noun")
        soup = bs4.BeautifulSoup(resp.content, 'html.parser')
        word = soup.find_all(id="random_word")[0].get_text()
        return word

    def translate(self, words: str):
        translator = Translator()
        result = translator.translate(words, src='en', dest='id').text
        return result
