#!/usr/bin/env python3

import yaml
import sys
import fileinput
import subprocess
import os
from datetime import datetime

try:
    print("Parsing config file...")
    # Load yaml config file as dict
    owd = os.getcwd()
    os.chdir("..")
    infpth = str(os.path.abspath(os.curdir)) + "/config.yml"
    os.chdir(owd)
    data = {}
    with open(infpth, 'r') as stream:
        try:
            data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print("\n Config file 'config.yml' could not be found in the DynamicDashboard directory\n")
    print("Initializing docker containers...")
    subprocess.run("docker start grafana", shell=True)
    subprocess.run("sudo docker run -d -p 9091:9091 prom/pushgateway", shell=True)
    print("Starting script...")
    # Help Command
    # Get current time stamp
    now = datetime.now()
    current_time = now.strftime("%d/%m/%Y_%H:%M:%S")
    timeTxt = " ( " + str(current_time) + " )"
    if data['switchNum'] == 1:
        print("Single Network Element Flow Detected")
        print("Collecting dashboard template...")
        # Map of replacements to complete from template.json to out.json
        replacements = {'IPHOSTA': str(data['hostA']['IP']), 
                        'IPHOSTB': str(data['hostB']['IP']),
                        'IFNAMEHOSTA': str(data['hostA']['interfaceName']),
                        'IFNAMEHOSTB': str(data['hostB']['interfaceName']),
                        'IFNAMESWITCHHOSTA': str(data['hostA']['switchPort']['ifIndex']),
                        'NAMEIFSWITCHA': str(data['hostA']['switchPort']['ifName']),
                        'NAMEIFSWITCHB': str(data['hostB']['switchPort']['ifName']),
                        'IFNAMESWITCHHOSTB': str(data['hostB']['switchPort']['ifIndex']),
                        'DATAPLANEIPA': str(data['hostA']['interfaceIP']),
                        'DATAPLANEIPB': str(data['hostB']['interfaceIP']),
                        'IPSWITCH': str(data['switchData']['target']),
                        'PUSHPORT': str(data['pushgatewayPort']),
                        'PUSHGATEWAYNAME': "pushgateway",
                        'PARAMS': str(data['switchData']['params']),
                        'SNMPHOSTIP': str(data['switchData']['SNMPHostIP']),
                        'DASHTITLE': str(data['dashTitle']) + timeTxt,
                        'DEBUGTITLE': str(data['debugTitle']) + timeTxt}
        print("Creating custom Grafana JSON Dashboard...")
        print("Creating custom L2 Debugging Dashboard...")
        # Iteratively find and replace in one go 
        with open('newTemplate.json') as infile, open('out.json', 'w') as outfile:
            for line in infile:
                for src, target in replacements.items():
                    line = line.replace(src, target)
                outfile.write(line)
        with open('debugTemplate.json') as infile, open('outDebug.json', 'w') as outfile:
            for line in infile:
                for src, target in replacements.items():
                    line = line.replace(src, target)
                outfile.write(line)
        print("Generating custom Prometheus config file...")
        # Iteratively find and replace in one go 
        with open('prometheusTemplate.yml') as infile, open('prometheus.yml', 'w') as outfile:
            for line in infile:
                for src, target in replacements.items():
                    line = line.replace(src, target)
                outfile.write(line)
        subprocess.run("sudo docker run -d  -p 9090:9090     -v $PWD/prometheus.yml:/etc/prometheus/prometheus.yml     prom/prometheus:v2.2.1", shell=True)

        print("Applying dashboard JSON to Grafana API...")
        # Run the API script to convert output JSON to Grafana dashboard automatically
        print("Loading Grafana dashboard on Grafana server...")
        cmd = "sudo python3 api.py out.json outDebug.json"
        subprocess.run(cmd, shell=True)
        print("Loaded Grafana dashboard")
    else:
        print("Multiple Network Element Flow Detected")
        print("Collecting dashboard template...")
        # Map of replacements to complete from template.json to out.json
        replacements = {}
        if data['switchNum'] == 2:
            replacements = {'IPHOSTA': str(data['hostA']['IP']), 
                            'IPHOSTB': str(data['hostB']['IP']),
                            'IFNAMEHOSTA': str(data['hostA']['interfaceName']),
                            'IFNAMEHOSTB': str(data['hostB']['interfaceName']),
                            'IFNAMESWITCHHOSTA': str(data['hostA']['switchPort']['ifIndex']),
                            'IFNAMESWITCHHOSTB': str(data['hostB']['switchPort']['ifIndex']),
                            'SWITCHBINCOMING': str(data['switchDataB']['portIn']['ifIndex']),
                            'SWITCHAOUTGOING': str(data['switchDataA']['portOut']['ifIndex']),
                            'NAMEIFAIN': str(data['hostA']['switchPort']['ifName']),
                            'NAMEIFAOUT': str(data['switchDataA']['portOut']['ifName']),
                            'NAMEIFBIN': str(data['switchDataB']['portIn']['ifName']),
                            'NAMEIFBOUT': str(data['hostB']['switchPort']['ifName']),
                            'DATAPLANEIPA': str(data['hostA']['interfaceIP']),
                            'DATAPLANEIPB': str(data['hostB']['interfaceIP']),
                            'PUSHPORT': str(data['pushgatewayPort']),
                            'PUSHGATEWAYNAME': "pushgateway",
                            'IPSWITCHA': str(data['switchDataA']['target']),
                            'IPSWITCHB': str(data['switchDataB']['target']),
                            'DASHTITLE':str(data['dashTitle']) + timeTxt,
                            'DEBUGTITLE': str(data['debugTitle']) + timeTxt}
        elif data['switchNum'] == 3:
            replacements = {'IPHOSTA': str(data['hostA']['IP']), 
                            'IPHOSTB': str(data['hostB']['IP']),
                            'IFNAMEHOSTA': str(data['hostA']['interfaceName']),
                            'IFNAMEHOSTB': str(data['hostB']['interfaceName']),
                            'IFNAMESWITCHHOSTA': str(data['hostA']['switchPort']['ifIndex']),
                            'SWITCHAOUTGOING': str(data['switchDataA']['portOut']['ifIndex']),
                            'SWITCHBINCOMING': str(data['switchDataB']['portIn']['ifIndex']),
                            'SWITCHBOUTGOING': str(data['switchDataB']['portOut']['ifIndex']),
                            'SWITCHCINCOMING': str(data['switchDataC']['portIn']['ifIndex']),
                            'IFNAMESWITCHHOSTB': str(data['hostB']['switchPort']['ifIndex']),
                            'NAMEIFAIN': str(data['switchDataA']['portIn']['ifName']),
                            'NAMEIFAOUT': str(data['switchDataA']['portOut']['ifName']),
                            'NAMEIFBIN': str(data['switchDataB']['portIn']['ifName']),
                            'NAMEIFBOUT': str(data['switchDataB']['portOut']['ifName']),
                            'NAMEIFCIN': str(data['switchDataC']['portIn']['ifName']),
                            'NAMEIFCOUT': str(data['switchDataC']['portOut']['ifName']),
                            'DATAPLANEIPA': str(data['hostA']['interfaceIP']),
                            'DATAPLANEIPB': str(data['hostB']['interfaceIP']),
                            'IPSWITCHA': str(data['switchDataA']['target']),
                            'IPSWITCHB': str(data['switchDataB']['target']),
                            'IPSWITCHC': str(data['switchDataC']['target']),
                            'PUSHPORT': str(data['pushgatewayPort']),
                            'PUSHGATEWAYNAME': "pushgateway",
                            'DASHTITLE':str(data['dashTitle']) + timeTxt,
                            'DEBUGTITLE': str(data['debugTitle']) + timeTxt}
        else:
            replacements = {'IPHOSTA': str(data['hostA']['IP']), 
                            'IPHOSTB': str(data['hostB']['IP']),
                            'IFNAMEHOSTA': str(data['hostA']['interfaceName']),
                            'IFNAMEHOSTB': str(data['hostB']['interfaceName']),
                            'IFNAMESWITCHHOSTA': str(data['hostA']['switchPort']['ifIndex']),
                            'SWITCHAOUTGOING': str(data['switchDataA']['portOut']['ifIndex']),
                            'SWITCHBINCOMING': str(data['switchDataB']['portIn']['ifIndex']),
                            'SWITCHBOUTGOING': str(data['switchDataB']['portOut']['ifIndex']),
                            'SWITCHCINCOMING': str(data['switchDataC']['portIn']['ifIndex']),
                            'SWITCHCOUTGOING': str(data['switchDataC']['portOut']['ifIndex']),
                            'SWITCHDINCOMING': str(data['switchDataD']['portIn']['ifIndex']),
                            'IFNAMESWITCHHOSTB': str(data['hostB']['switchPort']['ifIndex']),
                            'NAMEIFAIN': str(data['switchDataA']['portIn']['ifName']),
                            'NAMEIFAOUT': str(data['switchDataA']['portOut']['ifName']),
                            'NAMEIFBIN': str(data['switchDataB']['portIn']['ifName']),
                            'NAMEIFBOUT': str(data['switchDataB']['portOut']['ifName']),
                            'NAMEIFCIN': str(data['switchDataC']['portIn']['ifName']),
                            'NAMEIFCOUT': str(data['switchDataC']['portOut']['ifName']),
                            'NAMEIFDIN': str(data['switchDataD']['portIn']['ifName']),
                            'NAMEIFDOUT': str(data['switchDataD']['portOut']['ifName']),
                            'DATAPLANEIPA': str(data['hostA']['interfaceIP']),
                            'DATAPLANEIPB': str(data['hostB']['interfaceIP']),
                            'IPSWITCHA': str(data['switchDataA']['target']),
                            'IPSWITCHB': str(data['switchDataB']['target']),
                            'IPSWITCHC': str(data['switchDataC']['target']),
                            'IPSWITCHD': str(data['switchDataD']['target']),
                            'PUSHPORT': str(data['pushgatewayPort']),
                            'PUSHGATEWAYNAME': "pushgateway",
                            'DASHTITLE':str(data['dashTitle']) + timeTxt,
                            'DEBUGTITLE': str(data['debugTitle']) + timeTxt}
        print("Creating custom Grafana JSON Dashboard...")
        print("Creating custom L2 Debugging JSON Dashboard...")
        # Iteratively find and replace in one go 
        fname = "template" + str(data['switchNum']) + ".json"
        dname = "debugTemplate" + str(data['switchNum']) + ".json"
        with open(fname) as infile, open('out.json', 'w') as outfile:
            for line in infile:
                for src, target in replacements.items():
                    line = line.replace(src, target)
                outfile.write(line)     
        with open(dname) as infile, open('outDebug.json', 'w') as outfile:
            for line in infile:
                for src, target in replacements.items():
                    line = line.replace(src, target)
                outfile.write(line)            
        print("Applying dashboard JSON to Grafana API...")
        # Run the API script to convert output JSON to Grafana dashboard automatically
        print("Loading Grafana dashboard on Grafana server...")
        cmd = "sudo python3 api.py out.json outDebug.json"
        subprocess.run(cmd, shell=True)
        print("Loaded Grafana dashboard")
except KeyboardInterrupt:
    print("Interrupt detected")
    print("Shutting down SNMP Exporter instance to save resources...")