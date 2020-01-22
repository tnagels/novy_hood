import appdaemon.plugins.hass.hassapi as hass

class NovyHoodControl(hass.Hass):

    def initialize(self):
        # Read settings
        self.hood_name = self.args['hood']['name']
        self.hood_speeds = self.args['hood']['speeds']
        self.remote_id = self.args['remote']['id']
        self.command_up = self.args['remote']['up']
        self.command_down = self.args['remote']['down']
        self.command_down = self.args['remote']['toggle']
        # Create fan entity
        if not self.entity_exists(self.hood_name):
            self.set_state(self.hood_name, state = "off")
