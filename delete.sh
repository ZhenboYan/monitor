#! /bin/bash
echo "!!    Delete pushgateway and promethues containers"
echo "!!    Stop grafana-server service"
docker rm -f startpush startprom startgrafana
rm -f PrometheusGrafana/prometheus.yml
sudo systemctl stop grafana-server
