import { useState, useRef, useEffect } from "react";
import NLPSidebar from "@/components/NLPSidebar";
import RiskBar from "@/components/RiskBar";
import ProcessingOverlay from "@/components/ProcessingOverlay";
import { Upload } from "lucide-react";

const API_URL = "/analyze";
const SIMULATE_URL = "/simulate";

interface Lifestyle {
  exercise_minutes_per_day: number;
  diet_type: string;
  smoking_status: boolean;
  alcohol_units_per_week: number;
  sleep_hours_per_night: number;
  stress_level: string;
}

interface AnalysisResult {
  status: string;
  // Extracted vitals
  systolic_bp: number;
  diastolic_bp: number;
  glucose_level: number;
  cholesterol_level: number;
  age: number;
  medications: string[];
  dosage?: Record<string, string>;
  // Predictions
  predicted_systolic_bp: number;
  predicted_diastolic_bp: number;
  predicted_glucose_level: number;
  predicted_cholesterol_level: number;
  cardiovascular_risk_score: number;
  diabetes_risk_score: number;
  extracted_at: string;
  message?: string;
}

const DEFAULT_LIFESTYLE: Lifestyle = {
  exercise_minutes_per_day: 30,
  diet_type: "balanced",
  smoking_status: false,
  alcohol_units_per_week: 2,
  sleep_hours_per_night: 7,
  stress_level: "medium",
};

const Index = () => {
  const [processing, setProcessing] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [lifestyle, setLifestyle] = useState<Lifestyle>(DEFAULT_LIFESTYLE);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setProcessing(true);
    setError(null);
    setResult(null);

    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("lifestyle", JSON.stringify(lifestyle));

      const res = await fetch(API_URL, { method: "POST", body: formData });
      const data: AnalysisResult = await res.json();

      if (data.status === "error") {
        setError(data.message ?? "Unknown error from server.");
      } else {
        setResult(data);
      }
    } catch {
      setError("Could not connect to the AI server. Make sure server.py is running on port 8000.");
    } finally {
      setProcessing(false);
      // Reset input so same file can be re-uploaded after lifestyle changes
      if (fileInputRef.current) fileInputRef.current.value = "";
    }
  };

  // Run simulation interactively when lifestyle changes
  useEffect(() => {
    // Only run if we already have a loaded prescription (result has vitals)
    if (!result) return;
    
    const runSimulation = async () => {
      try {
        const vitalsPayload = {
          systolic_bp: result.systolic_bp,
          diastolic_bp: result.diastolic_bp,
          glucose_level: result.glucose_level,
          cholesterol_level: result.cholesterol_level,
          age: result.age,
          medications: result.medications,
          dosage: result.dosage || {}
        };
        
        const res = await fetch(SIMULATE_URL, {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            vitals: vitalsPayload,
            lifestyle: lifestyle
          })
        });
        
        const data = await res.json();
        if (data.status === "success") {
          // Update just the prediction parts of the result
          setResult(prev => {
            if (!prev) return prev;
            return {
              ...prev,
              predicted_systolic_bp: data.predicted_systolic_bp,
              predicted_diastolic_bp: data.predicted_diastolic_bp,
              predicted_glucose_level: data.predicted_glucose_level,
              predicted_cholesterol_level: data.predicted_cholesterol_level,
              cardiovascular_risk_score: data.cardiovascular_risk_score,
              diabetes_risk_score: data.diabetes_risk_score
            };
          });
        }
      } catch (err) {
        console.error("Simulation failed:", err);
      }
    };
    
    // De-bounce slightly to avoid spamming the backend
    const timeoutId = setTimeout(runSimulation, 300);
    return () => clearTimeout(timeoutId);
    
  }, [lifestyle]);

  const cardValue = result
    ? result.predicted_systolic_bp.toFixed(0)
    : "—";

  const cardiovascularPct = result
    ? Math.round(result.cardiovascular_risk_score * 100)
    : 0;

  const diabetesPct = result
    ? Math.round(result.diabetes_risk_score * 100)
    : 0;

  return (
    <div className="flex min-h-screen w-full bg-background">
      {/* Hidden file input */}
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        className="hidden"
        onChange={handleFileChange}
      />

      <NLPSidebar
        systolicBp={result?.systolic_bp ?? null}
        diastolicBp={result?.diastolic_bp ?? null}
        glucoseLevel={result?.glucose_level ?? null}
        age={result?.age ?? null}
        medications={result?.medications ?? []}
        extractedAt={result?.extracted_at}
        lifestyle={lifestyle}
        onLifestyleChange={setLifestyle}
      />

      <div className="flex-1 relative">
        {/* Floating header */}
        <div className="absolute top-6 right-6 z-30">
          <button
            onClick={handleUploadClick}
            disabled={processing}
            className="flex items-center gap-2 px-5 py-2.5 rounded-lg bg-primary text-primary-foreground font-mono-data text-sm font-medium hover:opacity-90 transition-opacity disabled:opacity-50"
          >
            <Upload size={16} />
            Upload Prescription
          </button>
        </div>

        {/* Main content */}
        <div className="flex flex-col items-center justify-center min-h-screen px-8 gap-10">

          {/* Error banner */}
          {error && (
            <div className="bg-red-500/10 border border-red-500/30 rounded-xl px-6 py-4 max-w-lg w-full text-center">
              <p className="font-mono-data text-sm text-red-400">{error}</p>
            </div>
          )}

          {/* Projection card */}
          <div className="glass-card rounded-2xl p-12 text-center max-w-lg w-full">
            <p className="text-xs font-light tracking-[0.3em] uppercase text-muted-foreground mb-2">
              Health Projection
            </p>
            <p className="text-[10px] font-mono-data text-muted-foreground mb-8 tracking-wide">
              Predicted Systolic BP — 6 Month Forecast
            </p>
            <div className="glow-box rounded-2xl inline-block px-8 py-4">
              <span className="font-mono-data text-7xl font-light text-primary glow-text">
                {cardValue}
              </span>
            </div>
            <p className="font-mono-data text-xs text-muted-foreground mt-6">
              {result
                ? `mmHg · Diastolic: ${result.predicted_diastolic_bp.toFixed(0)} · Glucose: ${result.predicted_glucose_level.toFixed(0)} mg/dL`
                : "Upload a prescription to run the simulation"}
            </p>
          </div>

          {/* Risk analysis */}
          <div className="w-full max-w-lg space-y-6">
            <p className="text-xs font-light tracking-[0.3em] uppercase text-muted-foreground">
              Risk Analysis
            </p>
            <RiskBar label="Cardiovascular Risk" percentage={cardiovascularPct} />
            <RiskBar label="Diabetes Risk" percentage={diabetesPct} />
          </div>
        </div>
      </div>

      {processing && <ProcessingOverlay />}
    </div>
  );
};

export default Index;
