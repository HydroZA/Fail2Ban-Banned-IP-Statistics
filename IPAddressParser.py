# fail2ban ip output parser

from ip2geotools.databases.noncommercial import DbIpCity
from ip2geotools.errors import InvalidRequestError
from iso3166 import countries
import platform
import subprocess

if platform.system() != 'Linux':
	print ("This program is designed to run on linux only, you are using " + platform.system())
	quit()

names = []

def getOccurences(names, entries):
	found = []
	d = {}

	for name in names:
		occurences = names.count(name)
		if name in found:
			pass
		else:
			found.append(name)
			d[name] = round(occurences / entries * 100, 2)
	return d

def getIps(jail):
	cmd = 'sudo fail2ban-client status ' + jail
	stdoutdata = subprocess.getoutput(cmd)
	return stdoutdata

while True:
	try:
		ipStr = getIps(input("Enter the name of the jail to parse: ")) 
		ips = ipStr.split(' ')
		ips[0:34] = [] # Delete the fluff and keep only the list of IPs
		ips[0] = ips[0][6:] # ips[0] has text at the start of it, lets remove that
		print("\nSuccessfully retrieved IPs from fail2ban")
		break
	except IndexError:
		print ("\nUnable to parse IPs for the selected jail. Ensure jail name is identical to Fail2Ban")
		continue

ipsLen = len(ips)

print("Your Fail2Ban has " + str(ipsLen) + " IP addresses listed as banned")
while True:
	try:
		entries = input ("How many IP entries would you like to check? Press Enter for all. 0-")
		if entries == "":
			entries = ipsLen
			break
		else:
			entries = int(entries)
			if entries == 0:
				raise ValueError
			elif entries < 0:
				raise ValueError
			elif entries >= ipsLen:
				entries = ipsLen
				break
			elif entries < ipsLen:
				ips = ips[0:entries]
				ipsLen = len(ips)
				break
	except ValueError:
		print ("Invalid input")
		continue

progress = 0
for ip in ips:
	try:
		ip = ip.strip() # Remove all whitespace
		response = DbIpCity.get(ip, api_key="free") # Get all location information on IP
		country = str(countries.get(response.country)) # convert country code to full country name using ISO3166 library 
		fullNames = country.split('\'') # $country is a long string with other information in it, lets isolate the different parts of it 
		names.append(fullNames[1]) # Append only the country name to the names[]
	except KeyError:
		print(ip + " - country not found")
	except InvalidRequestError:
		print ("Location DB is down or you have been timed out, please try again later")
		quit()
	progress+=1
	print ("Progress: " + str(round((progress/ipsLen)*100)) + "%", end="\r")

d = getOccurences(names, int(entries))

print("\n")

sortedArr = sorted(d.items(), reverse=True, key = lambda x : x[1])
countryList = [x[0] for x in sortedArr]
percentages = [x[1] for x in sortedArr]

i = 0
for country in countryList:
	print (country + " = " + str(percentages[i]) + "%")
	i+=1
print ("\nThe most common country is " + countryList[0] + " with " + str(percentages[0]) + "%")
print ("The least common country is " + countryList[len(countryList)-1] + " with " + str(percentages[len(percentages)-1]) + "%")