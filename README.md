# Fail2Ban-Banned-IP-Statistics
## Description
Python program that parses a file created from the output of `sudo fail2ban-client status [JAILNAMEHERE]` and returns statistics on the location of the IP's.

## Installation
1. `pip3 install ip2geotools`
2. `pip3 install iso3166`

## Usage
1. Run `sudo fail2ban-client status [JAILNAMEHERE] > ips` in a terminal from the directory of the python executable
2. `python3 IPAddressParser.py`
3. Input the amount of IP's to check up to, or press enter to check the entire file. Checking 1000 IP's will take roughly 5 minutes depending on internet speed

## Issues
Currently, I've determined the `ip2geotools` package only allows roughly 1000 IP's to be queried before it will time you out for a few hours. I believe its possible to purchase a commercial license that will enable the ability to query more IPs.
