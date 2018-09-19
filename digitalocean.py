#!/usr/bin/env python3
# DigitalOcean API Wrapper for Python3
# Created on 17th September 2018
# Author: Dave Russell Jr / Create Azure (https://createazure.com)
from urllib import request
from urllib.parse import urlencode
import json

class DOAPI():
    def __init__(self, api_key):
        self.api_key = api_key
        self.uri = 'https://api.digitalocean.com'

    def buildRequest(self, request_url, data=None, method=None):
        return request.Request(
            request_url,
            data = data,
            method = method,
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + self.api_key
            }
        )

    def handleRequest(self, req):
        response = request.urlopen(req)

        if (response.reason == 'OK'):
            return response.read().decode('utf-8')
        else:
            return response.status

    def getAllDroplets(self, page=1, limit_per_page=1):
        request_url = self.uri + '/v2/droplets'
        req = self.buildRequest(request_url)

        return self.handleRequest(req)

    def getDropletById(self, droplet_id):
        request_url = self.uri + '/v2/droplets/' + droplet_id
        req = self.buildRequest(request_url)

        return self.handleRequest(req)

    def getDropletsByTag(self, tag):
        request_url = self.uri + "/v2/droplets?%s" % urlencode({'tag_name': tag})
        req = self.buildRequest(request_url)

        return self.handleRequest(req)

    def getDropletsByHostname(self, hostname):
        droplets = json.loads(self.getAllDroplets())
        for droplet in droplets:
            if droplet['name'] == hostname:
                return droplet

        return False

    def deleteDroplet(self, droplet_id):
        request_uri = self.uri + '/v2/droplets/' + droplet_id
        req = self.buildRequest(request_url, method='DELETE')
        handledRequest = self.handleRequest(req)

        if (handledRequest = 204):
            return True
        else:
            return self.handleRequest(req)

    def createDroplet(self, hostname, region, droplet_size, image_id, ssh_keys,
        backups_enabled=False, ipv6=True, private_networking=True,
        user_data=None, monitoring=True, volumes=[], tags=[]):
        # Set up request data
        request_data = url_encode(
            {
                'name': hostname,
                'region': region,
                'size': droplet_size,
                'image': image_id,
                'ssh_keys': ssh_keys,
                'user_data': user_data,
                'backups': backups,
                'ipv6': ipv6,
                'private_networking': private_networking,
                'monitoring': monitoring,
                'volumes': volumes,
                'tags': tags
            }
        ).encode()
        request_url = self.uri + '/v2/droplets'
        req = self.buildRequest(request_url, data, 'POST')

        return self.handleRequest(req)

    def getAvailableSSHKeys(self):
        request_url = self.uri + '/v2/account/keys'
        req = self.buildRequest(request_url)

        return self.handleRequest(req)

    def getKeyInfo(self, keys):
        output = []
        if (isinstance(keys, str)):
            keys = list(keys)

        availableKeys = self.getAvailableSSHKeys()
        for key in availableKeys:
            for key_needle in keys:
                if (key['fingerprint'] == key_needle or key['id'] == key_needle):
                    output.append(key) 

        if (len(output) > 0):
            return output

        return False

    def createNewSSHKey(self, label, public_key):
        request_url = self.uri + '/v2/account/keys'
        request_data = url_encode(
            {
                'name': label,
                'public_key': public_key
            }
        ).encode()
        req = self.buildRequest(request_url, data, 'POST')

        return self.handleRequest(req)

    def deleteSSHKey(self, fingerprint):
        request_url = self.uri + '/v2/account/keys/' + fingerprint
        req = self.buildRequest(request_url, method='DELETE')

        return self.handleRequest(req)

    def listAllImages(self):
        request_url = self.uri + '/v2/images'
        req = self.buildRequest(request_url)

        return self.handleRequest(req)

    def listAllRegions(self):
        request_url = self.uri + '/v2/regions'
        req = self.buildRequest(request_url)

        return self.handleRequest(req)

    def getAvailableRegions(self):
        regions = json.loads(self.listAllRegions())
        if (isinstance(regions, int)):
            raise IndexError('Unable to retrieve regions')

        available_regions = []

        for region in regions['regions']:
            if (region['available'] == True):
                available_regions.append(region)

        return available_regions

    def getAvailableSizesForRegion(self, region_slug):
        regions = json.loads(self.listAllRegions())

        if (isinstance(regions, int)):
            raise IndexError('Unable to retrieve regions')

        for region in regions['regions']:
            if (region['slug'] == region_slug):
                if (region['available'] == True):
                    return region['sizes']
                else:
                    return False
        return False

