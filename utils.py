import time
from machine import Pin, Timer
from utime import ticks_diff, ticks_us, sleep_ms


def log(line):
    '{} - {}'.format(time.localtime(), line)

class tank:

    def __init__(self, valve_pin, echo_pin, pump_pin, trig_pin, depth=100):
        self.valve_pin = valve_pin
        self.echo_pin = echo_pin
        self.pump_pin = pump_pin
        self.trig_pin = trig_pin
        self.depth = depth # in CM
        self.level_monitor_timer = Timer(2)
        self.target_level = 100
        self.get_level()

    def fill(self, unused=None):
        self.pump(100)

    def pump(self, target_level=100):
        target_level = min(target_level, 100)
        self.target_level = target_level
        self.level_monitor_timer.deinit()
        self.level_monitor_timer.init(
            period=5000,
            mode=Timer.PERIODIC,
            callback=self.monitor)
        self.valve_pin.on()
        # 3 seconds to let valve settle
        sleep_ms(3000)
        self.pump_pin.on()

    def stop(self):
        self.pump_pin.off()
        self.valve_pin.off()
        self.level_monitor_timer.deinit()

    def get_level(self):
        # 10ms HC-SR04 trigger signal
        self.trig_pin.off()
        self.trig_pin.on()
        sleep_ms(10)
        self.trig_pin.off()
        rise = 0
        fall = 0

        # Wait for echo pin to go high
        while not self.echo_pin.value():
            rise = ticks_us()

        # Wait for echo pin to go low or timeout after 11ms (2meters)
        while self.echo_pin.value() and fall-rise < 12000:
            fall = ticks_us()

        # math the diff for distance in cm
        self.current_level_cm = (fall - rise)/58

        # return that in %
        self.current_level = self.current_level_cm/self.depth*100
        return self.current_level


    def monitor(self, unused):
        if self.get_level() >= self.target_level:
            self.stop()
