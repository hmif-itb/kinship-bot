from random import randint


def text_contains(text, keywords, series=False, max_len=9999):
    if len(text) > max_len:
        return False

    if series:
        idx = 0
        for keyword in keywords:
            new_idx = text.find(keyword)
            if new_idx < idx:
                return False
            idx = new_idx
        return True

    for keyword in keywords:
        if (text.find(keyword) == -1):
            return False
    return True


class Message:

    def randomize(self, messages: list):
        if (len(messages) == 0):
            return "Failed to get message"
        return messages[randint(0, len(messages)-1)]

    def YesOrNo(self):
        messages = [
            'yes',
            'no',
            'ya',
            'gak',
            'iya',
            'tentatif',
            'belum tentu',
            'mungkin',
            'tidak',
            'yep',
            'tidak mungkin',
            'tidak bisa dipungkiri',
            'pastilah',
            'gak yakin'
        ]
        return messages[randint(0, len(messages)-1)]

    def NoBirthday(self):
        messages = [
            'Gak ada yang ultah',
            'Libur... gada yang ultah',
            'None, ga ada didata',
        ]
        return self.randomize(messages)

    def FindWait(self):
        messages = [
            'Bentar, dicari dulu gan',
            'Sedang mencari data',
            'Ok, tunggu bentar',
            'Lagi memproses, lagi nyariin nih...',
            'Sabar ya, dicari duls'
        ]
        return self.randomize(messages)

    def EditWait(self, nim: int):
        nstr = str(nim)
        messages = [
            'Bentar, ngedit dulu gan',
            'Sedang mengedit foto nim ' + nstr,
            'Edit? OK, tunggu sebentar',
            nstr + "? wait, dicari dulu fotonya yak..."
        ]
        return self.randomize(messages)

    def PanggilanNotFound(self, pg):
        messages = [
            'panggilan ' + pg + ' gak ditemukan',
            'panggilan ' + pg + ' tidak ditemukan',
            'panggilan ' + pg + ' gak ada coi',
            'panggilan ' + pg + ' tidak ada di database',
            'coba lagi dengan nama panggilan yang lain, panggilan ' + pg + ' gak ada',
        ]
        return self.randomize(messages)

    def NIMNotFound(self, nim: int):
        nstr = str(nim)
        messages = [
            nstr + ' memangnya ada?',
            'NIM ' + nstr + ' tidak ditemukan',
            'NIM ' + nstr + ' gak ada coi',
            'NIM ' + nstr + ' tidak ada di database'
        ]
        return self.randomize(messages)

    def MemeWait(self, count=1):
        messages = []
        if (count == 1):
            messages = [
                'Bentar memenya dicari dulu...',
                'Ok, buka list meme dulu',
                'Wait ya, lagi ngeliat list meme',
                'Memproses sebuah meme',
                'Tunggu sebentar, nyari meme yang oke dulu',
            ]
        else:
            cstr = str(count)
            messages = [
                'Sebentar, nyari ' + cstr + ' meme di internet...',
                'Sabar ya, ' + cstr + ' meme lagi ngupload nih',
                'Nih, tunggu ya, ' + cstr + ' meme lagi diproses',
                'Sedang mencari ' + cstr + ' meme'
            ]
        return self.randomize(messages)

    def Hai(self):
        messages = [
            'Hai juga',
            'Hai sayang',
            'Halo halo',
            'Halo sayang <3',
            'Hai, ada apa?',
            'Halo juga'
        ]
        return self.randomize(messages)

    def Thankyou(self):
        messages = [
            'Yo thx',
            'Thankyou',
            'Yoi',
            'thanks',
            'makasih'
        ]
        return self.randomize(messages)

    def Welcome(self):
        messages = [
            'Yo sama-sama',
            'Sama-sama',
            'Yoi',
            'my pleasure'
        ]
        return self.randomize(messages)

    def NamaOrang(self):
        name = [
            'kotsar',
            'hanif',
            'rakha',
            'gibet',
            'nicho',
            'tata',
            'ilman',
            'adila',
            'wildan',
            'tugus',
            'shifa',
            'jek',
            'fauzan',
            'kotsar',
            'hanif',
            'rakha',
            'gibet',
            'nicho',
            'tata',
            'ilman',
            'adila',
            'wildan',
            'tugus',
            'shifa',
            'jek',
            'fauzan'
        ]
        return self.randomize(name)
