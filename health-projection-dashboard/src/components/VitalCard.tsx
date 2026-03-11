interface VitalCardProps {
  label: string;
  value: string;
  unit: string;
}

const VitalCard = ({ label, value, unit }: VitalCardProps) => {
  return (
    <div className="border-b border-border py-6 px-2 last:border-b-0">
      <p className="text-xs font-light tracking-widest uppercase text-muted-foreground mb-3">
        {label}
      </p>
      <div className="flex items-baseline gap-2">
        <span className="font-mono-data text-2xl font-light text-foreground">
          {value}
        </span>
        <span className="font-mono-data text-xs text-muted-foreground">
          {unit}
        </span>
      </div>
    </div>
  );
};

export default VitalCard;
