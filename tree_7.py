import glob, array, argparse, math
import ROOT
import sys, os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__))+'/JES_ResponseFitter/scripts/')
import JES_BalanceFitter
#import the jets
inFile2 = ROOT.TFile.Open("/afs/cern.ch/work/a/addropul/new_jets/group.perf-jets.361107.ZmmPP8_mc16d_PU_031218_tree.root ","READ")
tree = inFile2.Get("outTree_Nominal")
if( not tree ):
    print("Error, could not get input tree")
    
#intially, turn off all the branches to save time
tree.SetBranchStatus("*", 0)
#data_tree.SetBranchStatus("*", 0)


#tree.Show(i)
tree.Print()
#tree.Scan()
print(tree.GetEntries())
#turn on the branches you want to use
NPV = array.array('i', [0])
tree.SetBranchStatus("NPV", 1)
tree.SetBranchAddress("NPV", NPV)
#data_tree.SetBranchStatus("NPV", 1)
#data_tree.SetBranchAddress("NPV", NPV)

correct_mu = array.array('f',[0])
tree.SetBranchStatus("correct_mu",1)
tree.SetBranchAddress("correct_mu",correct_mu)

jet_pt = ROOT.std.vector('float')()
tree.SetBranchStatus("jet_pt", 1)
tree.SetBranchAddress("jet_pt", jet_pt)
#data_tree.SetBranchStatus("jet_pt", 1)
#data_tree.SetBranchAddress("jet_pt", jet_pt)

jet_track_pt = ROOT.std.vector('float')()
tree.SetBranchStatus("jet_track_pt", 1)
tree.SetBranchAddress("jet_track_pt", jet_track_pt)
#data_tree.SetBranchStatus("jet_track_pt", 1)
#data_tree.SetBranchAddress("jet_track_pt", jet_track_pt)

jet_phi = ROOT.std.vector('float')()
tree.SetBranchStatus("jet_phi", 1)
tree.SetBranchAddress("jet_phi", jet_phi)
#data_tree.SetBranchStatus("jet_phi", 1)
#data_tree.SetBranchAddress("jet_phi", jet_phi)

jet_track_phi = ROOT.std.vector('float')()
tree.SetBranchStatus("jet_track_phi", 1)
tree.SetBranchAddress("jet_track_phi", jet_track_phi)
#data_tree.SetBranchStatus("jet_track_phi", 1)
#data_tree.SetBranchAddress("jet_track_phi", jet_track_phi)

jet_eta = ROOT.std.vector('float')()
tree.SetBranchStatus("jet_eta", 1)
tree.SetBranchAddress("jet_eta", jet_eta)
#data_tree.SetBranchStatus("jet_eta", 1)
#data_tree.SetBranchAddress("jet_eta", jet_eta)

jet_track_eta = ROOT.std.vector('float')()
tree.SetBranchStatus("jet_track_eta", 1)
tree.SetBranchAddress("jet_track_eta", jet_track_eta)
#data_tree.SetBranchStatus("jet_track_eta", 1)
#data_tree.SetBranchAddress("jet_track_eta", jet_track_eta)

#can put code here to make plots of individual variables


histograms = ROOT.TFile("histograms.root","RECREATE")
#bins to divide the data
eta_bins = [0.0,0.3,0.8,1.2,1.7,2.5]
NPV_bins = [8.0,14.0,17.0,20.0,24.0,30.0,36.0]
jet_track_pt_bins = [5,10,15,20,25,30,35,40,45,50]
mu_bins = [15.0,25.0,31.5,37.5,45.5,57.0,70.0]
#create the histograms
xrange = range;
h =[[[[0 for x in xrange(len(jet_track_pt_bins))] for y in xrange(len(mu_bins))] for z in xrange(len(NPV_bins))] for l in xrange(len(eta_bins))]
print(len(jet_track_pt_bins))
for eta_bin_i in xrange(1,len(eta_bins)):
	for NPV_bin_i in xrange(1,len(NPV_bins)):
		for mu_bin_i in xrange(1,len(mu_bins)):
			for jet_track_pt_bin_i in xrange(1,len(jet_track_pt_bins)):
				hist_name = 'h_pt_' + str(eta_bin_i) +'_'+ str(NPV_bin_i)+ '_'+str(mu_bin_i)+ '_'+ str(jet_track_pt_bin_i)
				h1 = ROOT.TH1F(hist_name,"jet_pt",50,0,100)
				h[eta_bin_i][NPV_bin_i][mu_bin_i][jet_track_pt_bin_i] = h1
