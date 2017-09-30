import csv
from datetime import datetime
import time
import operator

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

print("Enter cad unit and types comma delimited:")
res = raw_input()
res_arr = res.split(',')

unit_input = res_arr.pop(0)
types = res_arr

total_duration = 0
total_count = 0

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

		if unit == unit_input and disp_type in types:
			total_duration += calcTimeDuration(start, end)
			total_count += 1

avg = total_duration / total_count
print "Unit: " + unit_input + " Avg Duration: " + str(avg) + " Count: " + str(total_count)
		
		