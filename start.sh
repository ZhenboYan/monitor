#! /bin/bash

pip install pyymal
pip install requests

echo "!!    Make sure Port 3000, 9090, 9091 are not in use"
echo "!!    sudo lsof -i -P -n | grep LISTEN"
echo "!!    Check Port 3000"
sudo lsof -i -P -n | grep 3000
echo "!!    Check Port 9090"
sudo lsof -i -P -n | grep 9090
echo "!!    Check Port 9091"
sudo lsof -i -P -n | grep 9091

docker rm -f startpush startprom

# sudo docker run -d --name startgrafana -p 3000:3000 -e "GF_INSTALL_PLUGINS=jdbranham-diagram-panel" grafana/grafana
# sudo docker start startgrafana
sudo systemctl start grafana-server

cd PrometheusGrafana
sudo docker run -d --name startprom -p 9090:9090     -v $PWD/prometheus.yml:/etc/prometheus/prometheus.yml     prom/prometheus:v2.2.1
sudo docker run -d --name startpush -p 9091:9091 prom/pushgateway

python3 awsdynamic.py awsConfig.yml 