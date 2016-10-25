Py-ART Animation
================

Downloading NEXRAD files from `Amazon Web Services <https://aws.amazon.com/noaa-big-data/nexrad/>`_ between a datetime span from a chosen NEXRAD site. The user is allowed to chose a start and end date and receive all volumes of data betweenboth dates. Py-ART[1] is then used to plot each volume of data and a gif animation is created displaying the maps created. 

Source Codes
------------

The Python ARM Radar Toolkit, `Py-ART <http://arm-doe.github.io/pyart/>`_, is a Python module containing a collection of weather radar algorithms and utilities. Py-ART is used by the Atmospheric Radiation Measurement (ARM) Climate Research Facility for working with data from a number of its precipitation and cloud radars, but has been designed so that it can be used by others in the radar and atmospheric communities to examine, processes, and analyze data from many types of weather radars.

Helmus, J.J. & Collis, S.M., (2016). The Python ARM Radar Toolkit (Py-ART), a Library for Working with Weather Radar Data in the Python Programming Language. Journal of Open Research Software. 4(1), p.e25. DOI: http://doi.org/10.5334/jors.119

S3 Download code by Scott Collis: https://github.com/scollis/radar_in_the_cloud/blob/master/notebooks/any_nexrad.ipynb

Animation Code by Jonathan Helmus: `https://github.com/jjhelmus/presentations/blob/master/2015_SciPy_PyART_talk <https://github.com/jjhelmus/presentations/blob/master/2015_SciPy_PyART_talk/SciPy2015_OpenAccessRadar_jjh.ipynb>`_
Memory Fix Code by Robert Jackson: https://github.com/rcjackson/pyart_practice/blob/master/nexrad_animatedgif.py
