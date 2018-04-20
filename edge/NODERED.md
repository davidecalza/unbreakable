# Node-red configuration

## Node installation
```{bash}
sudo apt install nodejs
```

## Node-red setup
```{bash}
sudo npm install -g --unsafe-perm node-red
```

## Noble Bluetooth support
```{bash}
sudo apt install bluetooth bluez libbluetooth-dev libudev-dev
```
```{bash}
sudo npm install -g noble
```

## Run Node-red
```{bash}
sudo node-red
```
Open http://localhost:1880

## Flow diagram
see [flow.png](https://github.com/davide-calza/unbreakable/blob/master/edge/flow.png)

## Deserialize function
Given an input string like **X_axis_value&Y_axis_value&Z_axis_Value**
```javascript
var m = msg.payload.data.toString()
var s = "fanbad,"+m.split('&')[0] + "," + m.split('&')[1] + "," + m.split('&')[2]
if(m.includes('&')) return {payload:s}
```

## Credits
* [Node-red](https://github.com/node-red/node-red)
* [Noble](https://github.com/noble/noble)
