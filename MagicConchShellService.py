
from utils import Message, text_contains
from random import randint


class MagicConchShellService:
    message = Message()

    def handleMessage(self, event, msg: str):
        payload = ("Nothing",)
        if (text_contains(msg, ['siapa'], series=True, max_len=150)
                or text_contains(msg, ['siapakah'], series=True, max_len=150)):
            self.reply(event, ("ReplyText", self.message.NamaOrang()))

        elif text_contains(msg, ['apakah'], series=True, max_len=150):
            self.reply(event, ("ReplyText", self.message.YesOrNo()))

        elif (text_contains(msg, ['pilih'], series=True, max_len=150)
              or text_contains(msg, ['pilihin'], series=True, max_len=150)
              or text_contains(msg, ['pilihkan'], series=True, max_len=150)):
            splitMsg = msg.split(" ")
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

            # if text_contains(msg, ['atau'], series=True, max_len=150):
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

        return payload
