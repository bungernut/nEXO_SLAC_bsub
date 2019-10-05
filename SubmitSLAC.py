import sys
import os
import subprocess
import csv

"""
Useage: 
    Download CVS file that defines jobs.
    Run this script with the first argument the CSV file.
    macros belong in macro folder 
    sims will be put in sims folder

    You can add the following arguments as well:
       submit - required to submit jobs to bsub
       verbose - Prints out stuff to check stuff
"""

os.environ['MCSCRIPTSDIR'] = os.environ['PWD']
mac_location = os.environ['PWD'] + '/macros'
outdir = os.environ['PWD'] + '/sims'


sims = []  # MAC_NAME, jobs, sims, wall_time

if 'verbose' in sys.argv:
    print "Verbose"
    print sys.argv

with open(sys.argv[1], 'r') as csvfile:
    jobreader = csv.reader(csvfile, delimiter=',')
    for row in jobreader:
        print row
        if row[0][0] == '#':
            if 'verbose' in sys.argv:
                print row
            continue
        if row[1] == 'SLAC':
            #            MAC   , #Jobs     , #Events   , WallTime
            sims.append((row[0],int(row[2]),int(row[3]),int(row[4])))


# Print the jobs in CSV file if verbose=True
if 'verbose' in sys.argv:
    print "Here are the sims I read from the CSV file"
    print sims


# Check that all the macros exist
missing_mac = False
for sim in sims:
    if not os.path.isfile(mac_location + sim[0]):
        missing_mac = True
        print "Macro Missing: ", sim[0]
if missing_mac == True:
    print "Missing Macros, quitting"
    sys.exit()


# Check the environment is setup to run nEXO_Offline
if 'NEXOTOP' not in os.environ.keys():
    print "I dont see $NEXOTOP in your environment variables"
    print "Check that you are properly setup"
    sys.exit()


# Here we set the environment variables for the simulations 
# And submit them it the argument `submit` was provided
for sim in sims:
    os.environ['MCNAME'] = sim[0].split('.')[0]
    os.environ['MCMAC'] = mac_location + '/' + sim[0]
    os.environ['MCOUTDIR'] = outdir
    os.environ['MCNUMSIMS'] = str(sim[2])
    for i in range(sim[1]):
        print os.environ['MCNAME'] + ' :: ' + str(i)
        os.environ['MCSEED'] = str(i+1)
        if 'submit' in sys.argv:
            subprocess.call(["bsub", "-R", "centos7",\
                    "-W", str(sim[3]),\
                    "/bin/bash", "./SubmitSLAC.sh"])
