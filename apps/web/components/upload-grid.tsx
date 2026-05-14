import { CheckCircle2, UploadCloud } from "lucide-react";

import type { ProjectAsset } from "@/lib/types";

export function UploadGrid({ assets }: { assets: ProjectAsset[] }) {
  return (
    <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
      {assets.map((asset) => (
        <label
          className="group flex min-h-36 cursor-pointer flex-col justify-between rounded-md border border-dashed border-[#b9c2ba] bg-[#fbfcfa] p-4 transition hover:border-mint hover:bg-[#f4faf7]"
          key={asset.id}
        >
          <input accept={asset.acceptedFormats.replaceAll(" ", ",")} className="sr-only" type="file" />
          <div className="flex items-start justify-between gap-3">
            <div>
              <div className="flex items-center gap-2">
                <span className="font-medium">{asset.label}</span>
                {asset.required ? (
                  <span className="rounded-md bg-[#fbeceb] px-2 py-0.5 text-xs font-medium text-coral">Required</span>
                ) : null}
              </div>
              <p className="mt-2 text-sm leading-5 text-steel">{asset.description}</p>
            </div>
            <UploadCloud className="text-mint" size={20} />
          </div>
          <div className="mt-4 flex items-center justify-between gap-3 text-xs text-steel">
            <span>{asset.acceptedFormats}</span>
            <span className="inline-flex items-center gap-1 opacity-0 transition group-hover:opacity-100">
              <CheckCircle2 size={14} />
              Ready
            </span>
          </div>
        </label>
      ))}
    </div>
  );
}
