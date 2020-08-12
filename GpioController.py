from GpioService import GpioService

class GpioController:

    def __init__(self):
        self.service = GpioService()
    
    def get_get_routes(self, id):
        return {
            f'/pin/{id}' : self.service.get_pin,
            f'/pins' : self.service.get_all_pins,
            f'/' : self.service.get_all_pins,
        }

    def get_post_routes(self, id):
        return { 
            f'/heartbeat/disable' : self.service.heartbeat_disable,
            f'/heartbeat/enable' : self.service.heartbeat_enable,
            f'/heartbeat' : self.service.heartbeat,
            f'/pin/{id}/on' : self.service.pin_on,
            f'/pin/{id}/off' : self.service.pin_off,
        }
