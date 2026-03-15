export async function POST(req) {
  const { system, messages } = await req.json();

  const response = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "content-type": "application/json",
      "x-api-key": process.env.ANTHROPIC_API_KEY,
      "anthropic-version": "2023-06-01",
    },
    body: JSON.stringify({
      model: "claude-haiku-4-5-20251001",
      max_tokens: 1000,
      system,
      messages,
    }),
  });

  const data = await response.json();

  if (data.error) {
    return Response.json({ error: data.error.message }, { status: 400 });
  }

  return Response.json({ reply: data.content[0].text });
}
