import csv
from datetime import datetime
import time

def calcTimeDuration(start, end):
	start.replace("JUN", "Jun")
	start.replace("JUL", "Jul")
	start.replace("AUG", "Aug")

	fmt = '%d-%b-%y %H:%M:%S'
	d1 = datetime.strptime(start, fmt)
	d2 = datetime.strptime(end, fmt)

	# Convert to Unix timestamp
	d1_ts = time.mktime(d1.timetuple())
	d2_ts = time.mktime(d2.timetuple())

	# They are now in seconds, subtract and then divide by 60 to get minutes.
	diff = (d2_ts-d1_ts) / 60

	return diff

data_by_type = dict()
org_unit_data = dict()
data_by_unit = dict()
unit_avg_duration = dict()
unit_dispatch_count = dict()

with open('cad-events-boilermake-partial.csv', 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
	for row in spamreader:
		entry = dict()
		entry['unit'] = row[1]
		entry['org'] = row[2]
		entry['start'] = row[3]
		entry['end'] = row[4]
		entry['type'] = row[5]
		entry['code'] = row[6]
		entry['description'] = row[7]

		if entry['type'] == "SCHED" or entry['type'] == "ARREST":
			entry['duration'] = None
		else:
			entry['duration'] = calcTimeDuration(entry['start'], entry['end'])

			if not entry['unit'] in unit_dispatch_count:
				unit_dispatch_count[entry['unit']] = 0
			unit_dispatch_count[entry['unit']] += 1

			if not entry['unit'] in unit_avg_duration:
				unit_avg_duration[entry['unit']] = 0
			unit_avg_duration[entry['unit']] += entry['duration']

		if not entry['unit']in data_by_unit:
			data_by_unit[entry['unit']] = []
		data_by_unit[entry['unit']].append(entry)

		#sort org data
		if not entry['org'] in org_unit_data:
			org_unit_data[entry['org']] = set()
		if not entry['unit'] in org_unit_data[entry['org']]:
			org_unit_data[entry['org']].add(entry['unit'])

		#sort data by type
		if not entry['type'] in data_by_type:
			data_by_type[entry['type']] = []
		data_by_type[entry['type']].append(entry)

		print entry

for unit in unit_avg_duration:
	unit_avg_duration[unit] = unit_avg_duration[unit]/unit_dispatch_count[unit]
	print unit + ": " + str(unit_avg_duration[unit]) + " " + str(unit_dispatch_count[unit])
