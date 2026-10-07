import { NextRequest, NextResponse } from "next/server";

const BACKEND_URL = process.env.BACKEND_INTERNAL_URL || process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

async function proxyHandler(req: NextRequest, { params }: { params: Promise<{ slug: string[] }> }) {
  const resolvedParams = await params;
  const path = resolvedParams.slug.join("/");
  const searchParams = req.nextUrl.searchParams.toString();
  const targetUrl = `${BACKEND_URL.replace(/\/$/, "")}/api/v1/${path}${searchParams ? `?${searchParams}` : ""}`;

  try {
    const forwardHeaders: Record<string, string> = {};
    req.headers.forEach((value, key) => {
      const lower = key.toLowerCase();
      if (!["host", "connection", "content-length", "transfer-encoding"].includes(lower)) {
        forwardHeaders[lower] = value;
      }
    });

    let body: any = undefined;
    if (req.method !== "GET" && req.method !== "HEAD") {
      try {
        body = await req.arrayBuffer();
      } catch {
        body = undefined;
      }
    }

    const res = await fetch(targetUrl, {
      method: req.method,
      headers: forwardHeaders,
      body,
      cache: "no-store",
    });

    const data = await res.arrayBuffer();
    const responseHeaders = new Headers();
    res.headers.forEach((value, key) => {
      const lower = key.toLowerCase();
      if (!["content-length", "transfer-encoding", "content-encoding", "connection"].includes(lower)) {
        responseHeaders.set(key, value);
      }
    });

    return new NextResponse(data, {
      status: res.status,
      statusText: res.statusText,
      headers: responseHeaders,
    });
  } catch (err: any) {
    console.error(`[Next.js API Proxy Error] Failed to proxy ${req.method} ${targetUrl}:`, err);
    return NextResponse.json(
      {
        success: false,
        message: "Failed to connect to SkillSathi backend service. Please ensure FastAPI backend is running on port 8000.",
        error: err.message || String(err),
      },
      { status: 502 }
    );
  }
}

export const GET = proxyHandler;
export const POST = proxyHandler;
export const PUT = proxyHandler;
export const PATCH = proxyHandler;
export const DELETE = proxyHandler;
export const OPTIONS = proxyHandler;

