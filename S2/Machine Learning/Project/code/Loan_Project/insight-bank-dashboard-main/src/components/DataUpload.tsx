import React, { useCallback, useState } from "react";
import Papa from "papaparse";
import { Upload, FileText, CheckCircle, AlertCircle } from "lucide-react";
import type { LoanRecord } from "@/lib/dataUtils";

interface DataUploadProps {
  onDataLoaded: (data: LoanRecord[], filename: string) => void;
}

export const DataUpload: React.FC<DataUploadProps> = ({ onDataLoaded }) => {
  const [isDragging, setIsDragging] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loaded, setLoaded] = useState<string | null>(null);

  const processFile = useCallback(
    (file: File) => {
      if (!file.name.endsWith(".csv")) {
        setError("Please upload a valid .csv file.");
        return;
      }
      setLoading(true);
      setError(null);
      Papa.parse<LoanRecord>(file, {
        header: true,
        skipEmptyLines: true,
        dynamicTyping: false,
        complete: (result) => {
          const cleaned = result.data.map((row) => {
            const cleanRow: LoanRecord = {};
            Object.keys(row).forEach((k) => {
              cleanRow[k.trim()] = (row[k] as string)?.trim() ?? null;
            });
            return cleanRow;
          });
          onDataLoaded(cleaned, file.name);
          setLoaded(file.name);
          setLoading(false);
        },
        error: () => {
          setError("Failed to parse CSV file.");
          setLoading(false);
        },
      });
    },
    [onDataLoaded]
  );

  const handleDrop = useCallback(
    (e: React.DragEvent<HTMLLabelElement>) => {
      e.preventDefault();
      setIsDragging(false);
      const file = e.dataTransfer.files[0];
      if (file) processFile(file);
    },
    [processFile]
  );

  const handleChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const file = e.target.files?.[0];
      if (file) processFile(file);
    },
    [processFile]
  );

  return (
    <div className="animate-fade-in-up">
      <label
        className={`upload-zone block rounded-xl p-12 text-center cursor-pointer transition-all ${
          isDragging ? "drag-over" : ""
        }`}
        onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
      >
        <input
          type="file"
          accept=".csv"
          className="hidden"
          onChange={handleChange}
        />
        <div className="flex flex-col items-center gap-5">
          {loaded ? (
            <div className="w-16 h-16 rounded-full flex items-center justify-center"
              style={{ background: "hsl(145, 50%, 15%)" }}>
              <CheckCircle className="w-8 h-8" style={{ color: "hsl(145, 65%, 55%)" }} />
            </div>
          ) : loading ? (
            <div className="w-16 h-16 rounded-full flex items-center justify-center"
              style={{ background: "hsl(43, 50%, 15%)" }}>
              <div className="w-8 h-8 border-2 border-t-transparent rounded-full animate-spin"
                style={{ borderColor: "hsl(var(--primary))", borderTopColor: "transparent" }} />
            </div>
          ) : (
            <div className="w-16 h-16 rounded-full flex items-center justify-center"
              style={{ background: "hsl(43, 50%, 12%)" }}>
              <Upload className="w-8 h-8" style={{ color: "hsl(var(--primary))" }} />
            </div>
          )}

          {loaded ? (
            <div>
              <p className="font-display font-semibold text-lg" style={{ color: "hsl(145, 65%, 55%)" }}>
                Dataset Loaded Successfully
              </p>
              <p className="text-sm mt-1" style={{ color: "hsl(var(--muted-foreground))" }}>
                <FileText className="w-3.5 h-3.5 inline mr-1" />
                {loaded}
              </p>
              <p className="text-xs mt-2" style={{ color: "hsl(var(--muted-foreground))" }}>
                Click to upload a different file
              </p>
            </div>
          ) : loading ? (
            <div>
              <p className="font-display font-semibold text-lg" style={{ color: "hsl(var(--foreground))" }}>
                Processing Dataset...
              </p>
              <p className="text-sm mt-1" style={{ color: "hsl(var(--muted-foreground))" }}>
                Parsing CSV data
              </p>
            </div>
          ) : (
            <div>
              <p className="font-display font-semibold text-xl" style={{ color: "hsl(var(--foreground))" }}>
                Upload Loan Dataset
              </p>
              <p className="text-sm mt-2" style={{ color: "hsl(var(--muted-foreground))" }}>
                Drag & drop your <span style={{ color: "hsl(var(--primary))" }}>.csv</span> file here, or click to browse
              </p>
              <p className="text-xs mt-3" style={{ color: "hsl(var(--muted-foreground))" }}>
                Supports Loan.csv format with credit_score, annual_income, loan_amount, etc.
              </p>
            </div>
          )}
        </div>
      </label>

      {error && (
        <div className="mt-3 flex items-center gap-2 px-4 py-2.5 rounded-lg text-sm"
          style={{ background: "hsl(0, 50%, 12%)", color: "hsl(0, 72%, 65%)", border: "1px solid hsl(0, 50%, 22%)" }}>
          <AlertCircle className="w-4 h-4 flex-shrink-0" />
          {error}
        </div>
      )}
    </div>
  );
};
