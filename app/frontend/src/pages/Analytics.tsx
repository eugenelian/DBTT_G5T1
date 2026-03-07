import { useState, useEffect, useCallback } from "react";
import { RefreshCw } from "lucide-react";
import PageLayout from "@/components/PageLayout";
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from "recharts";
import { Users, Heart, Thermometer, AlertTriangle } from "lucide-react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

interface AnalyticsData {
  overview: {
    total_patients: number;
    urgent_patients: number;
    non_urgent_patients: number;
    overall_urgency_rate: number;
    avg_age: number;
    avg_bmi: number;
    avg_blood_pressure: number;
    avg_max_heart_rate: number;
  };
  urgency_by_age_group: { label: string; total: number; urgent: number; urgency_rate: number }[];
  urgency_by_chest_pain: { label: string; total: number; urgent: number; urgency_rate: number }[];
  urgency_by_smoking: { label: string; total: number; urgent: number; urgency_rate: number }[];
  urgency_by_bp_category: { label: string; total: number; urgent: number; urgency_rate: number }[];
  urgency_by_bmi_category: { label: string; total: number; urgent: number; urgency_rate: number }[];
  comorbidities: Record<string, { no: { urgent: number; total: number; urgency_rate: number }; yes: { urgent: number; total: number; urgency_rate: number } }>;
  distributions: Record<string, { labels: string[]; counts: number[] }>;
  feature_correlations: Record<string, number>;
  age_chest_pain_heatmap: { age_group: string; chest_pain: string; urgency_rate: number }[];
  risk_segments: { risk_factor_count: number; total: number; urgent: number; urgency_rate: number }[];
}

const COLORS = ["hsl(199, 89%, 36%)", "hsl(168, 60%, 42%)", "hsl(32, 95%, 55%)", "hsl(280, 60%, 55%)", "hsl(0, 72%, 55%)", "hsl(215, 25%, 50%)"];

const URGENCY_COLORS = ["hsl(199, 89%, 36%)", "hsl(0, 72%, 55%)"];

const ChartCard = ({ title, children, className = "" }: { title: string; children: React.ReactNode; className?: string }) => (
  <div className={`glass-card rounded-xl p-5 ${className}`}>
    <h3 className="font-display font-semibold text-sm mb-4">{title}</h3>
    {children}
  </div>
);

const StatCard = ({ icon: Icon, label, value, sub }: { icon: React.ElementType; label: string; value: string | number; sub?: string }) => (
  <div className="glass-card rounded-xl p-4 flex items-center gap-4">
    <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
      <Icon className="w-5 h-5 text-primary" />
    </div>
    <div>
      <p className="text-xs text-muted-foreground">{label}</p>
      <p className="text-lg font-display font-bold">{value}</p>
      {sub && <p className="text-xs text-muted-foreground">{sub}</p>}
    </div>
  </div>
);

const PAGE_TITLE = "Patient Analytics";
const PAGE_SUBTITLE = "Visualise Patient Analytics";
const BASE_URL = import.meta.env.VITE_API_URL;

