import glob, array, argparse, math
import ROOT
ROOT.gROOT.SetBatch(True)
import sys, os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__))+'/JES_ResponseFitter/scripts/')
import JES_BalanceFitter #JES_BalanceFitter written by Jeff Dandoy
from array import array
#parser = argparse.ArgumentParser()
#parser.add_argument('eta',type = int,  help = "Choose which bin to hold constant in eta. If eta is the parameter that should vary, type 0. Else, choose 1 for 0.0:0.3, 2 for 0.3:0.8, 3 for 0.8:1.2, 4 for 1.2:1.7, 5 for 1.7:2.5")
#parser.add_argument('NPV',type = int,  help = "Choose which bin to hold constant in NPV. If NPV is the parameter  that should vary, type 0. Else, choose 1 for 0:10, 2 for 10:20, 3 for 20:30")
#parser.add_argument('mu',type = int,  help = "Choose which bin to hold constant in mu. If mu is the parameter that should vary, type 0. Else, choose 1 for 5:15, choose 2 for 15:25, choose 3 for 25:35, choose 4 for 35:45, choose 5 for 45:55, choose 6 for 55:65, choose 7 for 65:75, choose 8 for 75:85")
#parser.add_argument('jet_track_pt',type = int, help = "Choose which bin to hold constant in jet_track_pt. If jet_track_pt is the parameter that should vary, type 0. Else, choose 1 for 5:10, choose 2 for 10:15, choose 3 for 15:20, choose 4 for 20:25, choose 5 for 25:30, choose 6 for 30:35, choose 7 for 35:40, choose 8 for 40:45, choose 9 for 45:50")
#
#args = parser.parse_args()

eta_bins = [0.0,0.3,0.8,1.2,1.7,2.5]
NPV_bins = [8.0,14.0,17.0,20.0,24.0,30.0,36.0]
jet_track_pt_bins = [5,10,15,20,25,30,35,40,45,50]
mu_bins = [15.0,25.0,31.5,37.5,45.5,57.0,70.0]
track_pt_low_edge = 0
#define a fitter
def MJB_fit(myFitter, h_response_distribution, low_threshold=1/2., high_threshold=1/2.):
  if h_response_distribution == h[3][2][3][9]:  print("low_threshold" + str(low_threshold))
  maxContent = h_response_distribution.GetBinContent(h_response_distribution.GetMaximumBin())
  if h_response_distribution == h[3][2][3][9]: print("maxContent" + str(maxContent))
  fitLow = h_response_distribution.GetXaxis().GetBinLowEdge( h_response_distribution.FindFirstBinAbove(maxContent*low_threshold)-1)
  if fitLow <= track_pt_low_edge:
	print(str(fitLow) + "fitLow <= track_pt_low_edge " + str(track_pt_low_edge))
	fitLow = track_pt_low_edge
  if h_response_distribution == h[3][2][3][9]: print("fit Low" + str(fitLow))
  fitHigh = h_response_distribution.GetXaxis().GetBinUpEdge( h_response_distribution.FindLastBinAbove(maxContent*high_threshold)+1 )
 # if fitHigh <= fitLow:
	#print("fit High" + str(fitHigh)+ "<= fitLow " + str(fitLow))
	#fitHigh = 85
  if h_response_distribution == h[3][2][3][9]: print("fit High" + str(fitHigh))
  fit_result = myFitter.Fit(h_response_distribution, fitLow, fitHigh )
  return fit_result

inFile2 = ROOT.TFile.Open("/afs/cern.ch/work/a/addropul/new_jets/histograms.root ","READ")

