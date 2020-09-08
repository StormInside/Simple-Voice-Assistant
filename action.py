import datetime
import pyttsx3
import socket
import os
import locale
import time

from settings import WORDS, WORDS_LIST, PROGRAMS
from recognition import Recognition

class Answer:

    def __init__(self):
        self.speak_engine = pyttsx3.init()

    def say(self, text):
        self.speak_engine.say( text )
        self.speak_engine.runAndWait()
        self.speak_engine.stop()


def send_sound(sound_name):
    try:
        sock = socket.socket()
        sock.settimeout(10)
        sock.connect(('192.168.0.200', 3228))
        sock.send(sound_name.encode("utf-8"))

        data = sock.recv(1024)
        sock.close()

        if data.decode("utf-8") == "200":
            return 200
        else:
            sock.close()
            return "Unknown Response"
    except Exception as e:
        sock.close()
        return e


class Action():

    def __init__(self):
        self.ans = Answer()
        self.rec = Recognition()
        locale.setlocale(locale.LC_ALL, "ru")

    def action(self, command, addition = None):
        if command == 'ctime':
            now = datetime.datetime.now()
            # self.ans.say("Сейчас " + str(now.hour) + ":" + str(now.minute))
            self.ans.say("Сейчас " + now.strftime("%H:%M"))
            print("Сейчас " + now.strftime("%H:%M"))
        
        if command == 'off':
            if "точно подтверждаю" in addition or "подтверждаю точно" in addition:
                self.ans.say("Выключаю пк через 10 секунд")
                time.sleep(10)
                print("Shutdown PC")
                # os.system('shutdown -s -t 0')
            else:
                self.ans.say("Нет подтвеждения")

        if command == 'reboot':
            # if "точно подтверждаю" in addition or "подтверждаю точно" in addition:
            #     self.ans.say("Перезагружаю пк через 10 секунд")
            #     time.sleep(10)
            #     print("Shutdown PC")
            #     # os.system('shutdown -r -t 0')
            # else:
            #     self.ans.say("Нет подтвеждения")
            self.ans.say("Точно перезагрузить?")
            for i in range(3):
                a = self.rec.recognite_simple()
                if a:
                    if "да" in a or "точно" in a or "перезагрузи" in a:
                        self.ans.say("Перезагружаю пк через 5 секунд")
                        for j in range(5):
                            a = self.rec.recognite_simple()
                            if a:
                                if "стой" in a or "подожди" in a or "стоп" in a:
                                    self.ans.say("Остановка перезагрузки")
                                    return 0
                            time.sleep(1)
                        print("Shutdown PC")
                        # os.system('shutdown -r -t 0')
                        break
                time.sleep(1)
            self.ans.say("Перезагрузка не подтверждена")
                    


        if command == 'here':
            self.ans.say("Я на месте, не кричи")

        if command == 'date':
            now = datetime.datetime.now()
            self.ans.say("Сегодня, " + now.strftime("%A, %d число. %B, %m месяц"))
            print("Сегодня " + now.strftime("%A, %d. %B, %m"))

        if command == 'run':
            if addition:
                print("Запускаю - " + addition)
                program = None
                for pr in PROGRAMS:
                    if pr in addition:
                        program = pr
                        break

                if program:
                    for p in PROGRAMS[program]:
                        os.startfile(p)
                    self.ans.say("Запускаю " + pr)
                else:
                    self.ans.say("Не определена программа")
            else:
                self.ans.say("Не передана программа")


        elif command == 'gachi':
            print("gachi - "+addition)
            sound = None

            for word in WORDS_LIST:
                if word in addition:
                    sound = word

            for word in WORDS:
                if word in addition:
                    sound = WORDS[word]

            if sound:
                print("SENDING...")
                resp = send_sound(sound)
                if(resp == 200):
                    print("SUCESS SEND")
                else:
                    print(resp)
        else:
            print('Команда не распознана, повторите!')

act = Action()