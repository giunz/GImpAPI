#!/usr/bin/python3.5
from requests import get
import os
import json
import logging
import sys
import urllib3
import ssl
import certifi
import configparser
import requests

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
headers = {'content-type': 'application/json'}
config = configparser.ConfigParser()
try:
  config.read('settings.ini')
  host = config['DEFAULT']['host']
  user = config['DEFAULT']['user']
  password= (config['DEFAULT']['password'])
except KeyError:
  logging.info("No configurations file found.")
 
logging.debug("Using Hostname "+host)
logging.debug("Using Username "+user)
logging.debug("Using Password "+password)

def login():
 logging.info('Logging in.')
 r = requests.post(host+'/SecureSphere/api/v1/auth/session', headers=headers ,auth=(user, password),verify=False)
 c = r.cookies['JSESSIONID']
 if (r.status_code == 200):
  logging.info('Successfully logged in.')
 else:
  logging.error('An error occured. Status code is '+r.status_code)
 return c
 
def logout(b):
 logging.info('Logging out')
 r = requests.delete(host+'/SecureSphere/api/v1/auth/session', headers=headers, cookies=b,verify=False)
 if (r.status_code == 200):
  logging.info('Logged out successfully.')
 else:
  logging.error('An error occured. Status code is '+r.status_code)

def getAllSites(b):
 logging.info('Getting Sites.')
 r = requests.get(host+'/SecureSphere/api/v1/conf/sites', headers=headers, cookies=b,verify=False)
 if (r.status_code == 200):
  sites = r.json()
  logging.info('Retrieved the sites successfully.\n' +str(sites))
  return sites
 else:
  logging.error('An error occured. Status code is '+r.status_code)

def getAllServerGroups(b,site):
 logging.info('Getting Server Groups.')
 r = requests.get(host+'/SecureSphere/api/v1/conf/serverGroups/'+site, headers=headers, cookies=b,verify=False)
 if (r.status_code == 200):
  sg = r.json()
  logging.info('Retrieved the Server Groups successfully.\n' +str(sg))
  return sg
 else:
  logging.error('An error occured. Status code is '+r.status_code)
 
def getAllWebServices(b,site,sg):
 logging.info('Getting Web Services.')
 r = requests.get(host+'/SecureSphere/api/v1/conf/serverGroups/'+site+'/'+sg, headers=headers, cookies=b,verify=False)
 if (r.status_code == 200):
  ws = r.json()
  logging.info('Retrieved the Server Groups successfully.\n' +str(ws))
  return ws
 else:
  logging.error('An error occured. Status code is '+r.status_code)
  
cookies=login()
logging.debug('JSESSIONID is '+cookies)
c = {'JSESSIONID':cookies}
sites = getAllSites(c)
logging.info('First site\'s name is.... '+sites['sites'][0])
site=sites['sites'][0]
sg=server_groups = getAllServerGroups(c,site)
logging.info('First Server Group\'s name for site '+site+' is.... '+sg)
#server_group=sg
#ws=getAllWebServices(c,site,sg)
#logging.info('First service\'s name for site '+site+'and Server Group '+sg+' is '+ws['web-services'][0] )
logout(c)