myFitter = JES_BalanceFitter.JES_BalanceFitter(1.6)
myFitter.SetGaus()
myFitter.SetFitColor(ROOT.kRed)
myFitter.rebin = False
#make the Stage 0 histograms
xrange = range;
h =[[[[0 for x in xrange(len(jet_track_pt_bins))] for y in xrange(len(mu_bins))] for z in xrange(len(NPV_bins))] for l in xrange(len(eta_bins))]
mean_h =[[[[0 for x in xrange(len(jet_track_pt_bins))] for y in xrange(len(mu_bins))] for z in xrange(len(NPV_bins))] for l in xrange(len(eta_bins))]
sigma_h =[[[[0 for x in xrange(len(jet_track_pt_bins))] for y in xrange(len(mu_bins))] for z in xrange(len(NPV_bins))] for l in xrange(len(eta_bins))]
h_fit = [[[[0 for x in xrange(len(jet_track_pt_bins))] for y in xrange(len(mu_bins))] for z in xrange(len(NPV_bins))] for l in xrange(len(eta_bins))]
print(len(jet_track_pt_bins))
for eta_bin_i in xrange(1,len(eta_bins)):
        for NPV_bin_i in xrange(1,len(NPV_bins)):
                for mu_bin_i in xrange(1,len(mu_bins)):
                        for jet_track_pt_bin_i in xrange(1,len(jet_track_pt_bins)):
				track_pt_low_edge = jet_track_pt_bins[jet_track_pt_bin_i - 1]
                                hist_name = 'h_pt_' + str(eta_bin_i) +'_'+ str(NPV_bin_i)+ '_'+str(mu_bin_i)+ '_'+ str(jet_track_pt_bin_i)
                                h1 = inFile2.Get(hist_name)
				if(not h1):
    					print("Error, could not get input histogram")
				h1.SetDirectory(0)
				if h1.GetEntries() <= 500:
					h1.Rebin(3)
				binX = h1.FindBin(track_pt_low_edge)
				for bin_i in range(1,binX):
					h1.SetBinContent(bin_i,0)
				h[eta_bin_i][NPV_bin_i][mu_bin_i][jet_track_pt_bin_i] = h1
				if h1.GetEntries() < 150 or track_pt_low_edge == 5:
					h_fit[eta_bin_i][NPV_bin_i][mu_bin_i][jet_track_pt_bin_i] = None
					mean_h[eta_bin_i][NPV_bin_i][mu_bin_i][jet_track_pt_bin_i] = None
					continue;
				fit_result = MJB_fit(myFitter,h1)
				h_fit[eta_bin_i][NPV_bin_i][mu_bin_i][jet_track_pt_bin_i] = fit_result
                                mean_h[eta_bin_i][NPV_bin_i][mu_bin_i][jet_track_pt_bin_i] = myFitter.GetMean()
				sigma_h[eta_bin_i][NPV_bin_i][mu_bin_i][jet_track_pt_bin_i] = myFitter.GetSigma()

#make the Stage 1 graphs
pt_mean = [[[0 for x in xrange(len(jet_track_pt_bins))] for y in xrange(len(mu_bins))] for l in xrange(len(eta_bins))]
pt_mean_error = [[[0 for x in xrange(len(jet_track_pt_bins))] for y in xrange(len(mu_bins))] for l in xrange(len(eta_bins))]
NPV_mean = [[[0 for x in xrange(len(jet_track_pt_bins))] for y in xrange(len(mu_bins))] for l in xrange(len(eta_bins))]
fit_NPV_pt = [[[0 for x in xrange(len(jet_track_pt_bins))] for y in xrange(len(mu_bins))] for l in xrange(len(eta_bins))]
slope_NPV_pt = [[[0 for x in xrange(len(jet_track_pt_bins))] for y in xrange(len(mu_bins))] for l in xrange(len(eta_bins))]
pt_mean_temp = []
NPV_mean_temp = []
pt_error_temp = []
lin =  ROOT.TF1("lin","[0] + [1]*x",0,40)

