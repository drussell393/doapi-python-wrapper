# DigitalOcean API Wrapper for Python

Quick notes:

    - This version (v1.0) does not include all of DO's API commands, instead it
      only includes the commands that I needed. These are listed below

    - I am still actively developing this, so I may add additional commands in
      the future.

    - You are allowed to make a pull request will the additional commands.
      Please read and understand my methodology behind how requests are made.


## Commands Currently Integrated

The following commands are currently integrated into this script:

    - DOAPI.buildRequest()
        - Builds the request using urllib when given from another function

    - DOAPI.handleRequest()
        - Handles the request using urllib

    - DOAPI.getAllDroplets()
        - Retrieves a list of your Droplets
        - Returns data in bytes. Use json.loads() or json.dumps() in your
          application to change this/display it better.

    - DOAPI.getDropletById(droplet_id)
        - Shows you information about one (1) droplet by id. 
        - Returns data in bytes. Use json.loads() or json.dumps() in your
          application to change this/display it better.

    - DOAPI.getDropletsByTag(tag)
        - Shows you information about all droplets that have a specific tag
        - Returns data in bytes. Use json.loads() or json.dumps() in your
          application to change this/display it better.

    - DOAPI.getDropletsByHostname(hostname)
        - Retrieves droplets by a hostname
        - Will retrieve more than one, if you have a droplet named the same for
          some weird reason
        - Returns data as a Python array (from json.loads())

    - DOAPI.deleteDroplet(droplet_id)
        - Deletes a droplet based on ID
        - Returns True on success, otherwise returns the HTTP status

    - DOAPI.createDroplet(hostname, region, droplet_size, image_id, ssh_keys=[], 
        backups_enabled=False, ipv6=True, private_networking=True, user_data=None,
        monitoring=True, volumes=[], tags=[])
        - Creates a new Droplet
        - Backups are defaulted to off (False)
        - private networking, monitoring and ipv6 default to true

    - DOAPI.getAvailableSSHKeys()
        - Lists all of the SSH keys on your account, along with their IDs and
          Fingerprints (used in the API)
        - Returns in bytes. Use json.loads() or json.dumps() to make this better
          for your needs.

    - DOAPI.getKeyInfo(key_id)
        - Lists key info for a key based on either a key ID or a key fingerprint
        - You can make "key_id" a list of key ids/fingerprints for more than one
          key as well.
        - Returns in bytes, amend to your liking as needed.

    - DOAPI.createNewSSHKey(label, public_key)
        - Adds a key (with label & public_key) onto your account

    - DOAPI.deleteSSHKey(key_fingerprint)
        - Deletes a key from your account based on fingerprint

    - DOAPI.listAllImages()
        - Lists all available images at DO
        - Returns in bytes

    - DOAPI.listAllRegions()
        - Lists all regions that DO has
        - Returns in bytes

    - DOAPI.getAvailableRegions()
        - Lists regions with availability
        - Returns in json.loads() format

    - DOAPI.getAvailableSizesForRegion(region_slug)
        - List available sizes in a specific region based on slug (ie. `nyc1`)

## Making a Pull Request

I welcome pull requests, but please make sure that any additional commands that
you add use the same buildRequest() and handleRequest() functions. You can use
these functions to handle `PUT`, `DELETE`, and `POST`requests as well.

For `GET` requests, DO's API doesn't allow us to send those through urllib (or
maybe urllib doesn't allow us). Either way, use urllib.parse.urlencode() --
already imported -- to urlencode the GET request, and append it to request_url.

Please also use the same naming conventions, so we can keep our heads on
straight... variables should have underscore_separated_words for readability,
functions shouldBeCamelCase, and classes should be CapitalCase unless where it's
all an acronym (ie. DO and API are acronyms, hence DOAPI).

In the future, we may want to force json.loads() returns (so it's not done at
the application level).. though I'm not 100% decided on that yet.
