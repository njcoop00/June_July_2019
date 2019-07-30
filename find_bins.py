import glob, array, argparse, math
import ROOT
ROOT.gROOT.SetBatch(True)
import sys, os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__))+'/JES_ResponseFitter/scripts/')
import JES_BalanceFitter
#import saved histograms
inFile2 = ROOT.TFile.Open("/afs/cern.ch/work/a/addropul/new_jets/histograms.root ","READ")
h1 = inFile2.Get("h_eta")
h2 = inFile2.Get("h_NPV")
h3 = inFile2.Get("h_mu")
h4 = inFile2.Get("h_track_pt")

#find appropriate bin edges for  NPV and mu
sum_entries = 0
mu_edges = []
num_mu_bins = h3.GetNbinsX()
print(num_mu_bins)
for bin_i in range(num_mu_bins):
	bin_entries = h3.GetBinContent(bin_i)
	sum_entries = sum_entries + bin_entries
	if sum_entries >= h3.Integral()/6:
		edge = h3.GetXaxis().GetBinLowEdge(bin_i)
		mu_edges.append( edge)
		sum_entries = 0
		continue;
print("mu_edges "+ str(mu_edges))

sum_entries1 = 0
NPV_edges = []
num_NPV_bins = h2.GetNbinsX()
print(num_NPV_bins)
for bin_i in range(num_NPV_bins):
        bin_entries = h2.GetBinContent(bin_i)
        sum_entries1 = sum_entries1 + bin_entries
        if sum_entries1 >= h2.Integral()/6:
                edge = h2.GetXaxis().GetBinLowEdge(bin_i)
                NPV_edges.append( edge)
                sum_entries1 = 0
                continue;
print("NPV_edges "+ str(NPV_edges))

#plotting eta, NPV, mu, and track_pt histograms
c1 = ROOT.TCanvas()
legend = ROOT.TLegend(0.8,0.4,0.95,0.55)
legend.SetTextSize(0.03)
h1.Draw()
h1.SetTitle("#eta Distribution")
#legend.AddEntry(h1,"eta","l")
#legend.Draw("same")
c1.Update()
c1.SaveAs("h_eta.png")

c2 = ROOT.TCanvas()
#legend2 = ROOT.TLegend(0.8,0.4,0.95,0.55)
#legend2.SetTextSize(0.03)
h2.Draw()
h2.SetTitle("N_{PV} Distribution")
#legend2.AddEntry(h2,"NPV","l")
#legend2.Draw("same")
c2.Update()
c2.SaveAs("h_NPV.png")

c3 = ROOT.TCanvas()
#legend3 = ROOT.TLegend(0.8,0.4,0.95,0.55)
#legend3.SetTextSize(0.03)
h3.Draw()
h3.SetTitle("<#mu> Distribution")
#legend3.AddEntry(h3,"mu","l")
#legend3.Draw("same")
c3.Update()
c3.SaveAs("h_mu.png")

c4 = ROOT.TCanvas()
#legend4 = ROOT.TLegend(0.8,0.4,0.95,0.55)
#legend4.SetTextSize(0.03)
h4.Draw()
h4.SetTitle("p^{track}_{T} Distribution")
#legend4.AddEntry(h4,"track_pt","l")
#legend4.Draw("same")
c4.Update()
c4.SaveAs("h_track_pt.png")


#eta_bins = ["0.0","0.3","0.8","1.2","1.7","2.5"]
#NPV_bins = ["0","10","20","30"]
#jet_track_pt_bins = ["5","10","15","20","25","30","35","40","45","50"]
#mu_bins = ["5","15","25","35","45","55","65","75","85"]
#
#myFitter = JES_BalanceFitter.JES_BalanceFitter(1.6)
#myFitter.SetGaus()
#myFitter.SetFitColor(ROOT.kRed)
#myFitter.rebin = False
#
#xrange = range;
#h =[[[[0 for x in xrange(len(jet_track_pt_bins))] for y in xrange(len(mu_bins))] for z in xrange(len(NPV_bins))] for l in xrange(len(eta_bins))]
#mean_h =[[[[0 for x in xrange(len(jet_track_pt_bins))] for y in xrange(len(mu_bins))] for z in xrange(len(NPV_bins))] for l in xrange(len(eta_bins))]
#print(len(jet_track_pt_bins))
#for eta_bin_i in xrange(1,len(eta_bins)):
#        for NPV_bin_i in xrange(1,len(NPV_bins)):
#                for mu_bin_i in xrange(1,len(mu_bins)):
#                        for jet_track_pt_bin_i in xrange(1,len(jet_track_pt_bins)):
#                                hist_name = 'h_pt_' + str(eta_bin_i) +'_'+ str(NPV_bin_i)+ '_'+str(mu_bin_i)+ '_'+ str(jet_track_pt_bin_i)
#                                h1 = inFile2.Get(hist_name)
#				if(not h1):
#    					print("Error, could not get input histogram")
#				h1.SetDirectory(0)
#				h[eta_bin_i][NPV_bin_i][mu_bin_i][jet_track_pt_bin_i] = h1
#
#				fit_result = MJB_fit(myFitter,h1)
#                                mean_h[eta_bin_i][NPV_bin_i][mu_bin_i][jet_track_pt_bin_i] = myFitter.GetMean()
#
#def MJB_fit(myFitter, h_response_distribution, low_threshold=1/2., high_threshold=1/2.):
#  maxContent = h_response_distribution.GetBinContent(h_response_distribution.GetMaximumBin())
#  fitLow = h_response_distribution.GetXaxis().GetBinLowEdge( h_response_distribution.FindFirstBinAbove(maxContent*low_threshold)-1 )
#  fitHigh = h_response_distribution.GetXaxis().GetBinUpEdge( h_response_distribution.FindLastBinAbove(maxContent*high_threshold)+1 )
#  fit_result = myFitter.Fit(h_response_distribution, fitLow, fitHigh )
#  return fit_result

#c1 = ROOT.TCanvas()
#legend = ROOT.TLegend(0.8,0.4,0.95,0.55)
#legend.SetTextSize(0.03)
#a = args.eta
#b = args.NPV
#c = args.mu
#d = args.jet_track_pt
#
#if args.eta == 0: bins = eta_bins
#elif args.NPV  == 0: bins =  NPV_bins
#elif args.mu  == 0: bins = mu_bins 
#elif args.jet_track_pt == 0: bins = jet_track_pt_bins
#
#for nhist in xrange(1,len(bins)):
#    if args.eta == 0: a = nhist
#    elif args.NPV  == 0: b =  nhist 
#    elif args.mu  == 0: c =  nhist 
#    elif args.jet_track_pt == 0: d = nhist
#    
#    hist1 = h[a][b][c][d]
#    print(a,b,c,d)
#    hist1.Draw("same")
#    hist1.SetLineColor(nhist)
#    hist_name1 = 'h_pt_' + str(a) +'_'+ str(b)+ '_'+str(c)+ '_'+ str(nhist)
#    legend.AddEntry(hist1,str(hist_name1),"l")
#    legend.Draw("same")
#    c1.Update() 
#
#c1.SaveAs(hist_name+".png") 
