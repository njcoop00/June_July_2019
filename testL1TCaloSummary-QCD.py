import os
import FWCore.ParameterSet.Config as cms

process = cms.Process("L1TCaloSummaryTest")

#import EventFilter.L1TXRawToDigi.util as util

from FWCore.ParameterSet.VarParsing import VarParsing

options = VarParsing()
options.register('runNumber', 0, VarParsing.multiplicity.singleton, VarParsing.varType.int, 'Run to analyze')
options.register('lumis', '1-max', VarParsing.multiplicity.singleton, VarParsing.varType.string, 'Lumis')
options.register('dataStream', '/ExpressPhysics/Run2015D-Express-v4/FEVT', VarParsing.multiplicity.singleton, VarParsing.varType.string, 'Dataset to look for run in')
options.register('inputFiles', [], VarParsing.multiplicity.list, VarParsing.varType.string, 'Manual file list input, will query DAS if empty')
options.register('inputFileList', '', VarParsing.multiplicity.singleton, VarParsing.varType.string, 'Manual file list input, will query DAS if empty')
options.register('useORCON', False, VarParsing.multiplicity.singleton, VarParsing.varType.bool, 'Use ORCON for conditions.  This is necessary for very recent runs where conditions have not propogated to Frontier')
options.parseArguments()

def formatLumis(lumistring, run) :
    lumis = (lrange.split('-') for lrange in lumistring.split(','))
    runlumis = (['%d:%s' % (run,lumi) for lumi in lrange] for lrange in lumis)
    return ['-'.join(l) for l in runlumis]

print 'Getting files for run %d...' % options.runNumber
#if len(options.inputFiles) is 0 and options.inputFileList is '' :
#    inputFiles = util.getFilesForRun(options.runNumber, options.dataStream)
#elif len(options.inputFileList) > 0 :
#    with open(options.inputFileList) as f :
#        inputFiles = list((line.strip() for line in f))
#else :
#    inputFiles = cms.untracked.vstring(options.inputFiles)
#if len(inputFiles) is 0 :
#    raise Exception('No files found for dataset %s run %d' % (options.dataStream, options.runNumber))
#print 'Ok, time to analyze'


# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.Geometry.GeometryExtended2016Reco_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.RawToDigi_Data_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')

# To get L1 CaloParams
#process.load('L1Trigger.L1TCalorimeter.caloStage2Params_cfi')
# To get CaloTPGTranscoder
#process.load('SimCalorimetry.HcalTrigPrimProducers.hcaltpdigi_cff')
#process.HcalTPGCoderULUT.LUTGenerationMode = cms.bool(False)

process.load('L1Trigger.Configuration.SimL1Emulator_cff')
process.load('L1Trigger.Configuration.CaloTriggerPrimitives_cff')

process.load('EventFilter.L1TXRawToDigi.caloLayer1Stage2Digis_cfi')

process.load('L1Trigger.L1TCaloSummary.uct2016EmulatorDigis_cfi')

process.load("L1Trigger.Run3Ntuplizer.l1TRun3Ntuplizer_cfi")

process.uct2016EmulatorDigis.useECALLUT = cms.bool(False)
process.uct2016EmulatorDigis.useHCALLUT = cms.bool(False)
process.uct2016EmulatorDigis.useHFLUT = cms.bool(False)
process.uct2016EmulatorDigis.useLSB = cms.bool(True)
process.uct2016EmulatorDigis.verbose = cms.bool(False)
process.uct2016EmulatorDigis.ecalToken = cms.InputTag("l1tCaloLayer1Digis")
process.uct2016EmulatorDigis.hcalToken = cms.InputTag("l1tCaloLayer1Digis")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(4000) )

