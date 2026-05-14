import type { ReactNode } from "react";

export function SectionCard({
  title,
  description,
  action,
  children,
  id
}: {
  title: string;
  description?: string;
  action?: ReactNode;
  children: ReactNode;
  id?: string;
}) {
  return (
    <section className="rounded-md border border-[#d9ded8] bg-white" id={id}>
      <div className="flex items-start justify-between gap-4 border-b border-[#edf0ec] px-5 py-4">
        <div>
          <h3 className="text-base font-semibold">{title}</h3>
          {description ? <p className="mt-1 text-sm text-steel">{description}</p> : null}
        </div>
        {action}
      </div>
      <div className="p-5">{children}</div>
    </section>
  );
}
