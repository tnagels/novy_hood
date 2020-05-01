import appdaemon.plugins.hass.hassapi as hass
import serial

class NovyHoodControl(hass.Hass):

    def initialize(self):
        # Read settings
        self.hood_name = self.args["hood"]["name"]
        self.hood_pretty = self.args["hood"]["friendly_name"]
        self.supported_features = 1                                     # Only speed is supported
        self.icon = "mdi:pot"
        self.hood_speed_list = ["Low", "Medium", "High", "Boost"]       # Speeds supported by the hood
        self.hood_boost_time = 300                                      # Set lower than the boost time of the hood
        self.hood_speed = self.hood_speed_list[0]                       # Startup on low speed
        self.hood_state = "off"                                         # Startup on off
        self.real_hood_speed = 0
        self.real_twin_delta = False
        self.serial_port = self.args["hood"]["port"]
        self.ser = serial.Serial(self.serial_port, 38400)  # open serial port
        self.comm_up = b'\x08\x17\x0B\x01\x00\x00\x02\x02\x00' # 4th byte is sequence, here fixed to 1 / 7th byte is the hood ID, in this case it is three.
        self.comm_down = b'\x08\x17\x0B\x01\x00\x00\x02\x03\x00'
        self.remote_id = self.args["remote"]["id"]
        self.command_up = self.args["remote"]["up"]
        self.command_down = self.args["remote"]["down"]
        self.command_toggle = self.args["remote"]["toggle"]
        # self.log(self.ser.name)
        # Create fan entity
        #if not self.entity_exists(self.hood_name):
        self.update_state()
        self.listen_event(self.change_state, event = "call_service")
        self.listen_event(self.receive_remote, "deconz_event", id = self.remote_id)
        self.listen_state(self.stop_boost, self.hood_name, attribute = "speed", new = self.hood_speed_list[len(self.hood_speed_list)-1], duration = self.hood_boost_time)

    def receive_remote(self, event_name, data, kwargs):
        self.log(data['event'])
        if (data["event"] == self.command_toggle):
            if (self.hood_state == "off"): self.hood_state = "on"
            else:
                self.hood_state = "off"
                if (self.hood_speed == self.hood_speed_list[-1]): self.hood_speed = self.hood_speed_list[-2]
        elif (data["event"] == self.command_up):
            self.hood_speed = self.hood_speed_list[self.hood_speed_list.index(self.hood_speed) + 1] if (self.hood_speed_list.index(self.hood_speed) + 1) < len(self.hood_speed_list) else self.hood_speed
            self.hood_state = "on"
        elif (data["event"] == self.command_down):
            self.hood_speed = self.hood_speed_list[self.hood_speed_list.index(self.hood_speed) - 1] if (self.hood_speed_list.index(self.hood_speed) - 1) >= 0 else self.hood_speed
            self.hood_state = "on"
        self.update_state()

    def change_state(self,event_name,data, kwargs):
        if "entity_id" in data["service_data"]:
            if (data["service_data"]["entity_id"] == self.hood_name):
                if(data["service"] == "toggle"):
                    if (self.hood_state == "off"): self.hood_state = "on"
                    else:
                        self.hood_state = "off"
                        if (self.hood_speed == self.hood_speed_list[-1]): self.hood_speed = self.hood_speed_list[-2]
                elif(data["service"] == "turn_off"):
                    self.hood_state = "off"
                    if (self.hood_speed == self.hood_speed_list[-1]): self.hood_speed = self.hood_speed_list[-2]
                elif(data["service"] == "turn_on"):
                    self.hood_state = "on"
                    if "speed" in data["service_data"]:
                        self.hood_speed = data["service_data"]["speed"]
                self.update_state()

    def update_state(self):
        self.set_state(self.hood_name, state = self.hood_state, attributes = {"speed_list": self.hood_speed_list, "friendly_name": self.hood_pretty, "speed": self.hood_speed, "supported_features": self.supported_features, "icon": self.icon})
        if (self.real_twin_delta == False): self.control_hood();

    def stop_boost(self, *kwargs):
            self.hood_speed = self.hood_speed_list[-2]
            self.update_state()

    def control_hood(self, *kwargs):    # Control the hood with the "up" "down" buttons only
        self.real_twin_delta = True
        if (self.hood_state == "off"):
            twin_hood_speed = 0
        else:
            twin_hood_speed = self.hood_speed_list.index(self.hood_speed) + 2 # Make it so that on switching off there is an additional "down" action to counter difference between real and twin
        if(self.real_hood_speed == twin_hood_speed):
            self.real_twin_delta = False
        else:
            if (self.real_hood_speed > twin_hood_speed):
                self.real_hood_speed -= 1
                # self.log("DOWN")
                self.ser.write(self.comm_down)
            elif (self.real_hood_speed < twin_hood_speed):
                if (self.real_hood_speed == 0): self.real_hood_speed += 1
                self.real_hood_speed += 1
                # self.log("UP")
                self.ser.write(self.comm_up)
            self.run_in(self.control_hood, 1)
