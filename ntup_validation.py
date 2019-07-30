import glob, array, argparse, math
import ROOT
ROOT.gROOT.SetBatch(True)
import sys, os

#import the ntup
inFile2 = ROOT.TFile.Open("/afs/cern.ch/user/a/addropul/CMSSW_10_6_0_pre4/src/L1Trigger/Run3Ntuplizer/test/l1TNtuple-VBF.root ","READ")
tree = inFile2.Get("l1NtupleProducer/Stage3Regions/genJetTree")
if( not tree ):
    print("Error, could not get input tree")

branch_list = tree.GetListOfBranches()
branch_names = [0 for x in range(0,branch_list.GetEntries())]
for num_branch in range(0,branch_list.GetEntries()):
	branch_names[num_branch] = branch_list[num_branch].GetName()

#intially, turn off all the branches to save time
tree.SetBranchStatus("*", 0)
#tree.Show(i)
#tree.Show()
#tree.Scan()
#print(tree.GetEntries())
#turn on the branches you want to use
genPt_1 = array.array('d',[0])
tree.SetBranchStatus("genPt_1", 1)
tree.SetBranchAddress("genPt_1", genPt_1)

genEta_1 = array.array('d', [0])
tree.SetBranchStatus("genEta_1", 1)
tree.SetBranchAddress("genEta_1", genEta_1)

genPhi_1 = array.array('d', [0])
tree.SetBranchStatus("genPhi_1", 1)
tree.SetBranchAddress("genPhi_1", genPhi_1)

genPt_2 = array.array('d',[0])
tree.SetBranchStatus("genPt_2", 1)
tree.SetBranchAddress("genPt_2", genPt_2)

genEta_2 = array.array('d', [0])
tree.SetBranchStatus("genEta_2", 1)
tree.SetBranchAddress("genEta_2", genEta_2)

genPhi_2 = array.array('d', [0])
tree.SetBranchStatus("genPhi_2", 1)
tree.SetBranchAddress("genPhi_2", genPhi_2)

genDeltaEta = array.array('d',[0])
tree.SetBranchStatus("genDeltaEta", 1)
tree.SetBranchAddress("genDeltaEta", genDeltaEta)

genDeltaPhi = array.array('d', [0])
tree.SetBranchStatus("genDeltaPhi", 1)
tree.SetBranchAddress("genDeltaPhi", genDeltaPhi)

genMass = array.array('d', [0])
tree.SetBranchStatus("genMass", 1)
tree.SetBranchAddress("genMass", genMass)

histograms = ROOT.TFile("histograms.root","RECREATE")

h_genPt_1 = ROOT.TH1F("h_genPt_1","Gen Jet_1 Pt Distribtion",100,0,450)
h_genEta_1 = ROOT.TH1F("h_genEta_1","Gen Jet_1 #eta Distribtion",100,-8,8)
h_genPhi_1 = ROOT.TH1F("h_genPhi_1","Gen Jet_1 #phi Distribtion",100,-8,8)
h_genPt_2 = ROOT.TH1F("h_genPt_2","Gen Jet_2 Pt Distribtion",100,0,450)
h_genEta_2 = ROOT.TH1F("h_genEta_2","Gen Jet_2 #eta Distribtion",100,-8,8)
h_genPhi_2 = ROOT.TH1F("h_genPhi_2","Gen Jet_2 #phi Distribtion",100,-8,8)
h_genMass = ROOT.TH1F("h_genMass","Gen Jet Mass Distribtion",100,0,3000)
h_genDeltaEta = ROOT.TH1F("h_genDeltaEta","Gen Jet #Delta#eta Distribtion",100,-8,8)
h_genDeltaPhi = ROOT.TH1F("h_genDeltaPhi","Gen Jet #Delta#phi Distribtion",100,-8,8)
i=0
while tree.GetEntry(i):
	i += 1
        h_genPt_1.Fill(genPt_1[0])
        h_genEta_1.Fill(genEta_1[0])
        h_genPhi_1.Fill(genPhi_1[0])
	h_genPt_2.Fill(genPt_2[0])
        h_genEta_2.Fill(genEta_2[0])
        h_genPhi_2.Fill(genPhi_2[0])
        h_genMass.Fill(genMass[0])
        h_genDeltaEta.Fill(genDeltaEta[0])
        h_genDeltaPhi.Fill(genDeltaPhi[0])

histograms.Write()
for branch_i in range(0, branch_list.GetEntries()):
	hist_name = 'h_' + str(branch_names[branch_i])
	print(ROOT.gDirectory.FindObject(hist_name))
	if not(ROOT.gDirectory.FindObject(hist_name)):
		continue;
	else:
		h = histograms.Get(hist_name)
		c1 = ROOT.TCanvas()
		#legend = ROOT.TLegend(0.8,0.4,0.95,0.55)
		legend = ROOT.TLegend(0.78,0.60,.98,0.75)
		legend.SetTextSize(0.03)
		legend.SetFillStyle(0)
                h.GetXaxis().SetTitle(hist_name)
                h.GetYaxis().SetTitle("Number of events")
		h.Draw()
		legend.AddEntry(h,"VBFH#tau#tau","l")
		legend.Draw("same")
		c1.Update()
		c1.SaveAs(hist_name + '.png')
