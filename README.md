# nEXO_SLAC_bsub
Manager for MC jobs at SLAC

## Useage
1) Checkout this repo where you want the sims to go (somewhere with space, etc)
2) Make sure ./sims directory exists in this directory, that is where sims will go
3) Download the JOB definitions sheet https://docs.google.com/spreadsheets/d/1_vZRHD24bRcF0OgAs-3pSoa7qDtm96nFlU6Rf0e80Dk/edit?usp=sharing
4) Put the macros in ./macros
5) Run this script `python SubmitSLAC.py nEXO_SIMS_AlphaN.csv submit`

## Help

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

