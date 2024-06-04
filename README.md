# NMRL Serial to SQL Database Instrument Interface

This package provides a command line interface for:
1. RS-232 device connection.
2. Direct serial port read


## Setup

Make sure you have Mysql/MariaDb installed

    create databse create database db_name;

    # create user if you are using mysql: 
    create user 'username'@'%' identified with mysql_native_password by '<password>'; 
    GRANT ALL PRIVILEGES ON db_name.* TO 'username'@'%';
    
    # create user if you are using mariadb 
    grant all privileges on databse_name.* TO 'username'@'%' identified by '<password>';

    # finally 
    flush privileges;
    

Download Miniconda and fix python to 3.11

    $ wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-s390x.sh
    $ bash Miniconda3-latest-Linux-s390x.sh
    $ conda install python=3.11


Check python version 

    $ python3 --version or python --version
    Python 3.x.x
    
    git clone https://github.com/NMRL-Zimbabwe/astm-improved.git
    cd astm-improved && git checkput hl7tcp
    pip3 install -r requirements.txt


Install the package as a simlink in order to local changes tracking:

    $ pip install -e .
    
    
Update configs 

    cd astm-improved/src/felicity/
    nano config.py  # and update as necessary
    

Make sure you have a working database before proceeding to this step

    # Run alembic migrations to generate our database tables
    cd astm-improved/src/felicity/
    bash ./al_upgrade.sh


Seed the Db with starter config data    
    
        $ nlablink seed


Check for the latest device connected to your computer by:
    
    $ s -lh /dev/
    

### add user to dialout
You might get a permission denied to accedd usb and serial ports: Add and reboot
    $ sudo gpasswd -a $USER dialout or sudo usermod -a -G dialout $USER


### Simulation Tests
Simulation test with socat:

    $ sudo apt-get install socat
    $ socat -d -d pty,raw,echo=0 pty,raw,echo=0
    2019/05/27 09:49:54 socat[19584] N PTY is /dev/pts/5
    2019/05/27 09:49:54 socat[19584] N PTY is /dev/pts/6
    2019/05/27 09:49:54 socat[19584] N starting data transfer loop with FDs [5,5] and [7,7]

    
Start the receiver (serial):

    $ serial -s -p /dev/pts/6
    
    
Simulate the receiver (instrument):

    $ echo -n -e '\x05' > /dev/pts/5
    Opening session
    -> <ENQ>
    Initiating Establishment Phase ...
    Ready for Transfer Phase ...
    <- <ACK>
       
    $ echo -n -e '\x021This is my first and last frame\x03F0\x0D\x0A' > /dev/pts/5
    -> <STX>1This is my first and last frame<ETX>F0<CR><LF>
     Frame accepted
    Transfer phase completed:
    --------------------------------------------------------------------------------
    This is my first and last frame
    --------------------------------------------------------------------------------
    Closing session: neutral state
    <- <ACK>
    
    $ echo -n -e '\x05' > /dev/pts/5
    $ echo -n -e '\x021This is my first frame\x17F0\x0D\x0A' > /dev/pts/5
    $ echo -n -e '\x022This is my second frame\x17F0\x0D\x0A' > /dev/pts/5
    $ echo -n -e '\x023This is my third frame\x17F0\x0D\x0A' > /dev/pts/5
    $ echo -n -e '\x024This is my fourth and last frame\x03F0\x0D\x0A' > /dev/pts/5
    Opening session
    -> <ENQ>
    Initiating Establishment Phase ...
    Ready for Transfer Phase ...
    <- <ACK>
    -> <STX>1This is my first frame<ETB>F0<CR><LF>
     Frame accepted
     Waiting for a new frame ...
    <- <ACK>
    -> <STX>2This is my second frame<ETB>F0<CR><LF>
     Frame accepted
     Waiting for a new frame ...
    <- <ACK>
    -> <STX>3This is my third frame<ETB>F0<CR><LF>
     Frame accepted
     Waiting for a new frame ...
    <- <ACK>
    -> <STX>4This is my fourth and last frame<ETX>F0<CR><LF>
     Frame accepted
    Transfer phase completed:
    --------------------------------------------------------------------------------
    This is my first frame
    This is my second frame
    This is my third frame
    This is my fourth and last frame
    --------------------------------------------------------------------------------
    Closing session: neutral state
    <- <ACK>
 
 
### Real Insrtument Setup
Serial ports are mostly set with a baudrate of 9600 by default, but you can modify these settings with stty command, if needed. Eg:
    
    $ sudo stty -F /dev/ttyUSB0 9600
    
    
The same command, but without specifying the baudrate will give you the actual configuration
 
    $ sudo stty -F /dev/ttyUSB0
    speed 9600 baud; line = 0;
    -brkint -imaxbel
    

All should be up by now: Test your serial or tcptip conections (Nb: use Web interface for production)

    nlablink serial --uid 0 --name AbbottM2000SP --code AbM200SP --path /dev/tty/USB0 --baud 9600 --protocol astm
    nlablink tcpip  --uid 1 --name AbbotAlinityM --code AlinityM --address 192.167.24.33 --port 3120 --socket server --protocol hl7
    
    
### Serial Management with supervisor
Setup supervisor for easier script management manager

installation:

    $ sudo apt update && sudo apt install supervisor
    
    
check status:

    $ sudo systemctl status supervisor
    
open supervisor config file:

    $ sudo nano /etc/supervisor/conf.d/astm_serial.conf
    

Copy and Paste any of the following programs based on available serial devices 

    [program:nmrl_lablink]
    command=/home/<user>/miniconda3/bin/python /home/<user>/miniconda3/bin/nlablink serve --host 0.0.0.0 --port 8080
    autostart=true
    autorestart=true
    stderr_logfile=/var/log/nmrl_lablink.err.log
    stdout_logfile=/var/log/nmrl_lablink.out.log
    
   
inform supervisor of our new programs:

    $ sudo supervisorctl reread
    

tell superviror enact any changes:

    $ sudo supervisorctl update
    
    
##### Supervisor management commands
check program status:

    $ sudo supervisorctl status
    
    
reload all services

    $ sudo supervisorctl reload


reload or retart a single program:
    
    $ sudo supervisorctl restart nmrl_lablink
    

tail error logs:

    $ sudo supervisorctl tail -f nmrl_lablink stderr
    or tail -f /var/log/nmrl_lablink.err.log
    
tail output logs:

    $ sudo supervisorctl tail -f nmrl_lablink stdout
    or tail -f /var/log/nmrl_lablink.out.log
    
    
View Serial Dashboard
    
    $ serial -d
    
   
Navigate to the dashboard [http://127.0.0.1:9999](http://127.0.0.1:9999)
    
Done!
