import csv
from datetime import datetime
import time
import operator

def putIfAbsent(dic, key, val):
	if not key in dic:
		dic[key] = val

def calcTimeDuration(start, end):
	fmt = '%d-%b-%y %H:%M:%S'
	d1 = datetime.strptime(start, fmt)
	d2 = datetime.strptime(end, fmt)

	# Convert to Unix timestamp
	d1_ts = time.mktime(d1.timetuple())
	d2_ts = time.mktime(d2.timetuple())

	# They are now in seconds, subtract and then divide by 60 to get minutes.
	diff = (d2_ts-d1_ts) / 60

	return diff

def displayAverages(min_threshold, types):
	print "displaying averages for min threshold " + str(min_threshold) + " with types " + str(types)
	unit_totals_for_type = dict()
	unit_counts_for_type = dict()
	unit_avg_for_type = dict()
	for unit in unit_total_duration:
		for t in types:
			if t in unit_total_duration[unit]:
				putIfAbsent(unit_totals_for_type, unit, 0)
				putIfAbsent(unit_counts_for_type, unit, 0)
				unit_totals_for_type[unit] += unit_total_duration[unit][t]
				unit_counts_for_type[unit] += unit_dispatch_count[unit][t]

	for unit in unit_totals_for_type:
		unit_avg_for_type[unit] = unit_totals_for_type[unit] / unit_counts_for_type[unit]

	unit_avgs_sorted = sorted(unit_avg_for_type.items(), key=operator.itemgetter(1))

	for unit, dur in unit_avgs_sorted:
		if unit_counts_for_type[unit] >= min_threshold:
			print "Unit: " + unit + " Avg Duration: " + str(dur) + " Count: " + str(unit_counts_for_type[unit])

data_by_type = dict()
org_unit_data = dict()
data_by_unit = dict()
unit_total_duration = dict()
unit_dispatch_count = dict()

with open('cad-events-boilermake-partial.csv', 'rb') as csvfile:
	datareader = csv.reader(csvfile, delimiter=',', quotechar='"')
	for row in datareader:
		unit = row[1]
		org = row[2]
		start = row[3]
		end = row[4]
		disp_type = row[5]
		code = row[6]
		descr = row[7]
		dur = calcTimeDuration(start, end)

		entry = dict()
		entry['unit'] = unit
		entry['org'] = org
		entry['start'] = start
		entry['end'] = end
		entry['type'] = disp_type
		entry['code'] = code
		entry['description'] = descr
		entry['duration'] = dur
		
		#count of dispatch calls by unit and type
		putIfAbsent(unit_dispatch_count, unit, dict())
		putIfAbsent(unit_dispatch_count[unit], disp_type, 0)
		unit_dispatch_count[unit][disp_type] += 1

		#count of total time spent on calls by unit and type
		putIfAbsent(unit_total_duration, unit, dict())
		putIfAbsent(unit_total_duration[unit], disp_type, 0)
		unit_total_duration[unit][disp_type] += dur

		#entries by unit
		putIfAbsent(data_by_unit, unit, [])
		data_by_unit[unit].append(entry)

		#sort org and unit data
		putIfAbsent(org_unit_data, org, set())
		if not unit in org_unit_data[org]:
			org_unit_data[org].add(unit)

		#entries by type
		putIfAbsent(data_by_type, disp_type, [])
		data_by_type[disp_type].append(entry)

displayAverages(100, ["DSP", "STKDSP", "TSTOP"])



