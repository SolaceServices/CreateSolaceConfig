#!/usr/bin/python
# CreateSolaceCfg.py
#   Script to generate Solace VPN and other config JSON files based on inputs
#   Demo for DevAdmin training
# Ramesh Natarajan, (ramesh.natarajan@solace.com) Solace PSG
# 1.0 01/21/2021

import argparse
import os, glob
import json

#-----------------------------------------------------------------------------
#   MAIN
#-----------------------------------------------------------------------------
# Parse args
p = argparse.ArgumentParser(description='Create Solace Config JSON Files',
                            formatter_class=argparse.RawDescriptionHelpFormatter)
p.add_argument('--vpn', action="store",  required=True, help='VPN Name')
p.add_argument('--dir', action="store",  required=True, help='Directory with input files')
p.add_argument('--defaults', action="store",  required=False, help='Defaults file', default="default")
p.add_argument( '--verbose', '-v', action="count",  required=False, default=0,
                help='Turn Verbose. Use -vvv to be very verbose')
r = p.parse_args()

d_fields = {}
d_inputs = {}

# collect all input files
if r.verbose > 0:
    print ('Arguments:\n\tVPN: {}\n\tDefaults file: {}\n\tDir: {}'.format(r.vpn, r.defaults, r.dir))

if not os.path.exists(r.dir):
    print ("Input dir {} not found".format(r.dir))
    exit(2)

adir='create'
# Open Defaults config files
defaults_file = 'cfg/{}.json'.format(r.defaults)
print ('Opening {} defaults file: {}'.format(r.defaults, defaults_file))
with open(defaults_file, 'r') as defaults_fd:
    defaults_json = json.load(defaults_fd)
    if r.verbose > 2:
        print (json.dumps(defaults_json, indent=3))

# read input CSV files into a dictionary of arrays (d_inputs)
# separate title into d_fields
print ('Opening input files from: {}'.format(r.dir))
files=glob.glob('{}/*.csv'.format(r.dir))
if r.verbose > 2:
    print ('files:', files)
for file in files:
    fname = os.path.splitext(os.path.basename(file))[0]
    if r.verbose > 0:
        print ('\tOpening file {}'.format(file))
    with open(file, 'r') as fd:
        d_fields[fname] = fd.readline().strip()
        d_inputs[fname] = fd.readlines()
# add vpn object -- its read in from arg
d_fields['vpn'] = 'msgVpnName'
d_inputs['vpn'] = [r.vpn]

# Loop thru the objects (acl_profile, client_profile, queues, ...)
for vpnobj in d_inputs.keys():
    # Read corresponding template json file
    print ('Generating {} configs'.format(vpnobj))
    template_file = 'templates/{}/{}.json'.format(adir, vpnobj)
    if r.verbose > 0:
        print ('\tOpening template file: {}'.format(template_file))
    with open(template_file, 'r') as template_fd:
        json_data = json.load(template_fd)
    if r.verbose > 2:
        print ('--- Data read')
        print (json.dumps(json_data))

    # replace passed in & read in values
    json_data["msgVpnName"] = r.vpn

    l_fields = d_fields[vpnobj].split(',')
    if r.verbose > 2:
        print ('title', d_fields[vpnobj])
        print ('title list', l_fields)
    output_dir = "output/{}-{}/{}_config".format(r.vpn, r.defaults, vpnobj)
    # If output dir doesn't exist, create it
    if not os.path.exists(output_dir):
        print ("Creating output dir: {}". format(output_dir))
        os.makedirs(output_dir, 0o0755, exist_ok=True)
    for l in d_inputs[vpnobj]:
        l = l.strip()
        # skip empty and comment lines
        if len(l) <= 1 or l.startswith('#'):
            continue
        l_values =  l.split(',')
        if r.verbose > 0:
            print ("\tCreating Config for {}: {}".format(vpnobj, l_values[0]))
        if r.verbose > 2:
            print('values list', l_values, len(l))

        # replace field value (eg: queueName) with value read in (eg: myqueue1)
        # multiple substitions used only for client_user now -- username, acl_profile, client_profile
        n = 0
        while n < len(l_fields):
            json_data[l_fields[n]] = l_values[n]
            n = n + 1

        if vpnobj in defaults_json.keys():
            vpnobj_values = defaults_json[vpnobj]
            for k, v in vpnobj_values.items():
                if (r.verbose > 0):
                    print ('\tSet {}.{} => {}'.format(vpnobj, k, v))
                json_data[k] = v
        if r.verbose > 2:
            print ('--- Data modified')
            print (json.dumps(json_data, indent=3))

        # Write output json file
        output_file = "{}/{}.json".format(output_dir, l_values[0])
        print ("\tCreating {}".format(output_file))
        with open(output_file, "w") as output_fd:
            json.dump(json_data, output_fd, indent=3)
