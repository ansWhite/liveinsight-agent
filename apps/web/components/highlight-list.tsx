import { Clapperboard } from "lucide-react";

import { scoreColor } from "@/lib/format";
import type { HighlightClip } from "@/lib/types";

export function HighlightList({ clips }: { clips: HighlightClip[] }) {
  return (
    <div className="space-y-3">
      {clips.map((clip) => (
        <article className="rounded-md border border-[#e3e7e2] p-4" key={clip.id}>
          <div className="flex items-start justify-between gap-3">
            <div>
              <p className="inline-flex items-center gap-2 text-xs font-medium text-steel">
                <Clapperboard size={14} />
                {clip.time}
              </p>
              <h4 className="mt-2 text-sm font-semibold">{clip.title}</h4>
            </div>
            <span className={`rounded-md px-2 py-1 text-xs font-semibold ${scoreColor(clip.score)}`}>{clip.score}</span>
          </div>
          <p className="mt-3 text-sm leading-5 text-steel">{clip.reason}</p>
          <p className="mt-3 rounded-md bg-[#fbfcfa] px-3 py-2 text-sm text-ink">{clip.useCase}</p>
        </article>
      ))}
    </div>
  );
}
