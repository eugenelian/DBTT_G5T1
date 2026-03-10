import { useState } from "react";
import PageLayout from "@/components/PageLayout";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { AlertTriangle, CheckCircle, Loader2, Send, RotateCcw } from "lucide-react";

interface TriageForm {
  age: string;
  chest_pain_type: string;
  blood_pressure: string;
  max_heart_rate: string;
  exercise_angina: string;
  bmi: string;
  hypertension: string;
  heart_disease: string;
  smoking_status: string;
}

interface TriageResult {
  urgency: number;
  age: number;
  chest_pain_type: number;
  blood_pressure: number;
  max_heart_rate: number;
  exercise_angina: number;
  bmi: number;
  hypertension: number;
  heart_disease: number;
  smoking_status: string;
}

const initialForm: TriageForm = {
  age: "",
  chest_pain_type: "",
  blood_pressure: "",
  max_heart_rate: "",
  exercise_angina: "",
  bmi: "",
  hypertension: "",
  heart_disease: "",
  smoking_status: ""
};

const CHEST_PAIN_OPTIONS = [
  { value: "1", label: "Typical Angina" },
  { value: "2", label: "Atypical Angina" },
  { value: "3", label: "Non-Anginal Pain" },
  { value: "4", label: "Asymptomatic" }
];

const SMOKING_OPTIONS = [
  { value: "formerly smoked", label: "Formerly Smoked" },
  { value: "never smoked", label: "Never Smoked" },
  { value: "smokes", label: "Currently Smokes" },
  { value: "Unknown", label: "Unknown" }
];

const BASE_URL = import.meta.env.VITE_API_URL;