for mu_bin_i in xrange(1,len(mu_bins)):
	for eta_bin_i in xrange(1,len(eta_bins)):
        	for jet_track_pt_bin_i in xrange(1,len(jet_track_pt_bins)):
                        for NPV_bin_i in xrange(1,len(NPV_bins)):
				if jet_track_pt_bin_i == 1: continue
				if mean_h[eta_bin_i][NPV_bin_i][mu_bin_i][jet_track_pt_bin_i] != None:
					pt_mean_temp.append(mean_h[eta_bin_i][NPV_bin_i][mu_bin_i][jet_track_pt_bin_i])
					NPV_mean_temp.append(NPV_bins[NPV_bin_i-1])
					pt_error_temp.append(sigma_h[eta_bin_i][NPV_bin_i][mu_bin_i][jet_track_pt_bin_i])
				if NPV_bins[NPV_bin_i] == NPV_bins[len(NPV_bins)-1]:
					pt_mean[eta_bin_i][mu_bin_i][jet_track_pt_bin_i] = pt_mean_temp
					pt_mean_error[eta_bin_i][mu_bin_i][jet_track_pt_bin_i] = pt_error_temp
					NPV_mean[eta_bin_i][mu_bin_i][jet_track_pt_bin_i] = NPV_mean_temp
					pt_mean_arr = array('f',pt_mean[eta_bin_i][mu_bin_i][jet_track_pt_bin_i])
					NPV_mean_arr = array('f',NPV_mean[eta_bin_i][mu_bin_i][jet_track_pt_bin_i])
					if len(NPV_mean_arr) <= 1:
						print(str(len(NPV_mean_arr)) + "too few points")
						continue
					NPV_vs_pt = ROOT.TGraph(len(NPV_mean_arr),NPV_mean_arr, pt_mean_arr)
					fit_NPV_pt[eta_bin_i][mu_bin_i][jet_track_pt_bin_i] = NPV_vs_pt.Fit(lin,"S")
					slope_NPV_pt[eta_bin_i][mu_bin_i][jet_track_pt_bin_i] = fit_NPV_pt[eta_bin_i][mu_bin_i][jet_track_pt_bin_i].Parameters()[1]
					pt_mean_temp = []
					NPV_mean_temp = []
					pt_error_temp = []
#Make the Stage 2 graphs
mu_stg1 = [[0 for x in xrange(len(jet_track_pt_bins))] for l in xrange(len(eta_bins))]
slope_stg1 = [[0 for x in xrange(len(jet_track_pt_bins))] for l in xrange(len(eta_bins))]
fit_stg2 = [[0 for x in xrange(len(jet_track_pt_bins))] for l in xrange(len(eta_bins))]
mean_stg2 = [[0 for x in xrange(len(jet_track_pt_bins))] for l in xrange(len(eta_bins))]
slope_stg1_temp = []
mu_temp = []

const =  ROOT.TF1("lin","[0]",0,40)

for eta_bin_i in xrange(1,len(eta_bins)):
	for jet_track_pt_bin_i in xrange(1,len(jet_track_pt_bins)):
		for mu_bin_i in xrange(1,len(mu_bins)):
			slope_stg1_temp.append(slope_NPV_pt[eta_bin_i][mu_bin_i][jet_track_pt_bin_i])#filling temp list to hold slope of stage 1
			mu_temp.append(mu_bins[mu_bin_i-1])# and associated mu for const eta, track_pt
			if mu_bins[mu_bin_i] == mu_bins[len(mu_bins)-1]:
				slope_stg1[eta_bin_i][jet_track_pt_bin_i] = slope_stg1_temp#fill new lists of lists  with temp lists
				mu_stg1[eta_bin_i][jet_track_pt_bin_i] = mu_temp
				slope_stg1_arr = array('f',slope_stg1[eta_bin_i][jet_track_pt_bin_i])#convert lists to arrays
                        	mu_arr = array('f', mu_stg1[eta_bin_i][jet_track_pt_bin_i])
				mu_vs_slopestg1 = ROOT.TGraph(6,mu_arr, slope_stg1_arr)#graph the data
				fit_stg2[eta_bin_i][jet_track_pt_bin_i] = mu_vs_slopestg1.Fit(const,"S")#this is a fit of the data
				mean_stg2[eta_bin_i][jet_track_pt_bin_i] = fit_stg2[eta_bin_i][jet_track_pt_bin_i].Parameters()[0]#this is the mean
				slope_stg1_temp = []
				mu_temp = []
#Make the Stage 3 graphs
avg_stg2_temp = []
track_pt_temp = []
avg_stg2 = [0 for l in xrange(len(eta_bins))]
track_pt_stg2 = [0 for l in xrange(len(eta_bins))]

