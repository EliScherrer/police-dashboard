import csv
from datetime import datetime
import time
import operator

def getAvgInfo():
	print "Enter min threshold and types, all comma delimited"
	res = raw_input()
	while(res != "exit"):
		res_arr = res.split(',')
		min_threshold = int(res_arr.pop(0))

		print res_arr
		print min_threshold

		displayAverages(min_threshold, res_arr)
		print "Enter min threshold and types, all comma delimited"
		res = raw_input()

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
	for unit in unit_data:
		for t in types:
			if unit_data[unit]['count'][t] != 0:
				putIfAbsent(unit_totals_for_type, unit, 0)
				putIfAbsent(unit_counts_for_type, unit, 0)
				unit_totals_for_type[unit] += unit_data[unit]['duration'][t]
				unit_counts_for_type[unit] += unit_data[unit]['count'][t]

	for unit in unit_totals_for_type:
		unit_avg_for_type[unit] = unit_totals_for_type[unit] / unit_counts_for_type[unit]

	unit_avgs_sorted = sorted(unit_avg_for_type.items(), key=operator.itemgetter(1))

	for unit, dur in unit_avgs_sorted:
		if unit_counts_for_type[unit] >= min_threshold:
			print "Unit: " + unit + " Avg Duration: " + str(dur) + " Count: " + str(unit_counts_for_type[unit])

def statsByOrg():
	org_stats = dict()
	for org in org_unit_data:
		org_stats[org] = {'count': {'ARREST': 0, 'DSP': 0, 'STKDSP': 0, 'OUTSER': 0, 'TSTOP': 0, 'SCHED': 0, 'OTHER': 0}, 
						'duration': {'ARREST': 0, 'DSP': 0, 'STKDSP': 0, 'OUTSER': 0, 'TSTOP': 0, 'SCHED': 0, 'OTHER': 0, 'UNPROD': 0}}

		for unit in org_unit_data[org]:
			other_count = 0
			for t in unimportant_types:
				other_count += unit_data[unit]['count'][t]

			other_dur = 0
			for t in unimportant_types:
				other_dur += unit_data[unit]['duration'][t]

			unproductive_dur = (unit_data[unit]['duration']["SCHED"]) - (unit_data[unit]['duration']["OUTSER"] + unit_data[unit]['duration']["ARREST"] + 
				unit_data[unit]['duration']["DSP"] + unit_data[unit]['duration']["STKDSP"] + unit_data[unit]['duration']["TSTOP"] + other_dur)

			org_stats[org]['count']['SCHED'] += unit_data[unit]['count']["SCHED"]
			org_stats[org]['count']['ARREST'] += unit_data[unit]['count']["ARREST"]
			org_stats[org]['count']['DSP'] += unit_data[unit]['count']["DSP"]
			org_stats[org]['count']['STKDSP'] += unit_data[unit]['count']["STKDSP"]
			org_stats[org]['count']['OUTSER'] += unit_data[unit]['count']["OUTSER"]
			org_stats[org]['count']['TSTOP'] += unit_data[unit]['count']["TSTOP"]
			org_stats[org]['count']['OTHER'] += other_count

			org_stats[org]['duration']['SCHED'] += unit_data[unit]['duration']["SCHED"]
			org_stats[org]['duration']['ARREST'] += unit_data[unit]['duration']["ARREST"]
			org_stats[org]['duration']['DSP'] += unit_data[unit]['duration']["DSP"]
			org_stats[org]['duration']['STKDSP'] += unit_data[unit]['duration']["STKDSP"]
			org_stats[org]['duration']['OUTSER'] += unit_data[unit]['duration']["OUTSER"]
			org_stats[org]['duration']['TSTOP'] += unit_data[unit]['duration']["TSTOP"]
			org_stats[org]['duration']['OTHER'] += other_dur
			org_stats[org]['duration']['UNPROD'] += unproductive_dur

	org_keys = dict()
	for org in org_unit_data:
		org_keys[org] = org_stats[org]['duration']['UNPROD'] / org_stats[org]['duration']['SCHED']

	org_keys_sorted = sorted(org_keys.items(), key=operator.itemgetter(1))

	rank = 1
	for org, unprod_perc in org_keys_sorted:
		outser_perc = org_stats[org]['duration']['OUTSER'] / org_stats[org]['duration']['SCHED']
		arrest_perc = org_stats[org]['duration']['ARREST'] / org_stats[org]['duration']['SCHED']
		dsp_perc = org_stats[org]['duration']['DSP'] / org_stats[org]['duration']['SCHED']
		stkdsp_perc = org_stats[org]['duration']['STKDSP'] / org_stats[org]['duration']['SCHED']
		tstop_perc = org_stats[org]['duration']['TSTOP'] / org_stats[org]['duration']['SCHED']
		other_perc = org_stats[org]['duration']['OTHER'] / org_stats[org]['duration']['SCHED']

		print("Rank " + str(rank) + ".  ORG: " + org)
		print("Counts - SCHED: " + str(org_stats[org]['count']['SCHED']) + " ARREST: " + str(org_stats[org]['count']['ARREST']) + " DSP: " + str(org_stats[org]['count']['DSP'])
			+ " STKDSP: " + str(org_stats[org]['count']['STKDSP']) + " OUTSER: " + str(org_stats[org]['count']['OUTSER']) + " TSTOP: " + str(org_stats[org]['count']['TSTOP'])
			+ " OTHER: " + str(org_stats[org]['count']['OTHER']))
		print("Durations - SCHED: " + str(org_stats[org]['duration']['SCHED']) + " ARREST: " + str(org_stats[org]['duration']['ARREST']) + " DSP: " + str(org_stats[org]['duration']['DSP'])
			+ " STKDSP: " + str(org_stats[org]['duration']['STKDSP']) + " OUTSER: " + str(org_stats[org]['duration']['OUTSER']) + " TSTOP: " + str(org_stats[org]['duration']['TSTOP'])
			+ " OTHER: " + str(org_stats[org]['duration']['OTHER']))
		print("Unproductive time: " + str(org_stats[org]['duration']['UNPROD'] ))
		print("Percentages - UNPROD: " + str(unprod_perc) + " OUTSER: " + str(outser_perc) + " ARREST: " + str(arrest_perc) + " DSP: " + str(dsp_perc)
			+ " STKDSP: " + str(stkdsp_perc) + " TSTOP: " + str(tstop_perc) + " OTHER: " + str(other_perc))
		print("")
		rank += 1



