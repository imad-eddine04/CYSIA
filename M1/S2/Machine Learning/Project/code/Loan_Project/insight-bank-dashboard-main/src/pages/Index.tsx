import React, { useState, useCallback, useRef } from "react";
import {
  Upload, BarChart3, Activity, Brain, AlertTriangle, Table2,
  ChevronRight, TrendingUp, Shield, Building2, Menu, X, DollarSign, Calculator,
} from "lucide-react";
import bankHeroBg from "@/assets/bank-hero-bg.jpg";
import { DataUpload } from "@/components/DataUpload";
import { DataPreview } from "@/components/DataPreview";
import { Charts } from "@/components/Charts";
import { MissingValues } from "@/components/MissingValues";
import { ModelTester } from "@/components/ModelTester";
import { MLVisualizations } from "@/components/MLVisualizations";
import { MLMetrics } from "@/components/MLMetrics";
import type { LoanRecord } from "@/lib/dataUtils";
import { getDatasetInfo, getMissingValues, cleanDataset } from "@/lib/dataUtils";

type Section =
  | "upload"
  | "preview"
  | "charts"
  | "missing"
  | "model-tester"
  | "pca-svm"
  | "metrics";

const navItems: { id: Section; label: string; icon: React.ReactNode; requiresData?: boolean }[] = [
  { id: "upload", label: "Upload Dataset", icon: <Upload className="w-4 h-4" /> },
  { id: "preview", label: "Data Preview", icon: <Table2 className="w-4 h-4" />, requiresData: true },
  { id: "charts", label: "Visualizations", icon: <BarChart3 className="w-4 h-4" />, requiresData: true },
  { id: "missing", label: "Missing Values", icon: <AlertTriangle className="w-4 h-4" />, requiresData: true },
  { id: "model-tester", label: "Model Tester", icon: <Calculator className="w-4 h-4" />, requiresData: true },
  { id: "pca-svm", label: "PCA & SVM", icon: <Brain className="w-4 h-4" />, requiresData: true },
  { id: "metrics", label: "ML Metrics", icon: <Activity className="w-4 h-4" />, requiresData: true },
];

const sectionTitles: Record<Section, { title: string; sub: string }> = {
  upload: { title: "Upload Dataset", sub: "Load your loan CSV file to begin analysis" },
  preview: { title: "Data Preview", sub: "First 10 rows and dataset shape" },
  charts: { title: "Visualizations", sub: "Histograms, Correlation Matrix & Scatter Plot" },
  missing: { title: "Missing Values", sub: "Detect and clean missing data" },
  "model-tester": { title: "Model Prediction Tester", sub: "Test loan default prediction with ML models" },
  "pca-svm": { title: "PCA & SVM Visualization", sub: "Dimensionality reduction and decision boundary" },
  metrics: { title: "ML Performance Metrics", sub: "Confusion Matrix, Accuracy, Precision, Recall, F1-Score" },
};

