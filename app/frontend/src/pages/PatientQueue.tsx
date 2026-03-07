import PageLayout from "@/components/PageLayout";
import { usePatientStore, Patient } from "@/store/patientStore";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { CheckCircle, Clock, UserCheck } from "lucide-react";
import { useState } from "react";

const doctors = ["Dr. Sarah Chen", "Dr. James Park", "Dr. Emily Taylor", "Dr. Michael Adams"];

const priorityColors: Record<string, string> = {
  high: "bg-destructive/10 text-destructive border-destructive/20",
  medium: "bg-warning/10 text-warning border-warning/20",
  low: "bg-success/10 text-success border-success/20"
};

const statusIcons: Record<string, React.ReactNode> = {
  waiting: <Clock size={14} />,
  assigned: <UserCheck size={14} />,
  seen: <CheckCircle size={14} />
};

const PatientRow = ({ patient }: { patient: Patient }) => {
  const { assignDoctor, markAsSeen, selectedPatientId, setSelectedPatientId } = usePatientStore();
  const [doctor, setDoctor] = useState(patient.assignedDoctor || "");
  const isSelected = selectedPatientId === patient.id;

  return (
    <tr
      className={`border-b border-border/50 transition-colors cursor-pointer ${isSelected ? "bg-primary/5" : "hover:bg-muted/50"}`}
      onClick={() => setSelectedPatientId(patient.id)}
    >
      <td className="px-4 py-3 text-sm font-medium text-muted-foreground">{patient.id}</td>
      <td className="px-4 py-3 text-sm font-semibold">{patient.name}</td>
      <td className="px-4 py-3 text-sm text-muted-foreground">
        {patient.age} / {patient.gender}
      </td>
      <td className="px-4 py-3 text-sm">{patient.condition}</td>
      <td className="px-4 py-3">
        <Badge variant="outline" className={priorityColors[patient.priority]}>
          {patient.priority}
        </Badge>
      </td>
      <td className="px-4 py-3 text-sm text-muted-foreground">{patient.arrivalTime}</td>
      <td className="px-4 py-3" onClick={e => e.stopPropagation()}>
        {patient.status !== "seen" ? (
          <Select
            value={doctor}
            onValueChange={v => {
              setDoctor(v);
              assignDoctor(patient.id, v);
            }}
          >
            <SelectTrigger className="h-8 w-40 text-xs">
              <SelectValue placeholder="Assign doctor" />
            </SelectTrigger>
            <SelectContent>
              {doctors.map(d => (
                <SelectItem key={d} value={d}>
                  {d}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        ) : (
          <span className="text-xs text-muted-foreground">{patient.assignedDoctor}</span>
        )}
      </td>
      <td className="px-4 py-3" onClick={e => e.stopPropagation()}>
        <div className="flex items-center gap-2">
          <span className="flex items-center gap-1 text-xs text-muted-foreground capitalize">
            {statusIcons[patient.status]} {patient.status}
          </span>
          {patient.status === "assigned" && (
            <Button size="sm" variant="outline" className="h-7 text-xs" onClick={() => markAsSeen(patient.id)}>
              Mark Seen
            </Button>
          )}
        </div>
      </td>
    </tr>
  );
};

const PatientQueue = () => {
  const { patients } = usePatientStore();
  const waiting = patients.filter(p => p.status !== "seen");
  const seen = patients.filter(p => p.status === "seen");

  return (
    <PageLayout title="Patient Queue" subtitle="Manage waiting list and assign doctors">
      <div className="glass-card rounded-xl overflow-hidden">
        <div className="px-5 py-4 border-b border-border/50">
          <h2 className="font-display font-semibold text-foreground">Waiting List</h2>
          <p className="text-xs text-muted-foreground mt-0.5">{waiting.length} patients waiting</p>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-border bg-muted/30">
                {["ID", "Name", "Age/Gender", "Condition", "Priority", "Arrival", "Doctor", "Status"].map(h => (
                  <th key={h} className="px-4 py-2.5 text-left text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {waiting.map(p => (
                <PatientRow key={p.id} patient={p} />
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {seen.length > 0 && (
        <div className="glass-card rounded-xl overflow-hidden mt-6">
          <div className="px-5 py-4 border-b border-border/50">
            <h2 className="font-display font-semibold text-foreground">Seen Patients</h2>
            <p className="text-xs text-muted-foreground mt-0.5">{seen.length} patients seen</p>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-border bg-muted/30">
                  {["ID", "Name", "Age/Gender", "Condition", "Priority", "Arrival", "Doctor", "Status"].map(h => (
                    <th key={h} className="px-4 py-2.5 text-left text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                      {h}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {seen.map(p => (
                  <PatientRow key={p.id} patient={p} />
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </PageLayout>
  );
};

export default PatientQueue;