#all code types -> ['ASSTER', 'XONS', 'ACK', 'DE', 'STKDSP', 'DOS', 'TSTOP', 'SCHED', 'XENR', 'AUTPRE', 'TPURS', 
#    'ASSTOS', 'PREMP', 'UNITINFO', 'OUTSER', 'SSTOP', 'CLEAR', 'MISC', 'DSP', 'ENR', 'FPURS', 'HOLD', 'EXCH', 
#    'REMINQ', 'ARREST', 'HOTE', 'ASST']

unimportant_types = ['ASSTER', 'XONS', 'ACK', 'DE', 'DOS', 'XENR', 'AUTPRE', 'TPURS', 
    'ASSTOS', 'PREMP', 'UNITINFO', 'SSTOP', 'CLEAR', 'MISC', 'ENR', 'FPURS', 'HOLD', 'EXCH', 
    'REMINQ', 'HOTE', 'ASST']

empty_type_dict = {'ASSTER': 0, 'XONS': 0, 'ACK': 0, 'DE': 0, 'STKDSP': 0, 'DOS': 0, 'TSTOP': 0, 'SCHED': 0, 'XENR': 0, 'AUTPRE': 0, 'TPURS': 0, 
    'ASSTOS': 0, 'PREMP': 0, 'UNITINFO': 0, 'OUTSER': 0, 'SSTOP': 0, 'CLEAR': 0, 'MISC': 0, 'DSP': 0, 'ENR': 0, 'FPURS': 0, 'HOLD': 0, 'EXCH': 0, 
    'REMINQ': 0, 'ARREST': 0, 'HOTE': 0, 'ASST': 0}

data_by_type = dict()
org_unit_data = dict()
unit_org_data = dict()
data_by_unit = dict()
unit_total_duration = dict()
unit_dispatch_count = dict()
unit_data = dict()

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
		
		# #count of dispatch calls by unit and type
		# putIfAbsent(unit_dispatch_count, unit, empty_type_dict.copy())
		# unit_dispatch_count[unit][disp_type] += 1

		# #count of total time spent on calls by unit and type
		# putIfAbsent(unit_total_duration, unit, empty_type_dict.copy())
		# unit_total_duration[unit][disp_type] += dur

		#count of dispatch calls by unit and type
		putIfAbsent(unit_data, unit, {'count': empty_type_dict.copy(), 'duration': empty_type_dict.copy()})
		unit_data[unit]['count'][disp_type] += 1

		#count of total time spent on calls by unit and type
		unit_data[unit]['duration'][disp_type] += dur

		#entries by unit
		putIfAbsent(data_by_unit, unit, [])
		data_by_unit[unit].append(entry)

		# org -> unit data
		putIfAbsent(org_unit_data, org, set())
		if not unit in org_unit_data[org]:
			org_unit_data[org].add(unit)

		# unit -> org data
		unit_org_data[unit] = org

		#entries by type
		putIfAbsent(data_by_type, disp_type, [])
		data_by_type[disp_type].append(entry)

displayAverages(100, ["DSP", "STKDSP", "TSTOP"])
