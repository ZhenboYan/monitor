#! /bin/bash

echo "!!    Make sure Port 3000, 9090, 9091 are not in use"
echo "!!    sudo lsof -i -P -n | grep LISTEN"
echo "!!    Check Port 3000"
sudo lsof -i -P -n | grep 3000
echo "!!    Check Port 9090"
sudo lsof -i -P -n | grep 9090
echo "!!    Check Port 9091"
sudo lsof -i -P -n | grep 9091

echo "!!    Remove previous containers"
docker rm -f startpush startprom
echo "!!    Previous containers revmoed"

# sudo docker run -d --name startgrafana -p 3000:3000 -e "GF_INSTALL_PLUGINS=jdbranham-diagram-panel" grafana/grafana
# sudo docker start startgrafana

read -r -p "!!    Input config file name: " config_file

if [ -f "PrometheusGrafana/$config_file" ]; then
    sudo systemctl start grafana-server
    cd PrometheusGrafana
    sudo docker run -d --name startprom -p 9090:9090     -v $PWD/prometheus.yml:/etc/prometheus/prometheus.yml     prom/prometheus:v2.2.1
    sudo docker run -d --name startpush -p 9091:9091 prom/pushgateway
    python3 two_dynamic.py $config_file
    # if [ "$hostnum" == "1" ]; then
    # python3 one_dynamic.py $config_file
    # fi
    # if [ "$hostnum" == "2" ]; then
    #     python3 two_dynamic.py $config_file
    # fi
    # if [ "$hostnum" == "3" ]; then
    #     python3 multi_dynamic.py $config_file
    # fi
else
    echo "!!    Config file doesn't exist"
    exit 1
fi
