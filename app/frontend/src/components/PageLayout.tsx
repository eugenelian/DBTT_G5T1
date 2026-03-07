import { ReactNode } from "react";

interface PageLayoutProps {
  title: string;
  subtitle?: string;
  children: ReactNode;
  actions?: ReactNode;
}

const PageLayout = ({ title, subtitle, children, actions }: PageLayoutProps) => (
  <div className="flex-1 overflow-auto">
    <header className="sticky top-0 z-10 bg-background/80 backdrop-blur-md border-b border-border px-8 py-5">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="font-display text-2xl font-bold text-foreground">{title}</h1>
          {subtitle && <p className="text-sm text-muted-foreground mt-0.5">{subtitle}</p>}
        </div>
        {actions && <div className="flex items-center gap-3">{actions}</div>}
      </div>
    </header>
    <main className="p-8">{children}</main>
  </div>
);

export default PageLayout;
