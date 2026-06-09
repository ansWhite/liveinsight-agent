import type { Metadata } from "next";
import "./styles.css";

// Next.js 页面元信息，会显示在浏览器标题和搜索摘要里。
export const metadata: Metadata = {
  title: "Shopping Guide Agent",
  description: "Multimodal RAG shopping guide Agent demo",
};

// 全局布局文件。所有页面都会被包在这个 html/body 结构里。
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
