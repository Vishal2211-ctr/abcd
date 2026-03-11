interface Lifestyle {
  exercise_minutes_per_day: number;
  diet_type: string;
  smoking_status: boolean;
  alcohol_units_per_week: number;
  sleep_hours_per_night: number;
  stress_level: string;
}

interface LifestylePanelProps {
  lifestyle: Lifestyle;
  onChange: (updated: Lifestyle) => void;
}

const LifestylePanel = ({ lifestyle, onChange }: LifestylePanelProps) => {
  const update = (key: keyof Lifestyle, value: number | string | boolean) =>
    onChange({ ...lifestyle, [key]: value });

  return (
    <div className="px-6 py-6 border-t border-border space-y-5">
      <p className="text-[10px] font-light tracking-[0.3em] uppercase text-muted-foreground">
        Lifestyle Parameters
      </p>

      {/* Exercise */}
      <div className="space-y-1">
        <div className="flex justify-between">
          <span className="text-xs text-muted-foreground">Exercise</span>
          <span className="font-mono-data text-xs text-foreground">
            {lifestyle.exercise_minutes_per_day} min/day
          </span>
        </div>
        <input
          type="range"
          min={0}
          max={120}
          value={lifestyle.exercise_minutes_per_day}
          onChange={(e) => update("exercise_minutes_per_day", Number(e.target.value))}
          className="w-full accent-primary"
        />
      </div>

      {/* Sleep */}
      <div className="space-y-1">
        <div className="flex justify-between">
          <span className="text-xs text-muted-foreground">Sleep</span>
          <span className="font-mono-data text-xs text-foreground">
            {lifestyle.sleep_hours_per_night} hrs/night
          </span>
        </div>
        <input
          type="range"
          min={3}
          max={12}
          value={lifestyle.sleep_hours_per_night}
          onChange={(e) => update("sleep_hours_per_night", Number(e.target.value))}
          className="w-full accent-primary"
        />
      </div>

      {/* Alcohol */}
      <div className="space-y-1">
        <div className="flex justify-between">
          <span className="text-xs text-muted-foreground">Alcohol</span>
          <span className="font-mono-data text-xs text-foreground">
            {lifestyle.alcohol_units_per_week} units/wk
          </span>
        </div>
        <input
          type="range"
          min={0}
          max={20}
          value={lifestyle.alcohol_units_per_week}
          onChange={(e) => update("alcohol_units_per_week", Number(e.target.value))}
          className="w-full accent-primary"
        />
      </div>

      {/* Diet */}
      <div className="space-y-1">
        <span className="text-xs text-muted-foreground">Diet</span>
        <select
          value={lifestyle.diet_type}
          onChange={(e) => update("diet_type", e.target.value)}
          className="w-full bg-surface border border-border rounded px-2 py-1 font-mono-data text-xs text-foreground"
        >
          <option value="balanced">Balanced</option>
          <option value="high_fat">High Fat</option>
        </select>
      </div>

      {/* Stress */}
      <div className="space-y-1">
        <span className="text-xs text-muted-foreground">Stress Level</span>
        <select
          value={lifestyle.stress_level}
          onChange={(e) => update("stress_level", e.target.value)}
          className="w-full bg-surface border border-border rounded px-2 py-1 font-mono-data text-xs text-foreground"
        >
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>
      </div>

      {/* Smoking */}
      <div className="flex items-center justify-between">
        <span className="text-xs text-muted-foreground">Smoking</span>
        <button
          onClick={() => update("smoking_status", !lifestyle.smoking_status)}
          className={`px-3 py-1 rounded text-xs font-mono-data transition-colors ${
            lifestyle.smoking_status
              ? "bg-red-500/20 text-red-400 border border-red-500/30"
              : "bg-green-500/10 text-green-400 border border-green-500/20"
          }`}
        >
          {lifestyle.smoking_status ? "Yes" : "No"}
        </button>
      </div>
    </div>
  );
};

export default LifestylePanel;