for eta_bin_i in xrange(1,len(eta_bins)):
	for jet_track_pt_bin_i in xrange(1,len(jet_track_pt_bins)):
		avg_stg2_temp.append(mean_stg2[eta_bin_i][jet_track_pt_bin_i])
		track_pt_temp.append(jet_track_pt_bins[jet_track_pt_bin_i-1])
		if jet_track_pt_bins[jet_track_pt_bin_i] == jet_track_pt_bins[len(jet_track_pt_bins)-1]:
			avg_stg2[eta_bin_i] = avg_stg2_temp
			track_pt_stg2[eta_bin_i] = track_pt_temp
			avg_stg2_arr = array('f',avg_stg2[eta_bin_i])
			track_pt_stg2_arr = array('f',track_pt_stg2[eta_bin_i])
			track_pt_vs_avg_stg2 = ROOT.TGraph(len(avg_stg2_arr), track_pt_stg2_arr,avg_stg2_arr)
			avg_stg2_temp = []
			track_pt_temp = []
#Plot the Stage 3 graphs
for eta_bin_i in xrange(1,len(eta_bins)):
        x, y = array('f',track_pt_stg2[eta_bin_i]), array('f', avg_stg2[eta_bin_i])
        c1 = ROOT.TCanvas()
        gr = ROOT.TGraph(len(x),x, y)
	gr.GetYaxis().SetTitle("< #partial <p^{reco}_{T}> / #partial N_{PV}>_{<#mu>}")
        gr.GetYaxis().SetTitleOffset(0.95)
        gr.GetXaxis().SetTitle("p^{track}_{T}")
	gr.GetYaxis().SetRangeUser(-0.5,0.5)
        gr.SetTitle("Average of Stage 2 vs p^{track}_{T}")
        gr.Draw("A*")
        const =  ROOT.TF1("const","[0]",0,40)
        fit1 = gr.Fit(const,"S")
        fit1.Draw("same")
        file_name = 'stage3_' + str(eta_bin_i) + '_final.png'
        legend = ROOT.TLegend(0.1,0.8,0.48,0.9)
        legend.SetFillStyle(0)
        #legend.SetHeader("Stage 3","C"); #option "C" allows to center the header
        label = 'eta: ' + str(eta_bins[eta_bin_i-1])+'-'+str( eta_bins[eta_bin_i])
        #legend.AddEntry(const,label,"l");
	hold = ROOT.TObject
        hold = None
        legend.AddEntry(hold,'#eta: ' + str(eta_bins[eta_bin_i-1])+'-'+str( eta_bins[eta_bin_i]),"")
        legend.AddEntry(hold,'Fit Mean: '+ str(fit1.Parameters()[0]),"")
        legend.Draw("same")
        c1.Update()
        c1.SaveAs(file_name)
        x = []
        y = []


