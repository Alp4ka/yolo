from math import *
import datetime
IN_SMS_PRICE = 0
IN_HOME_CALL_PRICE = 0
IN_ROAMING_CALL_PRICE = 8
OUT_HOME_SMS_PRICE_PER_70 = 1
OUT_ROAMING_SMS_PRICE_PER_70 = 5
OUT_HOME_CALL_PRICE_PER_MINUTE = 2
OUT_ROAMING_CALL_PRICE_PER_MINUTE = 20
OUT_CALL_NO_TARIFF_SEC = 3
HOME_MB_PRICE = 0.2
MAX_MESSAGE_LENGTH = 70
ROAMING_MB_PRICE = 5
PATH = "events.txt"

class Emulator():
    def __init__(self):
        self.balance = 0
        self.h_web_mb = 0
        self.h_web_spent = 0
        self.r_web_mb = 0
        self.r_web_spent = 0
        self.hr_vmessage_counter = 0
        self.hr_vmessage_spent = 0
        self.h_imessage_counter = 0
        self.h_imessage_spent = 0
        self.r_imessage_counter = 0
        self.r_imessage_spent = 0
        self.h_vcalls_spent = 0
        self.h_vcalls_duration = 0
        self.h_vcalls_counter = 0
        self.h_icalls_spent = 0
        self.h_icalls_duration = 0
        self.h_icalls_counter = 0
        self.r_vcalls_spent = 0
        self.r_vcalls_duration = 0
        self.r_vcalls_counter = 0
        self.r_icalls_spent = 0
        self.r_icalls_duration = 0
        self.r_icalls_counter = 0
        self.roaming = False

    def enter_roaming(self, args):
        print("<<< Включение роуминга")
        self.roaming = True

    def exit_roaming(self, args):
        print("<<< Выключение роуминга")
        self.roaming = False

    def make_deposit(self, args):
        print(f"<<< Пополнение баланса на сумму {args['value']}р")
        self.balance += args['value']

    def internet_session(self, args):
        print(f"<<< Использваоние мобильного интернета. {args['mb']}МБ")
        global HOME_MB_PRICE
        global ROAMING_MB_PRICE
        if self.roaming:
            self.r_web_mb += args['mb']
            self.r_web_spent += ROAMING_MB_PRICE * args['mb']
        else:
            self.home_internet_value += args['mb']
            self.home_internet_money += HOME_MB_PRICE * args['mb']

    def incoming_message(self, args):
        print(f"<<< Новое сообщение от номера {args['telephone']} : {args['message']}")
        self.hr_vmessage_counter += 1
        self.hr_vmessage_spent += 0

    def outgoing_message(self, args):
        print(f"<<< Новое сообщение на номер {args['telephone']} : {args['message']}")
        global MAX_MESSAGE_LENGTH
        global OUT_HOME_SMS_PRICE_PER_70
        global OUT_ROAMING_SMS_PRICE_PER_70
        if self.roaming:
            self.r_imessage_counter += 1
            self.r_imessage_spent += ceil(len(args['message']) / MAX_MESSAGE_LENGTH) * OUT_ROAMING_SMS_PRICE_PER_70
        else:
            self.h_imessage_spent += ceil(len(args['message']) / MAX_MESSAGE_LENGTH) * OUT_HOME_SMS_PRICE_PER_70
            self.h_imessage_counter += 1

    def incoming_call(self, args):
        print(f"<<< Входящий звонок от номера {args['telephone']}. Продолжительность: {args['duration']}с")
        global IN_ROAMING_CALL_PRICE
        if self.roaming:
            self.r_vcalls_counter += 1
            self.r_vcalls_duration += ceil(args['duration'] / 60)
            self.r_vcalls_spent += ceil(args['duration'] / 60) * IN_ROAMING_CALL_PRICE
        else:
            self.h_vcalls_counter += 1
            self.h_vcalls_duration += ceil(args['duration'] / 60)
            self.h_vcalls_spent += 0

    def outgoing_call(self, args):
        print(f"<<< Исходящий звонок на номер {args['telephone']}. Продолжительность: {args['duration']}с")
        global OUT_HOME_CALL_PRICE_PER_MINUTE
        global OUT_ROAMING_CALL_PRICE_PER_MINUTE
        global OUT_CALL_NO_TARIFF_SEC
        time_spent = int(ceil(args['duration'] / 60)) if args['duration'] >= OUT_CALL_NO_TARIFF_SEC else 0
        if self.roaming:
            self.r_icalls_counter += 1
            self.r_icalls_duration += time_spent
            self.r_icalls_spent += time_spent * OUT_ROAMING_CALL_PRICE_PER_MINUTE
        else:
            self.h_icalls_counter += 1
            self.h_icalls_duration += time_spent
            self.h_icalls_spent += time_spent * OUT_HOME_CALL_PRICE_PER_MINUTE

    def __str__(self):
        all_money = self.h_imessage_spent + self.h_vcalls_spent + self.r_icalls_spent + self.r_imessage_spent + \
                    self.h_icalls_spent + self.hr_vmessage_spent + self.r_vcalls_spent + self.h_web_spent + self.r_web_spent
        return "-------Статистика-------\n" +\
               f"Общая сумма пополнения: {self.balance} р.\n" + \
               f"Всего потрачено на услуги: {all_money} р.\n\n" +\
               f"Входящие звонки в домашней сети: {self.h_vcalls_counter}шт. " \
                     f"Общая продолжительность: {self.h_vcalls_duration}мин. " \
                     f"Потрачено: {self.h_vcalls_spent}р.\n" + \
               f"Входящие звонки в роуминге: {self.r_vcalls_counter}шт. " \
                     f"Общая продолжительность: {self.r_vcalls_duration}мин. " \
                     f"Потрачено: {self.r_vcalls_spent}р.\n" + \
               f"Исходящие звонки в домашней сети: {self.h_icalls_counter}шт. " \
                     f"Общая продолжительность: {self.h_icalls_duration}мин. " \
                     f"Потрачено: {self.h_icalls_spent}р.\n" +\
               f"Исходящие зввонки в роуминге: {self.r_icalls_counter}шт. " \
                     f"Общая продолжительность: {self.r_icalls_duration}мин. " \
                     f"Потрачено: {self.r_icalls_spent}р.\n" + \
               f"Входящие сообщения: {self.hr_vmessage_counter}шт. " \
               f"Потрачено: {self.hr_vmessage_spent}р.\n" +\
               f"Исходящие сообщения в домашней сети: {self.h_imessage_counter}шт. " \
               f"Потрачено: {self.h_imessage_spent}р.\n" + \
               f"Исходящие сообщения в роуминге: {self.r_imessage_counter}. " \
               f"Потрачено: {self.r_imessage_spent}р.\n" + \
               f"Интернет в домашней сети: {self.h_web_mb}MБ. " \
               f"Потрачено: {self.h_web_spent}р.\n" +\
               f"Интернет в роуминге: {self.r_web_mb}МБ. " \
               f"Потрачено: {self.r_web_spent}р.\n" + \
               "----------------------"


