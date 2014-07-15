
import json
import os
import re
import sys

from datetime import datetime

from geoip import open_database

db = None

def get_geoip_db():
    global db
    if db is None:
        db = open_database('data/GeoLite2-City.mmdb')
    return db


def get_location_info(ip):
    ipdb = get_geoip_db()
    data = {}

    match = ipdb.lookup(ip)
    if match is not None:
        info_dict = match.get_info_dict()
        data['city_id'] = info_dict.get('city', {}).get('geoname_id')
        data['city_name'] = info_dict.get('city', {}).get('names', {}).get('en')

        data['country_id'] = info_dict.get('country', {}).get('geoname_id')
        data['country_code'] = info_dict.get('country', {}).get('iso_code')
        data['country_name'] = info_dict.get('country', {}).get('names', {}).get('en')

        data['location'] = info_dict.get('location')
        data['postal'] = info_dict.get('postal')

    return data


def main():
    # print sys.argv
    if len(sys.argv) <= 1:
        print 'please specify log file'

    url_filter = None
    useragent_filter = None

    file_path = sys.argv[1]
    try:
        url_filter = sys.argv[2]
        useragent_filter = sys.argv[3]
    except Exception, e:
        pass


    regex = re.compile(r'(?P<ipaddress>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(?P<dateandtime>\d{2}\/[a-z]{3}\/\d{4}:\d{2}:\d{2}:\d{2} (\+|\-)\d{4})\] ((\"(GET|POST) )(?P<url>.+)(http\/1\.1")) (?P<statuscode>\d{3}) (?P<bytessent>\d+) (["](?P<refferer>(\-)|(.+))["]) (["](?P<useragent>.+)["])', re.IGNORECASE)
    logdata = []
    with open(file_path) as f:
        for line in f:
            match = regex.match(line)
            if not match:
                continue;
            data = match.groupdict()

            # filter
            if url_filter and url_filter not in data['url']:
                continue
            if useragent_filter and useragent_filter not in data['useragent']:
                continue

            if data.get('ipaddress', None):
                data['geoip'] = get_location_info(data['ipaddress'])
            else:
                data['geoip'] = {}

            if data.get('dateandtime', None):
                dt = datetime.strptime(data['dateandtime'].split()[0], "%d/%b/%Y:%H:%M:%S")
                data['date_isoformat'] = dt.isoformat()
            else:
                data['date_isoformat'] = None

            logdata.append(data)

    with open('data/log.json', 'w') as f:
        json.dump(logdata, f, sort_keys=True, indent=4, separators=(',', ': '))

if __name__ == '__main__':
    main()
