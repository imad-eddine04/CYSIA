import React from "react";
import { AlertTriangle, CheckCircle2, Sparkles } from "lucide-react";
import type { MissingInfo } from "@/lib/dataUtils";

interface MissingValuesProps {
  missingInfo: MissingInfo[];
  onClean: () => void;
  isCleaned: boolean;
}

export const MissingValues: React.FC<MissingValuesProps> = ({
  missingInfo, onClean, isCleaned,
}) => {
  const totalMissing = missingInfo.reduce((s, m) => s + m.missing, 0);
  const colsWithMissing = missingInfo.filter((m) => m.missing > 0);

  return (
    <div className="glass-card animate-fade-in-up">
      <div className="px-5 py-4 border-b flex items-center justify-between flex-wrap gap-3"
        style={{ borderColor: "hsl(var(--border))" }}>
        <div className="flex items-center gap-3">
          <h3 className="section-title">
            <AlertTriangle className="w-4 h-4" style={{ color: "hsl(43,85%,55%)" }} />
            Missing Values Analysis
          </h3>
          {isCleaned ? (
            <span className="metric-badge tag-success flex items-center gap-1">
              <CheckCircle2 className="w-3 h-3" />
              Dataset Cleaned
            </span>
          ) : (
            <span className="metric-badge tag-danger">
              {totalMissing} missing values
            </span>
          )}
        </div>
        {!isCleaned && colsWithMissing.length > 0 && (
          <button className="btn-gold" onClick={onClean}>
            <Sparkles className="w-4 h-4" />
            Clean Dataset
          </button>
        )}
        {isCleaned && (
          <div className="flex items-center gap-2 text-sm" style={{ color: "hsl(145,65%,55%)" }}>
            <CheckCircle2 className="w-4 h-4" />
            Missing values imputed with mean/mode
          </div>
        )}
      </div>
      <div className="p-5">
        {missingInfo.length === 0 ? (
          <p className="text-center py-4" style={{ color: "hsl(var(--muted-foreground))" }}>
            No data loaded
          </p>
        ) : (
          <div className="space-y-2.5">
            {missingInfo.map((info) => (
              <div key={info.column} className="flex items-center gap-3">
                <div className="w-36 text-right">
                  <span className="text-xs font-semibold truncate" style={{ color: "hsl(var(--foreground))" }}>
                    {info.column}
                  </span>
                </div>
                <div className="flex-1">
                  <div className="progress-bar-gold">
                    <div
                      className="progress-bar-gold-fill"
                      style={{
                        width: `${Math.max(info.percentage, info.missing > 0 ? 2 : 0)}%`,
                        background: info.missing === 0
                          ? "hsl(145,65%,42%)"
                          : info.percentage > 20
                          ? "hsl(0,72%,55%)"
                          : "hsl(43,85%,55%)",
                      }}
                    />
                  </div>
                </div>
                <div className="w-28 flex items-center justify-end gap-2">
                  {info.missing === 0 ? (
                    <span className="metric-badge tag-success text-xs">
                      <CheckCircle2 className="w-3 h-3 mr-0.5" />
                      Complete
                    </span>
                  ) : isCleaned ? (
                    <span className="metric-badge tag-success text-xs">
                      ✓ Fixed
                    </span>
                  ) : (
                    <span
                      className={`metric-badge text-xs ${info.percentage > 20 ? "tag-danger" : "tag-gold"}`}
                    >
                      {info.missing} ({info.percentage}%)
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}

        {!isCleaned && totalMissing > 0 && (
          <div className="mt-5 p-4 rounded-lg border text-sm"
            style={{ background: "hsl(43,50%,8%)", borderColor: "hsl(var(--border-gold))", color: "hsl(var(--muted-foreground))" }}>
            <p className="font-medium mb-1" style={{ color: "hsl(var(--primary))" }}>
              Cleaning Strategy:
            </p>
            <ul className="space-y-0.5 text-xs list-disc list-inside">
              <li>Numerical columns → imputed with column <strong>mean</strong></li>
              <li>Categorical columns → imputed with column <strong>mode</strong></li>
              <li>{colsWithMissing.length} column(s) affected</li>
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};
