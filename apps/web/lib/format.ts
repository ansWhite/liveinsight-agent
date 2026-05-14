export function cn(...classes: Array<string | false | null | undefined>): string {
  return classes.filter(Boolean).join(" ");
}

export function scoreColor(score: number): string {
  if (score >= 88) {
    return "bg-[#e7f4ee] text-mint";
  }
  if (score >= 78) {
    return "bg-[#fff4e5] text-amber";
  }
  return "bg-[#fbeceb] text-coral";
}
