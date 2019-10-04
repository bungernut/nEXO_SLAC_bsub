#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: lintao

#previously called RunSniper.py

import Sniper

def get_parser():
    import argparse
    parser = argparse.ArgumentParser(description='Run nEXO Detector Simulation.')
    parser.add_argument("--evtmax", type=int, default=10, help='events to be processed')
    parser.add_argument("--seed", type=int, default=42, help='seed')
    parser.add_argument("--vis", action="store_true", default=False, help="show vis")
    parser.add_argument("--run", default="run_gamma.in", help="specify run.mac")
    parser.add_argument("--output", default="sample-detsim.root", help="specify output filename")

    return parser

if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    print (args)

    task = Sniper.Task("task")
    # task.asTop()
    task.setEvtMax(args.evtmax)
    #task.setLogLevel(0)

    # = random svc =
    import RandomSvc
    rndm = task.createSvc("RandomSvc")
    rndm.property("Seed").set(args.seed)

    # = rootio =
    import RootIOSvc
    ros = task.createSvc("RootOutputSvc/OutputSvc")
    ros.property("OutputStreams").set({"/Event/Sim": args.output})

    # = BufferMemMgr =
    import BufferMemMgr
    bufMgr = task.createSvc("BufferMemMgr")
    bufMgr.property("TimeWindow").set([0, 0]);

    # = geometry service =
    import Geometry
    simgeomsvc = task.createSvc("SimGeomSvc")

    # = detsim =
    Sniper.loadDll("libnEXOSim.so")
    g4svc = task.createSvc("G4Svc")

    factory = task.createSvc("nEXOSimFactorySvc")

    detsimalg = task.createAlg("DetSimAlg")
    detsimalg.property("DetFactory").set(factory.objName())
    detsimalg.property("RunMac").set(args.run)
    if args.vis:
        detsimalg.property("VisMac").set("vis.mac")

    task.show()
    task.run()

