import { create } from "zustand";

export interface Patient {
  id: string;
  name: string;
  age: number;
  gender: string;
  condition: string;
  priority: "high" | "medium" | "low";
  status: "waiting" | "assigned" | "seen";
  assignedDoctor?: string;
  arrivalTime: string;
  symptoms?: string[];
  remarks?: string;
}

interface PatientStore {
  patients: Patient[];
  selectedPatientId: string | null;
  setSelectedPatientId: (id: string | null) => void;
  assignDoctor: (patientId: string, doctor: string) => void;
  markAsSeen: (patientId: string) => void;
  updatePatientSymptoms: (patientId: string, symptoms: string[], remarks: string) => void;
}

const initialPatients: Patient[] = [
  { id: "P001", name: "John Miller", age: 45, gender: "Male", condition: "Chest Pain", priority: "high", status: "waiting", arrivalTime: "08:15 AM" },
  { id: "P002", name: "Emma Watson", age: 32, gender: "Female", condition: "Migraine", priority: "medium", status: "waiting", arrivalTime: "08:30 AM" },
  { id: "P003", name: "Robert Lee", age: 67, gender: "Male", condition: "Diabetes Follow-up", priority: "low", status: "waiting", arrivalTime: "08:45 AM" },
  { id: "P004", name: "Lisa Chen", age: 28, gender: "Female", condition: "Fever & Cough", priority: "medium", status: "waiting", arrivalTime: "09:00 AM" },
  { id: "P005", name: "David Brown", age: 55, gender: "Male", condition: "Back Pain", priority: "low", status: "waiting", arrivalTime: "09:15 AM" },
  { id: "P006", name: "Maria Garcia", age: 40, gender: "Female", condition: "Allergic Reaction", priority: "high", status: "waiting", arrivalTime: "09:30 AM" }
];

export const usePatientStore = create<PatientStore>(set => ({
  patients: initialPatients,
  selectedPatientId: null,
  setSelectedPatientId: id => set({ selectedPatientId: id }),
  assignDoctor: (patientId, doctor) =>
    set(state => ({
      patients: state.patients.map(p => (p.id === patientId ? { ...p, assignedDoctor: doctor, status: "assigned" } : p))
    })),
  markAsSeen: patientId =>
    set(state => ({
      patients: state.patients.map(p => (p.id === patientId ? { ...p, status: "seen" } : p))
    })),
  updatePatientSymptoms: (patientId, symptoms, remarks) =>
    set(state => ({
      patients: state.patients.map(p => (p.id === patientId ? { ...p, symptoms, remarks } : p))
    }))
}));