const Analytics = () => {
  const [data, setData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchAnalytics = () => {
    setLoading(true);
    setError(null);
    fetch(`${BASE_URL}/api/v1/analytics`)
      .then(r => {
        if (!r.ok) throw new Error("Failed to fetch");
        return r.json();
      })
      .then(setData)
      .catch(() => setError("Unable to load analytics data."))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchAnalytics();
  }, []);

  if (loading)
    return (
      <PageLayout title={PAGE_TITLE} subtitle={PAGE_SUBTITLE}>
        <div className="flex flex-col items-center justify-center py-20 gap-3">
          <div className="animate-spin w-10 h-10 border-3 border-primary border-t-transparent rounded-full" />
          <p className="text-sm text-muted-foreground">Fetching latest analytics…</p>
        </div>
      </PageLayout>
    );

  if (error || !data)
    return (
      <PageLayout title={PAGE_TITLE} subtitle={PAGE_SUBTITLE}>
        <div className="flex flex-col items-center justify-center py-20 gap-4 text-center">
          <div className="w-14 h-14 rounded-full bg-destructive/10 flex items-center justify-center">
            <AlertTriangle className="w-7 h-7 text-destructive" />
          </div>
          <div>
            <p className="font-display font-semibold text-lg">Data Unavailable</p>
            <p className="text-sm text-muted-foreground mt-1">We couldn't retrieve the analytics data. Please try again later.</p>
          </div>
          <button
            onClick={fetchAnalytics}
            className="mt-2 px-4 py-2 rounded-lg bg-primary text-primary-foreground text-sm font-medium hover:bg-primary/90 transition-colors"
          >
            Retry
          </button>
        </div>
      </PageLayout>
    );

  const { overview } = data;
  const pieData = [
    { name: "Non-Urgent", value: overview.non_urgent_patients },
    { name: "Urgent", value: overview.urgent_patients }
  ];

  const correlationData = Object.entries(data.feature_correlations)
    .map(([name, value]) => ({ name, value, absValue: Math.abs(value) }))
    .sort((a, b) => b.absValue - a.absValue);

  const comorbidityData = Object.entries(data.comorbidities).map(([key, val]) => ({
    name: key.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase()),
    Without: +(val.no.urgency_rate * 100).toFixed(1),
    With: +(val.yes.urgency_rate * 100).toFixed(1)
  }));

  const ageGroups = [...new Set(data.age_chest_pain_heatmap.map(d => d.age_group))];
  const chestPainTypes = [...new Set(data.age_chest_pain_heatmap.map(d => d.chest_pain))];

  return (
    <PageLayout title={PAGE_TITLE} subtitle={PAGE_SUBTITLE}>
      {/* Refresh Button */}
      <div className="flex justify-end mb-4">
        <button
          onClick={fetchAnalytics}
          className="flex items-center gap-2 px-3 py-1.5 rounded-lg border border-border text-sm font-medium hover:bg-muted transition-colors"
        >
          <RefreshCw className="w-4 h-4" /> Refresh Data
        </button>
      </div>
      {/* Overview Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <StatCard
          icon={Users}
          label="Total Patients"
          value={overview.total_patients.toLocaleString()}
          sub={`${(overview.overall_urgency_rate * 100).toFixed(1)}% urgency rate`}
        />
        <StatCard icon={AlertTriangle} label="Urgent Patients" value={overview.urgent_patients} sub={`of ${overview.total_patients.toLocaleString()}`} />
        <StatCard icon={Heart} label="Avg Blood Pressure" value={overview.avg_blood_pressure} sub={`Heart Rate: ${overview.avg_max_heart_rate}`} />
        <StatCard icon={Thermometer} label="Avg BMI" value={overview.avg_bmi} sub={`Avg Age: ${overview.avg_age}`} />
      </div>

      <Tabs defaultValue="urgency" className="space-y-6">
        <TabsList>
          <TabsTrigger value="urgency">Urgency Analysis</TabsTrigger>
          <TabsTrigger value="distributions">Distributions</TabsTrigger>
          <TabsTrigger value="correlations">Correlations & Risk</TabsTrigger>
        </TabsList>

        {/* Urgency Analysis Tab */}
        <TabsContent value="urgency">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <ChartCard title="Patient Urgency Split">
              <ResponsiveContainer width="100%" height={260}>
                <PieChart>
                  <Pie
                    data={pieData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={100}
                    paddingAngle={4}
                    dataKey="value"
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(1)}%`}
                  >
                    {pieData.map((_, i) => (
                      <Cell key={i} fill={URGENCY_COLORS[i]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </ChartCard>

            <ChartCard title="Urgency by Age Group">
              <ResponsiveContainer width="100%" height={260}>
                <BarChart data={data.urgency_by_age_group}>
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                  <XAxis dataKey="label" tick={{ fontSize: 12 }} />
                  <YAxis tick={{ fontSize: 12 }} />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="urgent" name="Urgent" fill={URGENCY_COLORS[1]} radius={[4, 4, 0, 0]} />
                  <Bar dataKey="total" name="Total" fill={URGENCY_COLORS[0]} radius={[4, 4, 0, 0]} opacity={0.5} />
                </BarChart>
              </ResponsiveContainer>
            </ChartCard>

            <ChartCard title="Urgency by Chest Pain Type">
              <ResponsiveContainer width="100%" height={260}>
                <BarChart data={data.urgency_by_chest_pain} layout="vertical">
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                  <XAxis type="number" tick={{ fontSize: 12 }} />
                  <YAxis dataKey="label" type="category" tick={{ fontSize: 11 }} width={100} />
                  <Tooltip formatter={(val: number, name: string) => (name === "Urgency Rate" ? `${(val * 100).toFixed(1)}%` : val)} />
                  <Legend />
                  <Bar dataKey="urgent" name="Urgent" fill={URGENCY_COLORS[1]} radius={[0, 4, 4, 0]} />
                  <Bar dataKey="total" name="Total" fill={URGENCY_COLORS[0]} radius={[0, 4, 4, 0]} opacity={0.5} />
                </BarChart>
              </ResponsiveContainer>
            </ChartCard>

            <ChartCard title="Urgency by Smoking Status">
              <ResponsiveContainer width="100%" height={260}>
                <BarChart data={data.urgency_by_smoking}>
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                  <XAxis dataKey="label" tick={{ fontSize: 11 }} />
                  <YAxis tick={{ fontSize: 12 }} />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="urgent" name="Urgent" fill={URGENCY_COLORS[1]} radius={[4, 4, 0, 0]} />
                  <Bar dataKey="total" name="Total" fill={URGENCY_COLORS[0]} radius={[4, 4, 0, 0]} opacity={0.5} />
                </BarChart>
              </ResponsiveContainer>
            </ChartCard>

            <ChartCard title="Urgency by Blood Pressure Category">
              <ResponsiveContainer width="100%" height={260}>
                <BarChart data={data.urgency_by_bp_category}>
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                  <XAxis dataKey="label" tick={{ fontSize: 10 }} />
                  <YAxis tick={{ fontSize: 12 }} />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="urgent" name="Urgent" fill={URGENCY_COLORS[1]} radius={[4, 4, 0, 0]} />
                  <Bar dataKey="total" name="Total" fill={URGENCY_COLORS[0]} radius={[4, 4, 0, 0]} opacity={0.5} />
                </BarChart>
              </ResponsiveContainer>
            </ChartCard>

            <ChartCard title="Urgency by BMI Category">
              <ResponsiveContainer width="100%" height={260}>
                <BarChart data={data.urgency_by_bmi_category}>
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                  <XAxis dataKey="label" tick={{ fontSize: 12 }} />
                  <YAxis tick={{ fontSize: 12 }} />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="urgent" name="Urgent" fill={URGENCY_COLORS[1]} radius={[4, 4, 0, 0]} />
                  <Bar dataKey="total" name="Total" fill={URGENCY_COLORS[0]} radius={[4, 4, 0, 0]} opacity={0.5} />
                </BarChart>
              </ResponsiveContainer>
            </ChartCard>
          </div>
        </TabsContent>

        {/* Distributions Tab */}
        <TabsContent value="distributions">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {Object.entries(data.distributions).map(([key, dist]) => {
              const chartData = dist.labels.map((label, i) => ({ range: label, count: dist.counts[i] }));
              const title = key.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase()) + " Distribution";
              return (
                <ChartCard key={key} title={title}>
                  <ResponsiveContainer width="100%" height={260}>
                    <BarChart data={chartData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                      <XAxis dataKey="range" tick={{ fontSize: 10 }} angle={-30} textAnchor="end" height={50} />
                      <YAxis tick={{ fontSize: 12 }} />
                      <Tooltip />
                      <Bar dataKey="count" fill={COLORS[Object.keys(data.distributions).indexOf(key) % COLORS.length]} radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </ChartCard>
              );
            })}
          </div>
        </TabsContent>

        {/* Correlations & Risk Tab */}
        <TabsContent value="correlations">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <ChartCard title="Feature Correlations with Urgency">
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={correlationData} layout="vertical">
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                  <XAxis type="number" tick={{ fontSize: 12 }} domain={[-0.4, 0.4]} />
                  <YAxis dataKey="name" type="category" tick={{ fontSize: 11 }} width={120} />
                  <Tooltip formatter={(val: number) => val.toFixed(4)} />
                  <Bar dataKey="value" name="Correlation" radius={[0, 4, 4, 0]}>
                    {correlationData.map((entry, i) => (
                      <Cell key={i} fill={entry.value >= 0 ? "hsl(0, 72%, 55%)" : "hsl(199, 89%, 36%)"} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </ChartCard>

            <ChartCard title="Comorbidity Impact on Urgency Rate (%)">
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={comorbidityData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                  <XAxis dataKey="name" tick={{ fontSize: 11 }} />
                  <YAxis tick={{ fontSize: 12 }} />
                  <Tooltip formatter={(val: number) => `${val}%`} />
                  <Legend />
                  <Bar dataKey="Without" fill={URGENCY_COLORS[0]} radius={[4, 4, 0, 0]} />
                  <Bar dataKey="With" fill={URGENCY_COLORS[1]} radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </ChartCard>

            <ChartCard title="Risk Segments (by # Risk Factors)">
              <ResponsiveContainer width="100%" height={260}>
                <BarChart data={data.risk_segments.map(d => ({ ...d, label: `${d.risk_factor_count} factors`, rate: +(d.urgency_rate * 100).toFixed(1) }))}>
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                  <XAxis dataKey="label" tick={{ fontSize: 12 }} />
                  <YAxis tick={{ fontSize: 12 }} />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="total" name="Total" fill={URGENCY_COLORS[0]} radius={[4, 4, 0, 0]} opacity={0.5} />
                  <Bar dataKey="urgent" name="Urgent" fill={URGENCY_COLORS[1]} radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </ChartCard>

            <ChartCard title="Age × Chest Pain Urgency Heatmap">
              <div className="overflow-x-auto">
                <table className="w-full text-xs">
                  <thead>
                    <tr>
                      <th className="p-2 text-left text-muted-foreground">Age \ Chest Pain</th>
                      {chestPainTypes.map(cp => (
                        <th key={cp} className="p-2 text-center text-muted-foreground">
                          {cp}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {ageGroups.map(ag => (
                      <tr key={ag}>
                        <td className="p-2 font-medium">{ag}</td>
                        {chestPainTypes.map(cp => {
                          const cell = data.age_chest_pain_heatmap.find(d => d.age_group === ag && d.chest_pain === cp);
                          const rate = cell?.urgency_rate ?? 0;
                          const intensity = Math.min(rate, 1);
                          return (
                            <td
                              key={cp}
                              className="p-2 text-center rounded"
                              style={{
                                backgroundColor: `hsla(0, 72%, 55%, ${intensity * 0.8})`,
                                color: intensity > 0.4 ? "white" : "inherit"
                              }}
                            >
                              {(rate * 100).toFixed(0)}%
                            </td>
                          );
                        })}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </ChartCard>
          </div>
        </TabsContent>
      </Tabs>
    </PageLayout>
  );
};

export default Analytics;
