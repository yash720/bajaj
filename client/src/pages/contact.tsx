import React from "react";
import { Mail, Github, Linkedin, Instagram } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import Navigation from "@/components/navigation";
import kshitijPhoto from "@assets/1748867065584_1754504376880.jpeg";
import nihiraPhoto from "@assets/1749114006314_1754504376880.jpeg";
import yashPhoto from "@assets/Yash_1754504376881.jpg";
import gurleenPhoto from "@assets/Gurleen_1754504419770.jpg";

interface TeamMember {
  name: string;
  role: string;
  photo: string;
  email?: string;
  github?: string;
  linkedin: string;
  instagram?: string;
}

const teamMembers: TeamMember[] = [
  {
    name: "Kshitij Singh",
    role: "AI/ML Engineer",
    photo: kshitijPhoto,
    github: "https://github.com/kshitijhackathon",
    linkedin: "https://www.linkedin.com/in/kshitij-singh-915579222/",
    instagram: "https://www.instagram.com/kshitijsingh066/profilecard/?igsh=MWNkY3F6Y21nMG5yZw=="
  },
  {
    name: "Nihira Agrawal",
    role: "Frontend Developer & UI/UX Developer",
    photo: nihiraPhoto,
    email: "agrawalnihira@gmail.com",
    linkedin: "https://www.linkedin.com/in/nihira-agrawal-587810290/",
    instagram: "https://www.instagram.com/_nihiraa_?igsh=NWRsbXVkanVwZXpt"
  },
  {
    name: "Yash Sajwan",
    role: "Full Stack Developer",
    photo: yashPhoto,
    email: "yashsajwan2004@gmail.com",
    github: "https://github.com/yash720",
    linkedin: "https://www.linkedin.com/in/yash-sajwan-65a196328/"
  },
  {
    name: "Gurleen Kaur Bhatia",
    role: "Software Developer",
    photo: gurleenPhoto,
    email: "gurleenkaurbhatia211359@gmail.com",
    github: "https://github.com/Gurleen-ctrl1",
    linkedin: "https://www.linkedin.com/in/gurleenkaur-bhatia/",
    instagram: "https://www.instagram.com/gurleenkaurbhatia_?igsh=MTh1dDEzOTJ0aTk5eQ=="
  }
];

export default function Contact() {
  return (
    <div className="min-h-screen bg-bajaj-light-gray">
      <Navigation />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header Section */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Meet Our Team
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            The talented developers behind Bajaj Intelligent Claims Assistant
          </p>
        </div>

        {/* Team Members Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-8 mb-12">
          {teamMembers.map((member, index) => (
            <Card key={index} className="bg-white shadow-xl hover:shadow-2xl transition-shadow duration-300">
              <CardHeader className="text-center pb-4">
                <div className="w-32 h-32 mx-auto mb-4 rounded-full overflow-hidden border-4 border-bajaj-blue">
                  <img 
                    src={member.photo} 
                    alt={member.name}
                    className="w-full h-full object-cover"
                  />
                </div>
                <CardTitle className="text-xl font-bold text-gray-900">
                  {member.name}
                </CardTitle>
                <p className="text-bajaj-blue font-medium">
                  {member.role}
                </p>
              </CardHeader>
              
              <CardContent>
                <div className="flex justify-center space-x-4">
                  {member.email && (
                    <Button
                      variant="ghost"
                      size="sm"
                      className="text-gray-600 hover:text-bajaj-blue hover:bg-blue-50"
                      onClick={() => window.open(`mailto:${member.email}`, '_blank')}
                    >
                      <Mail className="h-5 w-5" />
                    </Button>
                  )}
                  
                  {member.github && (
                    <Button
                      variant="ghost"
                      size="sm"
                      className="text-gray-600 hover:text-bajaj-blue hover:bg-blue-50"
                      onClick={() => window.open(member.github, '_blank')}
                    >
                      <Github className="h-5 w-5" />
                    </Button>
                  )}
                  
                  <Button
                    variant="ghost"
                    size="sm"
                    className="text-gray-600 hover:text-bajaj-blue hover:bg-blue-50"
                    onClick={() => window.open(member.linkedin, '_blank')}
                  >
                    <Linkedin className="h-5 w-5" />
                  </Button>
                  
                  {member.instagram && (
                    <Button
                      variant="ghost"
                      size="sm"
                      className="text-gray-600 hover:text-bajaj-blue hover:bg-blue-50"
                      onClick={() => window.open(member.instagram, '_blank')}
                    >
                      <Instagram className="h-5 w-5" />
                    </Button>
                  )}
                </div>
                
                {/* Contact Info */}
                <div className="mt-4 text-center">
                  {member.email && (
                    <p className="text-sm text-gray-600 mb-1">
                      <Mail className="inline h-4 w-4 mr-1" />
                      {member.email}
                    </p>
                  )}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Contact Information */}
        <div className="bg-white rounded-lg shadow-xl p-8">
          <div className="text-center">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              Get In Touch
            </h2>
            <p className="text-gray-600 mb-6">
              Have questions about our AI-powered claims processing system? We'd love to hear from you!
            </p>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="text-center">
                <div className="bg-bajaj-blue rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-3">
                  <Mail className="h-6 w-6 text-white" />
                </div>
                <h3 className="font-semibold text-gray-900 mb-1">Email Us</h3>
                <p className="text-gray-600 text-sm">
                  Contact our team directly for support
                </p>
              </div>
              
              <div className="text-center">
                <div className="bg-bajaj-blue rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-3">
                  <Github className="h-6 w-6 text-white" />
                </div>
                <h3 className="font-semibold text-gray-900 mb-1">Open Source</h3>
                <p className="text-gray-600 text-sm">
                  Check out our code repositories
                </p>
              </div>
              
              <div className="text-center">
                <div className="bg-bajaj-blue rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-3">
                  <Linkedin className="h-6 w-6 text-white" />
                </div>
                <h3 className="font-semibold text-gray-900 mb-1">Professional Network</h3>
                <p className="text-gray-600 text-sm">
                  Connect with us professionally
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