class Server:
    def __init__(self):
        # key = date, value = [(time1, (func1, **args1)), (time2, (func2, **args2)), ...]
        self.actions = dict()

    def append_actions(self, key, value):
        if key not in self.actions.keys():
            self.actions[key] = []
            self.actions[key].append(value)
        else:
            self.actions[key].append(value)

    def read(self, emulator):
        global PATH
        with open(PATH) as f:
            for line in f.readlines():
                self.parse_line(line, emulator)

    def to_date(self, line):
        formatting = "%d.%m.%y"
        try:
            return datetime.datetime.strptime(line, formatting)
        except:
            return None

    def time_to_comparable(self, time):
        pt = datetime.datetime.strptime(time, '%H:%M:%S')
        return pt.second + pt.minute * 60 + pt.hour * 3600

    def parse_line(self, line, emulator):
        splitted = line.split()
        if splitted[0] == "deposit":
            key = date = self.to_date(splitted[2])
            time = splitted[3]
            args = {'value': float(splitted[1])}
            self.append_actions(key, (time, (emulator.make_deposit, args)))
        elif splitted[0] == "internet":
            key = date = self.to_date(splitted[2])
            time = splitted[3]
            args = {'mb': int(splitted[1])}
            self.append_actions(key, (time, (emulator.internet_session, args)))
        elif splitted[0] == "enter_roaming":
            key = date = self.to_date(splitted[1])
            time = splitted[2]
            return self.append_actions(key, (time, (emulator.enter_roaming, [])))
        elif splitted[0] == "exit_roaming":
            key = date = self.to_date(splitted[1])
            time = splitted[2]
            return self.append_actions(key, (time, (emulator.exit_roaming, [])))
        elif splitted[0] == "incoming_call":
            key = date = self.to_date(splitted[3])
            args = {'telephone': splitted[1],
                    'duration': int(splitted[2])}
            time = splitted[4]
            return self.append_actions(key, (time, (emulator.incoming_call, args)))
        elif splitted[0] == "outgoing_call":
            key = date = self.to_date(splitted[3])
            args = {'telephone': splitted[1],
                    'duration': int(splitted[2])}
            time = splitted[4]
            return self.append_actions(key, (time, (emulator.outgoing_call, args)))
        elif splitted[0] == "incoming_message":
            key = date = self.to_date(splitted[-2])
            args = {'telephone': splitted[1],
                    'message': " ".join(splitted[2:len(splitted)-2])}
            time = splitted[-1]
            return self.append_actions(key, (time, (emulator.incoming_message, args)))
        elif splitted[0] == "outgoing_message":
            key = date = self.to_date(splitted[-2])
            args = {'telephone': splitted[1],
                    'message': " ".join(splitted[2:len(splitted) - 2])}
            time = splitted[-1]
            return self.append_actions(key, (time, (emulator.outgoing_message, args)))
        else:
            return None

    def range(self, date1, date2):
        ans = list()
        temp = date1
        while temp <= date2:
            ans.append(temp)
            temp += datetime.timedelta(days=1)
        return ans

    def start(self):
        while True:
            emulator = Emulator()
            self.read(emulator)
            date1, date2 = None, None
            while date1 is None:
                print("Введите date1(d.m.y):")
                date1 = self.to_date(input())
            while date2 is None:
                print("Введите date2(d.m.y):")
                date2 = self.to_date(input())
            if date1 > date2:
                print("Ошибка! date1 > date2.")
                continue
            date_list = self.range(date1, date2)
            # print(self.actions)
            print("-------Алгоритм-------")
            for date in date_list:
                if date in self.actions.keys():
                    self.actions[date] = sorted(self.actions[date], key=lambda x: self.time_to_comparable(x[0]))
                    for action in self.actions[date]:
                        func = action[1][0]
                        args = action[1][1]
                        func(args)
            print("----------------------")
            print(emulator)
            print("\n\n\n")


a = Server()
a.start()
