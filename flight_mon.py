#!/usr/bin/env python

"""
This is a script to read the output of an
sdr capturing 1090Mhz channel and sending
the data to port 30003.
"""

import subprocess
import time

p1 = subprocess.Popen(['nc', '172.22.72.11', '30003'], stdout=subprocess.PIPE)

lastsave = 0

while True:
	if time.time() - lastsave > 3600:
		date_string = time.strftime("%Y-%m-%d-%H-%M-%S")
		output_file = './Data/' + str(date_string) + '.csv'
		f = open(output_file, 'w')
		lastsave = time.time()

	line = p1.stdout.readline()
	f.write(line)