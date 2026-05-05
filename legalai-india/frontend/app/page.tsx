"use client";
import { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import axios from "axios";
import { FileText, Upload, AlertCircle, CheckCircle, AlertTriangle, Info, Loader2 } from "lucide-react";

const SEVERITY_CONFIG = {
  critical: { color: "bg-red-50 border-red-200", badge: "bg-red-100 text-red-700", icon: <AlertCircle className="w-4 h-4 text-red-500" /> },
  high: { color: "bg-orange-50 border-orange-200", badge: "bg-orange-100 text-orange-700", icon: <AlertTriangle className="w-4 h-4 text-orange-500" /> },
  medium: { color: "bg-yellow-50 border-yellow-200", badge: "bg-yellow-100 text-yellow-700", icon: <Info className="w-4 h-4 text-yellow-500" /> },
  low: { color: "bg-blue-50 border-blue-200", badge: "bg-blue-100 text-blue-700", icon: <Info className="w-4 h-4 text-blue-500" /> },
};

type Gap = {
  code: string;
  section: string;
  issue: string;
  severity: "critical" | "high" | "medium" | "low";
  current_text: string;
  compliant_text: string;
};

type Analysis = {
  overall_score: number;
  summary: string;
  gaps: Gap[];
  compliant_areas: string[];
};

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [expandedGap, setExpandedGap] = useState<number | null>(null);

  const onDrop = useCallback((accepted: File[]) => {
    setFile(accepted[0]);
    setAnalysis(null);
    setError(null);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { "application/pdf": [".pdf"] },
    maxFiles: 1,
  });

  const runAudit = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);
    try {
      const form = new FormData();
      form.append("file", file);
      const res = await axios.post("https://solid-space-trout-g4q4j6wvq796cv7jv-8000.app.github.dev/api/v1/audit", form);
      setAnalysis(res.data.analysis);
    } catch (e: unknown) {
      setError("Analysis failed. Make sure the backend is running on port 8000.");
    } finally {
      setLoading(false);
    }
  };

  const scoreColor = (score: number) =>
    score >= 75 ? "text-green-600" : score >= 50 ? "text-yellow-600" : "text-red-600";

  const scoreBar = (score: number) =>
    score >= 75 ? "bg-green-500" : score >= 50 ? "bg-yellow-500" : "bg-red-500";

  const criticalCount = analysis?.gaps.filter(g => g.severity === "critical").length ?? 0;
  const highCount = analysis?.gaps.filter(g => g.severity === "high").length ?? 0;

  return (
    <main className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="max-w-4xl mx-auto flex items-center gap-3">
          <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
            <FileText className="w-4 h-4 text-white" />
          </div>
          <div>
            <h1 className="text-lg font-semibold text-gray-900">LegalAI India</h1>
            <p className="text-xs text-gray-500">Labour Code Compliance Engine</p>
          </div>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-6 py-8">
        {/* Upload Section */}
        <div className="bg-white rounded-xl border border-gray-200 p-6 mb-6">
          <h2 className="text-base font-semibold text-gray-900 mb-1">Upload HR Policy Document</h2>
          <p className="text-sm text-gray-500 mb-4">Upload your HR policy PDF and get an instant compliance audit against all four Labour Codes</p>

          <div
            {...getRootProps()}
            className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
              isDragActive ? "border-blue-400 bg-blue-50" : "border-gray-200 hover:border-blue-300 hover:bg-gray-50"
            }`}
          >
            <input {...getInputProps()} />
            <Upload className="w-8 h-8 text-gray-400 mx-auto mb-3" />
            {file ? (
              <div>
                <p className="text-sm font-medium text-gray-900">{file.name}</p>
                <p className="text-xs text-gray-500 mt-1">{(file.size / 1024).toFixed(1)} KB — click to change</p>
              </div>
            ) : (
              <div>
                <p className="text-sm font-medium text-gray-700">Drop your HR policy PDF here</p>
                <p className="text-xs text-gray-500 mt-1">or click to browse files</p>
              </div>
            )}
          </div>

          {file && (
            <button
              onClick={runAudit}
              disabled={loading}
              className="mt-4 w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 text-white text-sm font-medium py-2.5 px-4 rounded-lg transition-colors flex items-center justify-center gap-2"
            >
              {loading ? (
                <><Loader2 className="w-4 h-4 animate-spin" /> Analyzing — this takes 20–30 seconds...</>
              ) : (
                <><FileText className="w-4 h-4" /> Run Compliance Audit</>
              )}
            </button>
          )}

          {error && (
            <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg flex gap-2">
              <AlertCircle className="w-4 h-4 text-red-500 flex-shrink-0 mt-0.5" />
              <p className="text-sm text-red-700">{error}</p>
            </div>
          )}
        </div>

        {/* Results */}
        {analysis && (
          <div className="space-y-4">
            {/* Score Card */}
            <div className="bg-white rounded-xl border border-gray-200 p-6">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h2 className="text-base font-semibold text-gray-900">Compliance Report</h2>
                  <p className="text-sm text-gray-500 mt-1">{analysis.summary}</p>
                </div>
                <div className="text-right ml-6 flex-shrink-0">
                  <div className={`text-4xl font-bold ${scoreColor(analysis.overall_score)}`}>
                    {analysis.overall_score}
                  </div>
                  <div className="text-xs text-gray-500">out of 100</div>
                </div>
              </div>

              <div className="w-full bg-gray-100 rounded-full h-2 mb-4">
                <div
                  className={`h-2 rounded-full transition-all ${scoreBar(analysis.overall_score)}`}
                  style={{ width: `${analysis.overall_score}%` }}
                />
              </div>

              <div className="grid grid-cols-3 gap-3">
                <div className="bg-red-50 rounded-lg p-3 text-center">
                  <div className="text-2xl font-bold text-red-600">{criticalCount}</div>
                  <div className="text-xs text-red-600 mt-0.5">Critical</div>
                </div>
                <div className="bg-orange-50 rounded-lg p-3 text-center">
                  <div className="text-2xl font-bold text-orange-600">{highCount}</div>
                  <div className="text-xs text-orange-600 mt-0.5">High</div>
                </div>
                <div className="bg-green-50 rounded-lg p-3 text-center">
                  <div className="text-2xl font-bold text-green-600">{analysis.compliant_areas.length}</div>
                  <div className="text-xs text-green-600 mt-0.5">Compliant</div>
                </div>
              </div>
            </div>

            {/* Gaps */}
            <div className="bg-white rounded-xl border border-gray-200 p-6">
              <h3 className="text-base font-semibold text-gray-900 mb-4">
                Compliance Gaps ({analysis.gaps.length})
              </h3>
              <div className="space-y-3">
                {analysis.gaps.map((gap, i) => {
                  const config = SEVERITY_CONFIG[gap.severity] ?? SEVERITY_CONFIG.low;
                  const isOpen = expandedGap === i;
                  return (
                    <div key={i} className={`border rounded-lg overflow-hidden ${config.color}`}>
                      <button
                        onClick={() => setExpandedGap(isOpen ? null : i)}
                        className="w-full text-left p-4 flex items-start gap-3"
                      >
                        <div className="mt-0.5 flex-shrink-0">{config.icon}</div>
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2 flex-wrap">
                            <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${config.badge}`}>
                              {gap.severity.toUpperCase()}
                            </span>
                            <span className="text-xs text-gray-500">{gap.section}</span>
                          </div>
                          <p className="text-sm font-medium text-gray-900 mt-1">{gap.issue}</p>
                          <p className="text-xs text-gray-500 mt-0.5">{gap.code}</p>
                        </div>
                        <span className="text-gray-400 text-xs flex-shrink-0">{isOpen ? "▲" : "▼"}</span>
                      </button>
                      {isOpen && (
                        <div className="px-4 pb-4 space-y-3 border-t border-gray-200 pt-3">
                          {gap.current_text && (
                            <div>
                              <p className="text-xs font-medium text-gray-500 mb-1">Current (non-compliant)</p>
                              <p className="text-sm text-gray-700 bg-white rounded p-2 border border-gray-200">{gap.current_text}</p>
                            </div>
                          )}
                          <div>
                            <p className="text-xs font-medium text-gray-500 mb-1">Suggested compliant replacement</p>
                            <p className="text-sm text-gray-700 bg-white rounded p-2 border border-green-200">{gap.compliant_text}</p>
                          </div>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Compliant Areas */}
            {analysis.compliant_areas.length > 0 && (
              <div className="bg-white rounded-xl border border-gray-200 p-6">
                <h3 className="text-base font-semibold text-gray-900 mb-3">
                  Compliant Areas ({analysis.compliant_areas.length})
                </h3>
                <div className="space-y-2">
                  {analysis.compliant_areas.map((area, i) => (
                    <div key={i} className="flex items-center gap-2">
                      <CheckCircle className="w-4 h-4 text-green-500 flex-shrink-0" />
                      <span className="text-sm text-gray-700">{area}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </main>
  );
}