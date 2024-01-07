# Zakopianka

## Summary

This is a simple flask app that allows you to track car's speed in a tunnel. 

The idea behind this app is to allow a tunnel supervisor to observe car traffic that is going throw a tunnel by 
displaying a list of cars with their licence plate 
and their speed (+ highlight those that went above the limit for a given tunnel).

The car drive data is assumed to have been sent by a pair of devices. 
An entry device that reads licence and car enter time and an exit device that also reads licence and exit time. This data 
is then sent to the backend which consolidates the rest of necessary information.

## Architecture

### Overview

I am using a simple web development stack consisting of [sqlite](https://www.sqlite.org/index.html) database and a [flask](https://flask.palletsprojects.com/en/3.0.x/) server with [sqlalchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/) as ORM 
between them and [jinja](https://jinja.palletsprojects.com/en/3.1.x/) templates to render html. The graphic below depicts mentioned components. 

-- placeholder --

### Database structure

The data is modeled using two entities: **Tunnels** and **CarDrives**.
There is one-to-many relationship between them. The database diagram is shown below.

--placeholder--

### API
The backend responds on the following endpoints:
- GET /tunnels - returns list of tunnels. By default return html, unless a user requested json response via `Accept: application/json` header.
- GET /tunnels/:id - returns html with traffic information about a single tunnel.
- POST /enter_car_drives - allows you to add a new car drive entry.
- PUT /exit_car_drives - updates a car drive with exit time by provided licence


## Local development

In order to run this application follow these steps

### 1. Install dependencies

`pip install -r requirements.txt`

### 2. Run local server

`python app.py`

The server now should be available at port 5000.

## Auxiliary script

For testing purposes I have included scripts folder that contains traffic
generator script. The goal of this script is to imitate traffic of cars entering and leaving the tunnel.
This script connects to the local server and every three seconds sends a request imitating that car has entered and left 
the tunnel.  

In order to run this script execute the following command:

`python scripts/traffic_generator/runner.py`
