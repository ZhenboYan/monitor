#! /bin/bash
usage() {
    cat <<EOF
        Usage:      letsencrypt.sh <domain> 
        Arguments:
                    - domain: domain name of the server
EOF
}

if [ $# = 1 ]; then
    domain=$1
    # install tools
    sudo yum install snapd
    sudo systemctl enable --now snapd.socket
    sudo ln -s /var/lib/snapd/snap /snap
    sudo snap install core
    sudo snap refresh core
    # installation and certification
    sudo snap install --classic certbot
    grafana-cli plugins install jdbranham-diagram-panel

    if [ $(id -u) = 0 ]; then
        sudo ln -s /snap/bin/certbot /usr/bin/certbot
        sudo certbot certonly --standalone -n --agree-tos \
            --register-unsafely-without-email \
            --domains $domain
        if [ -f "/etc/letsencrypt/live/$domain/fullchain.pem" ]; then
            cp /etc/letsencrypt/live/dev2.virnao.com/*.pem /etc/grafana/
            chown :grafana /etc/grafana/fullchain.pem
            chown :grafana /etc/grafana/privkey.pem
            chmod 640 /etc/grafana/fullchain.pem
            chmod 640 /etc/grafana/privkey.pem

            # edit grafana initialization file
            sed -i '/;protocol = http/a\protocol = https' /etc/grafana/grafana.ini
            sed -i '/;cert_file =/a\cert_file = /etc/grafana/fullchain.pem' /etc/grafana/grafana.ini
            sed -i '/;cert_key =/a\cert_key = /etc/grafana/privkey.pem' /etc/grafana/grafana.ini

            # restart
            sudo service grafana-server restart
        else
            echo "!!    Certificate not found!"
            exit 1
        fi
    else
        echo "!!    User is not root. Please run script with sudo."
    fi
else 
    echo "!!    Invalid arguments passed."
    usage
fi