import { MessageSquareText, ShoppingCart, Tag } from "lucide-react";

import { scoreColor } from "@/lib/format";
import type { TimelineSegment } from "@/lib/types";

export function TimelinePanel({ segments }: { segments: TimelineSegment[] }) {
  return (
    <div className="space-y-3">
      {segments.map((segment) => (
        <article className="rounded-md border border-[#e3e7e2] p-4" key={segment.id}>
          <div className="flex flex-wrap items-start justify-between gap-3">
            <div>
              <p className="text-xs font-medium text-steel">
                {segment.start} - {segment.end}
              </p>
              <h4 className="mt-1 text-sm font-semibold">{segment.title}</h4>
            </div>
            <span className={`rounded-md px-2 py-1 text-xs font-semibold ${scoreColor(segment.score)}`}>
              {segment.score}
            </span>
          </div>
          <p className="mt-3 text-sm leading-6 text-steel">{segment.asr}</p>
          <div className="mt-3 flex flex-wrap gap-2">
            {segment.tags.map((tag) => (
              <span className="inline-flex items-center gap-1 rounded-md bg-[#eef2ef] px-2 py-1 text-xs text-steel" key={tag}>
                <Tag size={12} />
                {tag}
              </span>
            ))}
          </div>
          <div className="mt-4 grid gap-2 text-xs text-steel sm:grid-cols-3">
            <span className="inline-flex items-center gap-1">
              <ShoppingCart size={14} />
              Sales +{segment.salesDelta}
            </span>
            <span className="inline-flex items-center gap-1">
              <MessageSquareText size={14} />
              {segment.comments} comments
            </span>
            <span>OCR: {segment.ocr.join(", ")}</span>
          </div>
        </article>
      ))}
    </div>
  );
}
