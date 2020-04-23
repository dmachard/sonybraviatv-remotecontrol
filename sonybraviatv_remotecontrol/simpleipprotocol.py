
import socket
import time
import logging

MSG_HEADER = b'*S'

TYPE_CONTROL = b'C'
TYPE_ENQUIRY = b'E'
TYPE_ANSWER = b'A'
TYPE_NOTIFY = b'N'

CMD_POWR = b'POWR'
CMD_CHNN = b'CHNN'
CMD_IRCC = b'IRCC'

PARMS_NO = 16 * b"#"

PARMS_POWR_STANDBY = b'0000000000000000'
PARMS_POWR_ACTIVE = b'0000000000000001'

PARMS_IRCC_INPUT = b'0000000000000001'
PARMS_IRCC_GUIDE = b'0000000000000002'
PARMS_IRCC_EPG = b'0000000000000003'
PARMS_IRCC_FAVORITES = b'0000000000000004'
PARMS_IRCC_DISPLAY = b'0000000000000005'
PARMS_IRCC_HOME = b'0000000000000006'
PARMS_IRCC_OPTIONS = b'0000000000000007'

PARMS_IRCC_RETURN = b'0000000000000008'
PARMS_IRCC_UP = b'0000000000000009'
PARMS_IRCC_DOWN = b'0000000000000010'
PARMS_IRCC_RIGHT = b'0000000000000011'
PARMS_IRCC_LEFT = b'0000000000000012'
PARMS_IRCC_CONFIRM = b'0000000000000013'

PARMS_IRCC_RED = b'0000000000000014'
PARMS_IRCC_GREEN = b'0000000000000015'
PARMS_IRCC_YELLOW = b'0000000000000016'
PARMS_IRCC_BLUE = b'0000000000000017'

PARMS_IRCC_NUM1 = b'0000000000000018'
PARMS_IRCC_NUM2 = b'0000000000000019'
PARMS_IRCC_NUM3 = b'0000000000000020'
PARMS_IRCC_NUM4 = b'0000000000000021'
PARMS_IRCC_NUM5 = b'0000000000000022'
PARMS_IRCC_NUM6 = b'0000000000000023'
PARMS_IRCC_NUM7 = b'0000000000000024'
PARMS_IRCC_NUM8 = b'0000000000000025'
PARMS_IRCC_NUM9 = b'0000000000000026'
PARMS_IRCC_NUM0 = b'0000000000000027'
PARMS_IRCC_NUM11 = b'0000000000000028'
PARMS_IRCC_NUM12 = b'0000000000000029'

PARMS_IRCC_VOL_UP = b'0000000000000030'
PARMS_IRCC_VOL_DOWN = b'0000000000000031'
PARMS_IRCC_MUTE = b'0000000000000032'

PARMS_IRCC_CHANNEL_UP = b'0000000000000033'
PARMS_IRCC_CHANNEL_DOWN = b'0000000000000034'

PARMS_IRCC_SUBTITLE = b'0000000000000035'
PARMS_IRCC_CLOSED_CAPTION = b'0000000000000036'
PARMS_IRCC_ENTER = b'0000000000000037'
PARMS_IRCC_DOT = b'0000000000000038'
PARMS_IRCC_ANALOG = b'0000000000000039'
PARMS_IRCC_TELETEXT = b'0000000000000040'
PARMS_IRCC_EXIT = b'0000000000000041'
PARMS_IRCC_ANALOG2 = b'0000000000000042'
PARMS_IRCC_STAR_AD = b'0000000000000043'
PARMS_IRCC_DIGITAL = b'0000000000000044'
PARMS_IRCC_ANALOG_QUESTION = b'0000000000000045'

PARMS_IRCC_BS = b'0000000000000046'
PARMS_IRCC_CS = b'0000000000000047'
PARMS_IRCC_BS_CS = b'0000000000000048'
PARMS_IRCC_DDATA = b'0000000000000049'

PARMS_IRCC_PIC_OFF = b'0000000000000050'
PARMS_IRCC_TV_RADIO = b'0000000000000051'
PARMS_IRCC_THEATER = b'0000000000000052'
PARMS_IRCC_SEN = b'0000000000000053'
PARMS_IRCC_INTERNET_WIDGETS = b'0000000000000054'
PARMS_IRCC_INTERNET_VIDEO = b'0000000000000055'
PARMS_IRCC_NETFLIX = b'0000000000000056'
PARMS_IRCC_SCENE_SELECT = b'0000000000000057'
PARMS_IRCC_MODEL3D = b'0000000000000058'

