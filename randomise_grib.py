
import sys
import os

import gribapi
import numpy


def randomise_grib(filename):
	"""Randomise the data in the given GRIB file."""
	in_file = open(filename, "rb")
	out_file = open("out.grib", "wb")
	
	while True:
		grib_message = gribapi.grib_new_from_file(in_file)
		if not grib_message:
			break
			
		values = gribapi.grib_get_double_array(grib_message, "values")
		values = numpy.random.rand(len(values))
		gribapi.grib_set_double_array(grib_message, "values", values)
		gribapi.grib_write(grib_message, out_file)
		
	os.remove(filename)
	os.rename("out.grib", filename)
	

if __name__ == "__main__":
	for arg in sys.argv[1:]:
		randomise_grib(arg)
