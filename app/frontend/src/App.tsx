import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import AppSidebar from "@/components/AppSidebar";
import PatientQueue from "@/pages/PatientQueue";
import Analytics from "@/pages/Analytics";
import Chatbot from "@/pages/Chatbot";
import Diagnosis from "@/pages/Diagnosis";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <div className="flex min-h-screen">
          <AppSidebar />
          <Routes>
            <Route path="/" element={<PatientQueue />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/chatbot" element={<Chatbot />} />
            <Route path="/diagnosis" element={<Diagnosis />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </div>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
