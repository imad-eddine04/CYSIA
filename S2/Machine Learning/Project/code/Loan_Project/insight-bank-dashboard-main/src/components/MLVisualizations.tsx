import React from "react";
import {
  ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, Cell, ReferenceLine, Line, LineChart,
} from "recharts";
import type { LoanRecord } from "@/lib/dataUtils";
import { computePCA, computeSVMData } from "@/lib/dataUtils";

interface MLVisualizationsProps {
  data: LoanRecord[];
}

export const MLVisualizations: React.FC<MLVisualizationsProps> = ({ data }) => {
  const numericFeatures = [
    "credit_score", "annual_income", "loan_amount",
    "employment_duration", "Age", "Children_Count", "Previous_Loan_Count",
  ];

  const pcaPoints = computePCA(data, numericFeatures);
  const svmData = computeSVMData(pcaPoints);

  const class0 = pcaPoints.filter((p) => p.label === 0);
  const class1 = pcaPoints.filter((p) => p.label === 1);
  const sample0 = class0.filter((_, i) => i % 2 === 0).slice(0, 200);
  const sample1 = class1.filter((_, i) => i % 2 === 0).slice(0, 200);

  return (
    <div className="space-y-5 animate-fade-in-up">
      {/* PCA */}
      <div className="glass-card p-5">
        <div className="flex items-center justify-between mb-4 flex-wrap gap-2">
          <h3 className="section-title">
            <span style={{ color: "hsl(280,65%,65%)" }}>◉</span>
            PCA — 2D Projection
          </h3>
          <div className="flex items-center gap-3 text-xs" style={{ color: "hsl(var(--muted-foreground))" }}>
            <span>Features: {numericFeatures.length} → 2 principal components</span>
            <div className="flex items-center gap-1.5">
              <div className="w-2.5 h-2.5 rounded-full" style={{ background: "hsl(145,65%,42%)" }} />
              No Default ({class0.length})
            </div>
            <div className="flex items-center gap-1.5">
              <div className="w-2.5 h-2.5 rounded-full" style={{ background: "hsl(0,72%,55%)" }} />
              Default ({class1.length})
            </div>
          </div>
        </div>
        <ResponsiveContainer width="100%" height={320}>
          <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 10 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="hsl(220,25%,18%)" />
            <XAxis
              type="number" dataKey="pc1" name="PC1"
              tick={{ fill: "hsl(215,20%,55%)", fontSize: 11 }}
              axisLine={{ stroke: "hsl(220,25%,18%)" }}
              tickLine={false}
              label={{ value: "Principal Component 1", position: "insideBottom", offset: -12, fill: "hsl(215,20%,55%)", fontSize: 11 }}
            />
            <YAxis
              type="number" dataKey="pc2" name="PC2"
              tick={{ fill: "hsl(215,20%,55%)", fontSize: 11 }}
              axisLine={false} tickLine={false}
              label={{ value: "PC2", angle: -90, position: "insideLeft", offset: 15, fill: "hsl(215,20%,55%)", fontSize: 11 }}
            />
            <Tooltip
              content={({ active, payload }) => {
                if (active && payload?.length) {
                  const d = payload[0]?.payload;
                  return (
                    <div className="glass-card p-2.5 text-xs">
                      <p style={{ color: d?.label === 1 ? "hsl(0,72%,65%)" : "hsl(145,65%,55%)" }}>
                        {d?.label === 1 ? "⚠ Default" : "✓ No Default"}
                      </p>
                      <p style={{ color: "hsl(var(--foreground))" }}>PC1: {Number(d?.pc1).toFixed(3)}</p>
                      <p style={{ color: "hsl(var(--foreground))" }}>PC2: {Number(d?.pc2).toFixed(3)}</p>
                    </div>
                  );
                }
                return null;
              }}
            />
            <Scatter name="No Default" data={sample0} fill="hsl(145,65%,42%)" opacity={0.7} />
            <Scatter name="Default" data={sample1} fill="hsl(0,72%,55%)" opacity={0.7} />
          </ScatterChart>
        </ResponsiveContainer>
      </div>

      {/* SVM Hyperplane */}
      <div className="glass-card p-5">
        <div className="flex items-center justify-between mb-4 flex-wrap gap-2">
          <h3 className="section-title">
            <span style={{ color: "hsl(var(--accent))" }}>⊞</span>
            SVM Decision Hyperplane (PCA Space)
          </h3>
          <div className="flex items-center gap-3 text-xs" style={{ color: "hsl(var(--muted-foreground))" }}>
            <div className="flex items-center gap-1.5">
              <div className="w-6 h-0.5" style={{ background: "hsl(43,85%,55%)" }} />
              Decision Boundary
            </div>
            <div className="flex items-center gap-1.5">
              <div className="w-6 h-0.5 border-t border-dashed" style={{ borderColor: "hsl(43,50%,45%)" }} />
              Margin
            </div>
          </div>
        </div>
        <ResponsiveContainer width="100%" height={320}>
          <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 10 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="hsl(220,25%,18%)" />
            <XAxis
              type="number" dataKey="pc1" name="PC1"
              tick={{ fill: "hsl(215,20%,55%)", fontSize: 11 }}
              axisLine={{ stroke: "hsl(220,25%,18%)" }}
              tickLine={false}
              label={{ value: "PC1", position: "insideBottom", offset: -12, fill: "hsl(215,20%,55%)", fontSize: 11 }}
            />
            <YAxis
              type="number" dataKey="pc2" name="PC2"
              tick={{ fill: "hsl(215,20%,55%)", fontSize: 11 }}
              axisLine={false} tickLine={false}
              label={{ value: "PC2", angle: -90, position: "insideLeft", offset: 15, fill: "hsl(215,20%,55%)", fontSize: 11 }}
            />
            <Tooltip
              content={({ active, payload }) => {
                if (active && payload?.length) {
                  const d = payload[0]?.payload;
                  return (
                    <div className="glass-card p-2.5 text-xs">
                      <p style={{ color: d?.label === 1 ? "hsl(0,72%,65%)" : "hsl(145,65%,55%)" }}>
                        {d?.label === 1 ? "⚠ Default" : "✓ No Default"}
                      </p>
                    </div>
                  );
                }
                return null;
              }}
            />
            {/* Decision boundary as reference line */}
            {svmData.hyperplane.length === 2 && (
              <ReferenceLine
                segment={svmData.hyperplane.map((p) => ({ x: p.x, y: p.y }))}
                stroke="hsl(43,85%,55%)"
                strokeWidth={2.5}
                label=""
              />
            )}
            {svmData.margin1.length === 2 && (
              <ReferenceLine
                segment={svmData.margin1.map((p) => ({ x: p.x, y: p.y }))}
                stroke="hsl(43,50%,45%)"
                strokeWidth={1}
                strokeDasharray="6 4"
                label=""
              />
            )}
            {svmData.margin2.length === 2 && (
              <ReferenceLine
                segment={svmData.margin2.map((p) => ({ x: p.x, y: p.y }))}
                stroke="hsl(43,50%,45%)"
                strokeWidth={1}
                strokeDasharray="6 4"
                label=""
              />
            )}
            <Scatter name="No Default" data={sample0} fill="hsl(145,65%,42%)" opacity={0.65} />
            <Scatter name="Default" data={sample1} fill="hsl(0,72%,55%)" opacity={0.65} />
          </ScatterChart>
        </ResponsiveContainer>
        <p className="text-xs mt-2 text-center" style={{ color: "hsl(var(--muted-foreground))" }}>
          Linear SVM decision boundary estimated via centroid midpoint in PCA-projected feature space
        </p>
      </div>
    </div>
  );
};
