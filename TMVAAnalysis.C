//
// Macro for training Phase2L1BTagAnalyzer TTree using TMVA classifiers.
// TMVA is a ROOT-integrated toolkit for multivariate data analysis.
//
// Instructions:
// 1. Under the "Load data" section, make sure that dir and key together point
//    to a file that exists. The name of the .root file produced by the
//    Phase2L1BTagAnalyzer should be of the format "output_[keyword].root",
//    E.g. [keyword] is ZTT or ttbar or 1, 2, 3, ...
// 2. Run with
//        `root -l -b -q TMVAAnalysis.C`.    (add `>logRun' after .C if desired)
// 3. This will generate an output file "TMVA_output[keyword].root". Create and view desired
//    plots in the interactive TMVA GUI:
//        `root -l -e 'TMVA::TMVAGui("TMVA_output[keyword].root")'`.
//    Important: The output .eps files in `dataset/plots` will only be generated/
//               updated by creating them afresh in the interactive TMVA GUI, which
//               can be laggy. Check the Last Edited timestamp to avoid mistaking old
//               plots for new ones.
//
// Note: During Step 2, a lot of "Failed filling branch:efficiencyTree.[..]" errors
//       will pop up: these seem to be innocuous.
// 
// Based on ROOT tutorials/tmva/TMVAClassification.C and TMVAMinimalClassification.C
// by Andreas Hoecker and Kim Albertsson respectively, as well as
// tutorials/tree/copytree3.C for the tree splitting.

#include <cstdlib>
#include <iostream>
#include <map>
#include <string>

#include "TChain.h"
#include "TFile.h"
#include "TTree.h"
#include "TString.h"
#include "TObjString.h"
#include "TSystem.h"
#include "TROOT.h"

#include "TMVA/Factory.h"
#include "TMVA/DataLoader.h"
#include "TMVA/Tools.h"
#include "TMVA/TMVAGui.h"

