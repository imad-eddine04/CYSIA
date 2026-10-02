// Data processing utilities for bank loan analytics

export interface LoanRecord {
  [key: string]: string | number | null;
}

export interface DatasetInfo {
  rows: number;
  cols: number;
  columns: string[];
}

export interface MissingInfo {
  column: string;
  missing: number;
  total: number;
  percentage: number;
}

export function getDatasetInfo(data: LoanRecord[]): DatasetInfo {
  if (!data.length) return { rows: 0, cols: 0, columns: [] };
  return {
    rows: data.length,
    cols: Object.keys(data[0]).length,
    columns: Object.keys(data[0]),
  };
}

export function getMissingValues(data: LoanRecord[]): MissingInfo[] {
  if (!data.length) return [];
  const cols = Object.keys(data[0]);
  return cols.map((col) => {
    const missing = data.filter(
      (row) =>
        row[col] === null ||
        row[col] === undefined ||
        row[col] === "" ||
        (typeof row[col] === "number" && isNaN(row[col] as number))
    ).length;
    return {
      column: col,
      missing,
      total: data.length,
      percentage: parseFloat(((missing / data.length) * 100).toFixed(2)),
    };
  });
}

export function cleanDataset(data: LoanRecord[]): LoanRecord[] {
  const numericCols = ["credit_score", "annual_income", "loan_amount", "employment_duration", "Age", "Children_Count", "Previous_Loan_Count"];
  
  // Compute means for numeric cols
  const means: { [key: string]: number } = {};
  numericCols.forEach((col) => {
    const vals = data
      .map((row) => parseFloat(String(row[col])))
      .filter((v) => !isNaN(v));
    means[col] = vals.length ? vals.reduce((a, b) => a + b, 0) / vals.length : 0;
  });

  // Compute modes for categorical cols
  const catCols = ["EmploymentStatus", "MaritalStatus", "Vehicle_Ownership"];
  const modes: { [key: string]: string } = {};
  catCols.forEach((col) => {
    const freq: { [k: string]: number } = {};
    data.forEach((row) => {
      if (row[col] !== null && row[col] !== undefined && row[col] !== "") {
        const key = String(row[col]);
        freq[key] = (freq[key] || 0) + 1;
      }
    });
    modes[col] = Object.entries(freq).sort((a, b) => b[1] - a[1])[0]?.[0] || "";
  });

  return data.map((row) => {
    const cleaned = { ...row };
    numericCols.forEach((col) => {
      if (col in cleaned) {
        const val = parseFloat(String(cleaned[col]));
        if (isNaN(val) || cleaned[col] === null || cleaned[col] === "") {
          cleaned[col] = parseFloat(means[col].toFixed(2));
        }
      }
    });
    catCols.forEach((col) => {
      if (col in cleaned && (cleaned[col] === null || cleaned[col] === undefined || cleaned[col] === "")) {
        cleaned[col] = modes[col];
      }
    });
    return cleaned;
  });
}

export function computeHistogram(
  data: LoanRecord[],
  column: string,
  bins = 20
): { bin: string; count: number; range: [number, number] }[] {
  const vals = data
    .map((row) => parseFloat(String(row[column])))
    .filter((v) => !isNaN(v));
  if (!vals.length) return [];

  const min = Math.min(...vals);
  const max = Math.max(...vals);
  const binWidth = (max - min) / bins;

  const counts = Array(bins).fill(0);
  vals.forEach((v) => {
    let idx = Math.floor((v - min) / binWidth);
    if (idx >= bins) idx = bins - 1;
    counts[idx]++;
  });

  return counts.map((count, i) => {
    const lo = min + i * binWidth;
    const hi = lo + binWidth;
    return {
      bin: lo >= 1000 ? `${(lo / 1000).toFixed(0)}k` : lo.toFixed(0),
      count,
      range: [lo, hi],
    };
  });
}

