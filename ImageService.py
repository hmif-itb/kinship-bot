import requests
from PIL import Image, ImageFont, ImageDraw
import io
import base64


class ImageService:
    imgBB_API_KEY = ""
    imgExpiredTime = 43200  # 12 Hours

    def __init__(self, imgBB_API_KEY):
        self.imgBB_API_KEY = imgBB_API_KEY

    def getUnknownPhoto(self):
        img = Image.open("./img/unknown.png")

        result = io.BytesIO()
        img.save(result, format="png")
        return result

    def getPhoto(self, fileId):
        resp = requests.get(
            f"https://drive.google.com/uc?id={fileId}&export=download")
        rawOutput = io.BytesIO()
        rawOutput.write(resp.content)
        return rawOutput

    def resize(self, rawOutput: io.BytesIO, resizeMethod="Auto"):
        img = Image.open(rawOutput).convert("RGBA")

        w, h = img.size
        if (resizeMethod == "Auto"):
            wRatio = w/(w+h)
            hRatio = h/(w+h)
            wScale = wRatio/hRatio
            epsilon = abs(wScale-1.0)
            if (epsilon <= 0.2):
                resizeMethod = "Square"
            else:
                resizeMethod = "Rectangle"

        if (resizeMethod == "Square"):
            img = img.resize((532, 532), Image.BICUBIC)
        elif (resizeMethod == "Rectangle"):
            cut = 0
            if (w > h):
                cut = w-h
            cutHalf = (cut+1)//2
            box = (cutHalf, 0, w-cutHalf, h)
            img = img.crop(box)
            img = img.resize((532, 532), Image.BICUBIC)

        rawOutput.close()
        return img

    def editPhoto(self, photo: Image, nim: str, name: str):
        canvas = Image.new("RGBA", (800, 800), "black")
        canvas.paste(photo, (127, 137), photo)
        background = Image.open("./img/frame.png")
        background = background.resize((800, 800), Image.BICUBIC)
        canvas.paste(background, (0, 0), background)

        draw = ImageDraw.Draw(canvas)

        text = nim + "   " + name
        fontSize = 35
        dy = 18
        ssp = ImageFont.truetype(
            "./font/SourceSansPro-Bold.ttf", fontSize)
        textLength = ssp.getsize(text)[0]
        while (textLength > 640):
            fontSize -= 1
            dy += 0.5
            ssp = ImageFont.truetype(
                "./font/SourceSansPro-Bold.ttf", fontSize)
            textLength = ssp.getsize(text)[0]
        draw.text((30, 660+int(dy)), text, fill="black", font=ssp)
        return canvas

    def save(self, photo: Image, filename: str):
        content = io.BytesIO()
        photo.save(content, format="png")
        with open(filename, "wb") as f:
            f.write(content.getbuffer())
        content.close()

    def base64(self, photo: Image):
        content = io.BytesIO()
        photo.save(content, format="png")
        result = base64.b64encode(content.getvalue()).decode()
        content.close()
        return result

    def upload(self, photo: Image):
        if len(self.imgBB_API_KEY) == 0:
            return "Error: ImgBB API Key not found"
        dataBase64 = self.base64(photo)

        dataToPost = dict()
        dataToPost['image'] = dataBase64
        dataToPost['key'] = self.imgBB_API_KEY
        dataToPost['expiration'] = self.imgExpiredTime
        resp = requests.post(
            "https://api.imgbb.com/1/upload", data=dataToPost)
        if resp.status_code == 200:
            obj = resp.json()
            return obj['data']['url']
        return "Error: Failed to upload to ImgBB"
