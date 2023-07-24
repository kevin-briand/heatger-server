#!/bin/bash

GREEN="\033[0;32m"
NC="\033[0m"

echo -e "${GREEN}Heatger installer${NC}"
echo -e "${GREEN}Install pigpiod${NC}"
sudo apt-get install pigpiod -y
echo -e "${GREEN}run pigpiod on startup${NC}"
sudo systemctl enable pigpiod
echo -e "${GREEN}install python${NC}"
sudo apt-get install python3 python3-pip python3-venv python3-pil libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev libopenjp2-7 libtiff5 -y
echo -e "${GREEN}install dependencies${NC}"
sudo python -m pip install -r requirements.txt
if [ ! -f config.json ]
then
  echo -e "${GREEN}copy config.json${NC}"
  cp config_template.json config.json
fi
echo -e "${GREEN}install deamon${NC}"
sed -i "s/USER/$(whoami)/g" heatger.service
sudo cp heatger.service /lib/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable heatger.service
echo -e "${GREEN}reboot${NC}"
sudo reboot
