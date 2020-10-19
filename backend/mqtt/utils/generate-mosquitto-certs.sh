#!/bin/bash

C_DIR=`pwd`
mkdir certs
cd certs
echo "Common name should be the one that you will use in your Clients, e.g. 192.168.1.70 OR a domain name."

openssl genrsa -out mosq-ca.key 2048
openssl req -new -x509 -days 1830 -key mosq-ca.key -out mosq-ca.crt
openssl genrsa -out mosq-serv.key 2048
openssl req -new -key mosq-serv.key -out mosq-serv.csr
openssl x509 -req -in mosq-serv.csr -CA mosq-ca.crt -CAkey mosq-ca.key -CAcreateserial -out mosq-serv.crt -days 1830 -sha256

echo ""
echo "============================================"
echo ""
echo "What we need are mosq-ca.crt (/etc/mosquitto/ca_certificates), mosq-serv.crt and mosq-serv.key (both in /etc/mosquitto/certs)."
echo "Also, add in /etc/mosquitto/mosquitto.conf the lines:"
echo ""
echo "listener 8883"
echo "cafile /home/pi/ssl-cert-mosq/mosq-ca.crt"
echo "certfile /home/pi/ssl-cert-mosq/mosq-serv.crt"
echo "keyfile /home/pi/ssl-cert-mosq/mosq-serv.key"
echo ""
echo "Then, restart mosquitto service:"
echo "sudo service mosquitto stop/start"
echo ""

mosq_conf_append() {
    # Function to append to a root privileged file.
    echo $1 | sudo tee --append /etc/mosquitto/mosquitto.conf
}

read -p "Do the above automatically? [y/n]: " ans
if [ "$ans" = "y" ]; then
    sudo cp "${C_DIR}/certs/mosq-ca.crt" "/etc/mosquitto/ca_certificates"
    sudo cp "${C_DIR}/certs/mosq-serv.crt" "/etc/mosquitto/certs"
    sudo cp "${C_DIR}/certs/mosq-serv.key" "/etc/mosquitto/certs"

    mosq_conf_append ""
    mosq_conf_append "# Secure MQTT"
    mosq_conf_append "listener 8883"
    mosq_conf_append ""
    mosq_conf_append "cafile ${C_DIR}/certs/mosq-ca.crt"
    mosq_conf_append "certfile ${C_DIR}/certs/mosq-serv.crt"
    mosq_conf_append "keyfile ${C_DIR}/certs/mosq-serv.key"

    sudo service mosquitto stop
    sleep 2
    sudo service mosquitto start

    echo "Also, copy mosq-ca.crt to your client."
fi

cd ${C_DIR}
