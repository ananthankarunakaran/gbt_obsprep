import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


sdss = pd.read_csv('SDSSobjectsnearudgs.csv')

#targets = np.loadtxt('sample_mag19mu235re_nozero_noEVCC_noA100-selected.csv',delimiter=',',dtype=str,skiprows=0)
targets = pd.read_csv('test_for_sbmakerpd.csv')
dirpath_local = '/home/ananthan/Documents/Research/SMUDGes-Stripe82/21Afiller/sbfiles/'
dirpath_gbt = '/users/akarunak/projs/smudges/21a'
def onclick(event):
	global ix, iy
	ix, iy = event.xdata, event.ydata
	print('ra=%.2f, dec=%.2f' %(ix, iy))
	global temp_coords
	temp_coords.append((ix,iy))
	coords = np.array(temp_coords)
	ax.scatter(coords[:,0],coords[:,1],marker='s',s=250,c='r')
	for c in range(len(coords)-1,len(coords)):
		temp_circ = plt.Circle((coords[c,0],coords[c,1]),0.3,color='blue',ls='--',lw=2,fill=False)
		ax.add_artist(temp_circ)
	fig.canvas.draw()
	if len(temp_coords) == number_of_blocks-1:
		fig.canvas.mpl_disconnect(cid)
		plt.close(fig)
	return temp_coords
	
target_name = targets.Name.to_numpy()
target_ra = targets.ra.to_numpy()
target_dec = targets.dec.to_numpy()
target_obstime = targets.obstime.to_numpy()

