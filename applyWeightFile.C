/****************************************************
 applyWeightFile.C                                
 Stephanie Kwan + based on                        
 https://root.cern.ch/doc/v610/TMVAClassificationApplication_8C.html
 
 Usage:  % root -l -b -q applyWeightFile.C 
 ****************************************************/


#include <cstdlib>
#include <vector>
#include <iostream>
#include <map>
#include <string>
#include "TFile.h"
#include "TTree.h"
#include "TString.h"
#include "TSystem.h"
#include "TROOT.h"
#include "TH1F.h"
#include "TStopwatch.h"
#if not defined(__CINT__) || defined(__MAKECINT__)
#include "TMVA/Tools.h"
#include "TMVA/Reader.h"
#include "TMVA/MethodCuts.h"
#endif

using namespace TMVA;

// two types of category methods are implemented
Bool_t UseOffsetMethod = kTRUE;

/* Use trained classifiers within an analysis module. Does not take
 * an input. */
void applyWeightFile()
{   
   /* Load the library */
   TMVA::Tools::Instance();

   /* Variable for declaring MVA methods to be tested */
   std::map<std::string,int> Use;
   
   Use["BDT"] = 1;
   Use["MLP"] = 1;

   /* Create the Reader object. */
   Reader *reader = new Reader("!Color:!Silent");

   /* Create a set of variables and spectators and declare them
      to the reader. The variable names MUST corresponds in
      name and type to those given in the weight file(s)
      used.
   */

   Float_t recoTk1IP_uint;
   Float_t recoTk2IP_uint;
   Float_t recoTk3IP_uint;
   Float_t recoTk4IP_uint;
   Float_t muPt;
   Float_t muEta;
   Float_t muSIP2D;

   reader->AddVariable("recoTk1IP_uint", &recoTk1IP_uint);
   reader->AddVariable("recoTk2IP_uint", &recoTk2IP_uint);
   reader->AddVariable("recoTk3IP_uint", &recoTk3IP_uint);
   reader->AddVariable("recoTk4IP_uint", &recoTk4IP_uint);
   //reader->AddVariable("muPt", &muPt);
   //reader->AddVariable("muEta", &muEta);
   //reader->AddVariable("muSIP2D", &muSIP2D);


   /* Book the MVA methods. */
   for (std::map<std::string,int>::iterator it = Use.begin(); it != Use.end(); it++) {
      if (it->second)
      {  TString methodName = it->first + " method";
         TString weightfile = "dataset/weights/TMVAClassification_" + TString(it->first) + ".weights.xml";
         reader->BookMVA( methodName, weightfile );
      }
   }
   
   /* Book output histograms. */
   UInt_t nbin = 100;
   std::map<std::string,TH1*> hist;
	
   hist["BDT"] = new TH1F("MVA_BDT", "MVA_BDT", nbin, -1., 1.); 
   hist["MLP"] = new TH1F("MVA_MLP", "MVA_MLP", nbin, -1.25, 1.25);

   /* Prepare input tree. */
   TString fname = TString("/afs/cern.ch/work/s/skkwan/public/triggerDevel/CMSSW_10_1_5/src/L1Trigger/phase2L1BTagAnalyzer/test/analyzer_ZTT_backup.root");
   std::cout << "--- TMVAClassificationApp    : Accessing " << fname << "!" << std::endl;
   TFile *input = TFile::Open(fname);
   if (!input)
   {  std::cout << "ERROR: could not open data file: " << fname << std::endl;
      exit(1);
   }

   /********************************************/
   /* Event loop: prepare the tree   */

   TTree* theTree = (TTree*) input->Get("L1BTagAnalyzer/efficiencyTree");
   std::cout << "--- Use signal sample for evalution" << std::endl;
   theTree->SetBranchAddress("recoTk1IP", &recoTk1IP_uint);
   theTree->SetBranchAddress("recoTk2IP", &recoTk2IP_uint);
   theTree->SetBranchAddress("recoTk3IP", &recoTk3IP_uint);
   theTree->SetBranchAddress("recoTk4IP", &recoTk4IP_uint);

   // theTree->SetBranchAddress("muPt", &muPt);
   // theTree->SetBranchAddress("muEta", &muEta);
   // theTree->SetBranchAddress("muSIP2D",  &muSIP2D);

   std::cout << "--- Processing: " << theTree->GetEntries() << " events" << std::endl;
   TStopwatch sw;
   sw.Start();

   for (Long64_t ievt=0; ievt < theTree->GetEntries(); ievt++) {
      if (ievt%1000 == 0) std::cout << "--- ... Processing event: " << ievt << std::endl;
      theTree->GetEntry(ievt);
      // Return the MVA outputs and fill into histograms
      for (std::map<std::string,int>::iterator it = Use.begin(); it != Use.end(); it++) {
         if (!it->second) continue;
         TString methodName = it->first + " method";
         hist[it->first]->Fill( reader->EvaluateMVA( methodName ) );
      }
   }
   sw.Stop();
   std::cout << "--- End of event loop: "; sw.Print();

   /* Write histograms */
   TFile *target  = new TFile( "applyWeightFile_trainOnTTbar_evalOnZTT.root", "RECREATE" );
   for (std::map<std::string,int>::iterator it = Use.begin(); it != Use.end(); it++)
      if (it->second) hist[it->first]->Write();

   target->Close();
   std::cout << "--- Created root file containing the MVA output histograms" << std::endl;

   delete reader;
   std::cout << "==> TMVAClassificationApplication is done!" << std::endl << std::endl;

}

int main( int argc, char** argv )
{
   applyWeightFile();
   return 0;
}

