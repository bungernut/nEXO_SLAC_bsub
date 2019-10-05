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
            sims.append((row[0],int(row[2]),int(row[3]),int(row[4])))


if 'verbose' in sys.argv:
    print "Here are the sims"
    print sims


# TODO check for cards and NEXOTOP?


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
