import appdaemon.plugins.hass.hassapi as hass

class NovyHoodControl(hass.Hass):

    def initialize(self):
        # Read settings
        self.hood_name = self.args["hood"]
        self.hood_speed_list = ["Low", "Medium", "High", "Boost"]
        self.supported_features = 1
        self.hood_speed = "Low"
        self.hood_state = "off"
        self.remote_id = self.args["remote"]["id"]
        self.command_up = self.args["remote"]["up"]
        self.command_down = self.args["remote"]["down"]
        self.command_toggle = self.args["remote"]["toggle"]
        # Create fan entity
        #if not self.entity_exists(self.hood_name):
        self.set_state(self.hood_name, state = "off", attributes = {"speed_list": self.hood_speed_list, "speed": self.hood_speed, "supported_features": self.supported_features})
        self.listen_event(self.change_state, event = "call_service")
        self.listen_event(self.receive_remote, "deconz_event", id = self.remote_id)

    def change_state(self,event_name,data, kwargs):
        if "entity_id" in data["service_data"]:
            if (data["service_data"]["entity_id"] == self.hood_name):
                if(data["service"] == "toggle"):
                    if (self.hood_state == "off"): self.hood_state = "on"
                    else: self.hood_state = "off"
                elif(data["service"] == "turn_off"):
                    self.hood_state = "off"
                elif(data["service"] == "turn_on"):
                    self.hood_state = "on"
                    if "speed" in data["service_data"]:
                        self.hood_speed = data["service_data"]["speed"]
                self.set_state(self.hood_name, state = self.hood_state, attributes = {"speed_list": self.hood_speed_list, "speed": self.hood_speed, "supported_features": self.supported_features})

    def receive_remote(self, event_name, data, kwargs):
        if (data["event"] == self.command_toggle):
            if (self.hood_state == "off"): self.hood_state = "on"
            else: self.hood_state = "off"
        elif (data["event"] == self.command_up):
            self.hood_speed = self.hood_speed_list[self.hood_speed_list.index(self.hood_speed) + 1] if (self.hood_speed_list.index(self.hood_speed) + 1) < len(self.hood_speed_list) else self.hood_speed
            self.hood_state = "on"
        elif (data["event"] == self.command_down):
            self.hood_speed = self.hood_speed_list[self.hood_speed_list.index(self.hood_speed) - 1] if (self.hood_speed_list.index(self.hood_speed) - 1) >= 0 else self.hood_speed
            self.hood_state = "on"
        self.set_state(self.hood_name, state = self.hood_state, attributes = {"speed_list": self.hood_speed_list, "speed": self.hood_speed, "supported_features": self.supported_features})
        self.log(data["event"])