for x in range(2):
	temp_sdss = sdss[((sdss.ra <target_ra[x]+4) & (sdss.ra > target_ra[x]-4)\
	 & (sdss.dec <target_dec[x]+4) & (sdss.ra >target_ra[x]-4))]

	print(len(temp_sdss))
	temp_coords = []
	number_of_blocks = int(np.ceil(1+target_obstime[x]/10))
	print("Number of blocks needed=",number_of_blocks)
	



	fig = plt.figure(figsize=(12,10))
	ax = fig.add_subplot(111)
	sdssplot = ax.scatter(temp_sdss.ra,temp_sdss.dec,c=temp_sdss.velocity,cmap='viridis_r',marker='o',ec='black',s=200,zorder=-1)
	ax.scatter(target_ra[x],target_dec[x],marker='*',fc='none',edgecolor='k',s=300)
	circ = plt.Circle((target_ra[x],target_dec[x]),0.3,color='blue',ls='--',lw=3,fill=False)
	ax.add_artist(circ)
	ax.set_xlim([target_ra[x] -4.1,target_ra[x]+4.1])
	ax.set_ylim([target_dec[x] -4.1,target_dec[x]+4.1])
	ax.invert_xaxis()
	ax.set_title('Integration Time =%.0f Number of coords needed=%.0f' % (target_obstime[x], number_of_blocks-1),fontsize=24)
	cbar = fig.colorbar(sdssplot,orientation='vertical',ax=ax)
	cbar.ax.tick_params(labelsize=20)
	cid =fig.canvas.mpl_connect('button_press_event',onclick)
	plt.show()

	temp_coords = np.array(temp_coords)
	temp_delta = np.array([(temp_coords[j,0]-target_ra[x],temp_coords[j,1]-target_dec[x]) for j in range(len(temp_coords))])
	print('Here are the delta values',temp_delta)

	fig = plt.figure(figsize=(12,10))
	ax = fig.add_subplot(111)
	sdssplot = ax.scatter(temp_sdss.ra,temp_sdss.dec,c=temp_sdss.velocity,cmap='viridis_r',marker='o',ec='black',s=200,zorder=-1)
	ax.scatter(target_ra[x],target_dec[x],marker='*',fc='none',edgecolor='k',s=300)
	ax.scatter(temp_coords[:,0],temp_coords[:,1],marker='s',fc='none',edgecolor='r',s=250,lw=2)
	for n in range(len(temp_coords)):
		ax.text(temp_coords[n,0],temp_coords[n,1]+0.18,'Delta=%.2f,%.2f' %(temp_delta[n,0],temp_delta[n,1]))
	ax.set_title('Integration Time =%.0f Number of coords needed=%.0f' % (target_obstime[x], number_of_blocks-1),fontsize=24)
	ax.set_xlim([target_ra[x] -4.1,target_ra[x]+4.1])
	ax.set_ylim([target_dec[x] -4.1,target_dec[x]+4.1])
	ax.invert_xaxis()
	cbar = fig.colorbar(sdssplot,orientation='vertical',ax=ax)
	cbar.ax.tick_params(labelsize=20)

	plt.show()

	
	
	print('Creating SB file(s) for:',target_name[x])

	if number_of_blocks < 10:
		with open(dirpath_local+str(target_name[x])+"/onoff_"+str(target_name[x]),"a") as qc:
			openinglines = f'Catalog("{dirpath_gbt}/pointed.cat")\n\nexecfile("{dirpath_gbt}/vegas.conf")\nConfigure(conf)\n\nSlew("'+target_name[x]+'")'+"\nBalance()\nBalance('VEGAS',{'target_level':-20})\n\n"
			qc.write(openinglines)
			block1 ='OnOff("%s",Offset("J2000",%.2f,%.2f,cosv=False),60,"1")\n' % (target_name[x], temp_delta[0,0],temp_delta[0,1])
			qc.write(block1)
			block2 ='OnOff("%s",Offset("J2000",%.2f,%.2f,cosv=False),240,"1")\n' % (target_name[x], temp_delta[0,0],temp_delta[0,1])
			qc.write(block2)
		
			
			#if (number_of_blocks) == 2:
			#	block3 ='OnOff("%s",Offset("J2000",%.2f,%.2f,cosv=False),300,"1")\n' % (target_name[x], temp_delta[0,0],temp_delta[0,1])
			#	qc.write(block3)
			if (number_of_blocks) == 3:
				if targets[x,54].astype(float) == 15.:
					for k in range(number_of_blocks-2):
						temp_blocks ='OnOff("%s",Offset("J2000",%.2f,%.2f,cosv=False),150,"1")\n' % (target_name[x], temp_delta[k+1,0],temp_delta[k+1,1])
						qc.write(temp_blocks)
				else:	
					for k in range(number_of_blocks-2):
						temp_blocks ='OnOff("%s",Offset("J2000",%.2f,%.2f,cosv=False),300,"1")\n' % (target_name[x], temp_delta[k+1,0],temp_delta[k+1,1])
						qc.write(temp_blocks)
			elif (number_of_blocks) == 4:
				for k in range(number_of_blocks-2):
					temp_blocks ='OnOff("%s",Offset("J2000",%.2f,%.2f,cosv=False),300,"1")\n' % (target_name[x], temp_delta[k+1,0],temp_delta[k+1,1])
					qc.write(temp_blocks)
					if k ==1:
						qc.write("\nBalance('VEGAS',{'target_level':-20})\n\n")
			elif (number_of_blocks) == 6:
				for k in range(number_of_blocks-2):
					if k < number_of_blocks-3:				
						temp_blocks ='OnOff("%s",Offset("J2000",%.2f,%.2f,cosv=False),300,"1")\n' % (target_name[x], temp_delta[k+1,0],temp_delta[k+1,1])
						qc.write(temp_blocks)
					elif k == number_of_blocks -3:
						temp_blocks ='OnOff("%s",Offset("J2000",%.2f,%.2f,cosv=False),150,"1")\n' % (target_name[x],temp_delta[k+1,0],temp_delta[k+1,1])
						qc.write(temp_blocks)
					if k ==1:
						qc.write("\nBalance('VEGAS',{'target_level':-20})\n\n")

			elif (number_of_blocks) == 7:
				for k in range(number_of_blocks-2):
					temp_blocks ='OnOff("%s",Offset("J2000",%.2f,%.2f,cosv=False),300,"1")\n' % (target_name[x], temp_delta[k+1,0],temp_delta[k+1,1])
					qc.write(temp_blocks)
					if k ==1 or k==4:
						qc.write("\nBalance('VEGAS',{'target_level':-20})\n\n")
			elif (number_of_blocks) == 9:
				for k in range(number_of_blocks-2):
					temp_blocks ='OnOff("%s",Offset("J2000",%.2f,%.2f,cosv=False),300,"1")\n' % (target_name[x], temp_delta[k+1,0],temp_delta[k+1,1])
					qc.write(temp_blocks)
					if k ==1 or k==4:
						qc.write("\nBalance('VEGAS',{'target_level':-20})\n\n")

	else:
							
			if (number_of_blocks) == 11:
				with open(dirpath_local+str(target_name[x])+"/onoff_"+str(target_name[x])+"A","a") as qc1:
					openinglines = f'Catalog("{dirpath_gbt}/pointed.cat")\n\nexecfile("{dirpath_gbt}/vegas.conf")\nConfigure(conf)\n\nSlew("'+target_name[x]+'")'+"\nBalance()\nBalance('VEGAS',{'target_level':-20})\n\n"
					qc1.write(openinglines)
					block1 ='OnOff("%s",Offset("J2000",%.2f,%.2f,cosv=False),60,"1")\n' % (target_name[x], temp_delta[0,0],temp_delta[0,1])
					qc1.write(block1)
					block2 ='OnOff("%s",Offset("J2000",%.2f,%.2f,cosv=False),240,"1")\n' % (target_name[x], temp_delta[0,0],temp_delta[0,1])
					qc1.write(block2)
					for k in range(5):
						temp_blocks ='OnOff("%s",Offset("J2000",%.2f,%.2f,cosv=False),300,"1")\n' % (target_name[x], temp_delta[k+1,0],temp_delta[k+1,1])
						qc1.write(temp_blocks)
						if k ==1:
							qc1.write("\nBalance('VEGAS',{'target_level':-20})\n\n")

				with open(dirpath_local+str(target_name[x])+"/onoff_"+str(target_name[x])+"B","a") as qc2:
					openinglines = f'Catalog("{dirpath_gbt}/pointed.cat")\n\nexecfile("{dirpath_gbt}/vegas.conf")\nConfigure(conf)\n\nSlew("'+target_name[x]+'")'+"\nBalance()\nBalance('VEGAS',{'target_level':-20})\n\n"

					qc2.write(openinglines)
					block1 ='OnOff("%s",Offset("J2000",%.2f,%.2f,cosv=False),60,"1")\n' % (target_name[x], temp_delta[6,0],temp_delta[6,1])
					qc2.write(block1)
					block2 ='OnOff("%s",Offset("J2000",%.2f,%.2f,cosv=False),240,"1")\n' % (target_name[x], temp_delta[6,0],temp_delta[6,1])
					qc2.write(block2)
					for k in range(6,9):
						temp_blocks ='OnOff("%s",Offset("J2000",%.2f,%.2f,cosv=False),300,"1")\n' % (target_name[x], temp_delta[k+1,0],temp_delta[k+1,1])
						qc2.write(temp_blocks)
						if k ==7:
							qc2.write("\nBalance('VEGAS',{'target_level':-20})\n\n")

			elif (number_of_blocks) == 13 or (number_of_blocks) == 16:
				with open(dirpath_local+str(target_name[x])+"/onoff_"+str(target_name[x])+"A","a") as qc1:
					openinglines = f'Catalog("{dirpath_gbt}/pointed.cat")\n\nexecfile("{dirpath_gbt}/vegas.conf")\nConfigure(conf)\n\nSlew("'+target_name[x]+'")'+"\nBalance()\nBalance('VEGAS',{'target_level':-20})\n\n"
					qc1.write(openinglines)
					block1 ='OnOff("%s",Offset("J2000",%.2f,%.2f,cosv=False),60,"1")\n' % (target_name[x], temp_delta[0,0],temp_delta[0,1])
					qc1.write(block1)
					block2 ='OnOff("%s",Offset("J2000",%.2f,%.2f,cosv=False),240,"1")\n' % (target_name[x], temp_delta[0,0],temp_delta[0,1])
					qc1.write(block2)
					for k in range(5):
						temp_blocks ='OnOff("%s",Offset("J2000",%.2f,%.2f,cosv=False),300,"1")\n' % (target_name[x], temp_delta[k+1,0],temp_delta[k+1,1])
						qc1.write(temp_blocks)
						if k ==1:
							qc1.write("\nBalance('VEGAS',{'target_level':-20})\n\n")

				with open(dirpath_local+str(target_name[x])+"/onoff_"+str(target_name[x])+"B","a") as qc2:
					openinglines = f'Catalog("{dirpath_gbt}/pointed.cat")\n\nexecfile("{dirpath_gbt}/vegas.conf")\nConfigure(conf)\n\nSlew("'+target_name[x]+'")'+"\nBalance()\nBalance('VEGAS',{'target_level':-20})\n\n"
					qc2.write(openinglines)
					block1 ='OnOff("%s",Offset("J2000",%.2f,%.2f,cosv=False),60,"1")\n' % (target_name[x], temp_delta[6,0],temp_delta[6,1])
					qc2.write(block1)
					block2 ='OnOff("%s",Offset("J2000",%.2f,%.2f,cosv=False),240,"1")\n' % (target_name[x], temp_delta[6,0],temp_delta[6,1])
					qc2.write(block2)
					for k in range(6,11):
						temp_blocks ='OnOff("%s",Offset("J2000",%.2f,%.2f,cosv=False),300,"1")\n' % (target_name[x], temp_delta[k+1,0],temp_delta[k+1,1])
						qc2.write(temp_blocks)
						if k ==7:
							qc2.write("\nBalance('VEGAS',{'target_level':-20})\n\n")
							
	print('SB file(s) created for:',target_name[x])
	print('SB file(s) saved here:  '+dirpath_local+str(target_name[x]))