PARMS_IRCC_IMANUAL = b'0000000000000059'
PARMS_IRCC_AUDIO = b'0000000000000060'
PARMS_IRCC_WIDE = b'0000000000000061'
PARMS_IRCC_JUMP = b'0000000000000062'
PARMS_IRCC_PAP = b'0000000000000063'
PARMS_IRCC_MYEPG = b'0000000000000064'
PARMS_IRCC_PROGRAM_DESCRIPTION = b'0000000000000065'
PARMS_IRCC_WRITE_CHAPTER = b'0000000000000066'

PARMS_IRCC_TRACKID = b'0000000000000067'
PARMS_IRCC_TEN_KEY = b'0000000000000068'
PARMS_IRCC_APPLICAST = b'0000000000000069'
PARMS_IRCC_ACTVILA = b'0000000000000070'
PARMS_IRCC_DELETE_VIDEO = b'0000000000000071'
PARMS_IRCC_PHTO_FRAME = b'0000000000000072'
PARMS_IRCC_TV_PAUSE = b'0000000000000073'

PARMS_IRCC_KEY_PAD = b'0000000000000074'
PARMS_IRCC_MEDIA = b'0000000000000075'
PARMS_IRCC_SYNC_MENU = b'0000000000000076'
PARMS_IRCC_FORWARD = b'0000000000000077'
PARMS_IRCC_PLAY = b'0000000000000078'
PARMS_IRCC_REWIND = b'0000000000000079'
PARMS_IRCC_PREV = b'0000000000000080'

PARMS_IRCC_STOP = b'0000000000000081'
PARMS_IRCC_NEXT = b'0000000000000082'
PARMS_IRCC_REC = b'0000000000000083'
PARMS_IRCC_PAUSE = b'0000000000000084'
PARMS_IRCC_EJECT = b'0000000000000085'

PARMS_IRCC_FLASH_PLUS = b'0000000000000086'
PARMS_IRCC_FLASH_MINUS = b'0000000000000087'

PARMS_IRCC_TOP_MENUS = b'0000000000000088'
PARMS_IRCC_POPUP_MENU = b'0000000000000089'
PARMS_IRCC_RAKURAKU_START = b'0000000000000090'

PARMS_IRCC_ONE_TOUCH_TIME_REC = b'0000000000000091'
PARMS_IRCC_ONE_TOUCH_VIEW = b'0000000000000092'
PARMS_IRCC_ONE_TOUCH_REC = b'0000000000000093'
PARMS_IRCC_ONE_TOUCH_STOP = b'0000000000000094'

PARMS_IRCC_DUX = b'0000000000000095'
PARMS_IRCC_FOOTBALL_MODE = b'0000000000000096'
PARMS_IRCC_SOCIAL = b'0000000000000097'
PARMS_IRCC_POWER = b'000000000000098'
PARMS_IRCC_POWER_ON = b'0000000000000103'

PARMS_IRCC_SLEEP = b'0000000000000104'
PARMS_IRCC_SLEEP_TIMER = b'0000000000000105'

PARMS_IRCC_COMPOSITE1 = b'0000000000000107'
PARMS_IRCC_VIDEO2 = b'0000000000000108'

PARMS_IRCC_PICTURE_MODE = b'0000000000000110'
PARMS_IRCC_DEMO_SURROUND = b'0000000000000121'

PARMS_IRCC_HDMI1 = b'0000000000000124'
PARMS_IRCC_HDMI2 = b'0000000000000125'
PARMS_IRCC_HDMI3 = b'0000000000000126'
PARMS_IRCC_HDMI4 = b'0000000000000127'

PARMS_IRCC_ACTION_MENU = b'0000000000000129'
PARMS_IRCC_HELP = b'0000000000000130'

