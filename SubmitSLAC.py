import sys
import os
import subprocess

mac_location = os.environ['PWD'] + '/AlphaN_Neutrons'
outdir = mac_location + '/SIMS'
sims = []   # num jobs, #events/job,  MAC Name
sims.append((       3,          10, 'Vessel_HFEPo210_NB.mac'))
sims.append((       3,          10, 'SiPM_Si.mac'))
sims.append((       3,          10, 'SiPM_SiO2.mac'))


# TODO check for cards and NEXOTOP?

for sim in sims:
    os.environ['MCNAME'] = sim[2].split('.')[0]
    os.environ['MCMAC'] = mac_location + '/' + sim[2]
    os.environ['MCOUTDIR'] = outdir
    os.environ['MCNUMSIMS'] = str(sim[1])
    for i in range(sim[0]):
        print os.environ['MCNAME'] + ' :: ' + str(i)
        os.environ['MCSEED'] = str(i)
        subprocess.call(["bsub", "-R", "centos7", "-W", "200", "/bin/bash", "./SubmitSLAC.sh"])
