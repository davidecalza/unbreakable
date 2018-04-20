# Mosquitto

## Install dependancies
```bash
apt update
```
```{bash}
apt install build-essential libwrap0-dev libssl-dev libc-ares-dev uuid-dev 
```
```{bash}
xsltproc
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
##Setup
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
##...da completare