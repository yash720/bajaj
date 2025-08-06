import React, { useState, useEffect } from "react";
import Navigation from "@/components/navigation";
import LoadingAnimation from "@/components/loading-animation";
import QueryForm from "@/components/query-form";
import ResultsDisplay from "@/components/results-display";
import type { ClaimResponse } from "@shared/schema";

export default function Home() {
  const [showMainContent, setShowMainContent] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [results, setResults] = useState<(ClaimResponse & { id: string }) | null>(null);
  const [processStep, setProcessStep] = useState(1);

  useEffect(() => {
    if (isProcessing) {
      const timer1 = setTimeout(() => setProcessStep(2), 700);
      const timer2 = setTimeout(() => setProcessStep(3), 1400);
      
      return () => {
        clearTimeout(timer1);
        clearTimeout(timer2);
      };
    } else {
      setProcessStep(1);
    }
  }, [isProcessing]);

  const handleResults = (newResults: ClaimResponse & { id: string }) => {
    setResults(newResults);
    setIsProcessing(false);
    // Scroll to results
    setTimeout(() => {
      const resultsElement = document.getElementById('results-section');
      if (resultsElement) {
        resultsElement.scrollIntoView({ behavior: 'smooth' });
      }
    }, 100);
  };

  const handleNewQuery = () => {
    setResults(null);
    setIsProcessing(false);
    setProcessStep(1);
    // Scroll to form
    setTimeout(() => {
      const formElement = document.getElementById('query-form');
      if (formElement) {
        formElement.scrollIntoView({ behavior: 'smooth' });
      }
    }, 100);
  };

  return (
    <div className="min-h-screen bg-bajaj-light-gray">
      <LoadingAnimation onComplete={() => setShowMainContent(true)} />
      
      {showMainContent && (
        <>
          <Navigation />
          
          {/* Main Content */}
          <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            {/* Hero Section */}
            <div className="text-center mb-12">
              <h2 className="text-4xl font-bold text-gray-900 mb-4">
                AI-Powered Claims Processing
              </h2>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                Submit your insurance query and receive instant AI-powered analysis with comprehensive claim evaluation and recommendations.
              </p>
            </div>

            {/* Query Form */}
            <div id="query-form">
              <QueryForm
                onResults={handleResults}
                onLoading={setIsProcessing}
              />
            </div>

            {/* Loading State */}
            {isProcessing && (
              <div className="bg-white rounded-lg shadow-xl p-12 mb-8">
                <div className="text-center">
                  <div className="loading-spinner mx-auto mb-6"></div>
                  <h3 className="text-2xl font-semibold text-bajaj-blue mb-2">
                    Processing Your Claim
                  </h3>
                  <p className="text-gray-600">
                    Our AI is analyzing your query and checking policy details...
                  </p>
                  
                  {/* Progress Steps */}
                  <div className="mt-8 space-y-4">
                    <div className="flex items-center justify-center space-x-3">
                      <div className={`w-4 h-4 rounded-full ${processStep >= 1 ? 'bg-bajaj-blue animate-pulse' : 'bg-gray-300'}`}></div>
                      <span className={`text-sm ${processStep >= 1 ? 'text-gray-700' : 'text-gray-500'}`}>
                        Parsing claim information
                      </span>
                    </div>
                    <div className="flex items-center justify-center space-x-3">
                      <div className={`w-4 h-4 rounded-full ${processStep >= 2 ? 'bg-bajaj-blue animate-pulse' : 'bg-gray-300'}`}></div>
                      <span className={`text-sm ${processStep >= 2 ? 'text-gray-700' : 'text-gray-500'}`}>
                        Checking policy validity
                      </span>
                    </div>
                    <div className="flex items-center justify-center space-x-3">
                      <div className={`w-4 h-4 rounded-full ${processStep >= 3 ? 'bg-bajaj-blue animate-pulse' : 'bg-gray-300'}`}></div>
                      <span className={`text-sm ${processStep >= 3 ? 'text-gray-700' : 'text-gray-500'}`}>
                        Generating recommendations
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Results Section */}
            {results && (
              <div id="results-section">
                <ResultsDisplay
                  results={results}
                  onNewQuery={handleNewQuery}
                />
              </div>
            )}
          </main>

          {/* Footer */}
          <footer className="bg-bajaj-blue text-white py-6 mt-16">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="text-center">
                <p className="text-sm">
                  © 2025 Bajaj Auto Ltd. | AI-Powered Claims Processing
                </p>
                <div className="mt-2 space-x-4 text-sm">
                  <a href="#" className="hover:text-gray-300 transition-colors">
                    Privacy Policy
                  </a>
                  <span>|</span>
                  <a href="#" className="hover:text-gray-300 transition-colors">
                    Terms of Service
                  </a>
                  <span>|</span>
                  <a href="#" className="hover:text-gray-300 transition-colors">
                    Support
                  </a>
                </div>
              </div>
            </div>
          </footer>
        </>
      )}
    </div>
  );
}
