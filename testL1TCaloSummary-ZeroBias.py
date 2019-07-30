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
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data', '')

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

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100000) )

process.source = cms.Source("PoolSource",
                            #fileNames = cms.untracked.vstring(inputFiles)#,
                            #secondaryFileNames = cms.untracked.vstring(secondaryMap[options.inputFiles[0]])
                            fileNames = cms.untracked.vstring(
'/store/mc/RunIIAutumn18MiniAOD/QCD_Pt-15to7000_TuneCP5_Flat2018_13TeV_pythia8/MINIAODSIM/FlatPU0to70RAW_102X_upgrade2018_realistic_v15-v1/270000/3530CF72-C7DB-A74C-849F-ED7EEAB01927.root',
'/store/mc/RunIIAutumn18MiniAOD/QCD_Pt-15to7000_TuneCP5_Flat2018_13TeV_pythia8/MINIAODSIM/FlatPU0to70RAW_102X_upgrade2018_realistic_v15-v1/270000/15EE58A5-17E3-6340-9645-3A1CF05F6BB6.root',
'/store/mc/RunIIAutumn18MiniAOD/QCD_Pt-15to7000_TuneCP5_Flat2018_13TeV_pythia8/MINIAODSIM/FlatPU0to70RAW_HEMResub_102X_upgrade2018_realistic_v15-v1/40000/5C40E69D-7012-1F4F-B126-44DDE8C7B2F4.root'
#'/store/mc/RunIIAutumn18DR/QCD_Pt-15to7000_TuneCP5_Flat2018_13TeV_pythia8/AODSIM/FlatPU0to70RAW_102X_upgrade2018_realistic_v15-v1/270000/1355A713-923D-CC47-B41C-F10AB12A1038.root',
#'/store/mc/RunIIAutumn18HEMReReco/QCD_Pt-15to7000_TuneCP5_Flat2018_13TeV_pythia8/AODSIM/FlatPU0to70RAW_HEMResub_102X_upgrade2018_realistic_HEfail_v3-v1/40000/81D5C8A2-A22C-9F48-A164-9D42DF34CD9A.root'

#'/store/mc/PhaseIIMTDTDRAutumn18MiniAOD/DYToLL_M-50_14TeV_TuneCP5_pythia8/MINIAODSIM/NoPU_103X_upgrade2023_realistic_v2-v2/90000/E426D998-52F4-9B42-97BA-A0199F677808.root'
#DY one that works '/store/mc/PhaseIIMTDTDRAutumn18MiniAOD/DYToLL_M-50_14TeV_TuneCP5_pythia8/MINIAODSIM/NoPU_103X_upgrade2023_realistic_v2-v2/90000/F063E7F2-A71C-E14C-BF02-665560C6B3CC.root'
#'/store/data/Run2018E/ZeroBias/MINIAOD/PromptReco-v1/000/325/684/00000/7A23D558-A9D3-A546-95FA-12B56317C0A0.root',
#                                                              '/store/data/Run2018E/ZeroBias/MINIAOD/PromptReco-v1/000/325/484/00000/C08A230D-9ADC-F14E-AF94-3048FA9BA9F0.root',
#                                                              '/store/data/Run2018E/ZeroBias/MINIAOD/PromptReco-v1/000/325/449/00000/357A6203-9FE7-2F49-A7D3-04033E1F3DEC.root',
#                                                              '/store/data/Run2018E/ZeroBias/MINIAOD/PromptReco-v1/000/325/458/00000/E492B615-2F02-944E-A4D2-695290837592.root',
#                                                              '/store/data/Run2018E/ZeroBias/MINIAOD/PromptReco-v1/000/325/430/00000/76B231DA-491C-E244-B3C6-C89FEE3AD921.root',
#                                                              '/store/data/Run2018E/ZeroBias/MINIAOD/PromptReco-v1/000/325/283/00000/4A15B34D-ED00-784B-8AE9-CF03D646BF92.root'
                                                          ),
                            secondaryFileNames = cms.untracked.vstring(
'/store/mc/RunIIAutumn18DR/QCD_Pt-15to7000_TuneCP5_Flat2018_13TeV_pythia8/GEN-SIM-RAW/FlatPU0to70RAW_102X_upgrade2018_realistic_v15-v1/270000/9DC3346D-6D5F-BD46-B2E4-63B01DF63FD3.root',
'/store/mc/RunIIAutumn18DR/QCD_Pt-15to7000_TuneCP5_Flat2018_13TeV_pythia8/GEN-SIM-RAW/FlatPU0to70RAW_102X_upgrade2018_realistic_v15-v1/270000/EC102E80-912B-7F4F-B229-F79D2A0C107B.root',
'/store/mc/RunIIAutumn18DR/QCD_Pt-15to7000_TuneCP5_Flat2018_13TeV_pythia8/GEN-SIM-RAW/FlatPU0to70RAW_102X_upgrade2018_realistic_v15-v1/270000/F8DCD5D3-F848-7D48-83C0-2FEA62AFA973.root',
'/store/mc/RunIIAutumn18DR/QCD_Pt-15to7000_TuneCP5_Flat2018_13TeV_pythia8/GEN-SIM-RAW/FlatPU0to70RAW_102X_upgrade2018_realistic_v15-v1/270001/8501507C-9F5B-2240-9AB6-D4CE391192E3.root',
'/store/mc/RunIIAutumn18DR/QCD_Pt-15to7000_TuneCP5_Flat2018_13TeV_pythia8/GEN-SIM-RAW/FlatPU0to70RAW_102X_upgrade2018_realistic_v15-v1/270001/A749045B-AE90-8545-A1E7-F491FE037515.root',
'/store/mc/RunIIAutumn18DR/QCD_Pt-15to7000_TuneCP5_Flat2018_13TeV_pythia8/GEN-SIM-RAW/FlatPU0to70RAW_102X_upgrade2018_realistic_v15-v1/270001/C2CA8E1D-D223-FC41-8976-59C3DA4AA223.root'
#'/store/mc/PhaseIIMTDTDRAutumn18DR/DYToLL_M-50_14TeV_TuneCP5_pythia8/FEVT/NoPU_103X_upgrade2023_realistic_v2-v2/90000/9CDB6CBE-E063-9049-A794-244A09CA53A0.root',

#'/store/mc/PhaseIIMTDTDRAutumn18DR/DYToLL_M-50_14TeV_TuneCP5_pythia8/FEVT/NoPU_103X_upgrade2023_realistic_v2-v2/90000/354CC7AD-BD24-7249-A26A-93F07D8194FD.root',

#DY one that wotk s'/store/mc/PhaseIIMTDTDRAutumn18DR/DYToLL_M-50_14TeV_TuneCP5_pythia8/FEVT/NoPU_103X_upgrade2023_realistic_v2-v2/90000/FF015593-7F87-9142-8363-BCEAAA2B0620.root'
#'/store/mc/PhaseIIMTDTDRAutumn18DR/DYToLL_M-50_14TeV_TuneCP5_pythia8/FEVT/NoPU_103X_upgrade2023_realistic_v2-v2/90000/558C047E-1B35-2445-BC11-B479251645F1.root'
#                                '/store/data/Run2018E/ZeroBias/RAW/v1/000/325/684/00000/DAC64D8B-241A-2546-9100-65B44FFCCF83.root',
#                                '/store/data/Run2018E/ZeroBias/RAW/v1/000/325/484/00000/AF499180-B00E-6B40-9836-F0C5DC7D8497.root',
#                                '/store/data/Run2018E/ZeroBias/RAW/v1/000/325/449/00000/9D10EB45-D6E9-684E-8489-DDF7BC4A9A3E.root',
#                                '/store/data/Run2018E/ZeroBias/RAW/v1/000/325/458/00000/8CD5C424-E460-9541-94EC-679125C2ECE4.root',
#                                '/store/data/Run2018E/ZeroBias/RAW/v1/000/325/430/00000/7A52F28E-9F80-4845-92E2-1A71F82301F8.root',
#                                '/store/data/Run2018E/ZeroBias/RAW/v1/000/325/283/00000/2C9521F5-8784-FA47-963B-64BE55AB9CA7.root'
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
	fileName = cms.string("l1TNtuple-ZeroBias.root")
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
