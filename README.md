# Unbreakable Project
## Overview
The Unbreakable Project is a working prototype of **predictive maintenance**, a branch of the **Industry 4.0**. <br />This kind of system, is applied to one or more **cooling fans**. Each fan is located on a set of shock absorbers, and has an **accelerometer** attached on it, to detect vibrations. <br />Accelerometers' data is processed by many **Arduino microcontrollers**, which send data to an **edge**, via BLE (Bluetooth Low Energy). <br />The edge must have a Bluetooth adapter, and manages accelerometers' data transmission via node-red. Data is then sent via **MQTT** to the **central server**, which, with **machine learning algorithms** is able to train itself, understand whether a fan is in good or bad conditions, and even calculate when that fan is going to break down. In addition, the central server provides a dashboard, in which it's possible to see graphs of the fans' vibrations.

## Privacy and Encryption
It's important to encrypt data transmission between Arduino processors and edges, and between edges and the central server, to avoid sniffing and man-in-the-middle attacks. <br />*Data encryption is not implemented in the project, but it's a critical point.*

## Benefits
Compared to **programmed maintenance**:
* avoid worthless maintenances
* less downtime periods

Compared to **on-breakdown maintenance**:
* execute the maintenance when the payload of the system is minimal
* minimize damage

**General benefits**:
* money saving
* real time status of components
* prediction of the breakdown moment