i = 0;
j = 0;
h_eta = ROOT.TH1F("h_eta","Jet_eta Distribtion",100,-5,5)
h_NPV = ROOT.TH1F("h_NPV","Jet_NPV Distribtion",100,0,100)
h_mu = ROOT.TH1F("h_mu","Jet_mu Distribtion",100,0,100)
h_jet_track_pt = ROOT.TH1F("h_track_pt","Jet_track_pt Distribtion",100,0,100)
#fill the histograms
while tree.GetEntry(i):
  i += 1;
  a = -2
  b = -2
  c = -2
  d = -2
  for jet_i in xrange(0,jet_pt.size()):
	#print("eta=",jet_eta.at(jet_i),"NPV =", NPV[0],"mu =", correct_mu[0],"track_pt=", jet_track_pt.at(jet_i))
	if jet_eta.at(jet_i) >= eta_bins[0] and jet_eta.at(jet_i) < eta_bins[1]: 
            a = 1
    	elif jet_eta.at(jet_i) >= eta_bins[1] and jet_eta.at(jet_i) < eta_bins[2]: 
            a = 2
	elif jet_eta.at(jet_i) >= eta_bins[2] and jet_eta.at(jet_i) < eta_bins[3]:
            a = 3
	elif jet_eta.at(jet_i) >= eta_bins[3] and jet_eta.at(jet_i) < eta_bins[4]:     
            a = 4
	elif jet_eta.at(jet_i) >= eta_bins[4] and jet_eta.at(jet_i) < eta_bins[5]:
            a = 5
    	else:
            a = -1
        
	if NPV[0] >= NPV_bins[0] and  NPV[0] < NPV_bins[1]:
            b = 1
    	elif NPV[0] >= NPV_bins[1] and  NPV[0] < NPV_bins[2]:           
            b = 2
	elif NPV[0] >= NPV_bins[2] and  NPV[0] < NPV_bins[3]:
            b = 3
        elif NPV[0] >= NPV_bins[3] and  NPV[0] < NPV_bins[4]:
            b = 4
        elif NPV[0] >= NPV_bins[4] and  NPV[0] < NPV_bins[5]:
            b = 5
        elif NPV[0] >= NPV_bins[5] and  NPV[0] < NPV_bins[6]:
            b = 6
    	else:
            b = -1

	if correct_mu[0] >= mu_bins[0] and correct_mu[0] < mu_bins[1]:
            c = 1
    	elif correct_mu[0] >= mu_bins[1] and correct_mu[0] < mu_bins[2]:
            c = 2
	elif correct_mu[0] >= mu_bins[2] and correct_mu[0] < mu_bins[3]:
            c = 3
	elif correct_mu[0] >= mu_bins[3] and correct_mu[0] < mu_bins[4]:
            c = 4
	elif correct_mu[0] >= mu_bins[4] and correct_mu[0] < mu_bins[5]:
            c = 5
	elif correct_mu[0] >= mu_bins[5] and correct_mu[0] < mu_bins[6]:
            c = 6
    	else:
            c = -1

	if jet_track_pt.at(jet_i) >= jet_track_pt_bins[0] and jet_track_pt.at(jet_i) < jet_track_pt_bins[1]:
            d = 1
	elif jet_track_pt.at(jet_i) >= jet_track_pt_bins[1] and jet_track_pt.at(jet_i) < jet_track_pt_bins[2]:
            d = 2
	elif jet_track_pt.at(jet_i) >= jet_track_pt_bins[2] and jet_track_pt.at(jet_i) < jet_track_pt_bins[3]:
            d = 3
	elif jet_track_pt.at(jet_i) >= jet_track_pt_bins[3] and jet_track_pt.at(jet_i) < jet_track_pt_bins[4]:
            d = 4
	elif jet_track_pt.at(jet_i) >= jet_track_pt_bins[4] and jet_track_pt.at(jet_i) < jet_track_pt_bins[5]:
            d = 5
	elif jet_track_pt.at(jet_i) >= jet_track_pt_bins[5] and jet_track_pt.at(jet_i) < jet_track_pt_bins[6]:
            d = 6
	elif jet_track_pt.at(jet_i) >= jet_track_pt_bins[6] and jet_track_pt.at(jet_i) < jet_track_pt_bins[7]:
            d = 7
	elif jet_track_pt.at(jet_i) >= jet_track_pt_bins[7] and jet_track_pt.at(jet_i) < jet_track_pt_bins[8]:
            d = 8
	elif jet_track_pt.at(jet_i) >= jet_track_pt_bins[8] and jet_track_pt.at(jet_i) < jet_track_pt_bins[9]:
            d = 9
	else: 
            d = -1
        h_eta.Fill(jet_eta.at(jet_i))
        h_NPV.Fill(NPV[0])
	h_mu.Fill(correct_mu[0])
	h_jet_track_pt.Fill(jet_track_pt.at(jet_i))
	if a == -1 or b == -1 or c == -1 or d == -1:
		#print(a,b,c,d)
		continue;
  	else:          
  		hist = h[a][b][c][d]
  		#print(a,b,c,d)
  		hist.Fill(jet_pt.at(jet_i))

histograms.Write()
