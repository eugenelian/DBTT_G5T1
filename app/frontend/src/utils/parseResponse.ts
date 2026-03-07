export type ParsedResponse = {
  markdownContent: string;
  followUpQuestion: string | null;
};

export function parseResponse(text: string): ParsedResponse {
  // Normalize escaped newlines
  const cleaned = text.replace(/\\n/g, "\n");

  const match = cleaned.match(/<follow_up_question>(.*?)<\/follow_up_question>/s);

  const followUpQuestion = match ? match[1].trim() : null;

  const markdownContent = cleaned.replace(/<follow_up_question>.*?<\/follow_up_question>/s, "").trim();

  return {
    markdownContent,
    followUpQuestion
  };
}
