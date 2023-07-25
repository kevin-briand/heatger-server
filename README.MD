# Heatger
Heatger is a heating manager for raspberry pi.

features include : 
 - up to 2 zones
 - wait for ip found on network to return to comfort mode
 - use mqtt to communicate with home assistant
 - electric meter input to track heating consumption
 - I2C for physical user interface(under development)

---

### table of contents
- **[Install](#install)**
- **[setting up config.json](#setting-up-configjson)**
  - **[Mqtt](#mqtt)**
  - **[Network](#network)**
  - **[I2C](#i2c)**
  - **[Input](#input)**
  - **[API](#API)**
  - **[Zone](#zone)**
- **[Frontend](#Frontend)**
- **[Hardware](#Hardware)**

# Install
```shell
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install git -y
git clone https://github.com/kevin-briand/heatger.git
cd heatger
sudo chmod +x INSTALL.sh && ./INSTALL.sh
```

# setting up config.json
### mqtt
You will need to provide your MQTT broker credentials.
```json

{
  "mqtt": {
    "enabled": false,
    "host":"broker_ip",
    "port":1883,
    "username":"broker_username",
    "password":"broker_password"
  }
}
```
---
### network
This option allows you to enable network control and specify the IP address to use for the ping.

```json

{
  "network": {
    "enabled": false,
    "ip": [
      {
        "name": "Ip1",
        "ip": "192.168.1.2"
      }
    ]
  }
}
```
---
### I2C
This option is used to enable the I2C protocol for :
 - screen(type sh1106, OLED)
 - temperature(type bme280)
 - io(type PCF8574)

**Note: you should activate I2C protocol on your RPI :**
 - sudo raspi-config
 - interface->I2C
```json

{
  "i2c": {
    "temperature": {
      "enabled": false
    },
    "screen": {
      "enabled": false
    },
    "io": {
      "enabled": false
    }
  }
}
```
---
### input
This option is for enabling input :
 - electric_meter :
    - Enable if you want to track an electric meter(1 impulse = 1wh)
    - set gpio_input number where is wiring electric meter
```json

{
  "entry": {
    "electric_meter": {
      "enabled": false,
      "gpio_input": 23
    }
  }
}
```
---
### API
Credentials to access to the API. Required to use the panel.
```json
{
  "api": {
    "username": "admin",
    "password": "password"
  }
}
```
---
### zone
This option defines the zone, you can set up a maximum of 3 zones (2 by default).

parameters :
 - name : display name
 - enabled : enable clock
 - gpio_eco : GPIO number where is wiring eco relay
 - gpio_frostfree : GPIO number where is wiring frost-free relay
 - prog : list of progs

```json

{
  "zone1": {
    "name": "",
    "enabled": true,
    "gpio_eco": 17,
    "gpio_frostfree": 18,
    "prog": []
  }
}
```
 Prog object :
 - day: day of the week between 0(monday) and 6(sunday)
 - hour: hour of the day
 - order: send order(0=comfort, 1=eco)
```json
{
  "day": 3,
  "hour": "12:48:00",
  "order": 1
}
```

## Frontend

You can get card and/or panel for home assistant [here](https://github.com/kevin-briand/heatger_frontend)

---
## Hardware

You can get hardware [here](https://github.com/kevin-briand/heatger_hardware)

---

