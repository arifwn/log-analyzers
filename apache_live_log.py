
import os
import sys

import pygeoip

def get_country_dict(ip_dict, country_dict=None):
	if country_dict is None:
		country_dict = {}

	gi = pygeoip.GeoIP('data/GeoIP.dat')

	for ip in ip_dict:
		country = gi.country_name_by_addr(ip)
		count = country_dict.get(country, 0)
		country_dict[country] = count + 1

	return country_dict


def get_ip_dict(file_path, ip_dict=None):
	if ip_dict is None:
		ip_dict = {}
	with open(file_path) as f:
		for line in f:
			l = line.strip().split()
			if len(l) > 0:
				ip = l[0]
				count = ip_dict.get(ip, 0)
				ip_dict[ip] = count + 1
	return ip_dict


def main():
	# print sys.argv
	if len(sys.argv) <= 1:
		print 'please specify log files'
	
	files = []

	for f in sys.argv[1:]:
		try:
			os.stat(f)
			files.append(f)
		except OSError:
			pass

	print 'Found ', len(files), 'files!'
	ip_dict = {}
	for f in files:
		get_ip_dict(f, ip_dict)
	
	print 'total visitor ip:', len(ip_dict)

	country_dict = get_country_dict(ip_dict)
	print 'total country:', len(country_dict)

	for country in sorted(country_dict.iterkeys()):
		print country, ':', country_dict[country]

if __name__ == '__main__':
	main()