import VitalCard from "@/components/VitalCard";
import LifestylePanel from "@/components/LifestylePanel";

interface Lifestyle {
  exercise_minutes_per_day: number;
  diet_type: string;
  smoking_status: boolean;
  alcohol_units_per_week: number;
  sleep_hours_per_night: number;
  stress_level: string;
}

interface NLPSidebarProps {
  systolicBp?: number | null;
  diastolicBp?: number | null;
  glucoseLevel?: number | null;
  age?: number | null;
  medications?: string[];
  extractedAt?: string;
  lifestyle: Lifestyle;
  onLifestyleChange: (updated: Lifestyle) => void;
}

const NLPSidebar = ({
  systolicBp,
  diastolicBp,
  glucoseLevel,
  age,
  medications = [],
  extractedAt,
  lifestyle,
  onLifestyleChange,
}: NLPSidebarProps) => {
  const bpValue =
    systolicBp != null && diastolicBp != null
      ? `${systolicBp}/${diastolicBp}`
      : "—";
  const glucoseValue = glucoseLevel != null ? String(glucoseLevel) : "—";
  const ageValue = age != null ? String(age) : "—";

  return (
    <aside className="w-72 min-h-screen bg-surface border-r border-border flex flex-col shrink-0 overflow-y-auto">
      <div className="px-6 py-8">
        <p className="text-[10px] font-light tracking-[0.3em] uppercase text-muted-foreground">
          NLP Intelligence Layer
        </p>
      </div>

      <div className="px-6 flex-1">
        <VitalCard label="Blood Pressure" value={bpValue} unit="mmHg" />
        <VitalCard label="Glucose Level" value={glucoseValue} unit="mg/dL" />
        <VitalCard label="Patient Age" value={ageValue} unit="years" />

        {medications.length > 0 && (
          <div className="border-b border-border py-6 px-2">
            <p className="text-xs font-light tracking-widest uppercase text-muted-foreground mb-3">
              Medications
            </p>
            <ul className="space-y-1">
              {medications.map((med) => (
                <li key={med} className="font-mono-data text-sm text-foreground">
                  {med}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      <LifestylePanel lifestyle={lifestyle} onChange={onLifestyleChange} />

      <div className="px-6 py-4 border-t border-border">
        <p className="font-mono-data text-[10px] text-muted-foreground tracking-wide">
          {extractedAt
            ? `Last extraction: ${new Date(extractedAt).toLocaleTimeString()}`
            : "No extraction yet"}
        </p>
      </div>
    </aside>
  );
};

export default NLPSidebar;
