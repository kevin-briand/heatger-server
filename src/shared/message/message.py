from datetime import datetime


def info(classname, message):
    messageClient.write(F'INF - {classname}: {message}')


def debug(classname, message):
    current_date_str = datetime.now().strftime('%d/%m/%Y %H:%M:%S - ')
    print(F'{current_date_str}ERR - {classname}: {message}')


def error(classname, message):
    messageClient.write(F'ERROR - {classname}: {message}')


class Message:
    def __init__(self):
        self.message_file = open('logs.txt', 'a')
        if not self.message_file.writable():
            print('logs file not writable')

    def write(self, message: str):
        current_date_str = datetime.now().strftime('%d/%m/%Y %H:%M:%S - ')
        print(current_date_str + message)
        self.message_file.write(current_date_str + message + '\n')
        self.message_file.flush()


messageClient = Message()
