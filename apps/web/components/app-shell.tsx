import { Play, Settings } from "lucide-react";
import type { ReactNode } from "react";

import { navigation } from "@/lib/mock-data";

export function AppShell({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen bg-[#f7f8f6] text-ink">
      <aside className="fixed inset-y-0 left-0 hidden w-64 border-r border-[#d9ded8] bg-white lg:block">
        <div className="border-b border-[#e2e6e1] px-5 py-5">
          <h1 className="text-lg font-semibold tracking-normal">LiveInsight Agent</h1>
          <p className="mt-1 text-xs leading-5 text-steel">Multimodal live-commerce analysis workspace</p>
        </div>
        <nav className="space-y-1 px-3 py-4">
          {navigation.map((item) => (
            <a
              className="flex items-center gap-3 rounded-md px-3 py-2 text-sm text-steel transition hover:bg-[#eef2ef] hover:text-ink"
              href={item.href}
              key={item.label}
            >
              <item.icon size={17} />
              {item.label}
            </a>
          ))}
        </nav>
      </aside>

      <div className="lg:pl-64">
        <header className="sticky top-0 z-10 border-b border-[#d9ded8] bg-white/95 backdrop-blur">
          <div className="flex min-h-16 items-center justify-between gap-4 px-5 lg:px-7">
            <div>
              <p className="text-xs font-medium uppercase tracking-[0.18em] text-mint">Workspace</p>
              <h2 className="text-lg font-semibold">May skincare livestream replay</h2>
            </div>
            <div className="flex items-center gap-2">
              <button className="hidden h-9 items-center gap-2 rounded-md border border-[#d9ded8] px-3 text-sm font-medium text-steel md:inline-flex">
                <Settings size={16} />
                Settings
              </button>
              <button className="inline-flex h-9 items-center gap-2 rounded-md bg-ink px-3 text-sm font-medium text-white">
                <Play size={16} />
                Run analysis
              </button>
            </div>
          </div>
        </header>
        {children}
      </div>
    </div>
  );
}
