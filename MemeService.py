import requests


class MemeService:

    def getMeme(self, count=1):
        if (count == 1):
            try:
                response = requests.get('https://meme-api.herokuapp.com/gimme')
                response.raise_for_status()
                memeData = response.json()
                while memeData['nsfw']:
                    response = requests.get(
                        'https://meme-api.herokuapp.com/gimme')
                    response.raise_for_status()
                    memeData = response.json()
                return [memeData['url']]
            except:
                return None
        else:
            try:
                response = requests.get(
                    'https://meme-api.herokuapp.com/gimme/'+str(count))
                response.raise_for_status()
                memeData = response.json()
                memes = memeData['memes']
                nsfwContent = 0
                result = []
                for item in memes:
                    if item['nsfw']:
                        nsfwContent += 1
                    else:
                        result.append(item['url'])

                if nsfwContent == 1:
                    sisa = self.getMeme(1)
                    if (sisa == None):
                        return None
                    else:
                        result.append(sisa)
                elif nsfwContent > 1:
                    sisaBanyak = self.getMeme(nsfwContent)
                    if (sisaBanyak == None):
                        return None
                    else:
                        result = result + sisaBanyak

                return result
            except Exception as e:
                print(e)
                return None

    def reply(self, count=1):
        if count > 5:
            count = 5
        if count < 0:
            count = 1

        memes = self.getMeme(count)
        if (memes == None):
            return ("ReplyText", "Failed to fetch meme, sorry!")
        # return ("Image", memes)
        return ("ReplyImage", memes[0])
