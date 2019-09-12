# Fail2Ban Banned IP Statistics
## Description
Python program that parses the output created from `sudo fail2ban-client status [JAILNAMEHERE]` and returns statistics on the location of the IP's.

This allows admins to determine where attacks on their servers originate from and take action accordingly.

## Installation
This program is only designed to work on Linux and is verified to work on Fail2Ban v0.10.2
1. `git clone https://github.com/HydroZA/Fail2Ban-Banned-IP-Statistics`
2. `pip3 install ip2geotools`
3. `pip3 install iso3166`

## Usage
1. `python3 IPAddressParser.py`
2. Enter the name of the jail to parse
3. Input the amount of IP's to check up to, or press enter to check the entire file. Checking 1000 IP's will take roughly 5 minutes depending on internet speed

## Issues
Currently, I've determined the `ip2geotools` package only allows roughly 1000 IP's to be queried before it will time you out for a few hours. I believe its possible to purchase a commercial license that will enable the ability to query more IPs.
