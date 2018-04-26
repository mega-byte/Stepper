import socket , stepper, os, psutil , sys, logging, datetime
#
# First check if socketserver is already running
#
#logging.basicConfig(filename='/home/pi/Stepper/serverlog.log' , level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='/home/pi/Stepper/serverlog.log',
                    filemode='w')
logging.info('    ****** Server Startup ******')
numberOfServerInstances = 0
for pid in psutil.pids():
    if 'socketserver.py' in (psutil.Process(pid).cmdline()):
        numberOfServerInstances  += 1
logging.debug('The number of server program instances already running on this computer is ' + str(numberOfServerInstances))
#
#   Note - since we moved to running this as a service the test for multiple instances is (virtually) redundant
#
if numberOfServerInstances > 0 :
    logging.warning('Server start rejected, the server is already running....') 
    sys.exit('SERVER: Request to start a second instance of Server program rejected')
#
# set up the socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('0.0.0.0', 2008))
serversocket.listen(5)
#
#
logging.debug('Server started and listening on port 2008...' )
stepper.blink(0.020,200)
#
# process connections from clients
try: 
     while True:
         logging.debug('Server waiting for data from the client' )
         (clientSocket, address) = serversocket.accept()
         cmd = clientSocket.recv(1024)
         logging.info('Server received the raw command: ' + cmd )
         if (len(cmd) > 4) and (cmd[:3] == "Log"):
            logging.info(cmd[3:])         
            reply = 'Log command processed'
         elif cmd == "Key_1":
             stepper.forward(0.003,520)  # parameters are delay in ms and no of steps
             reply = 'Payload up request processed'
         elif cmd == "Key_2":
             stepper.backwards(0.003,520)
             reply = 'Payload down request processed'
         elif cmd == "Key_3":
             # Ignore Key_3 command....'
             reply = 'Key_3 command processed (ignored)'
         elif cmd == "Key_4":
             # Ignore Key_4 command...'
             reply = 'Key_4 command processed (ignored)'
         elif cmd == "Key_5":
             # Ignore Key_5 command....'
             reply = 'Key_5 command processed (ignored)'
         elif cmd == "Key_6":
             reply = 'Key_6 command processed (ignored by server)'   # note Key_6 is processed by the client
         elif cmd == "Key_VolumeUp":
             stepper.forward(0.003,52)
             reply = 'Step mode - Payload up request processed'
         elif cmd == "Key_VolumeDown":
             stepper.backwards(0.003,52)
             reply = 'Step mode - Payload down request processed'
         elif cmd == "Key_Aux":
             reply = 'Key_Aux command processed (ignored)'
         else: 
             reply = "ERROR: Unrecognised command: " + cmd
             logging.warning('Unrecognised command ' + cmd + ' received by server' )
         clientSocket.send(reply)
         clientSocket.close()
except KeyboardInterrupt:
  logging.warning('Control c Keyboard interupt pressed ' )
except (RuntimeError,TypeError):
  logging.warning('Server runtime or TypeError detected' )
finally:
    stepper.cleanup()
    logging.info('Server has completed cleanup in Stepper including GPIO cleanup()' )

