# GBT Observation Preparation Files

The two python scripts included thus far aid in creating ON-OFF observing scripts for the Green Bank Telescope.

First running the "sdsssqueryforsbmaker.py" script will run an SQL query of the SDSS DR16 database and retrieve objects in those catalogs with photometric and spectroscopic information. This script requires an input file of the target list with at least the following columns in the header/first row: * ra 
     * dec
     * Name 

The output will be a csv file ('SDSSobjectsneartargets.csv') that will be read into the next script.


The "sb_maker_pd.py" script will take in the target list and the SDSS objects from above. The goal of this script is to allow the user to interactively select relatively sparse regions of the sky near their target of interest. Once these regions are selected, a scheduling blocks are generated following a previously established format.

In addition to the columns above, this second script requires a "obstime" column that indicates the amount of time in minutes (ideally, rounded to the nearest 5 or 10 minutes). Since the scheduling blocks are made following an established format, there is relatively little flexibility (for now) in their generation and edits may need to be made afterwards.