export function computeCorrelationMatrix(
  data: LoanRecord[],
  columns: string[]
): { column: string; correlations: { [key: string]: number } }[] {
  const numCols = columns.filter((col) => {
    const vals = data.map((row) => parseFloat(String(row[col]))).filter((v) => !isNaN(v));
    return vals.length > data.length * 0.5;
  });

  const getVals = (col: string) =>
    data.map((row) => parseFloat(String(row[col]))).map((v) => (isNaN(v) ? 0 : v));

  const mean = (arr: number[]) => arr.reduce((a, b) => a + b, 0) / arr.length;
  const corr = (a: number[], b: number[]) => {
    const ma = mean(a);
    const mb = mean(b);
    const num = a.reduce((s, v, i) => s + (v - ma) * (b[i] - mb), 0);
    const da = Math.sqrt(a.reduce((s, v) => s + (v - ma) ** 2, 0));
    const db = Math.sqrt(b.reduce((s, v) => s + (v - mb) ** 2, 0));
    return da && db ? parseFloat((num / (da * db)).toFixed(3)) : 0;
  };

  return numCols.map((col) => {
    const aVals = getVals(col);
    const correlations: { [key: string]: number } = {};
    numCols.forEach((col2) => {
      correlations[col2] = corr(aVals, getVals(col2));
    });
    return { column: col, correlations };
  });
}

export function computeScatterData(
  data: LoanRecord[],
  xCol: string,
  yCol: string,
  colorCol?: string
): { x: number; y: number; color: number; label: string }[] {
  return data
    .map((row) => ({
      x: parseFloat(String(row[xCol])),
      y: parseFloat(String(row[yCol])),
      color: colorCol ? parseFloat(String(row[colorCol])) : 0,
      label: String(row["first_name"] || ""),
    }))
    .filter((d) => !isNaN(d.x) && !isNaN(d.y));
}

// Simple PCA (2D) implementation
export function computePCA(
  data: LoanRecord[],
  features: string[]
): { pc1: number; pc2: number; label: number }[] {
  const numFeatures = features.filter((f) => {
    const vals = data.map((row) => parseFloat(String(row[f]))).filter((v) => !isNaN(v));
    return vals.length > data.length * 0.5;
  });

  if (numFeatures.length < 2) return [];

  // Build matrix
  const matrix = data.map((row) =>
    numFeatures.map((f) => {
      const v = parseFloat(String(row[f]));
      return isNaN(v) ? 0 : v;
    })
  );

  // Standardize
  const means = numFeatures.map((_, j) => {
    const col = matrix.map((r) => r[j]);
    return col.reduce((a, b) => a + b, 0) / col.length;
  });
  const stds = numFeatures.map((_, j) => {
    const col = matrix.map((r) => r[j]);
    const m = means[j];
    return Math.sqrt(col.reduce((s, v) => s + (v - m) ** 2, 0) / col.length) || 1;
  });

  const standardized = matrix.map((row) =>
    row.map((v, j) => (v - means[j]) / stds[j])
  );

  // Use first 2 features as PC1, PC2 proxy (simplified PCA via projection)
  // Real PCA requires SVD - we use a simplified version
  const n = standardized.length;
  const cov = (a: number[], b: number[]) => {
    const ma = a.reduce((s, v) => s + v, 0) / n;
    const mb = b.reduce((s, v) => s + v, 0) / n;
    return a.reduce((s, v, i) => s + (v - ma) * (b[i] - mb), 0) / n;
  };

  // Power iteration for first eigenvector
  let v1: number[] = numFeatures.map((_, j) => (j === 0 ? 1 : 0));
  for (let iter = 0; iter < 50; iter++) {
    const next: number[] = v1.map((_, j) =>
      numFeatures.reduce((s, _, k) => {
        const col_j = standardized.map((r) => r[j]);
        const col_k = standardized.map((r) => r[k]);
        return s + cov(col_j, col_k) * v1[k];
      }, 0)
    );
    const norm = Math.sqrt(next.reduce((s, v) => s + v * v, 0)) || 1;
    v1 = next.map((v) => v / norm);
  }

  // Second eigenvector (orthogonal to v1)
  let v2: number[] = numFeatures.map((_, j) => (j === 1 ? 1 : j === 0 ? -v1[1] / (v1[0] || 1) : 0));
  const norm2 = Math.sqrt(v2.reduce((s, v) => s + v * v, 0)) || 1;
  v2 = v2.map((v) => v / norm2);

  const labels = data.map((row) => {
    const v = parseFloat(String(row["default"]));
    return isNaN(v) ? 0 : v;
  });

  return standardized.map((row, i) => ({
    pc1: parseFloat(row.reduce((s, v, j) => s + v * v1[j], 0).toFixed(3)),
    pc2: parseFloat(row.reduce((s, v, j) => s + v * v2[j], 0).toFixed(3)),
    label: labels[i],
  }));
}

