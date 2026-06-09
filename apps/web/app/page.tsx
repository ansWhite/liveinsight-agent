"use client";

import { FormEvent, useEffect, useRef, useState } from "react";
import { ImagePlus, Send, ThumbsDown, ThumbsUp } from "lucide-react";

type ProductCard = {
  product_id: string;
  title: string;
  price?: number | null;
  image_url?: string | null;
  reason: string;
};

type ChatMessage = {
  id: string;
  role: "user" | "assistant";
  content: string;
  cards?: ProductCard[];
};

// 默认调用 Next.js 内置 Demo API，保证只启动前端也能体验流式交互。
// 如果后续要切到 FastAPI，可在 .env.local 里配置 NEXT_PUBLIC_API_BASE_URL=http://localhost:8000。
const CHAT_STREAM_URL = process.env.NEXT_PUBLIC_API_BASE_URL
  ? `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/v1/chat/stream`
  : "/api/chat/stream";

function createId(prefix: string) {
  return `${prefix}_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
}

export default function Home() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "welcome",
      role: "assistant",
      content:
        "你好，我是电商智能导购。你可以告诉我预算、使用场景、品牌偏好，或者上传商品图片来做推荐。",
    },
  ]);
  const [input, setInput] = useState("预算3000以内，拍照好一点的手机推荐哪个？");
  const [isStreaming, setIsStreaming] = useState(false);
  const [error, setError] = useState("");
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  function appendAssistantText(messageId: string, content: string) {
    setMessages((current) =>
      current.map((message) =>
        message.id === messageId
          ? { ...message, content: `${message.content}${content}` }
          : message,
      ),
    );
  }

  function appendProductCard(messageId: string, card: ProductCard) {
    setMessages((current) =>
      current.map((message) =>
        message.id === messageId
          ? { ...message, cards: [...(message.cards ?? []), card] }
          : message,
      ),
    );
  }

  function handleSseBlock(block: string, assistantId: string) {
    const dataLines = block
      .split("\n")
      .filter((line) => line.startsWith("data:"))
      .map((line) => line.replace(/^data:\s?/, ""));

    if (dataLines.length === 0) {
      return;
    }

    const payload = JSON.parse(dataLines.join("\n"));
    if (payload.type === "text_delta") {
      appendAssistantText(assistantId, payload.content);
    }
    if (payload.type === "product_card") {
      appendProductCard(assistantId, payload.data);
    }
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const trimmed = input.trim();
    if (!trimmed || isStreaming) {
      return;
    }

    const userMessage: ChatMessage = {
      id: createId("user"),
      role: "user",
      content: trimmed,
    };
    const assistantId = createId("assistant");
    const assistantMessage: ChatMessage = {
      id: assistantId,
      role: "assistant",
      content: "",
      cards: [],
    };

    setMessages((current) => [...current, userMessage, assistantMessage]);
    setInput("");
    setError("");
    setIsStreaming(true);

    try {
      const response = await fetch(CHAT_STREAM_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          session_id: "demo-session",
          message: trimmed,
        }),
      });

      if (!response.ok || !response.body) {
        throw new Error("后端流式接口请求失败");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) {
          break;
        }

        buffer += decoder.decode(value, { stream: true });
        const blocks = buffer.split(/\r?\n\r?\n/);
        buffer = blocks.pop() ?? "";
        for (const block of blocks) {
          handleSseBlock(block, assistantId);
        }
      }

      if (buffer.trim()) {
        handleSseBlock(buffer, assistantId);
      }
    } catch (caught) {
      const message = caught instanceof Error ? caught.message : "未知错误";
      setError(`${message}。请确认前端开发服务器仍在运行。`);
      appendAssistantText(assistantId, "抱歉，我暂时连接不上流式接口，请稍后再试。");
    } finally {
      setIsStreaming(false);
    }
  }

  return (
    <main className="shell">
      <section className="chat">
        {/* 顶部栏：展示产品名，并预留图片上传入口。 */}
        <header className="topbar">
          <div>
            <p className="eyebrow">Multimodal RAG Agent</p>
            <h1>电商智能导购</h1>
          </div>
          <button className="iconButton" aria-label="上传图片">
            <ImagePlus size={20} />
          </button>
        </header>

        {/* 对话区：未来会按消息列表渲染用户消息、AI 流式文本和商品卡片。 */}
        <div className="messages">
          {messages.map((message) => (
            <div className="messageGroup" key={message.id}>
              <div className={`bubble ${message.role}`}>
                {message.content || (message.role === "assistant" ? "正在思考..." : "")}
              </div>

              {message.cards && message.cards.length > 0 ? (
                <div className="cards">
                  {message.cards.map((card) => (
                    // 商品卡片是导购 Agent 的关键输出，不只是文本推荐。
                    <article className="productCard" key={card.product_id}>
                      <div className="imageSlot" />
                      <div>
                        <h2>{card.title}</h2>
                        {card.price ? <p className="price">RMB {card.price}</p> : null}
                        <p>{card.reason}</p>
                      </div>
                    </article>
                  ))}
                </div>
              ) : null}
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        {/* 输入区：反馈按钮、文本输入和发送按钮；后续会接真实状态和接口。 */}
        <form className="composer" onSubmit={handleSubmit}>
          <button className="iconButton" aria-label="点赞">
            <ThumbsUp size={18} />
          </button>
          <button className="iconButton" aria-label="点踩">
            <ThumbsDown size={18} />
          </button>
          <input
            disabled={isStreaming}
            onChange={(event) => setInput(event.target.value)}
            placeholder="说出预算、场景、偏好，或上传图片..."
            value={input}
          />
          <button className="sendButton" aria-label="发送" disabled={isStreaming}>
            <Send size={18} />
          </button>
          {error ? <p className="errorText">{error}</p> : null}
        </form>
      </section>
    </main>
  );
}
