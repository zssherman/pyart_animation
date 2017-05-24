"""
Py-ART Animation

Choosing the radar volume from a Nexrad site over a time span.

Based on code by Scott Collis:
https://github.com/scollis/radar_in_the_cloud/blob/master/notebooks/Matthew.ipynb

Jonathan Helmus:
https://anaconda.org/jjhelmus/scipy2015_openaccessradar_jjh/notebook

and memory fixes by Robert Jackson:
https://github.com/rcjackson/pyart_practice/blob/master/nexrad_animatedgif.py

Note: NEXRAD s3 files are set in UTC.

Note: Rendering gifs does take some time. For example, KLOT examples takes
about 3 minutes.

"""

from boto.s3.connection import S3Connection
import pyart
import gzip
from matplotlib import pyplot as plt
from datetime import date, datetime, timedelta
from matplotlib import animation
import tempfile
import numpy as np
import pandas as pd


# Function for pulling all keys between two dates at a chosen nexrad site.
def nexrad_site_datespan(start_date=None, start_date_time=None,
                         end_date=None, end_date_time=None, site=None):

    """
    Get all volumes of NEXRAD data between two particular datetimes.

    Parameters
    ----------
    start_date : string
        Eight number date, for example '20150623'
    start_date_time : string
        Six number time, for example '145501'
    end_date : string
        Eight number date or 'Now' to retrieve current UTC
    end_date_time : string, optional if end_date = 'Now'
        Six number time
    site : string
        Four letter radar designation in, for example 'KJAX'

    Reference
    ---------
    Helmus, J.J. & Collis, S.M., (2016). The Python ARM Radar Toolkit
    (Py-ART), a Library for Working with Weather Radar Data in the
    Python Programming Language. Journal of Open Research Software.
    4(1), p.e25. DOI: http://doi.org/10.5334/jors.119

    """

    fmt = '%Y%m%d_%H%M%S'

    # Allows for the choice of now for the end date so current UTC is pulled.

    if end_date.upper() == 'NOW':
        e_d_selected = datetime.utcnow()
    else:
        e_d_selected = datetime.strptime(end_date + '_' + end_date_time, fmt)

    s_d = datetime.strptime(start_date + '_' + start_date_time, fmt)
    e_d_fixed = e_d_selected + timedelta(days=1)

    if s_d > e_d_selected:
            raise ValueError('You provided a start date' 
                             ' that comes after the end date.')

    times = []
    for timestamp in datespan((s_d), (e_d_fixed), delta=timedelta(days=1)):
        time = timestamp
        times += [datetime.strftime(time, '%Y/%m/%d/' + site.upper())]

    conn = S3Connection(anon=True)
    bucket = conn.get_bucket('noaa-nexrad-level2')

    # Get a list of files
    keys = []
    datetimes = []
    for time in times:
        bucket_list = list(bucket.list(time))
        for i in range(len(bucket_list)):
            this_str = str(bucket_list[i].key)
            if 'gz' in this_str:
                endme = this_str[-22:-3]
                fmt = '%Y%m%d_%H%M%S_V06'
                dt = datetime.strptime(endme, fmt)
                datetimes.append(dt)
                keys.append(bucket_list[i])

            if this_str[-3::] == 'V06':
                endme = this_str[-19::]
                fmt = '%Y%m%d_%H%M%S_V06'
                dt = datetime.strptime(endme, fmt)
                datetimes.append(dt)
                keys.append(bucket_list[i])

    # Code belows chooses all keys between the user's dates.
    d = {'keys': keys}
    key_object = pd.DataFrame(data=d, index=pd.to_datetime(datetimes))
    selected_keys = key_object.loc[s_d: e_d_selected, :]
    # radar_datetimes = selected_keys.index.tolist()
    data_keys = selected_keys['keys'].tolist()
    return data_keys


# Conversion of keys to pyart radar objects.
def radar_keys_to_data(keys):
    """ Stores keys into temporary localfile to be read with pyart. """
    localfile = tempfile.NamedTemporaryFile()
    keys.get_contents_to_filename(localfile.name)
    # Only pulling two scans for the sake of time and memory.
    radar = pyart.io.read_nexrad_archive(localfile.name, scans=[0, 1])
    return radar


def datespan(start_date, end_date, delta=timedelta(days=1)):
    """ Retrieves all dates between the start and end date. """
    current_date = start_date
    while current_date < end_date:
        yield current_date
        current_date += delta


# Pull all data keys from NEXRAD between user define start and end datetimes.
my_data_keys_klot = nexrad_site_datespan(start_date='20161019',
                                         start_date_time='125000',
                                         end_date='20161019',
                                         end_date_time='165000',
                                         site='klot')


# Creating a gif of all volumes between user chosen dates.
def animate(nframe):
    plt.clf()
    radar = radar_keys_to_data(my_data_keys_klot[nframe])
    display = pyart.graph.RadarMapDisplay(radar)
    # Delete radar after use to save memory.
    del radar
    display.plot_ppi_map('reflectivity', sweep=0, resolution='l',
                         vmin=-8, vmax=64, mask_outside=False,
                         cmap=pyart.graph.cm.NWSRef,
                         lat_lines=None, lon_lines=None)
    display.basemap.drawcounties()
fig = plt.figure(figsize=(10, 8))
anim_klot = animation.FuncAnimation(fig, animate,
                                    frames=len(my_data_keys_klot))
anim_klot.save('reflectivity_animation.gif',
               writer='imagemagick', fps=5)
plt.close()
