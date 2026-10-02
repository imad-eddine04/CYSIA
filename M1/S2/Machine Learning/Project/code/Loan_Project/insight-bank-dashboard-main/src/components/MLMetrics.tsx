import React from "react";
import { Target, BarChart2, TrendingUp, Activity, Award } from "lucide-react";
import type { LoanRecord } from "@/lib/dataUtils";
import { computeMLMetrics } from "@/lib/dataUtils";

interface MLMetricsProps {
  data: LoanRecord[];
}

const MetricCard: React.FC<{
  label: string;
  value: number;
  icon: React.ReactNode;
  color: string;
  description: string;
}> = ({ label, value, icon, color, description }) => {
  const pct = Math.round(value * 100);
  return (
    <div className="stat-card flex-1 min-w-[160px]">
      <div className="flex items-start justify-between mb-3">
        <div className="w-9 h-9 rounded-lg flex items-center justify-center"
          style={{ background: `${color}20` }}>
          <div style={{ color }}>{icon}</div>
        </div>
        <span
          className="metric-badge text-xs"
          style={{ background: `${color}20`, color }}
        >
          {pct}%
        </span>
      </div>
      <p className="text-2xl font-display font-bold" style={{ color }}>
        {(value * 100).toFixed(2)}%
      </p>
      <p className="text-sm font-semibold mt-0.5" style={{ color: "hsl(var(--foreground))" }}>
        {label}
      </p>
      <p className="text-xs mt-1" style={{ color: "hsl(var(--muted-foreground))" }}>
        {description}
      </p>
      <div className="progress-bar-gold mt-3">
        <div
          className="progress-bar-gold-fill"
          style={{ width: `${pct}%`, background: `linear-gradient(90deg, ${color}99, ${color})` }}
        />
      </div>
    </div>
  );
};