#Plot the Stage 1 graphs
for eta_bin_i in xrange(1,len(eta_bins)):
        for mu_bin_i in xrange(1,len(mu_bins)):
                for jet_track_pt_bin_i in xrange(1,len(jet_track_pt_bins)):
        		if jet_track_pt_bin_i == 1: continue
        		x, y, z = array('f',NPV_mean[eta_bin_i][mu_bin_i][jet_track_pt_bin_i]), array('f',pt_mean[eta_bin_i][mu_bin_i][jet_track_pt_bin_i]), array('f',pt_mean_error[eta_bin_i][mu_bin_i][jet_track_pt_bin_i])
        		c1 = ROOT.TCanvas()
			print(str(z)+"errors")
			zero = [0 for l in xrange(len(x))]
			zeros = array('f',zero)
        		gr = ROOT.TGraphErrors(len(x),x, y,zeros,z)
			gr.GetXaxis().SetTitle("N_{PV}")
                        gr.GetYaxis().SetTitle("<p^{reco}_{T}>")
			gr.GetYaxis().SetRangeUser(0,80)
                        gr.SetTitle("Average Reconstructed Transverse Momentum vs Number of Primary Vertices")
        		gr.Draw("A*")
        		lin =  ROOT.TF1("lin","[0] + [1]*x",0,40)
        		fit1 = gr.Fit(lin,"S")
        		fit1.Draw("same")
        		file_name = 'stage1_' + str(eta_bin_i) + '_'+str(mu_bin_i)+ '_'+ str(jet_track_pt_bin_i)+ '_final.png'
        		legend = ROOT.TLegend(0.1,0.7,0.48,0.9) 
        		legend.SetFillStyle(0)
        		#legend.SetHeader("Stage 1","C"); #option "C" allows to center the header
        		label = 'eta: ' + str(eta_bins[eta_bin_i-1])+'-'+str( eta_bins[eta_bin_i]) + ',mu: ' +str( mu_bins[mu_bin_i-1])+'-'+str(mu_bins[mu_bin_i])+ ',track_pt: ' + str(jet_track_pt_bins[jet_track_pt_bin_i-1]) + '-'+str( jet_track_pt_bins[jet_track_pt_bin_i])
                        legend.AddEntry(lin,"<p^{reco}_{T}>","l")
		        hold = ROOT.TObject
                        hold = None 
                        legend.AddEntry(hold,'#eta: ' + str(eta_bins[eta_bin_i-1])+'-'+str( eta_bins[eta_bin_i]),"")
                        legend.AddEntry(hold,'<#mu>: '+str( mu_bins[mu_bin_i-1])+'-'+str(mu_bins[mu_bin_i]),"")
                        legend.AddEntry(hold,'p^{track}_{T}: '+str(jet_track_pt_bins[jet_track_pt_bin_i-1]) + '-'+str( jet_track_pt_bins[jet_track_pt_bin_i]),"")
        		legend.AddEntry(hold,'Fit y-int: '+ str(fit1.Parameters()[0]),"")
			legend.AddEntry(hold,'Fit slope: '+ str(fit1.Parameters()[1]),"")
			legend.SetFillStyle(0)
        		legend.Draw("same")
        		c1.Update()
			c1.SaveAs(file_name)
			x = []
			y = []


#Plot the Stage 2 graphs
for eta_bin_i in xrange(1,len(eta_bins)):
                for jet_track_pt_bin_i in xrange(1,len(jet_track_pt_bins)):
			if jet_track_pt_bin_i == 1: continue
                        x, y = array('f',mu_stg1[eta_bin_i][jet_track_pt_bin_i]), array('f', slope_stg1[eta_bin_i][jet_track_pt_bin_i])
                        c1 = ROOT.TCanvas()
                        gr = ROOT.TGraph(len(x),x, y)
                        gr.GetYaxis().SetTitle("< #partial <p^{reco}_{T}> / #partial N_{PV}>")
			gr.GetYaxis().SetTitleOffset(0.8)
			gr.GetYaxis().SetRangeUser(-1,1)
                        gr.GetXaxis().SetTitle("<#mu>")
                        gr.SetTitle("Slope of Stage 1 vs Average Number of Interactions per Bunch Crossing")
                        gr.Draw("A*")
                        const =  ROOT.TF1("const","[0]",0,40)
                        fit1 = gr.Fit(const,"S")
                        fit1.Draw("same")
                        file_name = 'stage2_' + str(eta_bin_i) + '_'+ str(jet_track_pt_bin_i)+ '_final.png'
                        legend = ROOT.TLegend(0.1,0.8,0.48,0.9)
                        legend.SetFillStyle(0)
                        #legend.SetHeader("Stage 2","C"); #option "C" allows to center the header
                        label = 'eta: ' + str(eta_bins[eta_bin_i-1])+'-'+str( eta_bins[eta_bin_i]) + ',track_pt: ' + str(jet_track_pt_bins[jet_track_pt_bin_i-1]) + '-'+str( jet_track_pt_bins[jet_track_pt_bin_i])
                        #legend.AddEntry(const,"Stage 1 Slope","l");
			hold = ROOT.TObject
                        hold = None
                        legend.AddEntry(hold,'#eta: ' + str(eta_bins[eta_bin_i-1])+'-'+str( eta_bins[eta_bin_i]),"")
                        legend.AddEntry(hold,'p^{track}_{T}: '+str(jet_track_pt_bins[jet_track_pt_bin_i-1]) + '-'+str( jet_track_pt_bins[jet_track_pt_bin_i]),"")
                        legend.AddEntry(hold,'Fit Mean: '+ str(fit1.Parameters()[0]),"")
                        legend.Draw("same")
                        c1.Update()
                        c1.SaveAs(file_name)
                        x = []
                        y = []


