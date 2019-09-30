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

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(60000) )

process.source = cms.Source("PoolSource",
                            #fileNames = cms.untracked.vstring(inputFiles)#,
                            #secondaryFileNames = cms.untracked.vstring(secondaryMap[options.inputFiles[0]])
                            fileNames = cms.untracked.vstring(
'/store/mc/RunIISpring18MiniAOD/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90000/D61F71C5-4A30-E811-AAED-FA163EFC9F83.root'#this one worked for DY
#'/store/mc/RunIIAutumn18MiniAOD/QCD_Pt-15to7000_TuneCP5_Flat2018_13TeV_pythia8/MINIAODSIM/FlatPU0to70RAW_102X_upgrade2018_realistic_v15-v1/270000/3530CF72-C7DB-A74C-849F-ED7EEAB01927.root'#this one worked for QCD
								),
                            secondaryFileNames = cms.untracked.vstring(
'/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90000/8445A728-2A2F-E811-A5E5-FA163EBD49DA.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90000/64970A9E-4C2F-E811-88E5-FA163EF027B6.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90000/1C68903C-362F-E811-A5CC-02163E015189.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90002/18466B6E-722F-E811-A5D9-FA163E92EC07.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90000/CE4496F5-1F2F-E811-A030-FA163EC9C155.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90000/E4C9189C-4C2F-E811-8C6E-FA163EA7D610.root',

'/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90000/72961E09-342F-E811-84F2-FA163EDD6A45.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90000/9C19C752-6C2F-E811-8F33-FA163E434352.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90001/E4C807F7-622F-E811-A42B-FA163E0F33B3.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90001/D6B73FD2-782F-E811-8088-FA163E6CF400.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90001/96477989-5B2F-E811-AC6E-FA163E58909B.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90001/048E4DDC-612F-E811-89E9-02163E019EA2.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90002/BEA2D72B-782F-E811-8E4E-FA163EF3EB39.root',

'/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90002/2A1C59A7-542F-E811-95C8-FA163E0F2333.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90000/1EDACE1B-362F-E811-B3B4-FA163EB77666.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90000/DC67028A-4D2F-E811-B2E9-FA163EC01FA2.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90000/E80EBB41-612F-E811-B060-FA163E9C3CEB.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90001/9EFAD695-592F-E811-9C9D-FA163E82F168.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90001/3A615125-2A2F-E811-9596-FA163E9C368A.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90003/FE7B245B-792F-E811-81E8-FA163EE4B249.root',

'/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90001/0A85565D-712F-E811-8DE2-FA163EE0B5EF.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90001/1AC5C5AE-562F-E811-AF56-FA163ECFD65A.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90002/126B1922-602F-E811-A713-02163E0130EA.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90001/EC278AC4-562F-E811-9856-FA163E6F273A.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90001/1E7A017D-342F-E811-85D9-FA163E42C0B5.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90001/1C94672F-632F-E811-A913-FA163E811693.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90003/5C23C099-492F-E811-95D4-FA163E6A88D6.root',

'/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90002/C0F69419-1D2F-E811-87DC-FA163E8973C5.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90002/9AF94950-272F-E811-A7EF-FA163EEA1DC3.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90001/F6343807-1D2F-E811-8589-FA163E15D3A9.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90003/E8FBBE0F-342F-E811-9967-FA163E2F9BC3.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90000/666B2412-342F-E811-8468-FA163EE00996.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90002/68DC0978-342F-E811-99F6-FA163EE0B5EF.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90001/2205A1F4-332F-E811-8E14-FA163E133A3E.root',

'/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90001/D8C497BD-712F-E811-8EF7-02163E00B8F2.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90001/168991E0-702F-E811-86D0-FA163E8A5B3D.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90000/F0C07A1A-6E2F-E811-9ECF-FA163ED9BE5A.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90002/707A25FC-A22F-E811-8767-FA163EC21A0B.root',

'/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90000/42072035-342F-E811-B3D5-02163E014E51.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90001/D2C59269-522F-E811-A69D-02163E01A01B.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90000/C665B62E-582F-E811-9769-FA163E41AAA4.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90000/CCAF4618-342F-E811-A0EB-FA163EB26BEA.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90001/54B8352D-592F-E811-B9CD-FA163EA5D5A9.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90003/5477A6F3-5D2F-E811-A521-FA163E9F09F8.root',

'/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90000/1A3EE78C-6A2F-E811-A273-FA163EDAD0E7.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90001/5CEBEE9E-342F-E811-8014-FA163E1D9711.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90002/000B7C3E-582F-E811-BD3B-FA163EC5A669.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90000/12FBA485-722F-E811-A3FF-FA163E9639D6.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90000/8435F79F-722F-E811-9E3D-FA163EBF0D83.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90002/DE5F6D73-362F-E811-91BB-02163E00AC8B.root',

'/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90000/4A424120-862E-E811-A7CE-FA163EF88454.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90000/0A970109-9B2E-E811-AB19-FA163EEFAEF0.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90001/5C97DB1C-152E-E811-B95B-FA163EB15818.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90002/0C4898A5-A02E-E811-B647-02163E01A10A.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90002/CC7B6A42-5C2E-E811-84A7-FA163E10C791.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90002/84A6F141-5C2E-E811-9B9D-FA163E02A9B8.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90002/908E1EDB-A62E-E811-A8E8-FA163EB96B07.root',

'/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90000/C83797FA-8C2E-E811-B598-FA163EA48C39.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90000/8297277E-872E-E811-8D00-FA163E2B102D.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90001/4A80DA1E-882E-E811-B448-FA163E039158.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90001/68042186-2E2E-E811-8BB0-FA163EB5EF29.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90002/9E336131-4C2E-E811-8BB2-FA163E57B0C7.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90002/A4EDC403-6A2E-E811-8522-FA163E7EF2D9.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90003/B038CD25-752E-E811-8BB3-FA163E3AC704.root'
#these worked for DY
#'/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90000/C83797FA-8C2E-E811-B598-FA163EA48C39.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90000/8297277E-872E-E811-8D00-FA163E2B102D.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90001/4A80DA1E-882E-E811-B448-FA163E039158.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90001/68042186-2E2E-E811-8BB0-FA163EB5EF29.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90002/9E336131-4C2E-E811-8BB2-FA163E57B0C7.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90002/A4EDC403-6A2E-E811-8522-FA163E7EF2D9.root', '/store/mc/RunIISpring18DR/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/GEN-SIM-RAW/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90003/B038CD25-752E-E811-8BB3-FA163E3AC704.root'
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
	fileName = cms.string("/afs/cern.ch/work/a/addropul/l1TNtuple-DY.root")
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
