import sys
import os
import subprocess
import csv

helpstr = """
Useage: 
    Download CVS file that defines jobs.
    Run this script with the first argument the CSV file.
    macros belong in macro folder 
    sims will be put in sims folder

    You can add the following arguments as well:
       submit - required to submit jobs to bsub
       verbose - Prints out stuff to check stuff
       check  - Check the sims dir for missing jobs and quit
       fix  - With "check" will submit missing jobs to bsub and quit
"""

os.environ['MCSCRIPTSDIR'] = os.environ['PWD']
mac_location = os.environ['PWD'] + '/macros'
outdir = os.environ['PWD'] + '/sims'


if 'help' in sys.argv or '-h' in sys.argv or '--help' in sys.argv:
    print helpstr
    sys.exit()

verbose = False
if 'verbose' in sys.argv:
    verbose = True
    print "Verbose"
    print sys.argv


# Open CSV file that describes the JOBS
sims = []
try:
    with open(sys.argv[1], 'r') as csvfile:
        jobreader = csv.reader(csvfile, delimiter=',')
        for row in jobreader:
            if row[0][0] == '#':
                if verbose: print row
                continue
            if row[1] == 'SLAC':
                #            MAC   , #Jobs     , #Events   , WallTime
                sims.append((row[0],int(row[2]),int(row[3]),int(row[4])))
except:
    print "Failed to load CSV with job descriptions"
    print helpstr
    sys.exit()


# Print the jobs in CSV file if verbose=True
if verbose:
    print "Here are the sims I read from the CSV file"
    print sims


# Check that all the macros exist
missing_mac = False
for sim in sims:
    if not os.path.isfile(mac_location + '/' + sim[0]):
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


# This checks the ./sims folder for missing files
# Right now since I don't understand the whole chain this only check for the G4
if 'check' in sys.argv:
    sims_missing = []
    for sim in sims:
        for i in range(sim[1]):
            filename = sim[0].split('.')[0] + '_' + str(i+1) + '.root'
            if not os.path.isfile(outdir + '/' + filename):
                sims_missing.append((sim[0], sim[1], sim[2], sim[3], i+1))
    if len(sims_missing)>0:
        print "Missing Sims"
        for i in sims_missing: 
            print i
            if 'fix' in sys.argv: 
                os.environ['MCNAME'] = i[0].split('.')[0]
                os.environ['MCMAC'] = mac_location + '/' + i[0]
                os.environ['MCOUTDIR'] = outdir
                os.environ['MCNUMSIMS'] = str(i[2])
                os.environ['MCSEED'] = str(i[4])
                subprocess.call(["bsub", "-R", "centos7",\
                        "-W", str(i[3]),\
                        "/bin/bash", "./SubmitSLAC.sh"])
    sys.exit()



# Here we set the environment variables for the simulations 
# And submit them if the argument `submit` was provided
for sim in sims:
    os.environ['MCNAME'] = sim[0].split('.')[0]
    os.environ['MCMAC'] = mac_location + '/' + sim[0]
    os.environ['MCOUTDIR'] = outdir
    os.environ['MCNUMSIMS'] = str(sim[2])
    for i in range(sim[1]):
        if verbose: print os.environ['MCNAME'] + ' :: ' + str(i)
        os.environ['MCSEED'] = str(i+1)
        if 'submit' in sys.argv:
            subprocess.call(["bsub", "-R", "centos7",\
                    "-W", str(sim[3]),\
                    "/bin/bash", "./SubmitSLAC.sh"])
