class ElectricMeterDto(object):
    def __init__(self, enabled, gpio_input, *args, **kwargs):
        self.enabled = enabled
        self.gpio_input = gpio_input
