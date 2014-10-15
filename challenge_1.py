#!/bin/env python

import pyrax
import os
import argparse
import time

def arg_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", required=True, help="The base name of the Cloud Server, e.g. Web")
    parser.add_argument("-c", "--count", required=True, type=int, help="Number of server to build")
    parser.add_argument("-i", "--image", type=int, help="The image that you would like to use")
    parser.add_argument("-f", "--flavor", type=int, help="The server flavor")
    parser.add_argument("-r", "--region", default='DFW', help="Region")
    my_args = parser.parse_args()
    my_args.region = my_args.region.upper()
    return my_args


def rack_creds():
  pyrax.set_setting("identity_type", "rackspace")
  pyrax.set_default_region("DFW")
  if os.path.isfile(os.path.expanduser("~/.rackspace_cloud_credentials")):
    creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
    pyrax.set_credential_file(creds_file)
  else:
    print("unable to locate rackspace cloud credentials file")

def listerator(resource):
  for k, v in enumerate(resource):
    print k, v.name


def build_cloud_server(count):
  cs = pyrax.cloudservers
  i_args = arg_input()
  i_args.name = i_args.name + str(count)
  if not i_args.image:
    print("Cloud server images: ")
    listerator(cs.images.list())
    i_args.image = raw_input("Enter image number:")
  i_args.image = cs.images.list()[int(i_args.image)]
  if not i_args.flavor:
    print("Cloud server flavors: ")
    listerator(cs.flavors.list())
    i_args.flavor = raw_input("Enter flavor number:")
  i_args.flavor = cs.flavors.list()[int(i_args.flavor)]
  server = cs.servers.create(i_args.name, i_args.image, i_args.flavor)
  print("Name:", server.name)
  print("ID:", server.id)
  print("Status:", server.status)
  print("Admin Password:", server.adminPass)
  while not server.networks:
    time.sleep(1)
    server = cs.servers.get(server.id)
  print("Networks:", server.networks)


def main():
  i_args = arg_input()
  i_args.count += 1
  print i_args
  rack_creds()
  for x in range(1, i_args.count):
    build_cloud_server(x)


if __name__ == "__main__":
    main()