class SimpleIpProtocol:
    def __init__(self, api_host,
                       api_port=20060
                       ):
        """event client class"""
        self.api_host = api_host
        self.api_port = api_port
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.start_client()

    def start_client(self):
        """start client only bravia if tv is ready"""
        logging.debug("Checking if Bravia tv is online...")

        timeout_max = 120
        timeout_raised = False
        tv_ready = False
        start_time = time.time()
        while (not tv_ready) and (not timeout_raised):
            if (time.time() - start_time) >= timeout_max:
                timeout_raised = True
            else:
                try:
                    self.sock.connect((self.api_host, self.api_port))
                    tv_ready = True
                except Exception as e:  
                    print(e)
                    time.sleep(10)

        if timeout_raised:
            raise Exception( "bravia TV simple IP api not ready ?" )

        if tv_ready:
            logging.debug("Bravia TV is ready")

    def send_command(self, msg_type, command, parms):
        """send command
        https://pro-bravia.sony.net/develop/integrate/ssip/command-definitions/index.html
        """
        msg_data = MSG_HEADER + msg_type + command + parms + b'\n'

        for m in msg_data.decode("utf8").splitlines():
            logging.debug("Sending command: %s" % m)

        self.sock.sendall(msg_data)

        response_received = self.sock.recv(1024)
        for m in response_received.decode("utf8").splitlines():
            logging.debug("Response received: %s" % m)

    def press_poweron(self):
        """press power on"""
        self.send_command(msg_type=TYPE_CONTROL, command=CMD_POWR, 
                          parms=PARMS_POWR_ACTIVE)

    def press_poweroff(self):
        """press power off"""
        self.send_command(msg_type=TYPE_CONTROL, command=CMD_POWR, 
                          parms=PARMS_POWR_STANDBY)

    def press_hdmi(self, hdmi_id):
        """press hdmi"""
        parms = PARMS_IRCC_HDMI1
        if hdmi_id == "2":
            parms = PARMS_IRCC_HDMI2
        if hdmi_id == "3":
            parms = PARMS_IRCC_HDMI3
        if hdmi_id == "4":
            parms = PARMS_IRCC_HDMI4 
        self.send_command(msg_type=TYPE_CONTROL, command=CMD_IRCC, 
                          parms=parms)

    def press_channel(self, channel_id):
        """press channel"""
        pad_left = 7 * b'0'
        pad_right = 7 * b'0'
        if len(channel_id) == 2:
            pad_left = 6 * b'0'
        self.send_command(msg_type=TYPE_CONTROL, command=CMD_CHNN, 
                          parms=b'%s%s.%s' % (pad_left, channel_id, pad_right) )

    def press_volup(self):
        """press volume up"""
        self.send_command(msg_type=TYPE_CONTROL, command=CMD_IRCC, 
                          parms=PARMS_IRCC_VOL_UP)

    def press_voldown(self):
        """press volume down"""
        self.send_command(msg_type=TYPE_CONTROL, command=CMD_IRCC, 
                          parms=PARMS_IRCC_VOL_DOWN)

    def press_netflix(self):
        """press netflix"""
        self.send_command(msg_type=TYPE_CONTROL, command=CMD_IRCC, 
                          parms=PARMS_IRCC_NETFLIX)

    def press_mute(self):
        """press mute"""
        self.send_command(msg_type=TYPE_CONTROL, command=CMD_IRCC, 
                          parms=PARMS_IRCC_MUTE)

    def press_left(self):
        """press left"""
        self.send_command(msg_type=TYPE_CONTROL, command=CMD_IRCC, 
                          parms=PARMS_IRCC_LEFT)

    def press_right(self):
        """press right"""
        self.send_command(msg_type=TYPE_CONTROL, command=CMD_IRCC, 
                          parms=PARMS_IRCC_RIGHT)

    def press_up(self):
        """press up"""
        self.send_command(msg_type=TYPE_CONTROL, command=CMD_IRCC, 
                          parms=PARMS_IRCC_UP)

    def press_down(self):
        """press down"""
        self.send_command(msg_type=TYPE_CONTROL, command=CMD_IRCC, 
                          parms=PARMS_IRCC_DOWN)

    def press_confirm(self):
        """press confirm"""
        self.send_command(msg_type=TYPE_CONTROL, command=CMD_IRCC, 
                          parms=PARMS_IRCC_CONFIRM)

    def press_back(self):
        """press back"""
        self.send_command(msg_type=TYPE_CONTROL, command=CMD_IRCC, 
                          parms=PARMS_IRCC_RETURN)

    def press_home(self):
        """press home"""
        self.send_command(msg_type=TYPE_CONTROL, command=CMD_IRCC, 
                          parms=PARMS_IRCC_HOME)

    def press_reset(self):
        """press reset"""
        self.sock.close()
        self.start_client()