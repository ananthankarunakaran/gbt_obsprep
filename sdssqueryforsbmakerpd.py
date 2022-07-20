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
	query = "select p.objid, p.ra, p.dec, p.u, p.err_u, p.g, p.err_g, p.r, p.err_r, p.i, p.err_i, p.z, p.err_z, s.z as z_best, s.zErr from Galaxy p, specobj s, dbo.fgetNearByObjEq({ra}, {dec}, 240) n where p.objid=s.bestobjid and p.objid=n.objid and s.bestobjid=n.objid and s.z < 0.06".format(ra = RA, dec = DEC)

	print('Querying data for', NAME, ' at position ra = ', RA, ' dec = ', DEC)
	base_url = 'http://skyserver.sdss.org/dr16/SkyServerWS/SearchTools/SqlSearch'
	parameters = {'cmd': query, 'format': 'fits'}
	url_params = urlencode(parameters)
	data_url = '{}?{}'.format(base_url, url_params)
	try:
		data_table = Table.read(data_url, format ='fits')
		data = data_table.to_pandas()
		data_total.append(data)
	except:
		print('No data for', NAME)
		continue
print(len(data_total))

df = pd.concat(data_total)
df['velocity'] = df.z_best*299792.458
print(df.shape[0])
df.to_csv('SDSSobjectsneartargets.csv',index=False)
