# novy_hood
Home Assistant Appdeamon app for a Novy Hood. This uses an RFXCOM interface which is controlled directly by the app. No other functions are possible with the RFXCOM.

It also has an code for a Zigbee remote using Deconz to replace the original.

Remember to add the `serial` python package to the AppDaemon config, otherwise it will not work.

Example config:

```yaml
novy_dampkap:
  module: novy
  class: NovyHoodControl
  hood: 
    name: fan.novy
    friendly_name: Dampkap
    port: /dev/serial/by-id/usb-RFXCOM_RFXtrx433XL_DO40IZIO-if00-port0
  remote:
    id: tradfri_remote_control
    up: 5002
    down: 4002
    toggle: 1002
```

Code is provided as-is without licence requirement, but also without warranty. Use at your own risk.
