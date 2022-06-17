#! /bin/bash
# START
echo "|| Grafana-Prometheus-Pushgateway Installer ||"
echo "||                                          ||"

## Read inputs
while getopts l: flag; do
    case "${flag}" in
    l) input_lets=${OPTARG} ;;
    esac
done

if [ -x "$(command -v docker)" ]; then
    echo "||        Found docker..."
    echo "||        Running docker login..."
    docker login
    echo "||        Checking docker swarm..."
    docker swarm init &>/dev/null
else
    echo "!!    Docker command not found."
    echo "!!        Please visit https://docs.docker.com/install/ for installation instructions."
    exit 1
fi

if [ -d "/script_exporter"]; then 
    echo "!!    script exporter already exists"
else
    echo "!!    downloading script exporter"
    git clone https://github.com/ricoberger/script_exporter.git
fi

# install grafana
sudo tee  /etc/yum.repos.d/grafana.repo<<EOF
[grafana]
name=grafana
baseurl=https://packages.grafana.com/oss/rpm
repo_gpgcheck=1
enabled=1
gpgcheck=1
gpgkey=https://packages.grafana.com/gpg.key
sslverify=1
sslcacert=/etc/pki/tls/certs/ca-bundle.crt
EOF
sudo yum  -y install grafana
sudo systemctl enable --now grafana-server
sudo firewall-cmd --add-port=3000/tcp --permanent
sudo firewall-cmd --reload
sudo yum –y install python3
sudo yum –y install python3-pip
pip3 install pyymal
pip3 install requests
echo "!!    Grafana is running on http://localhost:3000"
sudo systemctl start grafana-server

# Configuration starts
/bin/bash ./config.sh

# >Certificates

if [ -z "$input_lets" ]; then
    echo "Let's Encrypt Certificate Setup for Grafana to enable https on port 3000: "
    echo "      1) Let's Encrypt signed certificate. (this machine must be reachable via over the internet by the domain name)"
    echo "      2) Finish Install."
    read -r -p "Select a mode [1]: " sslmode
    sslmode=${sslmode:-1}
else
    echo "Let's Encrypt command-line input found."
    sslmode=${input_lets:-1}
fi
if [ "$sslmode" == "1" ]; then # Let's Encrypt
    echo "    Note: port 80 must be available for DNS challenges to succeed. "
    echo "          See https://certbot.eff.org/faq for more information."
    read -r -p "Please enter the domain name of this machine: " domain
    echo "||             Certbot running for ($domain)..."
    if [ $(id -u) = 0 ]; then
        /bin/bash ./certify.sh $domain
    else
        echo "??            User is not root! Certbot requires root for security reasons."
        echo "              Please run the following script after installation: sudo /certify.sh $domain" 
    fi
fi
