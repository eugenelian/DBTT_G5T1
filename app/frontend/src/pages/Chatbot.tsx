import PageLayout from "@/components/PageLayout";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Send, Trash2, Bot, User } from "lucide-react";
import { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";

interface Message {
  role: "user" | "assistant";
  content: string;
  followUpQuestion?: string | null;
}

function parseAssistantResponse(text: string) {
  const cleaned = text.replace(/\\n/g, "\n");

  const match = cleaned.match(/<follow_up_question>(.*?)<\/follow_up_question>/s);

  const followUpQuestion = match ? match[1].trim() : null;

  const markdownContent = cleaned.replace(/<follow_up_question>.*?<\/follow_up_question>/s, "").trim();

  return { markdownContent, followUpQuestion };
}

const BASE_URL = import.meta.env.VITE_API_URL;

const Chatbot = () => {
  const [id, setId] = useState(crypto.randomUUID());
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendQuery = async (displayText: string, backendQuery?: string) => {
    const userMsg: Message = { role: "user", content: displayText };
    setMessages(prev => [...prev, userMsg]);
    setLoading(true);

    const queryToSend = backendQuery ?? displayText;

    try {
      const res = await fetch(`${BASE_URL}/api/v1/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: id,
          session_id: id,
          user_query: queryToSend
        })
      });

      const data = await res.json();

      const parsed = parseAssistantResponse(data.content || "No response");

      setMessages(prev => [
        ...prev,
        {
          role: "assistant",
          content: parsed.markdownContent,
          followUpQuestion: parsed.followUpQuestion
        }
      ]);
    } catch {
      setMessages(prev => [
        ...prev,
        {
          role: "assistant",
          content: "⚠️ Could not reach the server. Make sure the backend is running on localhost:8000."
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const query = input.trim();
    setInput("");

    await sendQuery(query);
  };

  return (
    <PageLayout
      title="AI Chatbot"
      subtitle="Converse with the medical AI assistant"
      actions={
        messages.length > 0 ? (
          <Button variant="outline" size="sm" onClick={() => setMessages([])}>
            <Trash2 size={14} className="mr-1.5" /> Clear Chat
          </Button>
        ) : undefined
      }
    >
      <div className="glass-card rounded-xl flex flex-col" style={{ height: "calc(100vh - 180px)" }}>
        <ScrollArea className="flex-1 p-5">
          {messages.length === 0 && (
            <div className="flex flex-col items-center justify-center h-full text-muted-foreground py-20">
              <Bot size={48} className="mb-4 text-primary/40" />
              <p className="font-display font-semibold text-lg">How can I help you today?</p>
              <p className="text-sm mt-1">Ask me anything about patient care, diagnosis, or medical information.</p>
            </div>
          )}
          <div className="space-y-4 max-w-3xl mx-auto">
            {messages.map((msg, i) => (
              <div key={i} className={`flex gap-3 ${msg.role === "user" ? "justify-end" : ""}`}>
                {msg.role === "assistant" && (
                  <div className="w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0">
                    <Bot size={16} className="text-primary" />
                  </div>
                )}
                <div className={`max-w-[75%] rounded-xl px-4 py-3 text-sm ${msg.role === "user" ? "bg-primary text-primary-foreground" : "bg-muted"}`}>
                  {msg.role === "assistant" ? (
                    <div className="prose prose-sm max-w-none">
                      <>
                        <ReactMarkdown>{msg.content}</ReactMarkdown>

                        {msg.followUpQuestion && (
                          <div className="mt-3">
                            <Button
                              size="sm"
                              variant="outline"
                              className="mt-2 w-full max-w-full whitespace-normal break-words text-left h-auto py-2"
                              onClick={() => sendQuery("Yes, I would like to know more", `I would like to know more about "${msg.followUpQuestion}"`)}
                            >
                              {msg.followUpQuestion}
                            </Button>
                          </div>
                        )}
                      </>
                    </div>
                  ) : (
                    msg.content
                  )}
                </div>
                {msg.role === "user" && (
                  <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center flex-shrink-0">
                    <User size={16} className="text-primary-foreground" />
                  </div>
                )}
              </div>
            ))}
            {loading && (
              <div className="flex gap-3">
                <div className="w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0">
                  <Bot size={16} className="text-primary" />
                </div>
                <div className="bg-muted rounded-xl px-4 py-3">
                  <div className="flex gap-1">
                    <span className="w-2 h-2 bg-muted-foreground/40 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                    <span className="w-2 h-2 bg-muted-foreground/40 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                    <span className="w-2 h-2 bg-muted-foreground/40 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
                  </div>
                </div>
              </div>
            )}
            <div ref={scrollRef} />
          </div>
        </ScrollArea>
        <div className="p-4 border-t border-border/50">
          <form
            onSubmit={e => {
              e.preventDefault();
              sendMessage();
            }}
            className="flex gap-2 max-w-3xl mx-auto"
          >
            <Input value={input} onChange={e => setInput(e.target.value)} placeholder="Type your message..." className="flex-1" disabled={loading} />
            <Button type="submit" disabled={!input.trim() || loading}>
              <Send size={16} />
            </Button>
          </form>
        </div>
      </div>
    </PageLayout>
  );
};

export default Chatbot;
