
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

#cmds.add("Input=1");
#cmds.add("Guide=2");
#cmds.add("EPG=3");
#cmds.add("Favorites=4");
#cmds.add("Display=5");
#cmds.add("Home=6");
#cmds.add("Options=7");
#cmds.add("Return=8");
#cmds.add("Up=9");
#cmds.add("Down=10");
#cmds.add("Right=11");
#cmds.add("Left=12");
#cmds.add("Confirm=13");
#cmds.add("Red=14");
#cmds.add("Green=15");
#cmds.add("Yellow=16");
#cmds.add("Blue=17");
#cmds.add("Num1=18");
#cmds.add("Num2=19");
#cmds.add("Num3=20");
#cmds.add("Num4=21");
#cmds.add("Num5=22");
#cmds.add("Num6=23");
#cmds.add("Num7=24");
#cmds.add("Num8=25");
#cmds.add("Num9=26");
#cmds.add("Num0=27");
#cmds.add("Num11=28");
#cmds.add("Num12=29");
#cmds.add("Volume-Up=30");
#cmds.add("Volume-Down=31");
#cmds.add("Mute=32");
#cmds.add("Channel-Up=33");
#cmds.add("Channel-Down=34");
#cmds.add("Subtitle=35");
#cmds.add("Closed-Caption=36");
#cmds.add("Enter=37");
#cmds.add("DOT=38");
#cmds.add("Analog=39");
#cmds.add("Teletext=40");
#cmds.add("Exit=41");
#cmds.add("Analog2=42");
#cmds.add("*AD=43");
#cmds.add("Digital=44");
#cmds.add("Analog?=45");
#cmds.add("BS=46");
#cmds.add("CS=47");
#cmds.add("BS/CS=48");
#cmds.add("Ddata=49");
#cmds.add("Pic-Off=50");
#cmds.add("Tv_Radio=51");
#cmds.add("Theater=52");
#cmds.add("SEN=53");
#cmds.add("Internet-Widgets=54");
#cmds.add("Internet-Video=55");
#cmds.add("Netflix=56");
#cmds.add("Scene-Select=57");
#cmds.add("Model3D=58");
#cmds.add("iManual=59");
#cmds.add("Audio=60");
#cmds.add("Wide=61");
#cmds.add("Jump=62");
#cmds.add("PAP=63");
#cmds.add("MyEPG=64");
#cmds.add("Program-Description=65");
#cmds.add("Write-Chapter=66");
#cmds.add("TrackID=67");
#cmds.add("Ten-Key=68");
#cmds.add("AppliCast=69");
#cmds.add("acTVila=70");
#cmds.add("Delete-Video=71");
#cmds.add("Photo-Frame=72");
#cmds.add("TV-Pause=73");
#cmds.add("Key-Pad=74");
#cmds.add("Media=75");
#cmds.add("Sync-Menu=76");
#cmds.add("Forward=77");
#cmds.add("Play=78");
#cmds.add("Rewind=79");
#cmds.add("Prev=80");
#cmds.add("Stop=81");
#cmds.add("Next=82");
#cmds.add("Rec=83");
#cmds.add("Pause=84");
#cmds.add("Eject=85");
#cmds.add("Flash-Plus=86");
#cmds.add("Flash-Minus=87");
#cmds.add("Top-Menus=88");
#cmds.add("Popup-Menu=89");
#cmds.add("Rakuraku-Start=90");
#cmds.add("One-Touch-Time-Rec=91");
#cmds.add("One-Touch-View=92");
#cmds.add("One-Touch-Rec=93");
#cmds.add("One-Touch-Stop=94");
#cmds.add("DUX=95");
#cmds.add("Football-Mode=96");
#cmds.add("Social=97");
#cmds.add("Power=98");
#cmds.add("Power-On=103");
#cmds.add("Sleep=104");
#cmds.add("Sleep-Timer=105");
#cmds.add("Composite1=107");
#cmds.add("Video2=108");
#cmds.add("Picture-Mode=110");
#cmds.add("Demo-Surround=121");
#cmds.add("Hdmi1=124");
#cmds.add("Hdmi2=125");
#cmds.add("Hdmi3=126");
#cmds.add("Hdmi4=127");
#cmds.add("Action-Menu=129");
#cmds.add("Help=130");


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
        self.send_command(msg_type=TYPE_CONTROL, 
                          command=CMD_POWR, 
                          parms=b'0000000000000001')

    def press_poweroff(self):
        """press power off"""
        self.send_command(msg_type=TYPE_CONTROL, 
                          command=CMD_POWR, 
                          parms=b'0000000000000000')

    def press_hdmi(self, hdmi_id):
        """press hdmi"""
        parms = b'0000000000000124' #hdmi1
        if hdmi_id == "2":
            parms = b'0000000000000125'
        if hdmi_id == "3":
            parms = b'0000000000000126'
        if hdmi_id == "4":
            parms = b'0000000000000127'  
        self.send_command(msg_type=TYPE_CONTROL, 
                          command=CMD_IRCC, 
                          parms=parms)

    def press_channel(self, channel_id):
        """press channel"""
        pad_zero = 7 * b'0'
        if len(channel_id) == 2:
            pad_zero = 6 * b'0'
        self.send_command(msg_type=TYPE_CONTROL, 
                          command=CMD_CHNN, 
                          parms=b'%s%s.0000000' % (pad_zero, channel_id) )

    def press_volup(self):
        """press volume up"""
        self.send_command(msg_type=TYPE_CONTROL, 
                          command=CMD_IRCC, 
                          parms=b'0000000000000030')

    def press_voldown(self):
        """press volume down"""
        self.send_command(msg_type=TYPE_CONTROL, 
                          command=CMD_IRCC, 
                          parms=b'0000000000000031')

    def press_netflix(self):
        """press netflix"""
        self.send_command(msg_type=TYPE_CONTROL, 
                          command=CMD_IRCC, 
                          parms=b'0000000000000056')

    def press_mute(self):
        """press mute"""
        self.send_command(msg_type=TYPE_CONTROL, 
                          command=CMD_IRCC, 
                          parms=b'0000000000000032')

    def press_left(self):
        """press left"""
        self.send_command(msg_type=TYPE_CONTROL, 
                          command=CMD_IRCC, 
                          parms=b'0000000000000012')

    def press_right(self):
        """press right"""
        self.send_command(msg_type=TYPE_CONTROL, 
                          command=CMD_IRCC, 
                          parms=b'0000000000000011')

    def press_up(self):
        """press up"""
        self.send_command(msg_type=TYPE_CONTROL, 
                          command=CMD_IRCC, 
                          parms=b'0000000000000009')

    def press_down(self):
        """press down"""
        self.send_command(msg_type=TYPE_CONTROL, 
                          command=CMD_IRCC, 
                          parms=b'0000000000000010')

    def press_confirm(self):
        """press confirm"""
        self.send_command(msg_type=TYPE_CONTROL, 
                          command=CMD_IRCC, 
                          parms=b'0000000000000013')

    def press_back(self):
        """press back"""
        self.send_command(msg_type=TYPE_CONTROL, 
                          command=CMD_IRCC, 
                          parms=b'0000000000000008')

    def press_reset(self):
        """press reset"""
        self.sock.close()
        self.start_client()