#Plot the Stage 0 histograms
for eta_bin_i in xrange(1,len(eta_bins)):
	for NPV_bin_i in xrange(1,len(NPV_bins)):
		for mu_bin_i in xrange(1,len(mu_bins)):
                	for jet_track_pt_bin_i in xrange(1,len(jet_track_pt_bins)):
				track_pt_low_edge = jet_track_pt_bins[jet_track_pt_bin_i - 1]
				c1 = ROOT.TCanvas()
				legend = ROOT.TLegend(0.7,0.5,0.9,0.7)
				hist1 = h[eta_bin_i][NPV_bin_i][mu_bin_i][jet_track_pt_bin_i]
				fit1 = h_fit[eta_bin_i][NPV_bin_i][mu_bin_i][jet_track_pt_bin_i]
				sigma = sigma_h[eta_bin_i][NPV_bin_i][mu_bin_i][jet_track_pt_bin_i]
				mean = mean_h[eta_bin_i][NPV_bin_i][mu_bin_i][jet_track_pt_bin_i]
				ROOT.gStyle.SetOptStat()
				hist1.GetXaxis().SetTitle("p^{reco}_{T}")
				hist1.GetYaxis().SetTitle("Number of events")
				hist1.SetTitle("MC Jet Transverse Momentum Distribution")
				hist1.Draw("same")
				if hist1.GetEntries() >= 150 and track_pt_low_edge >  5:
					fit1.Draw("same")
				hist_name1 = 'h_pt_' + str(eta_bin_i) +'_'+ str(NPV_bin_i)+ '_'+str(mu_bin_i)+ '_'+ str(jet_track_pt_bin_i) + '_try5'
				label = 'eta: ' + str(eta_bins[eta_bin_i-1])+'-'+str( eta_bins[eta_bin_i]) +',NPV: '+ str(NPV_bins[NPV_bin_i -1])+'-'+str(NPV_bins[NPV_bin_i])+ ',mu: ' +str( mu_bins[mu_bin_i-1])+'-'+str(mu_bins[mu_bin_i])+ ',track_pt: ' + str(jet_track_pt_bins[jet_track_pt_bin_i-1]) + '-'+str( jet_track_pt_bins[jet_track_pt_bin_i])
				legend.AddEntry(hist1,'h_pt_' + str(eta_bin_i) +'_'+ str(NPV_bin_i)+ '_'+str(mu_bin_i)+ '_'+ str(jet_track_pt_bin_i),"l")
				hold = ROOT.TObject
				hold = None 
				legend.AddEntry(hold,'#eta: ' + str(eta_bins[eta_bin_i-1])+'-'+str( eta_bins[eta_bin_i]),"")
				legend.AddEntry(hold,'N_{PV}: '+ str(NPV_bins[NPV_bin_i -1])+'-'+str(NPV_bins[NPV_bin_i]),"")
				legend.AddEntry(hold,'<#mu>: '+str( mu_bins[mu_bin_i-1])+'-'+str(mu_bins[mu_bin_i]),"")
				legend.AddEntry(hold,'p^{track}_{T}: '+str(jet_track_pt_bins[jet_track_pt_bin_i-1]) + '-'+str( jet_track_pt_bins[jet_track_pt_bin_i]),"")
				legend.AddEntry(hold,'#sigma: '+ str(sigma),"")
				legend.AddEntry(hold,'Fit #mu: '+ str(mean),"")
                                legend.SetFillStyle(0)
				legend.Draw("same")
				c1.Update() 
				c1.SaveAs(str(hist_name1)+".png") 
