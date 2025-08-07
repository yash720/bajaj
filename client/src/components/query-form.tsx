import React, { useState, memo, useCallback } from "react";
import { useMutation } from "@tanstack/react-query";
import { Search } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { useToast } from "@/hooks/use-toast";
import PDFUpload from "./pdf-upload";
import { apiRequest } from "@/lib/queryClient";
import type { ClaimResponse } from "@shared/schema";

interface QueryFormProps {
  onResults: (results: ClaimResponse & { id: string }) => void;
  onLoading: (loading: boolean) => void;
}

const QueryForm = memo(function QueryForm({ onResults, onLoading }: QueryFormProps) {
  const [query, setQuery] = useState("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const { toast } = useToast();

  const submitMutation = useMutation({
    mutationFn: async (data: { query: string; pdf?: File }) => {
      const formData = new FormData();
      formData.append("query", data.query);
      if (data.pdf) {
        formData.append("pdf", data.pdf);
      }

      const response = await fetch("/api/claims", {
        method: "POST",
        body: formData,
        credentials: "include",
      });

      if (!response.ok) {
        const error = await response.text();
        throw new Error(error || "Failed to process claim");
      }

      return await response.json();
    },
    onMutate: () => {
      onLoading(true);
    },
    onSuccess: (data) => {
      onResults(data);
      onLoading(false);
      toast({
        title: "Claim Processed Successfully",
        description: `Your claim has been ${data.Decision.toLowerCase()}.`,
      });
    },
    onError: (error) => {
      onLoading(false);
      toast({
        title: "Error Processing Claim",
        description: error.message || "Failed to process your claim. Please try again.",
        variant: "destructive",
      });
    },
  });

  const handleSubmit = useCallback((e: React.FormEvent) => {
    e.preventDefault();
    
    if (!query.trim()) {
      toast({
        title: "Query Required",
        description: "Please enter your insurance query before submitting.",
        variant: "destructive",
      });
      return;
    }

    submitMutation.mutate({
      query: query.trim(),
      pdf: selectedFile || undefined,
    });
  }, [query, selectedFile, submitMutation, toast]);

  return (
    <div className="bg-white rounded-lg shadow-xl p-8 mb-8">
      <form onSubmit={handleSubmit} className="space-y-6">
        <PDFUpload
          selectedFile={selectedFile}
          onFileSelect={setSelectedFile}
        />

        <div>
          <label htmlFor="claimQuery" className="block text-lg font-medium text-gray-900 mb-2">
            Insurance Claim Query
          </label>
          <Textarea
            id="claimQuery"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            rows={6}
            className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-bajaj-blue focus:border-bajaj-blue transition-colors duration-200 resize-none"
            placeholder="46-year-old male, knee surgery in Pune, 3-month-old insurance policy"
            required
          />
          <p className="mt-2 text-sm text-gray-500">
            Provide detailed information about your insurance claim including age, medical procedure, location, and policy details.
          </p>
        </div>

        <div className="flex justify-center">
          <Button
            type="submit"
            disabled={submitMutation.isPending}
            className="bg-bajaj-blue text-white px-8 py-3 text-lg font-semibold hover:bg-blue-700 transform hover:scale-105 transition-all duration-200 focus:outline-none focus:ring-4 focus:ring-blue-300 shadow-lg"
          >
            <Search className="mr-2 h-5 w-5" />
            {submitMutation.isPending ? "Processing..." : "Process Claim"}
          </Button>
        </div>
      </form>
    </div>
  );
});

export default QueryForm;
