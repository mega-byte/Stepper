
###########################################################################################################################
#
#   This program was first written on 06-Jun-16 by Martin Taylor
#   It is used in conjunction with lirc and its config file /etc/lirc/lircrc
#
#
#   Note - the program name "irtest" in the file above must match the name used in the 
#          prog parameter in file /etc/lirc/lircrc
#        - Only key presses that are set up in lircrc are returned to the 
#          program.
#
#   15-Jan-18 MGT  Imported this program as ir-mgt-test2.py from card 3 which has been the 
#                  ir developemnt environment and started to adapt it
#                  to work with the stepper motor project. Stripped out a lot of stuff.
#                  The installation of LIRC and PYLIRC was done following these instructions:
#                   thevoiceofreasonbymo.blogspot.co.uk/2013/07/pylirc-made-easy.html
#                   alexba.in/blog/2013/01/06/setting-up-lirc-on-the-raspberrypi/
#                  |
#      Jan-18. This program receives commands that are sent to the server program which may 
#        reside on another computer using the 'socket' technique. The server program can equally be 
#        on the same computer. The program was inspired by the introduction to inter process communication at
#        http://www.alan-g.me.uk/tutor/tutsocket.htm
#
#      28-Jan-18 Copied ir-socketclient.py to this file (ir-sc.py) to continue development.
#                Stripped lots out so that the client merely:
#                1. Sorts out where the server is and checks it is working
#                2. Gets a valid keypress from the remote control
#                3. Passes it to the server without any checking (if not the exit Key_6 )
#                4.  Waits for a reply from the server (there is now a more intelligent server)
#                5.  Repeats
#
#       7-Apr-18 Added the ability to set whether there is a screen connected to the client program via the command
#                line parameter. Start using "python ir-sc.py n" or "python ir-sc.py N" if there is no screen, 
#                else just use "python ir-sc.py" and output messages will be displayed.
#       8-Apr-18 Things to do:
#                1. Set thereIsAScreen to false if started in the background - done
#                2. Flush the LIRC buffer so that commands cannot stack up ie wait for 
#                   completion before reading next command. - done
#                3. On startup check if the server is on this m/c and if so do not ask further 
#                   where is the server questions. (This is now required since the change 
#                   to run the server as a daemon service rather than a python program). - done
#                4. Enable client to send messge to server for logging and use it when it (the 
#                   client) starts or ends normally.  - done
#                5. Implement a client command to get the serverlog.log across and optionally displayed 
#                6. Test out with client on a different machine
#                7. Test what happens if server crashes when all is synced and running ok
#                8. Enable for use with the Sky remote
#                9. Allow commands to be detected using an IR receiver on the client m/c
#                   (as well / instead of the server)
#               10. Get files into new ~/Stepper directory and working as a Git repository

try:
    import os , sys, pylirc, time, subprocess, socket, psutil
except RuntimeError:
    print "Error mporting modules. This could be because you need super user priviledges"
serverprogramname = "socketserver.py"
defaultRemoteServerAddress = '192.168.1.96'
port = 2008      # NB Port allocation must match that on the server side
thereIsAScreen = False
if len(sys.argv) > 1 and (sys.argv[1] == 'n' or sys.argv[1] == 'N') :
    thereIsAScreen = False
#
if os.getpgrp() <> os.tcgetpgrp(sys.stdout.fileno()):
    # if running in background do not print to screen
    thereIsAScreen = False
#
def printx(arg1):
  if thereIsAScreen:
    print ("CLIENT: " + arg1)
#
def printy(arg1):
  if thereIsAScreen:
    print ("Server: " + arg1)
#
def dosockstuff(code,serveraddress,port):
    printx ('About to connect to socket using:' + serveraddress + ':' + str(port) )
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((serveraddress,port))
    printx ('Connected to the server; sending code ' + code )
    clientsocket.send(code)
    reply = clientsocket.recv(64)
    printy (reply)
    clientsocket.close()
    return (reply)
def flushCodes():
    for i in range(0,40):         # set to be the max number of presses possible during the execution of a command
        code = pylirc.nextcode()
