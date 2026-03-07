import PageLayout from "@/components/PageLayout";
import { usePatientStore } from "@/store/patientStore";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { Stethoscope, Sparkles, X } from "lucide-react";
import { useState } from "react";

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

const BASE_URL = import.meta.env.VITE_API_URL;

const Diagnosis = () => {
  const { patients, selectedPatientId, updatePatientSymptoms } = usePatientStore();
  const patient = patients.find(p => p.id === selectedPatientId);
  const [selectedSymptoms, setSelectedSymptoms] = useState<string[]>(patient?.symptoms || []);
  const [remarks, setRemarks] = useState(patient?.remarks || "");
  const [diagnosisResult, setDiagnosisResult] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const toggleSymptom = (s: string) => {
    setSelectedSymptoms(prev => (prev.includes(s) ? prev.filter(x => x !== s) : [...prev, s]));
  };

  const runDiagnosis = async () => {
    if (!patient) return;
    updatePatientSymptoms(patient.id, selectedSymptoms, remarks);
    setLoading(true);
    try {
      const res = await fetch(`${BASE_URL}/api/v1/diagnosis`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ patient_id: patient.id, symptoms: selectedSymptoms, remarks })
      });
      const data = await res.json();
      setDiagnosisResult(data.diagnosis || data.result || JSON.stringify(data));
    } catch {
      setDiagnosisResult("⚠️ An error occurred while running the diagnosis. Please try again later.");
    } finally {
      setLoading(false);
    }
  };

  if (!patient) {
    return (
      <PageLayout title="Diagnosis" subtitle="Select a patient from the queue first">
        <div className="glass-card rounded-xl p-12 flex flex-col items-center text-center">
          <Stethoscope size={48} className="text-muted-foreground/30 mb-4" />
          <h2 className="font-display font-semibold text-lg text-muted-foreground">No Patient Selected</h2>
          <p className="text-sm text-muted-foreground/70 mt-1 max-w-md">
            Go to the Patient Queue and click on a patient to select them, then return here to enter symptoms and generate a diagnosis.
          </p>
        </div>
      </PageLayout>
    );
  }

  return (
    <PageLayout title="Diagnosis" subtitle={`Patient: ${patient.name} (${patient.id})`}>
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
              <p className="text-sm text-foreground/90 whitespace-pre-wrap">{diagnosisResult}</p>
            </div>
          )}
        </div>

        <div className="glass-card rounded-xl p-5 h-fit">
          <h3 className="font-display font-semibold text-sm mb-4">Patient Info</h3>
          <div className="space-y-3 text-sm">
            {[
              ["Name", patient.name],
              ["ID", patient.id],
              ["Age", `${patient.age}`],
              ["Gender", patient.gender],
              ["Condition", patient.condition],
              ["Priority", patient.priority],
              ["Status", patient.status]
            ].map(([label, value]) => (
              <div key={label} className="flex justify-between">
                <span className="text-muted-foreground">{label}</span>
                <span className="font-medium capitalize">{value}</span>
              </div>
            ))}
          </div>
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
