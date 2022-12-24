# lma-ui-flask-bootstrap
Python/Flask web app for calling microservice

![](https://img.shields.io/github/languages/code-size/postnikovmu/lma-ui-flask-bootstrap)
![](https://img.shields.io/github/directory-file-count/postnikovmu/lma-ui-flask-bootstrap)
![](https://img.shields.io/github/languages/count/postnikovmu/lma-ui-flask-bootstrap)
![](https://img.shields.io/github/languages/top/postnikovmu/lma-ui-flask-bootstrap)

## General Info

This is a web app, which can be used to show information
about useful skills for certain profession.

Example of request (local usage):
http://localhost:3000/hh2

Responce will be shown at the web page.

## Install

### Prerequisites:
microservices: \
./lma-extractor-hh \
(...lma-analyzer is not on github yet...) \
./lma-dispatcher \
### Deploy:
Deploy is to SAP BTP platform CloudFoundry: the settings are in manifest.yml. (or another CloudFoundry)

## Technologies

Python

Flask
