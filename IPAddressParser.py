# fail2ban ip output parser

from ip2geotools.databases.noncommercial import DbIpCity
from ip2geotools.errors import InvalidRequestError
from iso3166 import countries
from datetime import datetime
import platform
import subprocess

if platform.system() != 'Linux':
	print ("This program is designed to run on linux only, you are using " 
		+ platform.system())
	quit()

names = []

def GetOccurences(names, entries):
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

def GetIps(jail):
	cmd = 'sudo fail2ban-client status ' + jail
	stdoutdata = subprocess.getoutput(cmd)
	return stdoutdata

while True:
	try:
		ips_string = GetIps(input("Enter the name of the jail to parse: ")) 
		ips = ips_string.split(' ')
		ips[0:34] = [] # Delete the fluff and keep only the list of IPs
		ips[0] = ips[0][6:] # ips[0] has text at the start of it, lets remove that
		print("\nSuccessfully retrieved IPs from fail2ban")
		break
	except IndexError:
		print ("\nUnable to parse IPs for the selected jail. Ensure jail name is identical to Fail2Ban")
		continue

ips_len = len(ips)

print("Your Fail2Ban has " + str(ips_len) + " IP addresses listed as banned")
while True:
	try:
		entries = input ("How many IP entries would you like to check? Press Enter for all. 0-")
		if entries == "":
			entries = ips_len
			break
		else:
			entries = int(entries)
			if entries == 0:
				raise ValueError
			elif entries < 0:
				raise ValueError
			elif entries >= ips_len:
				entries = ips_len
				break
			elif entries < ips_len:
				ips = ips[0:entries]
				ips_len = len(ips)
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
		full_names = country.split('\'') # isolate the different parts of $country 
		names.append(full_names[1]) # Append only the country name to the names[]
	except KeyError:
		print(ip + " - country not found")
	except InvalidRequestError:
		print ("Location DB is down or you have been timed out, please try again later")
		quit()

	progress+=1
	print ("Progress: " + str(round((progress/ips_len) * 100)) + "%", end="\r")

d = GetOccurences(names, int(entries))

print("\n")

sorted_dictionary = sorted(d.items(), reverse=True, key = lambda x : x[1])
country_list = [x[0] for x in sorted_dictionary]
percentages = [x[1] for x in sorted_dictionary]

i = 0
for country in country_list:
	print ("[" + str(i+1) + "] " + country + " = " + str(percentages[i]) + "%")
	i+=1
print ("\nThe most common country is " + country_list[0] + " with " 
	+ str(percentages[0]) + "%")
print ("The least common country is " + country_list[len(country_list)-1] 
	+ " with " + str(percentages[len(percentages)-1]) + "%")

while True:
	write_to_file = input("\nWould you like to write the output to a file? (Y/N) ")
	if write_to_file.upper() == 'Y':
		date = str(datetime.now()) # Get time and date to append to output file
		date = date[0:10] # Isolate only the date
		with open(date + ".stats", "w") as f:
			i = 0
			for country in country_list:
				f.write( ("[" + str(i+1) + "] " + country + " = " + str(percentages[i]) + "%\n"))
				i+=1
			f.write("\nThe most common country is " + country_list[0] + " with " 
				+ str(percentages[0]) + "%\n")
			f.write("The least common country is " + country_list[len(country_list)-1] 
				+ " with " + str(percentages[len(percentages)-1]) + "%\n")
			f.close()
		print ("Successfully created file \"" + date + ".stats\"")
		break
	elif write_to_file.upper() == 'N':	
		break
	else:
		print ("Invalid input")
print ("Thanks for using Fail2Ban IP Address Parser!")