export default function Index() {
  const [data, setData] = useState<LoanRecord[]>([]);
  const [cleanedData, setCleanedData] = useState<LoanRecord[] | null>(null);
  const [filename, setFilename] = useState<string>("");
  const [activeSection, setActiveSection] = useState<Section>("upload");
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isCleaned, setIsCleaned] = useState(false);

  const activeData = cleanedData ?? data;
  const info = getDatasetInfo(activeData);
  const missingInfo = getMissingValues(activeData);

  const handleDataLoaded = useCallback((loaded: LoanRecord[], name: string) => {
    setData(loaded);
    setCleanedData(null);
    setIsCleaned(false);
    setFilename(name);
    setActiveSection("preview");
  }, []);

  const handleClean = useCallback(() => {
    const cleaned = cleanDataset(activeData);
    setCleanedData(cleaned);
    setIsCleaned(true);
  }, [activeData]);

  const navigate = (section: Section) => {
    setActiveSection(section);
    setIsMobileMenuOpen(false);
  };

  const hasData = data.length > 0;
  const { title, sub } = sectionTitles[activeSection];

  return (
    <div className="min-h-screen flex" style={{ background: "hsl(var(--background))" }}>
      {/* Sidebar */}
      <aside
        className={`fixed inset-y-0 left-0 z-40 w-64 flex-shrink-0 flex flex-col transition-transform duration-300 ${
          isMobileMenuOpen ? "translate-x-0" : "-translate-x-full"
        } lg:relative lg:translate-x-0`}
        style={{ background: "hsl(var(--sidebar-background))", borderRight: "1px solid hsl(var(--sidebar-border))" }}
      >
        {/* Logo */}
        <div className="px-5 py-5 border-b" style={{ borderColor: "hsl(var(--sidebar-border))" }}>
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-lg flex items-center justify-center gap-1"
              style={{ background: "hsl(43,50%,15%)", border: "1px solid hsl(var(--border-gold))" }}>
              <Building2 className="w-4 h-4" style={{ color: "hsl(var(--primary))" }} />
              <DollarSign className="w-4 h-4" style={{ color: "hsl(145, 65%, 55%)" }} />
            </div>
            <div>
              <p className="font-display font-bold text-sm" style={{ color: "hsl(var(--foreground))" }}>
                LoanAnalytics
              </p>
              <p className="text-xs" style={{ color: "hsl(var(--muted-foreground))" }}>
                ML Risk Platform
              </p>
            </div>
          </div>
        </div>

        {/* Nav */}
        <nav className="flex-1 p-3 space-y-1 overflow-y-auto">
          <p className="text-xs font-semibold uppercase tracking-widest px-3 pt-2 pb-1"
            style={{ color: "hsl(var(--muted-foreground))" }}>
            Analysis Pipeline
          </p>
          {navItems.map((item, i) => {
            const disabled = item.requiresData && !hasData;
            const active = activeSection === item.id;
            return (
              <button
                key={item.id}
                onClick={() => !disabled && navigate(item.id)}
                disabled={disabled}
                className={`nav-item w-full text-left ${active ? "active" : ""} ${disabled ? "opacity-40 cursor-not-allowed" : ""}`}
              >
                <span className="flex items-center gap-2.5 w-full">
                  <span className={`flex-shrink-0 ${active ? "text-primary" : ""}`} style={active ? { color: "hsl(var(--primary))" } : {}}>
                    {item.icon}
                  </span>
                  <span className="flex-1">{item.label}</span>
                  {i > 0 && hasData && (
                    <ChevronRight className="w-3 h-3 opacity-50" />
                  )}
                </span>
              </button>
            );
          })}
        </nav>

        {/* Dataset info */}
        {hasData && (
          <div className="m-3 p-3 rounded-lg" style={{ background: "hsl(43,40%,10%)", border: "1px solid hsl(var(--border-gold))" }}>
            <div className="flex items-center gap-2 mb-2">
              <div className="w-1.5 h-1.5 rounded-full animate-pulse" style={{ background: "hsl(145,65%,42%)" }} />
              <p className="text-xs font-semibold" style={{ color: "hsl(var(--primary))" }}>Dataset Loaded</p>
            </div>
            <p className="text-xs truncate" style={{ color: "hsl(var(--muted-foreground))" }}>{filename}</p>
            <p className="text-xs mt-1" style={{ color: "hsl(var(--foreground))" }}>
              {info.rows.toLocaleString()} rows × {info.cols} cols
            </p>
            {isCleaned && (
              <p className="text-xs mt-1" style={{ color: "hsl(145,65%,55%)" }}>
                ✓ Data cleaned
              </p>
            )}
          </div>
        )}

        {/* Footer */}
        <div className="p-4 border-t" style={{ borderColor: "hsl(var(--sidebar-border))" }}>
          <div className="flex items-center gap-2">
            <Shield className="w-3.5 h-3.5" style={{ color: "hsl(var(--muted-foreground))" }} />
            <p className="text-xs" style={{ color: "hsl(var(--muted-foreground))" }}>
              Bank-grade Security
            </p>
          </div>
        </div>
      </aside>

      {/* Mobile overlay */}
      {isMobileMenuOpen && (
        <div
          className="fixed inset-0 z-30 bg-black/60 lg:hidden"
          onClick={() => setIsMobileMenuOpen(false)}
        />
      )}

      {/* Main content */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Header */}
        <header
          className="sticky top-0 z-20 px-5 lg:px-8 py-4 flex items-center justify-between"
          style={{
            background: "hsl(var(--card))",
            borderBottom: "1px solid hsl(var(--border))",
            backdropFilter: "blur(12px)",
          }}
        >
          <div className="flex items-center gap-4">
            <button
              className="lg:hidden p-2 rounded-lg"
              style={{ background: "hsl(var(--muted))" }}
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            >
              {isMobileMenuOpen ? <X className="w-4 h-4" /> : <Menu className="w-4 h-4" />}
            </button>
            <div>
              <h1 className="font-display font-bold text-lg leading-tight" style={{ color: "hsl(var(--foreground))" }}>
                {title}
              </h1>
              <p className="text-xs" style={{ color: "hsl(var(--muted-foreground))" }}>
                {sub}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            {/* Steps indicator */}
            <div className="hidden md:flex items-center gap-1">
              {navItems.map((item, i) => (
                <button
                  key={item.id}
                  onClick={() => !(item.requiresData && !hasData) && navigate(item.id)}
                  disabled={item.requiresData && !hasData}
                  className="w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold transition-all"
                  style={{
                    background: activeSection === item.id
                      ? "hsl(var(--primary))"
                      : item.requiresData && !hasData
                      ? "hsl(var(--muted))"
                      : "hsl(var(--secondary))",
                    color: activeSection === item.id
                      ? "hsl(var(--primary-foreground))"
                      : "hsl(var(--muted-foreground))",
                  }}
                  title={item.label}
                >
                  {i + 1}
                </button>
              ))}
            </div>

            <div className="flex items-center gap-2 px-3 py-1.5 rounded-full text-xs"
              style={{ background: "hsl(43,50%,10%)", border: "1px solid hsl(var(--border-gold))", color: "hsl(var(--primary))" }}>
              <TrendingUp className="w-3 h-3" />
              Loan Risk Analytics
            </div>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 p-5 lg:p-8 overflow-auto">
          {/* Hero banner — only on upload */}
          {activeSection === "upload" && (
            <div
              className="rounded-xl overflow-hidden mb-6 relative"
              style={{ minHeight: "180px" }}
            >
              <img
                src={bankHeroBg}
                alt="Bank Analytics"
                className="absolute inset-0 w-full h-full object-cover"
              />
              <div className="absolute inset-0"
                style={{ background: "linear-gradient(135deg, hsl(222,47%,6%,0.85) 0%, hsl(222,47%,6%,0.5) 100%)" }} />
              <div className="relative z-10 p-8">
                <div className="flex items-center gap-2 mb-3">
                  <span className="metric-badge tag-gold text-xs">
                    <Shield className="w-3 h-3 mr-1" />
                    Enterprise ML Platform
                  </span>
                </div>
                <h2 className="font-display font-bold text-3xl mb-2" style={{ color: "hsl(var(--foreground))" }}>
                  Loan Default Risk{" "}
                  <span className="gold-text">Prediction System</span>
                </h2>
                <p className="text-sm max-w-xl" style={{ color: "hsl(210,30%,75%)" }}>
                  Upload your loan dataset to perform comprehensive data analysis, visualizations,
                  dimensionality reduction (PCA), SVM classification, and ML performance evaluation.
                </p>
              </div>
            </div>
          )}

          {/* Sections */}
          <div key={activeSection} className="animate-fade-in-up">
            {activeSection === "upload" && (
              <DataUpload onDataLoaded={handleDataLoaded} />
            )}
            {activeSection === "preview" && hasData && (
              <DataPreview data={activeData} rows={info.rows} cols={info.cols} />
            )}
            {activeSection === "charts" && hasData && (
              <Charts data={activeData} />
            )}
            {activeSection === "missing" && hasData && (
              <MissingValues
                missingInfo={missingInfo}
                onClean={handleClean}
                isCleaned={isCleaned}
              />
            )}
            {activeSection === "model-tester" && hasData && (
              <ModelTester data={activeData} />
            )}
            {activeSection === "pca-svm" && hasData && (
              <MLVisualizations data={activeData} />
            )}
            {activeSection === "metrics" && hasData && (
              <MLMetrics data={activeData} />
            )}
          </div>

          {/* Navigation footer */}
          {hasData && activeSection !== "upload" && (
            <div className="mt-8 flex items-center justify-between pt-5"
              style={{ borderTop: "1px solid hsl(var(--border))" }}>
              <button
                className="btn-outline-gold"
                onClick={() => {
                  const idx = navItems.findIndex((n) => n.id === activeSection);
                  if (idx > 0) navigate(navItems[idx - 1].id);
                }}
                disabled={navItems.findIndex((n) => n.id === activeSection) === 0}
                style={{ opacity: navItems.findIndex((n) => n.id === activeSection) === 0 ? 0 : 1 }}
              >
                ← Previous
              </button>
              <div className="flex items-center gap-1.5">
                {navItems.map((item) => (
                  <div
                    key={item.id}
                    className="w-2 h-2 rounded-full transition-all"
                    style={{
                      background: activeSection === item.id
                        ? "hsl(var(--primary))"
                        : "hsl(var(--border))",
                      transform: activeSection === item.id ? "scale(1.3)" : "scale(1)",
                    }}
                  />
                ))}
              </div>
              <button
                className="btn-gold"
                onClick={() => {
                  const idx = navItems.findIndex((n) => n.id === activeSection);
                  if (idx < navItems.length - 1) navigate(navItems[idx + 1].id);
                }}
                disabled={navItems.findIndex((n) => n.id === activeSection) === navItems.length - 1}
                style={{ opacity: navItems.findIndex((n) => n.id === activeSection) === navItems.length - 1 ? 0 : 1 }}
              >
                Next →
              </button>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
