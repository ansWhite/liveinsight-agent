import { cn } from "@/lib/format";
import type { EvaluationMetric } from "@/lib/types";

const toneStyles = {
  mint: "bg-[#e7f4ee] text-mint",
  amber: "bg-[#fff4e5] text-amber",
  coral: "bg-[#fbeceb] text-coral",
  steel: "bg-[#eef2ef] text-steel"
};

export function EvaluationGrid({ metrics }: { metrics: EvaluationMetric[] }) {
  return (
    <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
      {metrics.map((metric) => (
        <div className="rounded-md border border-[#e3e7e2] p-4" key={metric.label}>
          <div className="flex items-center justify-between gap-3">
            <div className={cn("flex h-9 w-9 items-center justify-center rounded-md", toneStyles[metric.tone])}>
              <metric.icon size={18} />
            </div>
            <span className="rounded-md bg-[#fbfcfa] px-2 py-1 text-xs font-semibold text-mint">{metric.delta}</span>
          </div>
          <p className="mt-4 text-2xl font-semibold">{metric.value}</p>
          <p className="mt-1 text-sm text-steel">{metric.label}</p>
        </div>
      ))}
    </div>
  );
}
