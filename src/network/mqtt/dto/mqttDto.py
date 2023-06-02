class MqttDto(object):
    def __init__(self, enabled, host, port, username, password, *args, **kwargs):
        self.enabled = enabled
        self.host = host
        self.port = port
        self.username = username
        self.password = password
