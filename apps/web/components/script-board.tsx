import { Copy, Download } from "lucide-react";

import type { ScriptDraft } from "@/lib/types";

export function ScriptBoard({ scripts }: { scripts: ScriptDraft[] }) {
  return (
    <div className="grid gap-4 xl:grid-cols-2">
      {scripts.map((script) => (
        <article className="rounded-md border border-[#e3e7e2] p-4" key={script.id}>
          <div className="flex items-start justify-between gap-3">
            <div>
              <p className="text-xs font-medium uppercase tracking-[0.16em] text-mint">{script.platform}</p>
              <h4 className="mt-1 text-sm font-semibold">{script.title}</h4>
            </div>
            <div className="flex gap-1">
              <button className="flex h-8 w-8 items-center justify-center rounded-md border border-[#d9ded8] text-steel" title="Copy">
                <Copy size={15} />
              </button>
              <button className="flex h-8 w-8 items-center justify-center rounded-md border border-[#d9ded8] text-steel" title="Export">
                <Download size={15} />
              </button>
            </div>
          </div>
          <p className="mt-3 rounded-md bg-[#fbfcfa] px-3 py-2 text-sm font-medium">{script.hook}</p>
          <div className="mt-4 grid gap-4 md:grid-cols-2">
            <div>
              <p className="text-xs font-semibold text-steel">Voiceover</p>
              <ol className="mt-2 space-y-2 text-sm leading-5 text-steel">
                {script.voiceover.map((line) => (
                  <li key={line}>{line}</li>
                ))}
              </ol>
            </div>
            <div>
              <p className="text-xs font-semibold text-steel">Storyboard</p>
              <ol className="mt-2 space-y-2 text-sm leading-5 text-steel">
                {script.storyboard.map((line) => (
                  <li key={line}>{line}</li>
                ))}
              </ol>
            </div>
          </div>
          <p className="mt-4 text-xs text-steel">Cover: {script.coverCopy}</p>
        </article>
      ))}
    </div>
  );
}