#
#
sockid = pylirc.init("irtest", "/etc/lirc/lircrc", 0)
#
#  The irtest parameter above matches that in the /etc/lirc/lircrc file
#  Last parameter of 0 above means do not wait, set to 1 means wait when doing pylirc.nextcode()
#  Note: The pin used for the IR receiver is set in 2 files:
#        boot/config.txt and /etc/modules
#
#
#
#   Check out the client (this program's IP) and set up the IP of the server
#   First check if the server program is running just once on the client computer:
#
serverIsLocal = False
multipleServerProgs = False
#
#
def is_service_running(name):
    with open(os.devnull, 'wb') as hide_output:
        exit_code = subprocess.Popen(['service', name, 'status'], stdout=hide_output, stderr=hide_output).wait()
        return exit_code == 0
#
if is_service_running('mgts-pi'):  serverIsLocal = True
#
#   Next we establish this computers IP address and whether we can establish connections to the internet
#
canConnectToInternet = False
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    # arbitrary external IP address below; doesn't even have to be reachable
    s.connect(('10.255.255.255', 1))
    clientIP = s.getsockname()[0]
    canConnectToInternet = True
except:
    printx ('Could not make external connection') 
    # in this case set up default values on this computer
    clientIP = '127.0.0.1'
    serveraddress = '127.0.0.1'
finally:
    s.close()
#
#   
#
serveraddress = defaultRemoteServerAddress
if serverIsLocal: 
    serveraddress = clientIP
else:
    if canConnectToInternet and thereIsAScreen:
        ans = raw_input('Is the Server at the default remote IP of ' + defaultRemoteServerAddress + '? ' )
        if (ans <> 'y') and (ans <> 'Y'):
            serveraddress = raw_input('Enter IP address of the Server computer:')
#
# Now check out if we can communicate with the server program itself
#
canCommunicateWithServer = False
code = 'Log       ******    Client Started    ******'
reply = dosockstuff(code,serveraddress,port)
if reply <> "Log command processed":
    printx ("FATAL error - server not processing commands correctly")
    print (1/0) # Server not processing commands correctly - the client is crashing
else:
    canCommunicateWithServer = True
#
printx ('Discovery complete.')
printx ("This client computer's IP address is " + clientIP)
if canConnectToInternet:
    printx ("This computer can connect to the internet")
else:
    printx ("This computer cannot connect to the internet")
if serverIsLocal:
    if multipleServerProgs:
        printx ("WARNING - Multiple copies of the server program have been detected running on this computer")
    else:
        printx ("The server program has been detected on this computer")
else:
    printx ("The server is expected to be at " + serveraddress)
#
printx (" ")
printx (" Note: There is a logfile produced by this App which is on the server machine ")
printx ("       at /home/pi/Stepper/serverlog.log")
printx (" ")
printx ("Program to receive and act on IR input for use with stepper motor ")
printx ("Using the Bose_Wave IR control:")
printx ("Press 1     - Payload up")
printx ("Press 2     - Payload down")
printx ("Volume up   - Step mode - Payload up")
printx ("Volume down - Step mode - Payload down")
printx ("Press 5     - Test Communication")
printx ("Press 6     - Exit the IR client program")
printx (" ")
#
#
orig_stdout = sys.stdout
#
#
##################################################################
#
#   THIS IS THE MAIN PROGRAM LOOP.
#
##################################################################
#
flushCodes()
code='anything'
while code <> 'Key_6':
    code=pylirc.nextcode()
    if code <> None:
        code = code[0]
        printx ("Got the code below from the remote control " + code )
        reply = dosockstuff(code,serveraddress,port)
        if code <> 'Key_6' : 
          flushCodes()
code = 'Log     ****** Client Closing    ******'
reply = dosockstuff(code,serveraddress,port)
if reply <> "Log command processed":
    printx ("FATAL error - server not processing commands correctly")
    print (1/0) # cause crash
pylirc.exit()
sys.stdout = orig_stdout
#
#################################################################