process.source = cms.Source("PoolSource",
                            #fileNames = cms.untracked.vstring(inputFiles)#,
                            #secondaryFileNames = cms.untracked.vstring(secondaryMap[options.inputFiles[0]])
                            fileNames = cms.untracked.vstring(
#'/store/mc/RunIISummer17MiniAOD/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/MINIAODSIM/NZSFlatPU28to62_92X_upgrade2017_realistic_v10-v2/50000/960FACDE-52A2-E711-8DE1-02163E013F24.root'#this one worked for TT
'/store/mc/RunIISpring18MiniAOD/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90000/D61F71C5-4A30-E811-AAED-FA163EFC9F83.root'#this one worked for DY
#'/store/mc/RunIIAutumn18MiniAOD/QCD_Pt-15to7000_TuneCP5_Flat2018_13TeV_pythia8/MINIAODSIM/FlatPU0to70RAW_102X_upgrade2018_realistic_v15-v1/270000/3530CF72-C7DB-A74C-849F-ED7EEAB01927.root'#this one worked for QCD
								),
                            secondaryFileNames = cms.untracked.vstring(
#these worked for TT
#'/store/mc/RunIISummer17DRStdmix/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_92X_upgrade2017_realistic_v10-v2/50007/AA52D88E-B6A1-E711-B660-FA163E5521FB.root', '/store/mc/RunIISummer17DRStdmix/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_92X_upgrade2017_realistic_v10-v2/50007/0E12C3D5-B6A1-E711-A677-FA163E527E0B.root', '/store/mc/RunIISummer17DRStdmix/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_92X_upgrade2017_realistic_v10-v2/50002/540E1FFA-1BA2-E711-8B9B-FA163E5F3042.root', '/store/mc/RunIISummer17DRStdmix/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_92X_upgrade2017_realistic_v10-v2/50007/FEDCCD34-BFA1-E711-93DE-FA163E3ECCF5.root',
#'/store/mc/RunIISummer17DRStdmix/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_92X_upgrade2017_realistic_v10-v2/50002/025D410D-FEA1-E711-A263-FA163EA15274.root', '/store/mc/RunIISummer17DRStdmix/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_92X_upgrade2017_realistic_v10-v2/50002/0A8DF214-FEA1-E711-BF49-FA163EE2B40B.root', '/store/mc/RunIISummer17DRStdmix/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_92X_upgrade2017_realistic_v10-v2/50002/2E52180B-FEA1-E711-80DA-FA163ED37333.root', '/store/mc/RunIISummer17DRStdmix/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_92X_upgrade2017_realistic_v10-v2/50007/CEB03E9D-BAA1-E711-B0A4-FA163E0A2194.root'
#these worked for DY
'/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90000/C83797FA-8C2E-E811-B598-FA163EA48C39.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90000/8297277E-872E-E811-8D00-FA163E2B102D.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90001/4A80DA1E-882E-E811-B448-FA163E039158.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90001/68042186-2E2E-E811-8BB0-FA163EB5EF29.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90002/9E336131-4C2E-E811-8BB2-FA163E57B0C7.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90002/A4EDC403-6A2E-E811-8522-FA163E7EF2D9.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90003/B038CD25-752E-E811-8BB3-FA163E3AC704.root'
#these worked for QCD
#'/store/mc/RunIIAutumn18DR/QCD_Pt-15to7000_TuneCP5_Flat2018_13TeV_pythia8/GEN-SIM-RAW/FlatPU0to70RAW_102X_upgrade2018_realistic_v15-v1/270000/9DC3346D-6D5F-BD46-B2E4-63B01DF63FD3.root',
#
#'/store/mc/RunIIAutumn18DR/QCD_Pt-15to7000_TuneCP5_Flat2018_13TeV_pythia8/GEN-SIM-RAW/FlatPU0to70RAW_102X_upgrade2018_realistic_v15-v1/270000/EC102E80-912B-7F4F-B229-F79D2A0C107B.root',
#
#'/store/mc/RunIIAutumn18DR/QCD_Pt-15to7000_TuneCP5_Flat2018_13TeV_pythia8/GEN-SIM-RAW/FlatPU0to70RAW_102X_upgrade2018_realistic_v15-v1/270000/F8DCD5D3-F848-7D48-83C0-2FEA62AFA973.root',
#
#'/store/mc/RunIIAutumn18DR/QCD_Pt-15to7000_TuneCP5_Flat2018_13TeV_pythia8/GEN-SIM-RAW/FlatPU0to70RAW_102X_upgrade2018_realistic_v15-v1/270001/8501507C-9F5B-2240-9AB6-D4CE391192E3.root',
#
#'/store/mc/RunIIAutumn18DR/QCD_Pt-15to7000_TuneCP5_Flat2018_13TeV_pythia8/GEN-SIM-RAW/FlatPU0to70RAW_102X_upgrade2018_realistic_v15-v1/270001/A749045B-AE90-8545-A1E7-F491FE037515.root',
#'/store/mc/RunIIAutumn18DR/QCD_Pt-15to7000_TuneCP5_Flat2018_13TeV_pythia8/GEN-SIM-RAW/FlatPU0to70RAW_102X_upgrade2018_realistic_v15-v1/270001/C2CA8E1D-D223-FC41-8976-59C3DA4AA223.root'
                                                                   )
)

#process.source.lumisToProcess = cms.untracked.VLuminosityBlockRange("321149:1055","320757:185")

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('step2 nevts:1'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)


process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string("l1TFullEvent.root"),
    outputCommands = cms.untracked.vstring('drop *') #'keep *_*_*_L1TCaloSummaryTest')
    #outputCommands = cms.untracked.vstring('drop *', 'keep *_l1tCaloLayer1Digis_*_*, keep *_*_*_L1TCaloSummaryTest' )
)


#Output
process.TFileService = cms.Service(
	"TFileService",
	fileName = cms.string("l1TNtuple-DY.root")
)

process.p = cms.Path(process.l1tCaloLayer1Digis*process.uct2016EmulatorDigis*process.l1NtupleProducer)

#process.e = cms.EndPath(process.out)

process.schedule = cms.Schedule(process.p)

from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion

#dump_file = open('dump.py','w')
#dump_file.write(process.dumpPython())
