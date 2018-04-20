# Run Mosquitto on edge

## Install dependancies
```{bash}
apt update
```
```{bash}
apt install build-essential libwrap0-dev libssl-dev libc-ares-dev uuid-dev xsltproc
```
## Create user "Mosquitto"
```{bash}
adduser mosquitto
```
```{bash}
cd /home/mosquitto
```
## Install
```{bash}
wget http://mosquitto.org/files/source/mosquitto-1.4.9.tar.gz
```
```{bash}
tar xvzf mosquitto-1.4.9.tar.gz
```
```{bash}
cd mosquitto-1.4.9
```
```{bash}
make
```
```{bash}
make install
```
## Setup
```{bash}
mosquitto_passwd -c /etc/mosquitto/pwfile owntracks
```
```{bash}
mkdir /var/lib/mosquitto
```
```{bash}
chown mosquitto:mosquitto /var/lib/mosquitto/ -R
```
```{bash}
cp /etc/mosquitto/mosquitto.conf.example /etc/mosquitto/mosquitto.conf
```
```{bash}
vim /etc/mosquitto/mosquitto.conf
```
Append the following rows:
```{bash}
listener <port> <ip>
persistence true
persistence_location /var/lib/mosquitto/
persistence_file mosquitto.db
log_dest syslog
log_dest stdout
log_dest topic
log_type error
log_type warning
log_type notice
log_type information
connection_messages true
log_timestamp true
allow_anonymous false
password_file /etc/mosquitto/pwfile
```
Finally run:
```{bash}
/sbin/ldconfig
```
## To run Mosquitto
```{bash}
mosquitto -c /etc/mosquitto/mosquitto.conf
```

## To listen to the port
```{bash}
mosquitto_sub -h <ip> -p <port> -v -t 'prom1/#' -u <user> -P <password>
```

### Credits
* [DigitalOcean](https://www.digitalocean.com/community/questions/how-to-setup-a-mosquitto-mqtt-server-and-receive-data-from-owntracks)
* [Mosquitto](https://github.com/eclipse/mosquitto)
