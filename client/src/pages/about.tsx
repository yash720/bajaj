import React from "react";
import { Shield, Brain, Clock, Users, CheckCircle, Target } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import Navigation from "@/components/navigation";

export default function About() {
  const features = [
    {
      icon: Brain,
      title: "AI-Powered Analysis",
      description: "Advanced machine learning algorithms analyze your insurance claims with precision and accuracy."
    },
    {
      icon: Clock,
      title: "Instant Processing",
      description: "Get claim decisions in seconds, not days. Our AI processes claims 24/7 without delays."
    },
    {
      icon: Shield,
      title: "Secure & Reliable",
      description: "Your data is protected with enterprise-grade security and encryption protocols."
    },
    {
      icon: Users,
      title: "User-Friendly Interface",
      description: "Simple, intuitive design makes claim submission easy for everyone."
    }
  ];

  const benefits = [
    "Reduce claim processing time from days to seconds",
    "Eliminate human errors in claim evaluation",
    "24/7 availability for claim submissions",
    "Transparent decision-making with detailed justifications",
    "Support for multiple document formats (PDF, DOCX, etc.)",
    "Mobile-responsive design for on-the-go access"
  ];

  return (
    <div className="min-h-screen bg-bajaj-blue">
      <Navigation />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header Section */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-white mb-4">
            About Bajaj Intelligent Claims Assistant
          </h1>
          <p className="text-xl text-gray-200 max-w-3xl mx-auto">
            Revolutionizing insurance claim processing with artificial intelligence and machine learning
          </p>
        </div>

        {/* Overview Section */}
        <div className="bg-white rounded-lg shadow-xl p-8 mb-12">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-4">
                Transforming Insurance Claims
              </h2>
              <p className="text-gray-600 text-lg mb-6">
                Our AI-powered system analyzes insurance claims using advanced natural language processing 
                and machine learning algorithms. By processing policy documents and claim queries, we provide 
                instant, accurate decisions with complete transparency.
              </p>
              <p className="text-gray-600 text-lg">
                Built specifically for Bajaj Auto's insurance products, our system understands complex 
                policy terms, waiting periods, and coverage details to ensure fair and consistent claim evaluation.
              </p>
            </div>
            <div className="text-center">
              <div className="bg-bajaj-blue rounded-full w-32 h-32 flex items-center justify-center mx-auto mb-4">
                <Brain className="h-16 w-16 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-bajaj-blue">
                Powered by Advanced AI
              </h3>
            </div>
          </div>
        </div>

        {/* Features Section */}
        <div className="mb-12">
          <h2 className="text-3xl font-bold text-center text-white mb-8">
            Key Features
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature, index) => (
              <Card key={index} className="bg-white shadow-lg hover:shadow-xl transition-shadow duration-300">
                <CardHeader className="text-center pb-2">
                  <div className="bg-bajaj-blue rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-3">
                    <feature.icon className="h-6 w-6 text-white" />
                  </div>
                  <CardTitle className="text-lg font-semibold text-gray-900">
                    {feature.title}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-600 text-center text-sm">
                    {feature.description}
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* Benefits Section */}
        <div className="bg-white rounded-lg shadow-xl p-8 mb-12">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-6">
                Why Choose Our AI Assistant?
              </h2>
              <div className="space-y-4">
                {benefits.map((benefit, index) => (
                  <div key={index} className="flex items-start space-x-3">
                    <CheckCircle className="h-6 w-6 text-green-600 mt-0.5 flex-shrink-0" />
                    <p className="text-gray-700">{benefit}</p>
                  </div>
                ))}
              </div>
            </div>
            <div className="bg-bajaj-light-gray rounded-lg p-6">
              <div className="text-center">
                <Target className="h-16 w-16 text-bajaj-blue mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-gray-900 mb-3">
                  Our Mission
                </h3>
                <p className="text-gray-600">
                  To make insurance claim processing faster, more accurate, and completely transparent 
                  for every customer. We believe technology should simplify complex processes and 
                  provide instant, fair decisions.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Technology Section */}
        <div className="bg-gradient-to-r from-bajaj-blue to-blue-700 rounded-lg p-8 text-white">
          <div className="text-center">
            <h2 className="text-3xl font-bold mb-4">
              Advanced Technology Stack
            </h2>
            <p className="text-lg mb-8 max-w-3xl mx-auto">
              Our system leverages cutting-edge AI technologies including natural language processing, 
              document analysis, and machine learning models trained specifically on insurance policies and claims data.
            </p>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="text-center">
                <div className="bg-white bg-opacity-20 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-3">
                  <Brain className="h-8 w-8 text-white" />
                </div>
                <h3 className="font-semibold mb-2">Machine Learning</h3>
                <p className="text-sm opacity-90">
                  Advanced ML models for claim analysis and decision making
                </p>
              </div>
              
              <div className="text-center">
                <div className="bg-white bg-opacity-20 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-3">
                  <Shield className="h-8 w-8 text-white" />
                </div>
                <h3 className="font-semibold mb-2">Secure Processing</h3>
                <p className="text-sm opacity-90">
                  Enterprise-grade security for all document and data processing
                </p>
              </div>
              
              <div className="text-center">
                <div className="bg-white bg-opacity-20 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-3">
                  <Clock className="h-8 w-8 text-white" />
                </div>
                <h3 className="font-semibold mb-2">Real-time Analysis</h3>
                <p className="text-sm opacity-90">
                  Instant processing and response for immediate claim decisions
                </p>
              </div>
            </div>
          </div>
        </div>
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
    </div>
  );
}