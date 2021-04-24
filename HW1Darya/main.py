import math
IN_SMS_PRICE = 0
IN_HOME_CALL_PRICE = 0
IN_ROAMING_CALL_PRICE = 8
OUT_HOME_SMS_PRICE_PER_70 = 1
OUT_ROAMING_SMS_PRICE_PER_70 = 5
OUT_HOME_CALL_PRICE_PER_MINUTE = 2
OUT_ROAMING_CALL_PRICE_PER_MINUTE = 20
OUT_CALL_NO_TARIFF_SEC = 3
HOME_MB_PRICE = 0.2
ROAMING_MB_PRICE = 5
CEILING = True


class Emulator():
    def __init__(self):
        self.balance = 0

        self.h_web_value = 0
        self.h_web_spent = 0
        self.r_web_value = 0
        self.r_web_spent = 0

        self.hr_vmessage_counter = 0
        self.hr_vmessage_spent = 0
        self.h_imessage_counter = 0
        self.h_imessage_spent = 0
        self.r_imessage_counter = 0
        self.r_imessage_spent = 0

        self.h_vcalls_money = 0
        self.h_vcalls_duration = 0
        self.h_vcalls_counter = 0
        self.h_icalls_money = 0
        self.h_icalls_duration = 0
        self.h_icalls_counter = 0

        self.r_vcalls_spent = 0
        self.r_vcalls_duration = 0
        self.r_vcalls_counter = 0
        self.r_icalls_spent = 0
        self.r_icalls_duration = 0
        self.r_icalls_counter = 0

        self.roaming = False

    def enter_roaming(self, *args):
        pass

    def exit_roaming(self, *args):
        pass

    def __str__(self):
        pass


class Manager:
    def __init__(self):
        self.commands_list = {0: "HELP",
                              1: "DEPOSIT",
                              2: "INCOMING_CALL",
                              3: "OUTCOMING_CALL",
                              4: "INCOMING_SMS",
                              5: "OUTCOMING_SMS",
                              6: "INTERNET_SESSION",
                              7: "TO_HOME",
                              8: "TO_ROAMING"}
        self.commands_execute = {"HELP": self.help,
                                 "DEPOSIT": self.deposit,
                                 "INCOMING_CALL": self.incoming_call,
                                 "OUTCOMING_CALL": self.outcoming_call,
                                 "INCOMING_SMS": self.incoming_sms,
                                 "OUTCOMING_SMS": self.outcoming_sms,
                                 "INTERNET_SESSION": self.internet_session,
                                 "TO_HOME": self.to_home,
                                 "TO_ROAMING": self.to_roaming}
        # key: date; value: list of actions
        self.actions = dict()

    def read(self):
        f = open("events.txt")
        text = f.readlines()
        for line in text:
            pass
        f.close()

    def append_actions(self, key, value):
        if key in self.actions.keys():
            pass

    def parse(self, line):
        splitted = map(int, line.split())
        if len(splitted) != 1:
            print("Какой-то странный ввод:( Напишите 0 для вызова помощи.")
        integer = splitted[0]
        if integer in self.commands_list.keys():
            execute_key = self.commands_list[integer]
            self.commands_execute(execute_key)
        else:
            print("Нет такой команды:( Напишите 0 для вызова помощи.")

    @staticmethod
    def help(self):
        result = "Для взаимодействия с программой наберите на клавиатуре номер, соответсвующий требуемой функции. \n" \
                 "Ниже представлен весь функционал программы:\n" \
                 "\n" \
                 "0. Помощь\n" \
                 "1. Внести деньги на трубку.\n" \
                 "2. Входящий звонок.\n" \
                 "3. Исходящий звонок.\n" \
                 "4. Входящее СМС.\n" \
                 "5. Исходящее СМС.\n" \
                 "6. Текущая сессия в интернете.\n" \
                 "7. Вернуться на домашний тариф.\n" \
                 "8. Перейти в роуминг.\n" \
                 "\n"
        print(result)

    def deposit(self):
        print("--Положить деньги на трубку--")
        line = input("Введите сумму, которую хотите положить на телефон:")


    def run(self):
        line = None
        while True:
            line = input()
            if len(line) == 0:
                return

        print("Работа программы завершена:)")


a = Manager()
a.run()
