pip install pyymal
pip install requests

sudo docker run -d --name startprom --net host -p 9090:9090 -v $PWD/PrometheusGrafana/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus:v2.2.1
sudo docker run -d --name startgrafana -p 3000:https://localhost:3000 -e "GF_INSTALL_PLUGINS=jdbranham-diagram-panel" grafana/grafana
sudo docker start startgrafana
sudo docker run -d --name startpush -p 9091:9091 prom/pushgateway

cd PrometheusGrafana

python3 dynamic.py topFlowConfig.yml