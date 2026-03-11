interface RiskBarProps {
  label: string;
  percentage: number;
}

const RiskBar = ({ label, percentage }: RiskBarProps) => {
  const getGradient = () => {
    if (percentage <= 33) return "from-green-500 to-green-400";
    if (percentage <= 66) return "from-green-500 via-yellow-400 to-yellow-400";
    return "from-green-500 via-yellow-400 to-red-500";
  };

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <span className="text-xs font-light tracking-widest uppercase text-muted-foreground">
          {label}
        </span>
        <span className="font-mono-data text-sm text-muted-foreground">
          {percentage}%
        </span>
      </div>
      <div className="h-2 w-full rounded-full bg-secondary overflow-hidden">
        <div
          className={`h-full rounded-full bg-gradient-to-r ${getGradient()} transition-all duration-1000 ease-out`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
};

export default RiskBar;
