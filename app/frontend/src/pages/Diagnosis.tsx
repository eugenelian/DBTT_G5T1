import PageLayout from "@/components/PageLayout";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { Sparkles, X } from "lucide-react";
import { useState } from "react";
import ReactMarkdown from "react-markdown";

const symptomsList = [
  "Fever",
  "Cough",
  "Headache",
  "Chest Pain",
  "Shortness of Breath",
  "Nausea",
  "Fatigue",
  "Dizziness",
  "Back Pain",
  "Abdominal Pain",
  "Sore Throat",
  "Joint Pain",
  "Rash",
  "Blurred Vision",
  "Numbness",
  "Palpitations",
  "Weight Loss",
  "Insomnia",
  "Swelling",
  "Loss of Appetite"
];

function parseAssistantResponse(text: string) {
  const cleaned = text.replace(/\\n/g, "\n");
  const markdownContent = cleaned.replace(/<[^>]+>/g, "").trim();
  return markdownContent;
}

const BASE_URL = import.meta.env.VITE_API_URL;

const Diagnosis = () => {
  const [selectedSymptoms, setSelectedSymptoms] = useState<string[]>([]);
  const [remarks, setRemarks] = useState("");
  const [diagnosisResult, setDiagnosisResult] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const toggleSymptom = (s: string) => {
    setSelectedSymptoms(prev => (prev.includes(s) ? prev.filter(x => x !== s) : [...prev, s]));
  };

  const runDiagnosis = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${BASE_URL}/api/v1/chat/diagnosis`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ symptoms: selectedSymptoms, remarks: remarks })
      });
      const data = await res.json();
      setDiagnosisResult(parseAssistantResponse(data.content || "No response"));
    } catch {
      setDiagnosisResult("⚠️ An error occurred while running the diagnosis. Please try again later.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <PageLayout title="Diagnosis" subtitle={`Generate Automated Diagnosis`}>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <div className="glass-card rounded-xl p-5">
            <h3 className="font-display font-semibold text-sm mb-3">Select Symptoms</h3>
            <div className="flex flex-wrap gap-2">
              {symptomsList.map(s => {
                const active = selectedSymptoms.includes(s);
                return (
                  <button
                    key={s}
                    onClick={() => toggleSymptom(s)}
                    className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all border ${
                      active ? "bg-primary text-primary-foreground border-primary" : "bg-muted/50 text-muted-foreground border-border hover:bg-muted"
                    }`}
                  >
                    {s}
                    {active && <X size={12} className="inline ml-1.5 -mr-0.5" />}
                  </button>
                );
              })}
            </div>
          </div>

          <div className="glass-card rounded-xl p-5">
            <h3 className="font-display font-semibold text-sm mb-3">Doctor's Remarks</h3>
            <Textarea value={remarks} onChange={e => setRemarks(e.target.value)} placeholder="Enter additional observations, notes, or remarks..." rows={4} />
          </div>

          <Button onClick={runDiagnosis} disabled={loading || selectedSymptoms.length === 0} className="w-full">
            <Sparkles size={16} className="mr-2" />
            {loading ? "Generating Diagnosis..." : "Run AI Diagnosis"}
          </Button>

          {diagnosisResult && (
            <div className="glass-card rounded-xl p-5 border-l-4 border-l-primary">
              <h3 className="font-display font-semibold text-sm mb-2">AI Diagnosis Result</h3>
              <div className="text-sm text-foreground/90">
                <ReactMarkdown
                  components={{
                    h3: ({ node, ...props }) => <h3 className="mt-4 mb-2 font-semibold text-base" {...props} />,
                    p: ({ node, ...props }) => <p className="mb-3 leading-relaxed" {...props} />,
                    ul: ({ node, ...props }) => <ul className="list-disc pl-5 space-y-1" {...props} />,
                    li: ({ node, ...props }) => <li className="leading-relaxed" {...props} />
                  }}
                >
                  {diagnosisResult}
                </ReactMarkdown>
              </div>
            </div>
          )}
        </div>

        <div className="glass-card rounded-xl p-5 h-fit">
          <h3 className="font-display font-semibold text-sm mb-4">Patient Info</h3>
          {selectedSymptoms.length > 0 && (
            <div className="mt-4 pt-4 border-t border-border/50">
              <p className="text-xs text-muted-foreground mb-2">Selected Symptoms</p>
              <div className="flex flex-wrap gap-1.5">
                {selectedSymptoms.map(s => (
                  <Badge key={s} variant="secondary" className="text-xs">
                    {s}
                  </Badge>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </PageLayout>
  );
};

export default Diagnosis;
