from __future__ import print_function, division
import numpy as np
import pandas as pd
import datetime

NAN = object()

def add_dal_fields(in_path, out_path):
    ra = np.load(in_path)['x']
    names = ra.dtype.names
    columns = {nm : ra[nm] for nm in names}
    df = pd.DataFrame(columns)
    dates = []
    dates = [(NAN if np.isnan(x) else datetime.datetime.utcfromtimestamp(x).strftime("%Y-%m-%d %H:%M:%S"))
                     for x in df['timestamp']]
    df['date'] = dates
    df['SOG'] = df.speed
    df['LONGITUDE'] = df.lon
    df['LATITUDE'] = df.lat
    df['MMSI'] = df.mmsi
    # We aren't using the distshore in either model so set to large value for comparision
    df['distshore'] = 10000
    mask = np.array([(x is not NAN) for x in dates])
    df = df[mask]
    times = [datetime.datetime.utcfromtimestamp(x).strftime("%Y%m%d_%H%M%OS")
                     for x in df['timestamp']]
    df["TIME"] = times
    #
    df.to_csv(out_path)


for in_path, out_path in [("trawl", "trawler"),
                          ("ps", "purse_seine"),
                          ("longliner", "longliner")]:
    print(in_path)
    add_dal_fields("datasets/kristina_{}.measures.npz".format(in_path),
                   "datasets/kristina_{}.measures.from_npz.csv".format(out_path))
