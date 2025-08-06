import React from "react";
import { CheckCircle, IndianRupee, Info, Gavel, File, Code, Download, Plus, ChevronDown } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible";
import type { ClaimResponse } from "@shared/schema";

interface ResultsDisplayProps {
  results: ClaimResponse & { id: string };
  onNewQuery: () => void;
}

export default function ResultsDisplay({ results, onNewQuery }: ResultsDisplayProps) {
  const isApproved = results.Decision === "APPROVED";

  return (
    <div className="bg-white rounded-lg shadow-xl overflow-hidden">
      <div className="bg-bajaj-blue text-white px-8 py-4">
        <h3 className="text-2xl font-semibold flex items-center">
          <CheckCircle className="mr-3 h-6 w-6" />
          Claim Analysis Complete
        </h3>
      </div>
      
      <div className="p-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Decision Card */}
          <Card className={`${isApproved ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'}`}>
            <CardHeader className="pb-2">
              <CardTitle className="flex items-center text-lg">
                <CheckCircle className={`mr-3 h-5 w-5 ${isApproved ? 'text-green-600' : 'text-red-600'}`} />
                Claim Decision
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className={`text-2xl font-bold ${isApproved ? 'text-green-700' : 'text-red-700'}`}>
                {results.Decision}
              </p>
            </CardContent>
          </Card>

          {/* Amount Card */}
          <Card className="bg-blue-50 border-blue-200">
            <CardHeader className="pb-2">
              <CardTitle className="flex items-center text-lg text-bajaj-blue">
                <IndianRupee className="mr-3 h-5 w-5" />
                Claim Amount
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-2xl font-bold text-bajaj-blue">
                {results.Amount ? `₹${results.Amount.toLocaleString('en-IN')}` : 'N/A'}
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Detailed Response */}
        <div className="space-y-6">
          {/* Query Details */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Info className="mr-2 h-5 w-5 text-bajaj-blue" />
                Query Details
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="bg-gray-50 rounded-lg p-4">
                <pre className="text-sm text-gray-700 whitespace-pre-wrap font-mono">
                  {JSON.stringify(results.QueryDetails, null, 2)}
                </pre>
              </div>
            </CardContent>
          </Card>

          {/* Justification */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Gavel className="mr-2 h-5 w-5 text-bajaj-blue" />
                Justification
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="bg-gray-50 rounded-lg p-4">
                <p className="text-gray-700">
                  {results.Justification}
                </p>
              </div>
            </CardContent>
          </Card>

          {/* Relevant Policy Clauses */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <File className="mr-2 h-5 w-5 text-bajaj-blue" />
                Relevant Policy Clauses
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="bg-gray-50 rounded-lg p-4">
                <div className="space-y-3">
                  {results.RelevantClauses.map((clause, index) => (
                    <div key={index} className="border-l-4 border-bajaj-blue pl-4">
                      <div className="flex items-start space-x-2 mb-1">
                        <CheckCircle className="h-4 w-4 text-green-600 mt-1 flex-shrink-0" />
                        <span className="text-sm text-gray-700 font-medium">
                          {clause.text}
                        </span>
                      </div>
                      <div className="text-xs text-gray-500 ml-6">
                        Source: {clause.source} | Position: {clause.position}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Raw JSON Response */}
        <div className="mt-8">
          <Collapsible>
            <CollapsibleTrigger className="flex items-center w-full text-left p-4 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors">
              <Code className="mr-2 h-5 w-5 text-bajaj-blue" />
              <span className="text-lg font-semibold text-gray-900 flex-1">
                Raw JSON Response
              </span>
              <ChevronDown className="h-5 w-5 text-gray-500 transition-transform group-data-[state=open]:rotate-180" />
            </CollapsibleTrigger>
            <CollapsibleContent className="mt-2">
              <div className="bg-gray-900 rounded-lg p-4 text-green-400 overflow-x-auto">
                <pre className="text-sm">
                  {JSON.stringify(results, null, 2)}
                </pre>
              </div>
            </CollapsibleContent>
          </Collapsible>
        </div>

        {/* Action Buttons */}
        <div className="mt-8 flex flex-col sm:flex-row gap-4 justify-center">
          <Button className="bg-bajaj-blue text-white hover:bg-blue-700 transition-colors duration-200">
            <Download className="mr-2 h-4 w-4" />
            Download Report
          </Button>
          <Button
            variant="secondary"
            onClick={onNewQuery}
            className="bg-gray-600 text-white hover:bg-gray-700 transition-colors duration-200"
          >
            <Plus className="mr-2 h-4 w-4" />
            New Query
          </Button>
        </div>
      </div>
    </div>
  );
}
