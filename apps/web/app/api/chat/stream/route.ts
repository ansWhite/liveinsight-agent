import { readFile } from "node:fs/promises";
import path from "node:path";

type ChatRequest = {
  session_id: string;
  message: string;
};

type SampleProduct = {
  id: string;
  title: string;
  price: number;
  attributes?: {
    camera?: string;
    battery?: string;
  };
};

export const runtime = "nodejs";

function delay(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function loadSampleProduct(): Promise<SampleProduct> {
  // Next.js dev server 的工作目录通常是 apps/web，所以这里回到项目根目录读取 sample 数据。
  const productsFile = path.resolve(process.cwd(), "../../data/samples/products.json");
  const raw = await readFile(productsFile, "utf-8");
  const products = JSON.parse(raw) as SampleProduct[];
  return products[0];
}

function buildDemoAnswer(userMessage: string, product: SampleProduct) {
  // 这里先用规则拼接模拟“检索 + 生成”的结果，后续会替换成真实 RAG 和 LLM。
  const camera = product.attributes?.camera ?? "拍照能力较好";
  const battery = product.attributes?.battery ?? "续航表现较好";

  return (
    `我根据你的问题「${userMessage}」先做了一次本地商品样例匹配。` +
    `当前更推荐 ${product.title}，价格约 ${product.price} 元，符合 3000 以内的预算。` +
    `它的核心优势是 ${camera} 和 ${battery}，比较适合重视拍照、续航和性价比的用户。` +
    "需要注意的是，它不是专业游戏手机，长焦能力也不如旗舰机型。" +
    "如果你更看重游戏性能或轻薄手感，我可以继续帮你换一组筛选条件。"
  );
}

function encodeSse(event: string, data: unknown) {
  return `event: ${event}\ndata: ${JSON.stringify(data)}\n\n`;
}

export async function POST(request: Request) {
  const body = (await request.json()) as ChatRequest;
  const product = await loadSampleProduct();
  const answer = buildDemoAnswer(body.message, product);
  const encoder = new TextEncoder();

  const stream = new ReadableStream({
    async start(controller) {
      // text_delta 模拟大模型逐字流式输出。
      for (const char of answer) {
        controller.enqueue(
          encoder.encode(
            encodeSse("message", {
              type: "text_delta",
              content: char,
            }),
          ),
        );
        await delay(10);
      }

      // product_card 事件用于驱动前端实时渲染商品卡片。
      controller.enqueue(
        encoder.encode(
          encodeSse("message", {
            type: "product_card",
            data: {
              product_id: product.id,
              title: product.title,
              price: product.price,
              image_url: "",
              reason: "符合预算，主摄和续航表现更适合日常拍照需求。",
            },
          }),
        ),
      );

      controller.enqueue(encoder.encode(encodeSse("done", {})));
      controller.close();
    },
  });

  return new Response(stream, {
    headers: {
      "Content-Type": "text/event-stream; charset=utf-8",
      "Cache-Control": "no-cache, no-transform",
      Connection: "keep-alive",
    },
  });
}
