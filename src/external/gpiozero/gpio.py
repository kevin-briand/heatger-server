import platform


class Gpio:
    def set_pin(self, addr: int, status: bool):
        if platform.system().lower() == 'windows':
            print('set pin : ' + str(addr) + ' to ' + 'on' if status else 'off')
