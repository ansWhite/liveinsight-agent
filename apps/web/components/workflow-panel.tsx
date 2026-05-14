import { CheckCircle2, CircleDashed, Loader2 } from "lucide-react";
import type { ReactNode } from "react";

import { cn } from "@/lib/format";
import type { AgentStatus, WorkflowStep } from "@/lib/types";

const statusIcon: Record<AgentStatus, ReactNode> = {
  completed: <CheckCircle2 size={17} />,
  running: <Loader2 className="animate-spin" size={17} />,
  queued: <CircleDashed size={17} />,
  blocked: <CircleDashed size={17} />
};

export function WorkflowPanel({ steps }: { steps: WorkflowStep[] }) {
  return (
    <div className="space-y-3">
      {steps.map((step) => (
        <div className="rounded-md border border-[#e3e7e2] p-4" key={step.id}>
          <div className="flex items-start gap-3">
            <div
              className={cn(
                "mt-0.5 flex h-8 w-8 items-center justify-center rounded-md",
                step.status === "completed" && "bg-[#e7f4ee] text-mint",
                step.status === "running" && "bg-[#fff4e5] text-amber",
                step.status === "queued" && "bg-[#eef2ef] text-steel",
                step.status === "blocked" && "bg-[#fbeceb] text-coral"
              )}
            >
              {statusIcon[step.status]}
            </div>
            <div className="min-w-0 flex-1">
              <div className="flex items-center justify-between gap-3">
                <div>
                  <h4 className="text-sm font-semibold">{step.name}</h4>
                  <p className="mt-1 text-xs text-steel">{step.owner}</p>
                </div>
                <span className="text-sm font-semibold">{step.progress}%</span>
              </div>
              <div className="mt-3 h-2 rounded-full bg-[#edf0ec]">
                <div className="h-2 rounded-full bg-mint" style={{ width: `${step.progress}%` }} />
              </div>
              <p className="mt-3 text-sm leading-5 text-steel">{step.detail}</p>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
