import asyncio
import json
import websockets
import time
import argparse
import logging
import re

from sonybraviatv_remotecontrol import simpleipprotocol

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

parser = argparse.ArgumentParser()
parser.add_argument("--destport", type=int, default=20060, help="destination backend tcp port default=20060")
parser.add_argument("--desthost", type=str, default="127.0.0.1", help="destination backend host address default=127.0.0.1"), 
parser.add_argument("--bindport", type=int, default=8081, help="bind on port default=8081")
parser.add_argument("--bindhost", type=str, default="0.0.0.0", help="bind on host default=0.0.0.0")

# parse provided arguments and logging
args = parser.parse_args()
logging.debug( args )

sipp = None

reg_channel = re.compile(r'press_channel(\d+)')
reg_hdmi = re.compile(r'press_hdmi(\d+)')

async def handle_message(websocket, path):
    """handle websocket messages"""
    global sipp
    try:
        async for message in websocket:
            # decode message, json expected
            data = json.loads(message)

            if "button" not in data:
                raise Exception("bad received message, button is missing")
            logging.debug("button pressed: %s" % data["button"])

            m_chan = reg_channel.match(data["button"])
            m_hdmi = reg_hdmi.match(data["button"])
            if m_hdmi is not None:
                hdmi_id = m_hdmi.group(1).encode()
                sipp.press_hdmi(hdmi_id=hdmi_id)

            elif m_chan is not None:
                channel_id = m_chan.group(1).encode()
                sipp.press_channel(channel_id=channel_id)
            else:
                try:
                    press_function = getattr(sipp, data["button"])
                    press_function()
                except AttributeError as e:
                    logging.error("unsupported press button %s" % e)

    except Exception as e:
        logging.error("%s" % e)

async def wakeup_loop():
    """wakeup to accept keyboard interrupt"""
    while True:
        await asyncio.sleep(1)

def start_remotecontrol():
    """start remote control"""
    global sipp

    logging.info("Start websocket gateway...")

    # prepare the simple ip protocol client with destination ip/port provided
    sipp = simpleipprotocol.SimpleIpProtocol(api_host=args.desthost, 
                                 api_port=args.destport)

    # prepare the websocket server
    start_server = websockets.serve(handle_message, args.bindhost, args.bindport)

    # get the main event loop
    eventloop = asyncio.get_event_loop()

    # run server
    eventloop.run_until_complete(start_server)

    # hack to support KeyboardInterrupt
    eventloop.create_task(wakeup_loop())

    # run event loop
    try:
        eventloop.run_forever()
    except KeyboardInterrupt:
        pass