from transformers import pipeline
import re

def load_summarizer():
    return pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize(text):
    result = load_summarizer()(text[:1024], max_length=150, min_length=30, do_sample=False)
    return result[0]['summary_text'] # type: ignore

def extract_action_items(text):
    action_keywords = re.compile(
          r'\b(will|shall|going to|needs? to|should|must|have to|'
          r'action item|todo|follow.?up|next step)\b',
          re.IGNORECASE
      )
    sentences = re.split(r'(?<=[.!?])\s+', text)
    items = []
    for sentence in sentences:
          if action_keywords.search(sentence):
              items.append(sentence.strip())
    
    return items[:10]


