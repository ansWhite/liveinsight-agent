import {
  BarChart3,
  BrainCircuit,
  Clapperboard,
  DatabaseZap,
  FileText,
  MessagesSquare,
  SearchCheck,
  Sparkles,
  UploadCloud,
  Video
} from "lucide-react";

import type {
  EvaluationMetric,
  HighlightClip,
  ProjectAsset,
  ReportSection,
  ScriptDraft,
  TimelineSegment,
  WorkflowStep
} from "./types";

export const projectAssets: ProjectAsset[] = [
  {
    id: "video",
    kind: "video",
    label: "Livestream replay",
    description: "MP4, MOV, or FLV replay file",
    acceptedFormats: ".mp4 .mov .flv",
    required: true
  },
  {
    id: "product",
    kind: "product",
    label: "Product materials",
    description: "Title, detail page, FAQ, and selling points",
    acceptedFormats: ".pdf .md .txt .docx",
    required: true
  },
  {
    id: "comments",
    kind: "comments",
    label: "Comments and danmaku",
    description: "Timestamped user questions and reactions",
    acceptedFormats: ".csv .json",
    required: false
  },
  {
    id: "metrics",
    kind: "metrics",
    label: "Sales metrics",
    description: "Clicks, add-to-cart, orders, and GMV timeline",
    acceptedFormats: ".csv .xlsx",
    required: false
  },
  {
    id: "competitor",
    kind: "competitor",
    label: "Competitor evidence",
    description: "Competitor product page or livestream notes",
    acceptedFormats: ".pdf .md .txt .csv",
    required: false
  }
];

export const workflowSteps: WorkflowStep[] = [
  {
    id: "parse",
    name: "Multimodal parsing",
    owner: "Video Understanding Agent",
    status: "completed",
    progress: 100,
    detail: "Video slicing, keyframes, ASR, OCR, and visual summary extraction."
  },
  {
    id: "index",
    name: "RAG indexing",
    owner: "Product RAG Agent",
    status: "running",
    progress: 72,
    detail: "Product documents, comments, and segment summaries are being indexed."
  },
  {
    id: "metrics",
    name: "Metric alignment",
    owner: "Data Analysis Agent",
    status: "running",
    progress: 64,
    detail: "Sales, click, and comment timelines are aligned with video segments."
  },
  {
    id: "highlight",
    name: "Highlight scoring",
    owner: "Highlight Detection Agent",
    status: "queued",
    progress: 0,
    detail: "Candidate clips will be ranked with model and business signals."
  },
  {
    id: "report",
    name: "Replay report",
    owner: "Report Agent",
    status: "queued",
    progress: 0,
    detail: "A grounded report will cite timestamps, comments, and product evidence."
  },
  {
    id: "script",
    name: "Script generation",
    owner: "Content Generation Agent",
    status: "queued",
    progress: 0,
    detail: "Short-video titles, hooks, storyboards, subtitles, and cover copy."
  }
];

export const timelineSegments: TimelineSegment[] = [
  {
    id: "seg-001",
    start: "00:00",
    end: "00:30",
    title: "Opening offer and product positioning",
    asr: "This moisturizer is for users who need repair without a sticky finish.",
    ocr: ["Limited coupon", "Final price 99"],
    tags: ["hook", "discount", "product-intro"],
    score: 76,
    salesDelta: 42,
    comments: 18
  },
  {
    id: "seg-002",
    start: "01:52",
    end: "02:36",
    title: "High-density Q&A and product close-up",
    asr: "Sensitive skin users should check these ingredients before buying.",
    ocr: ["Sensitive skin tested", "Coupon ends soon"],
    tags: ["qa", "close-up", "high-intent"],
    score: 91,
    salesDelta: 138,
    comments: 64
  },
  {
    id: "seg-003",
    start: "07:10",
    end: "08:05",
    title: "Texture demo and objection handling",
    asr: "It absorbs in about ten seconds, so it works under makeup.",
    ocr: ["Before makeup", "Lightweight texture"],
    tags: ["demo", "objection", "visual-proof"],
    score: 84,
    salesDelta: 92,
    comments: 41
  }
];

export const highlightClips: HighlightClip[] = [
  {
    id: "clip-001",
    time: "01:52 - 02:36",
    score: 91,
    title: "Sensitive skin objection turned into conversion",
    reason: "Discount OCR, product close-up, and dense user questions overlap with the largest sales delta.",
    useCase: "Best as a short-video opening hook."
  },
  {
    id: "clip-002",
    time: "07:10 - 08:05",
    score: 84,
    title: "Texture demo with clear visual proof",
    reason: "The host answers a common objection while the product is shown in use.",
    useCase: "Best as a comparison or trust-building segment."
  }
];

export const reportSections: ReportSection[] = [
  {
    title: "Conversion driver",
    body: "The strongest conversion window appears when discount information, visual proof, and user questions appear in the same segment.",
    evidence: ["01:52-02:36 sales delta +138", "OCR detected coupon deadline", "64 comments aligned to the segment"]
  },
  {
    title: "Content gap",
    body: "The opening introduces the product clearly, but the first high-trust proof arrives too late. Move ingredient safety and texture proof into the first three minutes.",
    evidence: ["00:00-00:30 has only 18 comments", "07:10-08:05 contains strong texture proof"]
  },
  {
    title: "Next-session action",
    body: "Prepare a fixed Q&A card for sensitive skin, coupon claim path, and texture comparison. The agent should watch for these three topics during the next replay.",
    evidence: ["Top user questions repeat across two high-score segments"]
  }
];

export const scriptDrafts: ScriptDraft[] = [
  {
    id: "script-001",
    title: "Sensitive skin buyers should check these three details first",
    platform: "Douyin",
    hook: "Do not buy another moisturizer until you verify these three points.",
    voiceover: [
      "First, check whether the product directly addresses your skin concern.",
      "Second, compare the livestream coupon with the normal shelf price.",
      "Third, look at real user questions before deciding."
    ],
    storyboard: [
      "Product close-up with price overlay.",
      "Host texture demo and ingredient caption.",
      "Comment screenshot plus coupon recap."
    ],
    coverCopy: "Sensitive skin checklist"
  },
  {
    id: "script-002",
    title: "The livestream moment that made users ask to buy",
    platform: "Xiaohongshu",
    hook: "This one answer changed the whole comment section.",
    voiceover: [
      "The host did not start with a slogan.",
      "She answered the exact concern users were typing.",
      "Then the visual demo made the claim easier to trust."
    ],
    storyboard: ["Question overlay.", "Host answer.", "Texture close-up.", "Offer recap."],
    coverCopy: "From question to order"
  }
];

export const evaluationMetrics: EvaluationMetric[] = [
  { label: "RAG NDCG@10", value: "0.72", delta: "+0.11", tone: "mint", icon: SearchCheck },
  { label: "Highlight Top-K", value: "68%", delta: "+9%", tone: "amber", icon: Clapperboard },
  { label: "Tool success", value: "94%", delta: "+4%", tone: "mint", icon: BrainCircuit },
  { label: "Script win rate", value: "61%", delta: "+13%", tone: "coral", icon: FileText }
];

export const navigation = [
  { label: "Workspace", icon: Video, href: "#workspace" },
  { label: "Assets", icon: UploadCloud, href: "#assets" },
  { label: "RAG", icon: DatabaseZap, href: "#rag" },
  { label: "Agents", icon: Sparkles, href: "#agents" },
  { label: "Scripts", icon: MessagesSquare, href: "#scripts" },
  { label: "Evaluation", icon: BarChart3, href: "#evaluation" }
];
