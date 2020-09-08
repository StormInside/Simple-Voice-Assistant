import speech_recognition as sr
from fuzzywuzzy import fuzz
import time

from settings import opts, WORDS, WORDS_LIST
from action import Action

class Recognition:

    def __init__(self):
        self.act = Action()

        self.r = sr.Recognizer()
        self.m = sr.Microphone(device_index = 1)

    def callback(self, audio):
        try:
            voice = self.r.recognize_google(audio, language = "ru-RU").lower()
            print("[log] Распознано: " + voice)
            cmd = voice
        
            # for word in WORDS_LIST:
            #     if word in cmd:
            #         self.act.action(command = "gachi", addition = cmd)
            #         return 0

            # for word in WORDS:
            #     if word in cmd:
            #         self.act.action(command = "gachi", addition = cmd)
            #         return 0

            if voice.startswith(opts["alias"]):
                

                for x in opts['alias']:
                    cmd = cmd.replace(x, "").strip()
                
                for x in opts['tbr']:
                    cmd = cmd.replace(x, "").strip()
                
                cmd = self.recognize_cmd(cmd)
                self.act.action(command = cmd['cmd'], addition = cmd['add'])

        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))

    def recognize_cmd(self, cmd):
        RC = {'cmd': '', 'percent': 0, 'add': None}
        for c,v in opts['cmds'].items():

            for x in v:
                vrt = fuzz.ratio(cmd, x)
                if vrt > RC['percent']:
                    RC['cmd'] = c
                    RC['percent'] = vrt
                    RC['add'] = cmd.replace(x, "").strip()

        return RC

    def recognite_simple(self):
        try:
            with self.m as source:
                audio = self.r.listen(source)
                
            voice = self.r.recognize_google(audio, language = "ru-RU").lower()
            print("[log_simple] Распознано: " + voice)
            return voice
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))

    def start(self):
        with self.m as source:
            self.r.adjust_for_ambient_noise(source)
        
        print("Started")

        while True:
            with self.m as source:
                audio = self.r.listen(source)

            self.callback(audio)
            time.sleep(0.1)

rec = Recognition()
while True:
    rec.start()