export const MLMetrics: React.FC<MLMetricsProps> = ({ data }) => {
  const metrics = computeMLMetrics(data);
  const { accuracy, precision, recall, f1, confusionMatrix, classReport } = metrics;

  const cmLabels = ["Predicted: No Default", "Predicted: Default"];
  const cmRowLabels = ["Actual: No Default", "Actual: Default"];

  return (
    <div className="space-y-5 animate-fade-in-up">
      {/* Metric Cards */}
      <div className="flex gap-4 flex-wrap">
        <MetricCard
          label="Accuracy"
          value={accuracy}
          icon={<Award className="w-4 h-4" />}
          color="hsl(43,85%,55%)"
          description="Overall correct predictions"
        />
        <MetricCard
          label="Precision"
          value={precision}
          icon={<Target className="w-4 h-4" />}
          color="hsl(210,80%,55%)"
          description="True positives / predicted positives"
        />
        <MetricCard
          label="Recall"
          value={recall}
          icon={<TrendingUp className="w-4 h-4" />}
          color="hsl(145,65%,42%)"
          description="True positives / actual positives"
        />
        <MetricCard
          label="F1-Score"
          value={f1}
          icon={<Activity className="w-4 h-4" />}
          color="hsl(280,65%,65%)"
          description="Harmonic mean of precision & recall"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        {/* Confusion Matrix */}
        <div className="glass-card p-5">
          <h3 className="section-title mb-5">
            <BarChart2 className="w-4 h-4" style={{ color: "hsl(var(--primary))" }} />
            Confusion Matrix
          </h3>
          <div className="overflow-x-auto">
            <table className="w-full" style={{ borderCollapse: "separate", borderSpacing: "4px" }}>
              <thead>
                <tr>
                  <td />
                  {cmLabels.map((l) => (
                    <th key={l} className="text-center text-xs font-semibold pb-2"
                      style={{ color: "hsl(var(--primary))", fontSize: "0.7rem" }}>
                      {l}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {confusionMatrix.map((row, ri) => (
                  <tr key={ri}>
                    <td className="text-xs font-semibold pr-3" style={{ color: "hsl(var(--muted-foreground))", fontSize: "0.7rem", whiteSpace: "nowrap" }}>
                      {cmRowLabels[ri]}
                    </td>
                    {row.map((val, ci) => {
                      const isDiag = ri === ci;
                      return (
                        <td key={ci} className="text-center rounded-lg"
                          style={{
                            background: isDiag ? "hsl(43,50%,14%)" : "hsl(220,30%,12%)",
                            border: `1px solid ${isDiag ? "hsl(43,60%,30%)" : "hsl(220,25%,18%)"}`,
                            padding: "1rem",
                            minWidth: "100px",
                          }}>
                          <div className="text-2xl font-display font-bold"
                            style={{ color: isDiag ? "hsl(43,85%,55%)" : "hsl(0,72%,60%)" }}>
                            {val.toLocaleString()}
                          </div>
                          <div className="text-xs mt-1"
                            style={{ color: "hsl(var(--muted-foreground))" }}>
                            {isDiag ? (ri === 0 ? "True Neg." : "True Pos.") : (ri === 0 ? "False Pos." : "False Neg.")}
                          </div>
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Classification Report */}
        <div className="glass-card p-5">
          <h3 className="section-title mb-5">
            <Activity className="w-4 h-4" style={{ color: "hsl(var(--primary))" }} />
            Classification Report
          </h3>
          <div className="overflow-x-auto">
            <table className="data-table w-full">
              <thead>
                <tr>
                  <th className="text-left">Class</th>
                  <th className="text-center">Precision</th>
                  <th className="text-center">Recall</th>
                  <th className="text-center">F1-Score</th>
                  <th className="text-center">Support</th>
                </tr>
              </thead>
              <tbody>
                {classReport.map((row) => (
                  <tr key={row.class}>
                    <td className="font-medium">{row.class}</td>
                    <td className="text-center">
                      <span className="font-mono font-semibold" style={{ color: "hsl(210,80%,65%)" }}>
                        {(row.precision * 100).toFixed(1)}%
                      </span>
                    </td>
                    <td className="text-center">
                      <span className="font-mono font-semibold" style={{ color: "hsl(145,65%,55%)" }}>
                        {(row.recall * 100).toFixed(1)}%
                      </span>
                    </td>
                    <td className="text-center">
                      <span className="font-mono font-semibold" style={{ color: "hsl(280,65%,70%)" }}>
                        {(((2 * row.precision * row.recall) / (row.precision + row.recall || 1)) * 100).toFixed(1)}%
                      </span>
                    </td>
                    <td className="text-center">
                      <span className="font-mono" style={{ color: "hsl(var(--muted-foreground))" }}>
                        {row.support.toLocaleString()}
                      </span>
                    </td>
                  </tr>
                ))}
                <tr style={{ borderTop: "1px solid hsl(var(--border-gold))" }}>
                  <td className="font-semibold" style={{ color: "hsl(var(--primary))" }}>Weighted Avg.</td>
                  <td className="text-center font-mono font-bold" style={{ color: "hsl(var(--primary))" }}>
                    {(precision * 100).toFixed(1)}%
                  </td>
                  <td className="text-center font-mono font-bold" style={{ color: "hsl(var(--primary))" }}>
                    {(recall * 100).toFixed(1)}%
                  </td>
                  <td className="text-center font-mono font-bold" style={{ color: "hsl(var(--primary))" }}>
                    {(f1 * 100).toFixed(1)}%
                  </td>
                  <td className="text-center font-mono" style={{ color: "hsl(var(--muted-foreground))" }}>
                    {data.length.toLocaleString()}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <div className="mt-4 p-3 rounded-lg text-xs"
            style={{ background: "hsl(43,50%,8%)", border: "1px solid hsl(var(--border-gold))", color: "hsl(var(--muted-foreground))" }}>
            <p className="font-semibold mb-1" style={{ color: "hsl(var(--primary))" }}>Model Note:</p>
            Metrics computed using a threshold-based SVM proxy classifier on credit score (threshold = 650).
            For production accuracy, run the full SVM pipeline from <code className="font-mono">Loan_Prediction.py</code>.
          </div>
        </div>
      </div>
    </div>
  );
};