const Triage = () => {
  const [form, setForm] = useState<TriageForm>(initialForm);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<TriageResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const updateField = (field: keyof TriageForm, value: string) => {
    setForm(prev => ({ ...prev, [field]: value }));
    setResult(null);
    setError(null);
  };

  const isValid =
    form.age &&
    form.chest_pain_type &&
    form.blood_pressure &&
    form.max_heart_rate &&
    form.exercise_angina !== "" &&
    form.bmi &&
    form.hypertension !== "" &&
    form.heart_disease !== "" &&
    form.smoking_status;

  const handleSubmit = async () => {
    if (!isValid) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const payload = {
        age: parseInt(form.age),
        chest_pain_type: parseFloat(form.chest_pain_type),
        blood_pressure: parseInt(form.blood_pressure),
        max_heart_rate: parseInt(form.max_heart_rate),
        exercise_angina: parseInt(form.exercise_angina),
        bmi: parseFloat(form.bmi),
        hypertension: parseInt(form.hypertension),
        heart_disease: parseInt(form.heart_disease),
        smoking_status: form.smoking_status
      };
      const res = await fetch(`${BASE_URL}/api/v1/ml/urgency`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      if (!res.ok) throw new Error("Request failed");
      const data: TriageResult = await res.json();
      setResult(data);
    } catch {
      setError("Unable to process triage request. Please try again later.");
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setForm(initialForm);
    setResult(null);
    setError(null);
  };

  return (
    <PageLayout
      title="Automated Triaging"
      subtitle="AI-powered patient urgency classification"
      actions={
        <Button variant="outline" onClick={handleReset} className="gap-2">
          <RotateCcw size={16} /> Reset
        </Button>
      }
    >
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Form */}
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Patient Vitals</CardTitle>
              <CardDescription>Enter numeric measurements</CardDescription>
            </CardHeader>
            <CardContent className="grid grid-cols-1 sm:grid-cols-2 gap-5">
              <div className="space-y-2">
                <Label htmlFor="age">Age</Label>
                <Input id="age" type="number" placeholder="e.g. 55" value={form.age} onChange={e => updateField("age", e.target.value)} />
              </div>
              <div className="space-y-2">
                <Label htmlFor="bp">Systolic Blood Pressure</Label>
                <Input id="bp" type="number" placeholder="e.g. 130" value={form.blood_pressure} onChange={e => updateField("blood_pressure", e.target.value)} />
              </div>
              <div className="space-y-2">
                <Label htmlFor="hr">Maximum Heart Rate</Label>
                <Input id="hr" type="number" placeholder="e.g. 160" value={form.max_heart_rate} onChange={e => updateField("max_heart_rate", e.target.value)} />
              </div>
              <div className="space-y-2">
                <Label htmlFor="bmi">BMI</Label>
                <Input id="bmi" type="number" step="0.1" placeholder="e.g. 27.5" value={form.bmi} onChange={e => updateField("bmi", e.target.value)} />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Clinical Indicators</CardTitle>
              <CardDescription>Select applicable conditions</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-2">
                <Label>Chest Pain Type</Label>
                <Select value={form.chest_pain_type} onValueChange={v => updateField("chest_pain_type", v)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select chest pain type" />
                  </SelectTrigger>
                  <SelectContent>
                    {CHEST_PAIN_OPTIONS.map(o => (
                      <SelectItem key={o.value} value={o.value}>
                        {o.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label>Smoking Status</Label>
                <Select value={form.smoking_status} onValueChange={v => updateField("smoking_status", v)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select smoking status" />
                  </SelectTrigger>
                  <SelectContent>
                    {SMOKING_OPTIONS.map(o => (
                      <SelectItem key={o.value} value={o.value}>
                        {o.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
                <div className="space-y-3">
                  <Label>Exercise Angina</Label>
                  <RadioGroup value={form.exercise_angina} onValueChange={v => updateField("exercise_angina", v)}>
                    <div className="flex items-center gap-2">
                      <RadioGroupItem value="0" id="ea-no" />
                      <Label htmlFor="ea-no" className="font-normal">
                        No
                      </Label>
                    </div>
                    <div className="flex items-center gap-2">
                      <RadioGroupItem value="1" id="ea-yes" />
                      <Label htmlFor="ea-yes" className="font-normal">
                        Yes
                      </Label>
                    </div>
                  </RadioGroup>
                </div>
                <div className="space-y-3">
                  <Label>Hypertension</Label>
                  <RadioGroup value={form.hypertension} onValueChange={v => updateField("hypertension", v)}>
                    <div className="flex items-center gap-2">
                      <RadioGroupItem value="0" id="ht-no" />
                      <Label htmlFor="ht-no" className="font-normal">
                        No
                      </Label>
                    </div>
                    <div className="flex items-center gap-2">
                      <RadioGroupItem value="1" id="ht-yes" />
                      <Label htmlFor="ht-yes" className="font-normal">
                        Yes
                      </Label>
                    </div>
                  </RadioGroup>
                </div>
                <div className="space-y-3">
                  <Label>Heart Disease</Label>
                  <RadioGroup value={form.heart_disease} onValueChange={v => updateField("heart_disease", v)}>
                    <div className="flex items-center gap-2">
                      <RadioGroupItem value="0" id="hd-no" />
                      <Label htmlFor="hd-no" className="font-normal">
                        No
                      </Label>
                    </div>
                    <div className="flex items-center gap-2">
                      <RadioGroupItem value="1" id="hd-yes" />
                      <Label htmlFor="hd-yes" className="font-normal">
                        Yes
                      </Label>
                    </div>
                  </RadioGroup>
                </div>
              </div>
            </CardContent>
          </Card>

          <Button onClick={handleSubmit} disabled={!isValid || loading} className="w-full gap-2" size="lg">
            {loading ? <Loader2 size={18} className="animate-spin" /> : <Send size={18} />}
            {loading ? "Processing..." : "Run Triage Assessment"}
          </Button>
        </div>

        {/* Result Panel */}
        <div>
          <Card className="sticky top-24">
            <CardHeader>
              <CardTitle className="text-lg">Assessment Result</CardTitle>
            </CardHeader>
            <CardContent>
              {!result && !error && !loading && (
                <p className="text-sm text-muted-foreground text-center py-8">Fill in patient details and run the assessment to see the result.</p>
              )}
              {loading && (
                <div className="flex flex-col items-center gap-3 py-8">
                  <Loader2 size={32} className="animate-spin text-primary" />
                  <p className="text-sm text-muted-foreground">Analysing patient data...</p>
                </div>
              )}
              {error && (
                <div className="flex flex-col items-center gap-3 py-8 text-center">
                  <AlertTriangle size={32} className="text-destructive" />
                  <p className="text-sm text-destructive font-medium">{error}</p>
                </div>
              )}
              {result && (
                <div className="space-y-4">
                  <div
                    className={`flex flex-col items-center gap-3 p-6 rounded-lg ${
                      result.urgency === 1 ? "bg-destructive/10 border border-destructive/30" : "bg-accent/10 border border-accent/30"
                    }`}
                  >
                    {result.urgency === 1 ? <AlertTriangle size={40} className="text-destructive" /> : <CheckCircle size={40} className="text-accent" />}
                    <span className={`text-xl font-bold ${result.urgency === 1 ? "text-destructive" : "text-accent"}`}>
                      {result.urgency === 1 ? "URGENT" : "NON-URGENT"}
                    </span>
                    <p className="text-xs text-muted-foreground text-center">
                      {result.urgency === 1 ? "This patient requires immediate attention." : "This patient can proceed through standard care."}
                    </p>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </PageLayout>
  );
};

export default Triage;
