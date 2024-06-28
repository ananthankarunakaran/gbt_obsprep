from astroquery.sdss import SDSS
from astropy import units as u
from astropy import coordinates as coords
from astropy.table import Table
from urllib.parse import urlencode
import pandas as pd
import numpy as np


targets = pd.read_csv('test_for_sbmakerpd.csv')



data_total = []

for RA,DEC,NAME in zip(targets.ra.to_numpy(),targets.dec.to_numpy(),targets.Name.to_numpy()):
data_url = f'https://skyserver.sdss.org/dr16/SkyServerWS/SearchTools/SqlSearch?cmd=select+p.objid%2C+p.ra%2C+p.dec%2C+p.u%2C+p.err_u%2C+p.g%2C+p.err_g%2C+p.r%2C+p.err_r%2C+p.i%2C+p.err_i%2C+p.z%2C+p.err_z%2C+s.z+as+z_best%2C+s.zErr+from+Galaxy+p%2C+specobj+s%2C+dbo.fgetNearByObjEq%28{RA}%2C+{DEC}%2C+240%29+n+where+p.objid%3Ds.bestobjid+and+p.objid%3Dn.objid+and+s.bestobjid%3Dn.objid+and+s.z+%3C+0.06&format=csv'
	print(str(data_url))
	try:
		data = pd.read_csv(str(data_url),comment='#')
		data_total.append(data)
	except:
		print('No data for', NAME)
		continue
print(len(data_total))

df = pd.concat(data_total)
df['velocity'] = df.z_best*299792.458
print(df.shape[0])
df.to_csv('SDSSobjectsneartargets.csv',index=False)
