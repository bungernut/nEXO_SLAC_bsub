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

mac_location = os.environ['PWD'] + '/macros'
outdir = os.environ['PWD'] + '/sims'

sims = []  # MAC_NAME, jobs, sims, wall_time


with open(sys.argv[1]) as csvfile:
    jobreader = csv.reader(csvfile)
    for row in jobreader:
        if row[2] == 'SLAC':
            sims.append((row[0],row[2],row[3],row[4]))


if 'verbose' in sys.argv:
    print "Here are the sims"
    print sims


# TODO check for cards and NEXOTOP?


for sim in sims:
    os.environ['MCNAME'] = sim[2].split('.')[0]
    os.environ['MCMAC'] = mac_location + '/' + sim[2]
    os.environ['MCOUTDIR'] = outdir
    os.environ['MCNUMSIMS'] = str(sim[1])
    for i in range(sim[0]):
        print os.environ['MCNAME'] + ' :: ' + str(i)
        os.environ['MCSEED'] = str(i)
        if 'submit' in sys.argv:
            subprocess.call(["bsub", "-R", "centos7",\
                    "-W", str(sim[3]),\
                    "/bin/bash", "./SubmitSLAC.sh"])
