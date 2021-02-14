# Prestations2Caldav

This small python application is used to add the calendar events send by Portail CGDIS. As soon as your prestations 
is verified, the Portail CGDIS will send you an email with an .ics file. The Application will search your Email Inbox
for a new email from the Protail CGDIS and will add the .ics file in your caldav server.

# Installation

You can use it as a simple Script or you can use it as docker container

## Simple Script

Install the required python dependencies, this script will only run on Python3

```bash
pip install -r requirements.txt
```

Execute it as script

```bash
prestation2caldav.py --mail-server <Your-Email-Server> --mail-username <Your-Email-Username> --mail-password <Your-Email-Password> --caldav-url <Your-CalDav-URL> --caldav-username <Your-CalDav-Username> --caldav-password <Your-CalDav-Password>
```

## Docker

First build the application

```bash
docker build -t prestation2caldav:latest .
```

And then start it

```bash
docker run --detach -e "MAIL_SERVER=<Your-Email-Server>" -e "MAIL_USERNAME=<Your-Email-Username>" -e "MAIL_PASSWORD=<Your-Email-Password>" -e "CALDAV_URL=<Your-CalDav-URL>" -e "CALDAV_USERNAME=<Your-CalDav-Username>" -e "CALDAV_PASSWORD=<Your-CalDav-Password>" --restart unless-stopped --name prestation2caldav prestation2caldav:latest
```

# TODO:

* Add a better/secure way to save passwords