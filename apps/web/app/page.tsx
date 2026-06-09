import { ImagePlus, Send, ThumbsDown, ThumbsUp } from "lucide-react";

// 当前是静态演示商品卡片。
// 后续会从后端 SSE 的 product_card 事件中实时生成这些卡片。
const productCards = [
  {
    title: "Demo Phone Pro",
    price: "2899",
    reason: "主摄表现稳定，续航和预算都匹配。",
  },
  {
    title: "Demo Phone Lite",
    price: "2299",
    reason: "更轻薄，适合日常使用和礼物场景。",
  },
];

export default function Home() {
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
          <div className="bubble user">预算3000以内，拍照好一点的手机推荐哪个？</div>
          <div className="bubble assistant">
            我会结合预算、拍照需求、续航和商品知识库来推荐。下面是当前更合适的候选：
          </div>

          <div className="cards">
            {productCards.map((card) => (
              // 商品卡片是导购 Agent 的关键输出，不只是文本推荐。
              <article className="productCard" key={card.title}>
                <div className="imageSlot" />
                <div>
                  <h2>{card.title}</h2>
                  <p className="price">RMB {card.price}</p>
                  <p>{card.reason}</p>
                </div>
              </article>
            ))}
          </div>
        </div>

        {/* 输入区：反馈按钮、文本输入和发送按钮；后续会接真实状态和接口。 */}
        <footer className="composer">
          <button className="iconButton" aria-label="点赞">
            <ThumbsUp size={18} />
          </button>
          <button className="iconButton" aria-label="点踩">
            <ThumbsDown size={18} />
          </button>
          <input placeholder="说出预算、场景、偏好，或上传图片..." />
          <button className="sendButton" aria-label="发送">
            <Send size={18} />
          </button>
        </footer>
      </section>
    </main>
  );
}
