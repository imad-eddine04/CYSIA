import React from "react";
import { Database, Grid3X3 } from "lucide-react";
import type { LoanRecord } from "@/lib/dataUtils";

interface DataPreviewProps {
  data: LoanRecord[];
  rows: number;
  cols: number;
}

export const DataPreview: React.FC<DataPreviewProps> = ({ data, rows, cols }) => {
  const preview = data; // Show all data instead of first 10
  const columns = data.length ? Object.keys(data[0]) : [];

  return (
    <div className="space-y-4 animate-fade-in-up">
      {/* Shape Info */}
      <div className="flex gap-3 flex-wrap">
        <div className="stat-card flex items-center gap-3 flex-1 min-w-[160px]">
          <div className="w-10 h-10 rounded-lg flex items-center justify-center"
            style={{ background: "hsl(43, 50%, 12%)" }}>
            <Database className="w-5 h-5" style={{ color: "hsl(var(--primary))" }} />
          </div>
          <div>
            <p className="text-xs font-medium" style={{ color: "hsl(var(--muted-foreground))" }}>
              TOTAL ROWS
            </p>
            <p className="text-2xl font-display font-bold" style={{ color: "hsl(var(--primary))" }}>
              {rows.toLocaleString()}
            </p>
          </div>
        </div>
        <div className="stat-card flex items-center gap-3 flex-1 min-w-[160px]">
          <div className="w-10 h-10 rounded-lg flex items-center justify-center"
            style={{ background: "hsl(210, 50%, 12%)" }}>
            <Grid3X3 className="w-5 h-5" style={{ color: "hsl(var(--accent))" }} />
          </div>
          <div>
            <p className="text-xs font-medium" style={{ color: "hsl(var(--muted-foreground))" }}>
              FEATURES
            </p>
            <p className="text-2xl font-display font-bold" style={{ color: "hsl(var(--accent))" }}>
              {cols}
            </p>
          </div>
        </div>
        <div className="stat-card flex-1 min-w-[200px]">
          <p className="text-xs font-medium mb-2" style={{ color: "hsl(var(--muted-foreground))" }}>
            DATASET SHAPE
          </p>
          <p className="font-display font-bold text-lg" style={{ color: "hsl(var(--foreground))" }}>
            ({rows.toLocaleString()} × {cols})
          </p>
          <p className="text-xs mt-0.5" style={{ color: "hsl(var(--muted-foreground))" }}>
            rows × columns
          </p>
        </div>
      </div>

      {/* Complete dataset view */}
      <div className="glass-card overflow-hidden">
        <div className="px-5 py-3 border-b flex items-center justify-between"
          style={{ borderColor: "hsl(var(--border))" }}>
          <h3 className="section-title text-sm">
            <span style={{ color: "hsl(var(--primary))" }}>◆</span>
            Complete Dataset View
          </h3>
          <span className="metric-badge tag-default">
            {preview.length} rows total
          </span>
        </div>
        <div className="overflow-auto" style={{ maxHeight: "600px" }}>
          <table className="data-table w-full">
            <thead className="sticky top-0 z-10" style={{ background: "hsl(var(--card))" }}>
              <tr>
                <th className="text-left w-10">#</th>
                {columns.map((col) => (
                  <th key={col} className="text-left">{col}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {preview.map((row, i) => (
                <tr key={i}>
                  <td style={{ color: "hsl(var(--muted-foreground))", fontSize: "0.75rem" }}>
                    {i + 1}
                  </td>
                  {columns.map((col) => (
                    <td key={col}>
                      {row[col] === null || row[col] === undefined || row[col] === "" ? (
                        <span className="metric-badge tag-danger text-xs px-1.5 py-0.5">null</span>
                      ) : (
                        String(row[col])
                      )}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
