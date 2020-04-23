
# Python remote control for Sony Bravia TV

![](https://github.com/dmachard/sonybraviatv_remotecontrol/workflows/Publish%20to%20PyPI/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sonybraviatv-remotecontrol)

| | |
| ------------- | ------------- |
| Author |  Denis Machard <d.machard@gmail.com> |
| License |  MIT | 
| PyPI |  https://pypi.org/project/sonybravia-remotecontrol/ |
| | |

This is a Python remote control gateway for Sony Bravia TV with minimal but sufficient basic controls.
This remote control acts as a websocket Gateway of the **Simple IP** API for more reactivity.
More details on Simple IP control https://pro-bravia.sony.net/develop/integrate/ssip/overview/index.html

## Table of contents
* [Installation](#installation)
* [Start remote control](#start-remote-control)
* [Available buttons](#available-buttons)
* [Websocket client](#websocket-client)
* [Systemd service](#systemd-service)

## Installation

```python
pip install sonybraviatv_remotecontrol
```

## Start remote control

As prerequisite configure your TV, 

- Enable remote device control

  `[HOME] Settings > Network > Home network setup > Renderer > Renderer function > Enable [Default: Enable]`

- Enable “Simple IP control”

  `[HOME] Settings > Network > Home network setup > IP control > Simple IP control > Enable [Default: Disable]`
 
After that, you can start the remote control and provides the address IP of your Sony bravia TV.

```
sonybraviatv_remotecontrol --help
usage: sonybraviatv_remotecontrol [-h] [--destport DESTPORT] [--desthost DESTHOST]
                        [--bindport BINDPORT] [--bindhost BINDHOST]

optional arguments:
  -h, --help           show this help message and exit
  --destport DESTPORT  destination backend tcp port default=20060
  --desthost DESTHOST  destination backend host address default=127.0.0.1
  --bindport BINDPORT  bind on port default=8081
  --bindhost BINDHOST  bind on host default=0.0.0.0
```

## Available buttons

To interact with the remote control, you need to use a websocket client and 
send the following **JSON** commands to the address `ws://<remotecontrol_ip>:8081`.

### TV Navigation

```json
{"button": "press_up"} // press on up button
{"button": "press_down"} // press on down button
{"button": "press_left"} // press on left button
{"button": "press_right"} // press on right button
{"button": "press_back"} // press on back button
{"button": "press_confirm"} // press on confirm button
```

## Websocket client

### Basic demo

```html
<html>
  <head>
      <title>RemoteControl demo</title>
      <style type="text/css">
          .buttons {
              font-size: 1em;
              display: flex;
              justify-content: center;
          }
          .button {
              padding: 2rem;
              border: medium solid;
              min-height: 1em;
              min-width: 1em;
              cursor: pointer;
              user-select: none;
          }
      </style>
  </head>
  <body>
    <div class="buttons">
      <div class="poweron button">ON</div>
      <div class="poweroff button">OFF</div>
    </div>
    <script>
      var websocket = new WebSocket("ws://localhost:8081/");

      var poweron = document.querySelector('.poweron')
      var poweroff = document.querySelector('.poweroff')

      poweron.onclick = function (event) {
        websocket.send(JSON.stringify({button: 'press_poweron'}));
      }
      poweroff.onclick = function (event) {
        websocket.send(JSON.stringify({button: 'press_poweroff'}));
      }
    </script>
  </body>
</html>
````

## Systemd service

Example of system service file for Centos7

```bash
vim /etc/systemd/system/sonybraviatv_remotecontrol.service

[Unit]
Description=Sony Bravia TV remote control Service
After=network.target

[Service]
ExecStart=/usr/local/bin/sonybraviatv_remotecontrol --desthost=10.0.0.200
Restart=on-abort
Type=simple
User=root

[Install]
WantedBy=multi-user.target
```

```bash
systemctl daemon-reload
systemctl start sonybraviatv_remotecontrol
systemctl status sonybraviatv_remotecontrol
systemctl enable sonybraviatv_remotecontrol
```
