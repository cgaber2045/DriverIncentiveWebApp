# Introduction 
This project is a driver incentive program developed in Python using the Flask framework. It is for Dr. Van Scoy's CPSC 4910 class.

# Dependencies

* [flask](https://flask.palletsprojects.com/en/1.1.x/)
* [flask-restx](https://flask-restx.readthedocs.io/en/latest/)
* [mysql-connector-python](https://pypi.org/project/mysql-connector-python/)
* [requests](https://requests.readthedocs.io/en/master/)
* [etsy-python2](https://github.com/sscheetz/etsy-python2)
* [gunicorn](https://gunicorn.org)

# Installation

It is recommended that you run this project under a venv, but it is not necessary. To install these modules, run the command below inside of the root dir of the project repo:

```
python3 -m pip install -r requirements.txt
```

# Environment Setup
There are two servers that need to be setup prior to running this: nginx and gunicorn. Nginx will be through a server config file, and gunicorn through a systemd service file

## Nginx Setup

For this setup, please follow the steps below. Sidenote: **This setup will not include SSL configuration.**
1. Run `sudo apt-get install nginx`
2. Copy `config/nginx_config` to `/etc/nginx/sites-enabled`
3. Delete any other config files in above dir
4. Run `sudo nginx -s reload`
5. Test by going to your url, at this point it should have a 500 error

## Gunicorn setup

This setup involves using a systemd service config
1. Install gunicorn if you haven't already with `pip3 install gunicorn`
2. Copy `config/project.service` to `/etc/systemd/system` (you will need to use sudo here)
3. Run `sudo systemctl daemon-reload`
4. Run `sudo systemctl enable project`
5. Run `sudo systemctl start project`

At this point, you should be able to access the site from it's public IP address or domain and see the login page

If you are reading this and it came with a zip of the code, there should be an included .env file that is preconfigured, but if not let one of us know it is **crucial** to this project.
