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
'/store/mc/RunIIAutumn18MiniAOD/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/25775DB5-4DFF-8D48-9784-6A4F95BB702C.root',
'/store/mc/RunIIAutumn18MiniAOD/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/9F5E0C26-A64B-2D45-9BE7-CC2677A4413F.root' 
#'/store/mc/RunIISummer17MiniAOD/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/MINIAODSIM/NZSFlatPU28to62_92X_upgrade2017_realistic_v10-v2/50000/960FACDE-52A2-E711-8DE1-02163E013F24.root'#this one worked for TT
#'/store/mc/RunIISpring18MiniAOD/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/NZSPU40to70_100X_upgrade2018_realistic_v10-v2/90000/D61F71C5-4A30-E811-AAED-FA163EFC9F83.root'#this one worked for DY
#'/store/mc/RunIIAutumn18MiniAOD/QCD_Pt-15to7000_TuneCP5_Flat2018_13TeV_pythia8/MINIAODSIM/FlatPU0to70RAW_102X_upgrade2018_realistic_v15-v1/270000/3530CF72-C7DB-A74C-849F-ED7EEAB01927.root'#this one worked for QCD
								),
                            secondaryFileNames = cms.untracked.vstring(
'/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/C39AEE38-613E-0940-AFFA-09DC923FE179.root', '/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/310450D8-9B44-5A40-8871-944E283EB769.root', '/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/5B5CA197-46CE-B04E-94DC-61932A13E1AB.root',

'/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/00F3C844-3821-EA42-B34E-89F9E11CE41A.root', '/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/59757256-22DE-2643-8989-BF5ED4E4053A.root', '/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/9DD59747-25E3-0B46-9731-591971A36AB2.root', '/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/58632A4C-FDF5-9647-AC23-50D953AA6F6C.root', '/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/56885390-5AF4-4C47-BDC0-7A002BD6E391.root', '/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/1F2720B2-DB10-DB42-98C2-DB68D1589DA0.root',

'/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/D025D64C-393C-A34F-BADD-24F605A50803.root', '/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/7BFE23CF-CCD9-ED44-B537-765D8760208A.root', '/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/298C9888-6453-7148-A37D-997B13AB9279.root', '/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/4C88040A-2981-3C4B-B832-BEE7D122A3DD.root', '/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/530596FB-D551-554E-887B-C0A0BDCD0E07.root', '/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/E246FD05-5480-4644-8336-B5C6C83C8BD0.root', '/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/5E7C775C-1491-5F42-9F4A-3B1EB7DBD29B.root',

'/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/36B1607D-EA12-F844-BD36-8EE28D8F10E5.root', '/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/349BA64F-FF2A-CC4F-A75E-E4C40D39314C.root', '/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/DC55D06D-CAEB-2841-A4C1-2DA34DE1D36D.root', '/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/390BA7D6-B46C-0040-8AF3-CB72002ABB13.root', '/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/F82E663E-7866-0B45-BBBE-16B6DA5CD599.root', '/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/1F50E189-C909-8542-9A5C-46606A8C348F.root',

'/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/C13A21BC-6791-444E-8B23-38280B3828D8.root', '/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/44EDA072-6679-D544-AAF3-07047ECD4D82.root', '/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/A156585E-3BE0-D848-8AB1-0B24B505893A.root',
#second TT file 
'/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/335394DF-6C1C-8140-BCD3-2AC052E0765A.root', '/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/FE95F8BC-392D-714C-92D7-2A08C3F1306F.root', '/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/638236E2-43E6-1248-ADAD-463B2AC70C50.root',

		'/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/490861F2-E930-D344-A00D-917F7E11C97B.root', '/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/C10A717F-3CE8-F849-8F84-8966100C1416.root', '/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/E70B68A5-F462-2F40-BD33-6BA23F070208.root',


'/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/4081BD73-7AA3-BE46-B96A-4CEA38869A04.root', '/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/100F44D5-8F2C-C140-92FC-038A3D91A348.root', '/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/CE07BED4-BA92-0F46-A773-BFA8FEF2570C.root', '/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/822F37FF-20D9-5446-9615-39AA959DF8E1.root', '/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/E3036D1A-F67A-4544-B48D-91C9A7630D79.root', '/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/DF5E23EE-4846-B64B-8FC9-0C01E0F4A5B1.root',


'/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/60DFBDA6-7938-544D-9A1E-FF1461EA33EB.root', '/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/EB783433-DA80-3442-9D48-7DCD4644594D.root', '/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/9F56A9A6-602F-664E-AC64-666F2AD384C8.root', '/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/EA5EE5E0-9D3C-F74B-97BA-193C847A7292.root', '/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/F91C8CAF-95A7-E84B-BB3A-F92D57873793.root', '/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/57679493-0293-2A4D-B978-51D0732503F3.root', '/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/1F4FEDF7-0F7D-204C-8C5D-47F09734D2D6.root',


'/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/738ACA95-2FC1-7B41-9B29-1FBAFBA7EADB.root', '/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/DE88006D-6421-2746-82DD-42B8FAFFBC53.root', '/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/303C4615-CA09-2048-B0B0-3DF4372D8B29.root', '/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/8B9CA81C-B292-E244-903A-5F9693EBC98D.root', '/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/204695E3-8754-5948-87F4-E23E1C6F3432.root', '/store/mc/RunIIAutumn18DR/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/GEN-SIM-RAW/NZSFlatPU28to62_102X_upgrade2018_realistic_v15_ext1-v1/120000/FE29EAE3-F540-DE40-A2A3-B253AD8A577F.root'



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
#'/store/mc/RunIIAutumn18DR/QCD_Pt-15to7000_TuneCP5_Flat2018_13TeV_pythia8/GEN-SIM-RAW/FlatPU0to70RAW_102X_upgrade2018_realistic_v15-v1/270001/C2CA8E1D-D223-FC41-8976-
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
	fileName = cms.string("l1TNtuple-TT.root")
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
