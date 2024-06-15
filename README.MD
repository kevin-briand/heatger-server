# Heatger server
Heatger server is a heating manager for raspberry pi. 

It's a part of [Heatger](https://github.com/kevin-briand/heatger), an integration for home assistant.

features include : 
 - up to 2 zones
 - wait for user found on network to return to comfort mode
 - electric meter input to track heating consumption
 - I2C for physical user interface

### table of contents
- **[Install](#install)**
- **[setting up config.json](#setting-up-configjson)**
  - **[I2C](#i2c)**
  - **[Input](#input)**
  - **[Zone](#zone)**
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

### Port
You can override server default port (5000).
```json
{
  "ws_port": 6000
}
```

### I2C
This option is used to enable the I2C protocol for :
 - screen(type sh1106, OLED)
 - temperature(type bme280)
 - io(type PCF8574)

device parameter is to define the I2C address and port, you can see find your address with the following command :
```bash
# install i2ctools
sudo apt-get install i2c-tools
# where 1 is the port
sudo i2cdetect -y 1
```

**Note: you should activate I2C protocol on your RPI :**
 - sudo raspi-config
 - interface->I2C

```json

{
  "i2c": {
    "temperature": {
      "enabled": false,
      "device": {
        "address": "0x76",
        "port": 1
      }
    },
    "screen": {
      "enabled": false,
      "device": {
        "address": "0x3C",
        "port": 1
      }
    },
    "io": {
      "enabled": false,
      "device": {
        "address": "0x20",
        "port": 1
      }
    }
  }
}
```

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
    "gpio_eco": 17,
    "gpio_frostfree": 18
  }
}
```

# Home assistant integration

You can get card and/or panel for home assistant [here](https://github.com/kevin-briand/heatger)

# Hardware

You can get hardware [here](https://github.com/kevin-briand/heatger_hardware)