// Mock SVM hyperplane data (simplified linear boundary visualization)
export function computeSVMData(pcaPoints: { pc1: number; pc2: number; label: number }[]) {
  if (!pcaPoints.length) return { points: [], hyperplane: [], margin1: [], margin2: [] };

  // Simple linear decision boundary (midpoint between class centroids)
  const class0 = pcaPoints.filter((p) => p.label === 0);
  const class1 = pcaPoints.filter((p) => p.label === 1);

  const c0 = {
    x: class0.reduce((s, p) => s + p.pc1, 0) / (class0.length || 1),
    y: class0.reduce((s, p) => s + p.pc2, 0) / (class0.length || 1),
  };
  const c1 = {
    x: class1.reduce((s, p) => s + p.pc1, 0) / (class1.length || 1),
    y: class1.reduce((s, p) => s + p.pc2, 0) / (class1.length || 1),
  };

  const midX = (c0.x + c1.x) / 2;
  const midY = (c0.y + c1.y) / 2;
  const dx = c1.x - c0.x;
  const dy = c1.y - c0.y;
  const len = Math.sqrt(dx * dx + dy * dy) || 1;
  const nx = -dy / len;
  const ny = dx / len;
  const scale = 4;

  return {
    points: pcaPoints,
    hyperplane: [
      { x: midX - nx * scale, y: midY - ny * scale },
      { x: midX + nx * scale, y: midY + ny * scale },
    ],
    margin1: [
      { x: midX - nx * scale + (dx / len) * 0.5, y: midY - ny * scale + (dy / len) * 0.5 },
      { x: midX + nx * scale + (dx / len) * 0.5, y: midY + ny * scale + (dy / len) * 0.5 },
    ],
    margin2: [
      { x: midX - nx * scale - (dx / len) * 0.5, y: midY - ny * scale - (dy / len) * 0.5 },
      { x: midX + nx * scale - (dx / len) * 0.5, y: midY + ny * scale - (dy / len) * 0.5 },
    ],
  };
}

// Mock ML metrics (based on a simple threshold on credit_score)
export function computeMLMetrics(data: LoanRecord[]): {
  accuracy: number;
  precision: number;
  recall: number;
  f1: number;
  confusionMatrix: number[][];
  classReport: { class: string; precision: number; recall: number; f1: number; support: number }[];
} {
  const threshold = 650;
  const predictions: number[] = data.map((row) => {
    const cs = parseFloat(String(row["credit_score"]));
    return isNaN(cs) ? 0 : cs < threshold ? 1 : 0;
  });
  const actual: number[] = data.map((row) => {
    const v = parseFloat(String(row["default"]));
    return isNaN(v) ? 0 : v;
  });

  let tp = 0, tn = 0, fp = 0, fn = 0;
  predictions.forEach((p, i) => {
    const a = actual[i];
    if (p === 1 && a === 1) tp++;
    else if (p === 0 && a === 0) tn++;
    else if (p === 1 && a === 0) fp++;
    else fn++;
  });

  const accuracy = parseFloat(((tp + tn) / data.length).toFixed(4));
  const precision = parseFloat((tp / (tp + fp || 1)).toFixed(4));
  const recall = parseFloat((tp / (tp + fn || 1)).toFixed(4));
  const f1 = parseFloat(((2 * precision * recall) / (precision + recall || 1)).toFixed(4));

  return {
    accuracy,
    precision,
    recall,
    f1,
    confusionMatrix: [[tn, fp], [fn, tp]],
    classReport: [
      { class: "No Default (0)", precision: parseFloat((tn / (tn + fn || 1)).toFixed(4)), recall: parseFloat((tn / (tn + fp || 1)).toFixed(4)), f1: 0, support: tn + fp },
      { class: "Default (1)", precision, recall, f1, support: tp + fn },
    ],
  };
}
