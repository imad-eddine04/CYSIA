import React from "react";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  ScatterChart, Scatter, Cell, ReferenceLine,
} from "recharts";
import type { LoanRecord } from "@/lib/dataUtils";
import { computeHistogram, computeCorrelationMatrix, computeScatterData } from "@/lib/dataUtils";

interface ChartsProps {
  data: LoanRecord[];
}

const CustomTooltip = ({ active, payload, label }: { active?: boolean; payload?: { value: number }[]; label?: string }) => {
  if (active && payload?.length) {
    return (
      <div className="glass-card p-3 text-sm">
        <p style={{ color: "hsl(var(--primary))" }} className="font-semibold">{label}</p>
        <p style={{ color: "hsl(var(--foreground))" }}>Count: {payload[0]?.value}</p>
      </div>
    );
  }
  return null;
};

const HistogramCard: React.FC<{ data: LoanRecord[]; column: string; label: string; color: string }> = ({
  data, column, label, color,
}) => {
  const histData = computeHistogram(data, column, 18);
  return (
    <div className="glass-card p-5">
      <h3 className="section-title mb-4">
        <span style={{ color }}>{`▐`}</span>
        {label}
      </h3>
      <ResponsiveContainer width="100%" height={220}>
        <BarChart data={histData} margin={{ top: 0, right: 10, left: -10, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="hsl(220,25%,18%)" vertical={false} />
          <XAxis
            dataKey="bin"
            tick={{ fill: "hsl(215,20%,55%)", fontSize: 11 }}
            axisLine={{ stroke: "hsl(220,25%,18%)" }}
            tickLine={false}
            interval="preserveStartEnd"
          />
          <YAxis
            tick={{ fill: "hsl(215,20%,55%)", fontSize: 11 }}
            axisLine={false}
            tickLine={false}
          />
          <Tooltip content={<CustomTooltip />} />
          <Bar dataKey="count" fill={color} radius={[3, 3, 0, 0]} opacity={0.9} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

const CorrelationMatrix: React.FC<{ data: LoanRecord[] }> = ({ data }) => {
  const numCols = ["credit_score", "annual_income", "loan_amount", "employment_duration", "Age", "Children_Count", "Previous_Loan_Count", "default"];
  const matrix = computeCorrelationMatrix(data, numCols);

  const getColor = (val: number) => {
    if (val > 0.6) return "hsl(43, 85%, 45%)";
    if (val > 0.3) return "hsl(43, 70%, 35%)";
    if (val > 0) return "hsl(220, 40%, 20%)";
    if (val > -0.3) return "hsl(210, 40%, 18%)";
    if (val > -0.6) return "hsl(200, 60%, 25%)";
    return "hsl(210, 80%, 35%)";
  };

  const textColor = (val: number) => {
    const abs = Math.abs(val);
    return abs > 0.3 ? "hsl(var(--foreground))" : "hsl(var(--muted-foreground))";
  };

  const shortName = (col: string) =>
    col.replace("_score", "_sc").replace("annual_", "ann_").replace("loan_", "").replace("employment_", "emp_");

  return (
    <div className="glass-card p-5">
      <h3 className="section-title mb-4">
        <span style={{ color: "hsl(var(--primary))" }}>◈</span>
        Correlation Matrix
      </h3>
      <div className="overflow-x-auto">
        <table className="w-full" style={{ borderCollapse: "separate", borderSpacing: "2px" }}>
          <thead>
            <tr>
              <td className="p-1" />
              {matrix.map((col) => (
                <td key={col.column} className="p-1 text-center" style={{ fontSize: "0.65rem", color: "hsl(var(--primary))", fontWeight: 600, minWidth: "60px" }}>
                  {shortName(col.column)}
                </td>
              ))}
            </tr>
          </thead>
          <tbody>
            {matrix.map((row) => (
              <tr key={row.column}>
                <td className="p-1 text-right pr-2" style={{ fontSize: "0.65rem", color: "hsl(var(--primary))", fontWeight: 600, whiteSpace: "nowrap" }}>
                  {shortName(row.column)}
                </td>
                {matrix.map((col) => {
                  const val = row.correlations[col.column] ?? 0;
                  return (
                    <td
                      key={col.column}
                      className="p-1 text-center rounded"
                      style={{
                        background: getColor(val),
                        fontSize: "0.7rem",
                        fontWeight: 600,
                        color: textColor(val),
                        minWidth: "60px",
                        height: "36px",
                      }}
                    >
                      {val.toFixed(2)}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="flex items-center gap-4 mt-4 text-xs" style={{ color: "hsl(var(--muted-foreground))" }}>
        <div className="flex items-center gap-1.5">
          <div className="w-8 h-3 rounded" style={{ background: "hsl(43, 85%, 45%)" }} />
          Strong Positive
        </div>
        <div className="flex items-center gap-1.5">
          <div className="w-8 h-3 rounded" style={{ background: "hsl(220, 40%, 20%)" }} />
          Weak
        </div>
        <div className="flex items-center gap-1.5">
          <div className="w-8 h-3 rounded" style={{ background: "hsl(210, 80%, 35%)" }} />
          Strong Negative
        </div>
      </div>
    </div>
  );
};

const ScatterPlot: React.FC<{ data: LoanRecord[] }> = ({ data }) => {
  const points = computeScatterData(data, "annual_income", "loan_amount", "default");
  const sample = points.filter((_, i) => i % 3 === 0).slice(0, 300);

  return (
    <div className="glass-card p-5">
      <h3 className="section-title mb-4">
        <span style={{ color: "hsl(210, 80%, 55%)" }}>⊕</span>
        Scatter Plot: Annual Income vs Loan Amount
      </h3>
      <ResponsiveContainer width="100%" height={280}>
        <ScatterChart margin={{ top: 10, right: 20, bottom: 20, left: 10 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="hsl(220,25%,18%)" />
          <XAxis
            type="number"
            dataKey="x"
            name="Annual Income"
            tick={{ fill: "hsl(215,20%,55%)", fontSize: 11 }}
            axisLine={{ stroke: "hsl(220,25%,18%)" }}
            tickLine={false}
            tickFormatter={(v) => `${(v / 1000).toFixed(0)}k`}
            label={{ value: "Annual Income", position: "insideBottom", offset: -10, fill: "hsl(215,20%,55%)", fontSize: 11 }}
          />
          <YAxis
            type="number"
            dataKey="y"
            name="Loan Amount"
            tick={{ fill: "hsl(215,20%,55%)", fontSize: 11 }}
            axisLine={false}
            tickLine={false}
            tickFormatter={(v) => `${(v / 1000).toFixed(0)}k`}
            label={{ value: "Loan Amount", angle: -90, position: "insideLeft", offset: 15, fill: "hsl(215,20%,55%)", fontSize: 11 }}
          />
          <Tooltip
            cursor={{ strokeDasharray: "3 3" }}
            content={({ active, payload }) => {
              if (active && payload?.length) {
                const d = payload[0]?.payload;
                return (
                  <div className="glass-card p-3 text-xs">
                    <p style={{ color: d?.color === 1 ? "hsl(0,72%,65%)" : "hsl(145,65%,55%)" }}>
                      {d?.color === 1 ? "⚠ Default" : "✓ No Default"}
                    </p>
                    <p style={{ color: "hsl(var(--foreground))" }}>Income: {Number(d?.x).toLocaleString()}</p>
                    <p style={{ color: "hsl(var(--foreground))" }}>Loan: {Number(d?.y).toLocaleString()}</p>
                  </div>
                );
              }
              return null;
            }}
          />
          <Scatter data={sample} fill="hsl(var(--primary))">
            {sample.map((entry, i) => (
              <Cell
                key={i}
                fill={entry.color === 1 ? "hsl(0,72%,55%)" : "hsl(145,65%,42%)"}
                opacity={0.7}
              />
            ))}
          </Scatter>
        </ScatterChart>
      </ResponsiveContainer>
      <div className="flex items-center gap-4 mt-2 text-xs justify-end" style={{ color: "hsl(var(--muted-foreground))" }}>
        <div className="flex items-center gap-1.5">
          <div className="w-3 h-3 rounded-full" style={{ background: "hsl(145,65%,42%)" }} />
          No Default
        </div>
        <div className="flex items-center gap-1.5">
          <div className="w-3 h-3 rounded-full" style={{ background: "hsl(0,72%,55%)" }} />
          Default
        </div>
      </div>
    </div>
  );
};

export const Charts: React.FC<ChartsProps> = ({ data }) => {
  return (
    <div className="space-y-5 animate-fade-in-up">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <HistogramCard
          data={data}
          column="credit_score"
          label="Credit Score Distribution"
          color="hsl(43, 85%, 55%)"
        />
        <HistogramCard
          data={data}
          column="loan_amount"
          label="Loan Amount Distribution"
          color="hsl(210, 80%, 55%)"
        />
        <HistogramCard
          data={data}
          column="annual_income"
          label="Annual Income Distribution"
          color="hsl(145, 65%, 42%)"
        />
      </div>
      <CorrelationMatrix data={data} />
      <ScatterPlot data={data} />
    </div>
  );
};
