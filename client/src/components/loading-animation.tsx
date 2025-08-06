import React, { useEffect, useState } from "react";
import bajajLogoPath from "@assets/bajaj-auto-bike-logo-11549750548dzky3ovjqc_1754502098000.png";

interface LoadingAnimationProps {
  onComplete: () => void;
}

export default function LoadingAnimation({ onComplete }: LoadingAnimationProps) {
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsVisible(false);
      onComplete();
    }, 2500);

    return () => clearTimeout(timer);
  }, [onComplete]);

  if (!isVisible) return null;

  return (
    <div className="fixed inset-0 bg-white z-50 flex items-center justify-center">
      <div className="text-center">
        <div className="animate-fade-in-spin mb-4">
          <img 
            src={bajajLogoPath} 
            alt="Bajaj Logo" 
            className="w-20 h-20 mx-auto"
          />
        </div>
        <p className="text-bajaj-blue text-lg font-medium">
          Loading Bajaj Intelligent Claims Assistant...
        </p>
      </div>
    </div>
  );
}
