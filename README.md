# June_July_2019
On lxplus, this directory is located at 
/afs/cern.ch/user/a/addropul/CMSSW_10_6_0_pre4/src/L1Trigger/Run3Ntuplizer/test/June_July_2019

The Run3Ntuplizer was forked from isobelojalvo/Run3Ntuplizer. When I was still learning how to use github this summer, I accidentally cloned Isobel's Run3Nutplizer (jul4 branch) to my lxplus, instead of my own forked version. I did check using "git diff" though, and the only change that I made is that I renamed "EfficiencyTree" to "RegionTree" (in both files /plugins/L1TRegionNtupleProducer.cc and /plugins/Run3Ntuplizer.cc), as there is already another "efficiencyTree" created.

The ntuples that I created, located at /afs/cern.ch/work/a/addropul, contain the variables vRegionEt, vRegionPhi, vRegionEta, vRegionEG, vRegionTau. I think they are filled event-by-event. For the tree named ZeroBias_all.root, these variables are in the EfficiencyTree. For the trees l1TNtuple-DY.root,  l1TNtuple-TT.root, and  l1TNtuple-VBF.root, they are contained in the RegionTree, 1. 

Files labeled testL1TCaloSummary-* are the files which created the ntuples. ntup_validation_2.py is the plotting script. TMVAAnalysis.C is the mva training script; it can be run by the commands commented at the top of the code. 


