import { Quote } from "lucide-react";

import type { ReportSection } from "@/lib/types";

export function ReportPanel({ sections }: { sections: ReportSection[] }) {
  return (
    <div className="space-y-4">
      {sections.map((section) => (
        <article className="rounded-md border border-[#e3e7e2] p-4" key={section.title}>
          <h4 className="text-sm font-semibold">{section.title}</h4>
          <p className="mt-2 text-sm leading-6 text-steel">{section.body}</p>
          <div className="mt-3 space-y-2">
            {section.evidence.map((item) => (
              <p className="flex items-start gap-2 text-xs leading-5 text-steel" key={item}>
                <Quote className="mt-0.5 shrink-0 text-mint" size={13} />
                {item}
              </p>
            ))}
          </div>
        </article>
      ))}
    </div>
  );
}
