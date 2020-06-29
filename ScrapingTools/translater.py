
#from googletrans import Translator
import goslate


class Trans():
    def __init__(self, dest='en'):
        self.dest = dest

    def translate(self, to_translate):
        translater = goslate.Goslate()
        try:
            translated_string = translater.translate(to_translate, self.dest)
        except Exception:
            translated_string = to_translate
        return translated_string

"""
import goslate

class Trans():
    def __init__(self, dest = 'en'):
        self.dest = dest
        
    def translate(self, to_translate):
        translater = goslate.Goslate()
        try:
            translated_string = translater.translate(to_translate, self.dest)
        except Exception:
            translated_string = to_translate
        return translated_string


class Trans():
    def __init__(self, lang = None, dest = 'en'):
        self.lang = lang
        self.dest = dest
        self.translater = Translator()

    def identify_lang(self, to_translate):
        self.lang = self.translater.detect(to_translate).lang

    def translate(self, to_translate):
        if self.lang == None:
            self.identify_lang(to_translate)
        try:
            translated_string = self.translater.translate(to_translate, src=self.lang, dest=self.dest).text
        except Exception:
            translated_string = to_translate
        return translated_string


from textblob import TextBlob

class Translator:
    def __init__(self, lang = None, new_lang = 'eng'):
        self.lang = lang
        self.new_lang = new_lang

    def identify_lang(self, to_translate):
        self.lang = TextBlob(to_translate).detect_language()
        print("detecting " + self.lang)

    def translate(self, to_translate):
        if self.lang == None:
            self.identify_lang(to_translate)
        try:
            detected_string = TextBlob(to_translate)
            translated = detected_string.translate(to=self.new_lang)
        except Exception:
            translated = to_translate
        return translated
"""


