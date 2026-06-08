import type { Metadata } from "next";
import "./styles.css";

export const metadata: Metadata = {
  title: "Shopping Guide Agent",
  description: "Multimodal RAG shopping guide Agent demo",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  );
}
