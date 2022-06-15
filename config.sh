#! /bin/bash
MYIP=$(hostname -I | head -n1 | awk '{print $1;}')

read -r -p "Is this your IP address ${MYIP} [y/N]" correct_ip

if [ "$correct_ip" == "N" ]; then
    read -r -p "Type in your ip address: " MYIP
fi

echo "||    Inserting your IP address ${MYIP} to prometheus.yml file"
echo "||    If the IP address is incorrect please update manually"
sed -i -e "s@your_ip:9091 @${MYIP}:9091 @" PrometheusGrafana/prometheus.yml

echo "!!    Make sure you have configured the config file before runing start.sh"
echo "!!    PrometheusGrafana/config.yml"
echo "!!    Visit Google Doc for API instruction"
echo "!!    https://docs.google.com/document/d/e/2PACX-1vRAwtpqlMKbii-hiqMoFD_N5PghMSw2eTMts9VhBww3AoSnXnQkjEcra4ReyLLsXrAuE_VEwLHRg33c/pub"
echo "!!    configuration templates are provided PrometheusGrafana/*_template.yml"
echo "vim PrometheusGrafana/config.yml"
echo "nano PrometheusGrafana/config.yml"