from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq
import os
# Initialize FastAPI app
app = FastAPI()
load_dotenv()
# Replace 'your_groq_api_key' with your actual API key
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
client = Groq(api_key=GROQ_API_KEY)  # Initialize client with API key

# Request model for input validation
class TextInput(BaseModel):
    text: str

# Function to convert text to ISL gloss
def isl_gloss_translation(text: str) -> str:
    prompt = f"""
You are an expert in Indian Sign Language (ISL) gloss translation. Your task is to accurately convert standard English text into ISL gloss while ensuring proper grammar, normalization, and structuring. Follow these strict rules for ISL conversion while also placing words in an order that best conveys meaning in ISL.

1. ISL follows a topic-comment structure.
   - The main idea (topic) comes first.
   - The details (comment) follow after.
   - Example:
     - English: "I will go to school tomorrow."
     - ISL Gloss: TOMORROW SCHOOL GO

2. Prioritize meaning-based word order.
   - Place the most important or emphasized concept at the beginning.
   - Example:
     - English: "I am very tired and I don’t want to go to school tomorrow."
     - ISL Gloss: TIRED. TOMORROW SCHOOL GO NOT.

3. Remove auxiliary verbs (is, am, are, was, were, will, have, had, etc.).
   - English: "She is happy."
   - ISL Gloss: SHE HAPPY

4. Remove articles (a, an, the).
   - English: "The boy is playing with a ball."
   - ISL Gloss: BOY PLAY BALL

5. Remove prepositions (on, in, at, with, etc.).
   - English: "The book is on the table."
   - ISL Gloss: BOOK TABLE

6. No tense inflections (indicate past or future separately).
   - English: "I had eaten food."
   - ISL Gloss: PAST FOOD EAT

7. Minimize pronoun dont ommit.
   - English: "He loves her."
   - ISL Gloss: HE LOVE HER

8. Time and place come first.
   - English: "I will meet you at the park in the evening."
   - ISL Gloss: EVENING PARK MEET

9. Questions move wh-words to the end.
   - English: "Where is my phone?"
   - ISL Gloss: MY PHONE WHERE

10. Negation appears at the end.
   - English: "I do not like spicy food."
   - ISL Gloss: SPICY FOOD LIKE NOT

11. Commands and imperatives use direct verbs.
   - English: "Give me the book."
   - ISL Gloss: BOOK GIVE ME

12. Consider context and natural ISL flow when structuring words. Words should be placed in an order that conveys the intended meaning in the most natural ISL way.

Normalize spelling, correct punctuation, and return the final output in all uppercase. Only return the ISL gloss output without explanation.

Now process the following text:
{text}
"""

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=1,
        max_tokens=256,
        top_p=1,
        stream=False,
    )
    return completion.choices[0].message.content.strip()

# API endpoint to receive text and return ISL gloss
@app.post("/translate")
def translate_text(input_data: TextInput):
    try:
        gloss_text = isl_gloss_translation(input_data.text)
        return {"isl_gloss": gloss_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
