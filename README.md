# novy_hood
Home Assistant Appdeamon app for a Novy Hood

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
