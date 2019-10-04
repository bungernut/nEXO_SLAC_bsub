#!/bin/bash

echo "(>**)> Environment Vars:"
printenv

# Quit if this is not a batch job at SLAC
if [ -z ${LSB_JOBID} ]; then
    echo "This is not a batch job"
    exit 999
fi
# Check the JOB has the proper information
if [ -z ${MCMAC} -o -z ${MCOUTDIR} -o -z ${MCSEED} -o -z ${MCNAME} ]; then
    echo "JOB missing important parameter: MCMAC, MCOUTDIR, MCNAME, or MCSEED"
fi
if [ -z ${MCNUMSIMS} ]; then
    echo "Job missing important parameter: MCNUMSIMS"
fi

# Check if output directory exists
if [ ! -d ${MCOUTDIR} -a ! -w ${MCOUTDIR} ]; then
    echo ${MCOUTDIR} "d.n.e or is not writeable"
    exit 999
fi

# Setup a scratch directory on node
scratch_dir=/scratch/${USER}/${LSB_JOBID}
echo "(>**)> Make scratch" $scratch_dir
mkdir -p  $scratch_dir
export HOME=$scratch_dir
cd ${HOME}

# Runs the stuff
echo "(>**)> Running"
cp /nfs/slac/g/exo/bmong/nEXO_MC/RunDetSim.py ${HOME}
cp -r /nfs/slac/g/exo/bmong/nEXO_MC/yamls ${HOME}

python ./RunDetSim.py \
    --run ${MCMAC} \
    --output ${MCNAME}_${MCSEED}.root \
    --seed ${MCSEED} \
    --evtmax ${MCNUMSIMS}

# COPY files to MCOUTDIR
echo "(>**)> Copying Files"
cp -v $scratch_dir/*.root ${MCOUTDIR}/ #move stuff from scratch to where data should be after the job is done. 

# CLEAN up scratch_dir
echo "(>**)> Cleaning Up scratch"
rm -vrf $scratch_dir/ 

echo "t(**t) Done"