void TMVAAnalysis()
{
    //--------------------------------------------
    // Choose TMVA methods to use
    //--------------------------------------------

    // Use key-value pairs to indicate which TMVA methods we want to use
    std::map<std::string, int> Use;

    // Neural Networks (all are feed-forward Multilayer Perceptrons)
        Use["MLP"] = 1;  // Recommended ANN
	
	// Boosted Decision Trees
	Use["BDT"] = 1;  // uses Adaptive Boost

	//--------------------------------------------
	// Load data
	//--------------------------------------------
	TString dir = "/afs/cern.ch/user/a/addropul/CMSSW_10_6_0_pre4/src/L1Trigger/Run3Ntuplizer/test/";
	//TString key = "5";
	TString inputFilename_VBF = dir + "l1TNtuple-VBF.root";
	TString inputFilename_QCD = dir + "l1TNtuple-QCD.root";

	// Get input file and declare output file where TMVA will store ntuples, hists, etc.
	TFile *inputFile_VBF = new TFile(inputFilename_VBF.Data());
	TFile *inputFile_QCD = new TFile(inputFilename_QCD.Data());
	TString outputFilename = "TMVA_output.root";
	TFile *outFile = new TFile(outputFilename, "RECREATE");
	
	// Get input tree
	TTree *inputTree_VBF = (TTree*) inputFile_VBF->Get("l1NtupleProducer/Stage3Regions/efficiencyTree");
	TTree *inputTree_QCD = (TTree*) inputFile_QCD->Get("l1NtupleProducer/Stage3Regions/efficiencyTree");

	// Split the signal and background into two trees
	TTree *sigTree = inputTree_VBF->CloneTree(0);    // Create a clone of oldtree and copy 0 entries
	TTree *bkgTree = inputTree_QCD->CloneTree(0);

	// Declare variables to read from TTree
	Double_t recoPt_1, recoEta_1, recoPhi_1, recoNthJet_1, recoPt_2, recoEta_2, recoPhi_2, recoNthJet_2,
	recoDeltaEta, recoDeltaPhi, recoDeltaR, recoMass, l1Pt_1, l1Eta_1, l1Phi_1, l1NthJet_1, l1Pt_2, l1Eta_2,
	l1Phi_2, l1NthJet_2, l1DeltaEta, l1DeltaPhi, l1DeltaR, l1Mass, l1Matched_1, l1Matched_2;
	
	Int_t  nRecoJets, nL1Jets;

	// Set branch addresses
        /*
        inputTree->SetBranchAddress("recoPt",  &recoPt);
	inputTree->SetBranchAddress("recoEta", &recoEta);
	inputTree->SetBranchAddress("recoPhi", &recoPhi);
	inputTree->SetBranchAddress("hadronFlavor", &hadronFlavor);
	inputTree->SetBranchAddress("recoTk1IP", &recoTk1IP);
	inputTree->SetBranchAddress("recoTk2IP", &recoTk2IP);
	inputTree->SetBranchAddress("recoTk3IP", &recoTk3IP);
	inputTree->SetBranchAddress("recoTk4IP", &recoTk4IP);
	*/

	inputTree_VBF->SetBranchAddress("recoPt_1", &recoPt_1);
	inputTree_VBF->SetBranchAddress("recoPt_2", &recoPt_2);
	inputTree_VBF->SetBranchAddress("recoDeltaEta", &recoDeltaEta);
	inputTree_VBF->SetBranchAddress("recoDeltaPhi", &recoDeltaPhi);
	inputTree_VBF->SetBranchAddress("recoMass", &recoMass);
	inputTree_VBF->SetBranchAddress("l1Pt_1",    &l1Pt_1);
	inputTree_VBF->SetBranchAddress("l1Pt_2",   &l1Pt_2);
	inputTree_VBF->SetBranchAddress("l1DeltaEta", &l1DeltaEta);
        inputTree_VBF->SetBranchAddress("l1DeltaPhi",   &l1DeltaPhi);
        inputTree_VBF->SetBranchAddress("l1Mass", &l1Mass);

        inputTree_QCD->SetBranchAddress("recoPt_1", &recoPt_1);
        inputTree_QCD->SetBranchAddress("recoPt_2", &recoPt_2);
        inputTree_QCD->SetBranchAddress("recoDeltaEta", &recoDeltaEta);
        inputTree_QCD->SetBranchAddress("recoDeltaPhi", &recoDeltaPhi);
        inputTree_QCD->SetBranchAddress("recoMass", &recoMass);
        inputTree_QCD->SetBranchAddress("l1Pt_1",    &l1Pt_1);
        inputTree_QCD->SetBranchAddress("l1Pt_2",   &l1Pt_2);
        inputTree_QCD->SetBranchAddress("l1DeltaEta", &l1DeltaEta);
        inputTree_QCD->SetBranchAddress("l1DeltaPhi",   &l1DeltaPhi);
        inputTree_QCD->SetBranchAddress("l1Mass", &l1Mass);

	// Loop through jets and fill sigTree and bkgTree
	Int_t i;
	Int_t j;
	for ( i = 0; i < inputTree_VBF->GetEntries(); i++ ) {
	        inputTree_VBF->GetEntry(i);
		sigTree->Fill();
	}
	for ( j = 0; j < inputTree_QCD->GetEntries(); j++ ) {
		inputTree_QCD->GetEntry(j);
		bkgTree->Fill();
	} // end jet loop

	//--------------------------------------------
	// Set up TMVA
	//--------------------------------------------	

	// Create the factory object. Later we can choose the methods whose
	// performance we'd like to investigate. The factory is the only 
	// TMVA object we have to interact with.
	//
	// The first argument is the base of the name of all the weightfiles
	// in the directory weight/
	// 
	// The second argument is the output file for the training results.
	TString factoryOptions = "AnalysisType=Classification";

	TMVA::Factory *factory = new TMVA::Factory("TMVAClassification",
						   outFile,
						   factoryOptions);

	TMVA::DataLoader *dataloader = new TMVA::DataLoader("dataset");

	// Define the input variables that will be used for the MVA training
	// Note that you may also use variable expressions, such as: 
	// "3*var1/var2*abs(var3)". [All types of expressions that can also be
	// parsed by TTree::Draw( "expression" )]

	dataloader->AddVariable("l1Pt_1", 'D');
	dataloader->AddVariable("l1Pt_2", 'D');
	dataloader->AddVariable("l1DeltaEta", 'D');
	dataloader->AddVariable("l1DeltaPhi", 'D');
	dataloader->AddVariable("l1Mass",    'D');

	// You can add an arbitrary number of signal or background trees
	// Here we set the global event weights per tree to 1.0
	// It is possible to set event-wise weights (see tutorial)
	dataloader->AddSignalTree(sigTree, 1.0);
	dataloader->AddBackgroundTree(bkgTree, 1.0);

	// End of tree registration

	// Apply additional cuts on the signal and background samples
	// e.g. TCut mycuts = "abs(var1)<0.5 && abs(var2-0.5)<1";
	
	/*
	TCut signalCut     = "recoTk1IP > -99 && recoTk2IP > -99 && recoTk3IP > -99  && recoTk4IP > -99";   
	TCut backgroundCut = "recoTk1IP > -99 && recoTk2IP > -99 && recoTk3IP > -99  && recoTk4IP > -99"; 
	*/

	TCut signalCut     = "l1Pt_1 > 0 && l1Pt_2 > 0 && l1Mass > 0 && l1Pt_1 < 511 && l1Pt_2 < 511";
	TCut backgroundCut = "l1Pt_1 > 0 && l1Pt_2 > 0 && l1Mass > 0 && l1Pt_1 < 511 && l1Pt_2 < 511";

	//TCut signalCut = "";
	//TCut backgroundCut = "";

	TString datasetOptions = "SplitMode=Random";
	dataloader->PrepareTrainingAndTestTree(signalCut, backgroundCut, datasetOptions);

	// Method specification
	TString methodOptions = "";
	//  Adaptive Boost
	if (Use["BDT"])
	  factory->BookMethod(dataloader, TMVA::Types::kBDT, "BDT", methodOptions);
	//  TMVA ANN: MLP (recommended ANN) -- all ANNs in TMVA are Multilayer Perceptrons
	if (Use["MLP"])
	  //factory->BookMethod(dataloader, TMVA::Types::kMLP, "MLP", methodOptions);
	factory->BookMethod( dataloader, TMVA::Types::kMLP, "MLP", "H:!V:NeuronType=tanh:VarTransform=N:NCycles=600:HiddenLayers=N+5:TestRate=5:!UseRegulator" );
	// Training and Evaluation
	factory->TrainAllMethods();
	factory->TestAllMethods();
	factory->EvaluateAllMethods();

	// Clean up
	outFile->Close();

	delete outFile;
}

