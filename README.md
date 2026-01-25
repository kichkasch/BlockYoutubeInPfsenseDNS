# BlockYoutubeInPfsenseDNS

If you need to temporarily block access to youtube (for instance if your children 
are using it on the smart tv when not supervised) using DNS, BlockYoutubeInPfsenseDNS
might be your solution.

## General mode of operation

For accessing content from youtube, the endpoint in the network (SmartTV, other devices are possible) first needs to 
resolve the DNS name (youtube.com) to the corresponding IP address. Only after that, the videos (and
additional content) can be downloaded from that IP address.  
This mapping (DNS names to IP addresses: https://en.wikipedia.org/wiki/Domain_Name_System) is usually taken
care of by a network device in your local network, called **resolver**. Whenever the requests arrives at
the resolver, it will in turn ask other DNS servers in the internet (e.g. a DNS server of your internet
provider or generic ones such as 8.8.8.8 from Google) to provide the requested IP information
for DNS names.  
Some network devices allow for configuration of their resolvers in a way, that certain domains are being
resolved by a specific IP address instead of the ones in the internet. We take advantage of this behaviour
and pass on requests for youtube to an IP, which does not answer DNS requests (0.0.0.0). The default
configuration includes the domains "youtube.com" and "youtube.de" to be re-directed; other domains may be added
easily (see .venv configuration below).

## Limitations

Just key words, no details here - this blocker is by purpose not bullet-proof, it is primarily ment to 
serve as challenge for a teenager aiming for watching Youtube (when not "supervised"). If he overcomes
the protection, he deserves some extra hours. ;-)

- access control on endpoints
- DNS over HTTPS
- DNS entry in DHCP configuration
- Alternative internet connectivity

## Technological overview

### Application architecture

The python module *fwaccess.py* handles all communication with the firewall through the rest API.  
The flask application *app.py* includes the actual web services: it only contains two endpoints:
- /youtubeoff, and
- /youtubeon  

whose implementation take advantage of the functionality in fwaccess.py.

So after installation and starting the service, the web services are exposed in the LAN. Assuming that
your application is deployed on a small server (e.g. Raspberry Pi) with IP *192.168.1.30* and that you
have not changed the pre-configured ports (being 8080 for the application server), you can activate and
deactivate the youtube blocker through a web browser:

http://192.168.1.30:8080/youtubeoff

Since this is not convenient for everyday use, you should integrate with some user interface such as
smart home environments. I configured successfully HTTP endpoints in Loxone, other environments such as
HomeAssistant will perform as good.

### Technologies

- Python
- Python venv (Virtual environments for Python, https://docs.python.org/3/library/venv.html)
- Packages
  - flask (web application framework, https://flask.palletsprojects.com/en/stable/)
  - waitress (running the flask web app, https://flask.palletsprojects.com/en/stable/deploying/waitress/)
  - environs (read configuration provided in .env file, https://pypi.org/project/environs/)
  - requests (API requests against the firewall running the DNS resolver, https://pypi.org/project/requests/)

## Installation

### Prerequisites:

- You need a firewall running pfsense (working successful with CE 2.8.1); the out of the box DNS resolver of 
pfsense includes a functionality "Domain Overrides", which we will take advantage of.
- On that firewall you have API access enabled using the package pfrest (https://pfrest.org/); export
an API key as documented on that page (https://pfrest.org/AUTHENTICATION_AND_AUTHORIZATION/#api-key-authentication)
- You need to provide your details (IP of pfsense and API key) in the .env file (see below in installation instructions for details)

### Actual Installation

On server (tested on Raspberry 5 running Pi OS) to run the python code:
1) Install Python Venv 

> sudo apt-get install python3-venv

2) Create application directory and change working directory there
> sudo su  
> mkdir /opt/youtubeblock & cd /opt/youtubeblock

3) Create virtual Python environment:
> python -m venv .venv

3) Activate the environment
> . .venv/bin/activate

4) Install required python packages through pip
> pip install waitress   
> pip install flask  
> pip install requests  
> pip install environs

5) Install the app itself
> wget https://github.com/kichkasch/BlockYoutubeInPfsenseDNS/archive/refs/heads/master.zip  
> unzip master.zip

6) Prepare the app to match your environment and settings  
Change into directory:  
> cd /opt/youtubeblock/BlockYoutubeInPfsenseDNS-master

rename .env.default to .env  
> mv .env.default .env   

and edit this file to apply your settings (especially API key and IP address of your firewall).  

7) Deploy systemd service file (for automatically starting youtube blocker at system boot)

> cp youtubeblock.service /etc/systemd/system/  
> systemctl start youtubeblock # start the service  
> systemctl enable youtubeblock # automatically start at boot up  
> exit    # return to normal privileges (no more su)

### Additional instructions

For making this work, you have to make sure, that the pfsense firewall is used as DNS resolver 
(by your smart tv and maybe other relevant devices). Make sure, that

1) Your DHCP server includes the IP of the firewall as DNS resolver, and
2) (if paranoid) block outgoing traffic to other DNS servers (PORT 53 TCP /UDP) on your firewall.

## Authors and contributors

Michael Pilgermann (kickkasch@posteo.de)

## Change log

- 2026-01-25 First end-to-end functioning application.
- 2025-11-02 Initial import: backend (access to firewall via API) fully functional - frontend tbd 

## License
MIT License
See LICENSE.txt
