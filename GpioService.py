from datetime import datetime
from gpiozero import LED
from threading import Thread
from time import sleep

class GpioService:
    
    def __init__(self):

        self.pins = {}
        self.heartbeat_last = datetime.now()
        self.heartbeat_enabled = False
        self.have_heartbeat = False;
        self.heartbeat_timeout_seconds = 2

        self.heartbeat_thread = Thread(target=self.service_heartbeat)
        self.heartbeat_thread.start();

        self.loss_action = self.default_heartbeat_loss_action;

    def get_pin(self, id):
        self.maybe_add(id)
        return self.pins[id].value

    def get_all_pins(self):
        return [(id, led.value) for id, led in self.pins.items()]

    def pin_on(self, id):
        self.maybe_add(id)
        return self.pins[id].on()

    def pin_off(self, id):
        self.maybe_add(id)
        return self.pins[id].off()

    def heartbeat(self):
        self.heartbeat_last = datetime.now()
        self.have_heartbeat = True;

    def heartbeat_enable(self):
        self.heartbeat_enabled = True

    def heartbeat_disable(self):
        self.heartbeat_enabled = False

    def maybe_add(self, id):
        if id not in self.pins:
            self.pins[id] = LED(id)

    def heartbeat_ok(self):
        return self.heartbeat_enabled == False \
          or (datetime.now() - self.heartbeat_last).total_seconds() \
            < self.heartbeat_timeout_seconds

    def service_heartbeat(self):
        self.run = True;
        while (self.run):
            if self.have_heartbeat and not self.heartbeat_ok():
                self.have_heartbeat = False;
                print("Heartbeat lost")
                self.loss_action();

            sleep(1)

    def default_heartbeat_loss_action(self):
        for id, led in self.pins.items():
            led.off()

    def close(self):
        self.run = False;
        self.heartbeat_thread.join();
