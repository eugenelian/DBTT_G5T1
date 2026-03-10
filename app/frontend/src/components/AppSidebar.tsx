import { NavLink, useLocation } from "react-router-dom";
import { Users, BarChart3, MessageSquare, Stethoscope, Activity } from "lucide-react";

const navItems = [
  { to: "/", icon: Users, label: "Patient Queue" },
  { to: "/analytics", icon: BarChart3, label: "Analytics" },
  { to: "/chatbot", icon: MessageSquare, label: "AI Chatbot" },
  { to: "/diagnosis", icon: Stethoscope, label: "Automated Diagnosis" },
  { to: "/triage", icon: Activity, label: "Automated Triage" }
];

const AppSidebar = () => {
  const location = useLocation();

  return (
    <aside className="w-64 min-h-screen bg-sidebar flex flex-col border-r border-sidebar-border">
      <div className="p-6">
        <h1 className="font-display text-xl font-bold text-sidebar-primary-foreground tracking-tight">
          <span className="text-sidebar-primary">Med</span>Dashboard
        </h1>
        <p className="text-xs text-sidebar-foreground/60 mt-1">Patient Intelligence Platform</p>
      </div>
      <nav className="flex-1 px-3 space-y-1">
        {navItems.map(({ to, icon: Icon, label }) => {
          const isActive = location.pathname === to;
          return (
            <NavLink
              key={to}
              to={to}
              className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                isActive ? "bg-sidebar-accent text-sidebar-primary" : "text-sidebar-foreground/70 hover:text-sidebar-foreground hover:bg-sidebar-accent/50"
              }`}
            >
              <Icon size={18} />
              {label}
            </NavLink>
          );
        })}
      </nav>
      {/* <div className="p-4 mx-3 mb-4 rounded-lg bg-sidebar-accent/50">
        <p className="text-xs text-sidebar-foreground/60">Logged in as</p>
        <p className="text-sm font-medium text-sidebar-foreground">Dr. Sarah Chen</p>
      </div> */}
    </aside>
  );
};

export default AppSidebar;
