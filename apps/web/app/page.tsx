import { BrainCircuit, DatabaseZap, FileText, SlidersHorizontal } from "lucide-react";

import { AppShell } from "@/components/app-shell";
import { EvaluationGrid } from "@/components/evaluation-grid";
import { HighlightList } from "@/components/highlight-list";
import { ReportPanel } from "@/components/report-panel";
import { ScriptBoard } from "@/components/script-board";
import { SectionCard } from "@/components/section-card";
import { TimelinePanel } from "@/components/timeline-panel";
import { UploadGrid } from "@/components/upload-grid";
import { WorkflowPanel } from "@/components/workflow-panel";
import {
  evaluationMetrics,
  highlightClips,
  projectAssets,
  reportSections,
  scriptDrafts,
  timelineSegments,
  workflowSteps
} from "@/lib/mock-data";

const knowledgeCards = [
  {
    title: "Product RAG",
    body: "Indexes product details, FAQ, reviews, historical scripts, and selling point cards with metadata filters."
  },
  {
    title: "Multimodal segments",
    body: "Stores ASR, OCR, visual summaries, comments, and sales deltas as searchable timeline evidence."
  },
  {
    title: "Competitor memory",
    body: "Keeps competitor pricing, claims, review pain points, and livestream tactics for side-by-side analysis."
  }
];

const trainingTracks = [
  "Reranker fine-tuning for RAG relevance",
  "LoRA segment classifier for highlight pre-filtering",
  "DPO preference optimization for script quality",
  "Agent trajectory SFT for tool-calling decisions"
];

export default function HomePage() {
  return (
    <AppShell>
      <main className="mx-auto max-w-7xl space-y-5 px-5 py-5 lg:px-7">
        <section className="grid gap-5 xl:grid-cols-[1.35fr_0.65fr]" id="workspace">
          <SectionCard
            description="Collect the files and metrics needed for an end-to-end livestream replay analysis."
            id="assets"
            title="Project Assets"
          >
            <UploadGrid assets={projectAssets} />
          </SectionCard>

          <SectionCard
            action={
              <button className="inline-flex h-8 items-center gap-2 rounded-md border border-[#d9ded8] px-3 text-xs font-medium text-steel">
                <SlidersHorizontal size={14} />
                Configure
              </button>
            }
            description="Each step maps to a specialized agent or toolchain."
            id="agents"
            title="Agent Workflow"
          >
            <WorkflowPanel steps={workflowSteps} />
          </SectionCard>
        </section>

        <EvaluationGrid metrics={evaluationMetrics} />

        <section className="grid gap-5 xl:grid-cols-[1fr_0.85fr]">
          <SectionCard
            description="Structured video evidence aligned by timestamp, ASR, OCR, visual tags, comments, and sales movement."
            title="Video Timeline"
          >
            <TimelinePanel segments={timelineSegments} />
          </SectionCard>

          <SectionCard description="Top clips scored by multimodal and business signals." title="Highlight Clips">
            <HighlightList clips={highlightClips} />
          </SectionCard>
        </section>

        <section className="grid gap-5 xl:grid-cols-[0.85fr_1.15fr]">
          <SectionCard
            action={<DatabaseZap className="text-mint" size={20} />}
            description="Knowledge stores that ground the agent's answers and reports."
            id="rag"
            title="RAG Knowledge Layer"
          >
            <div className="grid gap-3">
              {knowledgeCards.map((card) => (
                <article className="rounded-md border border-[#e3e7e2] p-4" key={card.title}>
                  <h4 className="text-sm font-semibold">{card.title}</h4>
                  <p className="mt-2 text-sm leading-5 text-steel">{card.body}</p>
                </article>
              ))}
            </div>
          </SectionCard>

          <SectionCard
            action={<BrainCircuit className="text-amber" size={20} />}
            description="Training modules are shown as first-class project tracks, not hidden implementation details."
            title="Model Optimization Tracks"
          >
            <div className="grid gap-3 md:grid-cols-2">
              {trainingTracks.map((track, index) => (
                <div className="rounded-md border border-[#e3e7e2] p-4" key={track}>
                  <span className="flex h-7 w-7 items-center justify-center rounded-md bg-[#fff4e5] text-sm font-semibold text-amber">
                    {index + 1}
                  </span>
                  <p className="mt-3 text-sm font-medium leading-5">{track}</p>
                </div>
              ))}
            </div>
          </SectionCard>
        </section>

        <section className="grid gap-5 xl:grid-cols-[0.9fr_1.1fr]">
          <SectionCard
            action={<FileText className="text-mint" size={20} />}
            description="Grounded findings with timestamped evidence and next-session actions."
            title="Replay Report"
          >
            <ReportPanel sections={reportSections} />
          </SectionCard>

          <SectionCard
            description="Generated drafts include platform, hook, voiceover, storyboard, cover copy, and export actions."
            id="scripts"
            title="Short-Video Scripts"
          >
            <ScriptBoard scripts={scriptDrafts} />
          </SectionCard>
        </section>

        <SectionCard
          description="These metrics make the project interview-ready by showing retrieval, agent, highlight, and generation quality."
          id="evaluation"
          title="Evaluation System"
        >
          <div className="grid gap-4 md:grid-cols-3">
            <EvaluationNote title="Retrieval" body="Track Recall@K, MRR, and NDCG@10 before and after reranker fine-tuning." />
            <EvaluationNote title="Agent" body="Track tool-call success, retry count, trace completeness, and structured-output validity." />
            <EvaluationNote title="Business" body="Track highlight Top-K hit rate, report factuality, and script preference win rate." />
          </div>
        </SectionCard>
      </main>
    </AppShell>
  );
}

function EvaluationNote({ title, body }: { title: string; body: string }) {
  return (
    <article className="rounded-md border border-[#e3e7e2] p-4">
      <h4 className="text-sm font-semibold">{title}</h4>
      <p className="mt-2 text-sm leading-6 text-steel">{body}</p>
    </article>
  );
}
