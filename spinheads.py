#!/usr/bin/env python
# We will import pyrax, os and argparse to get things done
import pyrax
import os
import argparse
import getpass
import time

pyrax.set_setting("identity_type", "rackspace")
pyrax.set_default_region("DFW")
#
#Build  and parse command-line arguments
#
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--name", 
                    help="The base name of the Cloud Server, e.g. Web")
args = parser.parse_args()
name = args.name

#
#Check if -n or --name option was supplied.  If it wasn't return an error
#
if args.name:
    pass
else:
    print("The Name argument is required.")

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")

try:
    pyrax.set_credential_file(creds_file)
except:
    print("Unable to locate" + creds_file + "!")


#
#Assign the pyrax.cloudservers object to cs
#
cs = pyrax.cloudservers


#
#Get the image name and ID, then assign the ID to the variable image_id
#
try:
    image = [img for img in cs.images.list()
        if "14.04" in img.name
        and "PVHVM" in img.name][0]
except:
    print("Unable to get image name Ubuntu 14.04.")


#
#Get the flavor name and ID, then assign the ID to the variable flavor_id
#
try:
    flavor_1GB = [flavor for flavor in cs.flavors.list()
        if flavor.ram == 1024][0]
except:
    print("Unable to get flavor name for 1GB server")


#
#Create the server_name variable from args.name
#
print "Creating server(s) now, please stand by."
print "..."
for num in range(1, 4):
    server_name = name + str(num)
    server = cs.servers.create(server_name, image.id, flavor_1GB.id)
    print "Server Name:", server.name
    print "Server ID:",  server.id
    print "Status:", server.status
    print "Admin password:", server.adminPass
    while not server.accessIPv4:
        time.sleep(1)
        server = cs.servers.get(server.id)
    print"Public: ", server.accessIPv4
    print ""
    print "..."
