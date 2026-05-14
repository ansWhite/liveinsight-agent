import type { LucideIcon } from "lucide-react";

export type ProjectAssetKind = "video" | "product" | "comments" | "metrics" | "competitor";

export type AgentStatus = "queued" | "running" | "completed" | "blocked";

export type MetricTone = "mint" | "amber" | "coral" | "steel";

export interface ProjectAsset {
  id: string;
  kind: ProjectAssetKind;
  label: string;
  description: string;
  acceptedFormats: string;
  required: boolean;
}

export interface WorkflowStep {
  id: string;
  name: string;
  owner: string;
  status: AgentStatus;
  progress: number;
  detail: string;
}

export interface TimelineSegment {
  id: string;
  start: string;
  end: string;
  title: string;
  asr: string;
  ocr: string[];
  tags: string[];
  score: number;
  salesDelta: number;
  comments: number;
}

export interface HighlightClip {
  id: string;
  time: string;
  score: number;
  title: string;
  reason: string;
  useCase: string;
}

export interface ReportSection {
  title: string;
  body: string;
  evidence: string[];
}

export interface ScriptDraft {
  id: string;
  title: string;
  platform: string;
  hook: string;
  voiceover: string[];
  storyboard: string[];
  coverCopy: string;
}

export interface EvaluationMetric {
  label: string;
  value: string;
  delta: string;
  tone: MetricTone;
  icon: LucideIcon;
}
