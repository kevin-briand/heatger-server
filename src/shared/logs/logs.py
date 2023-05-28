from datetime import datetime


class Logs:
    def __init__(self):
        self.message_file = open('logs.txt', 'a')
        if not self.message_file.writable():
            print('logs file not writable')

    def write(self, message: str):
        current_date_str = datetime.now().strftime('%d/%m/%Y %H:%M:%S - ')
        print(current_date_str + message)
        self.message_file.write(current_date_str + message + '\n')
        self.message_file.flush()

    @staticmethod
    def info(classname, message):
        logs_client.write(F'INF - {classname}: {message}')

    @staticmethod
    def debug(classname, message):
        current_date_str = datetime.now().strftime('%d/%m/%Y %H:%M:%S - ')
        print(F'{current_date_str}ERR - {classname}: {message}')

    @staticmethod
    def error(classname, message):
        logs_client.write(F'ERROR - {classname}: {message}')


logs_client = Logs()
