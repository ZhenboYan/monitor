Set up Promethues-Grafana-Pushgateway on any remote server

Root access is required in order to install successfully. Systemd is required to enable Grafana HTTPS on port 3000. 

```./install.sh``` to get started and follow the step by step instructions.

```./start.sh``` after inital installation and configuration, this starts the three bundle on the remote server.

Alternative to systemd for Grafana:
```docker run -d --name grafana -p 3000:3000 -e "GF_INSTALL_PLUGINS=jdbranham-diagram-panel" grafana/grafana```
```docker start grafana```