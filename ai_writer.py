import json
from openai import OpenAI
from config import API_KEY, TEXT_MODEL

if not API_KEY:
    raise RuntimeError(
        "OPENAI_API_KEY is not set. "
        "Set your API key before running the program."
    )self.client
Welcome to Gboard clipboard, any text you copy will be saved here.
client = OpenAI(api_key=API_KEY)


def ask_ai(prompt):
    response = client.responses.create(
        model=TEXT_MODEL,
        input=prompt
    )

    return response.output_text


def analyze_poem(title, urdu_text):

    prompt = f"""
You are an expert in Urdu literature and Allama Muhammad Iqbal.

We are preparing an educational bilingual ebook about five poems
from Bang-e-Dara.

Poem title:
{title}

Original Urdu poem:
{urdu_text}

Prepare the following material.

1. ENGLISH TRANSLATION
Translate the poem faithfully into clear literary English.
Do not invent lines that are not present.

2. ENGLISH SUMMARY
Explain the central meaning and message of the poem.

3. URDU SUMMARY
Explain the central meaning in clear modern Urdu.

4. DIFFICULT WORDS
Select important difficult Urdu words or expressions from the poem.
For each give:
- Urdu word
- English meaning
- Urdu explanation

5. IQBAL'S PERSONALITY
Based ONLY on this poem, explain what it reveals about Iqbal's
personality, values, ideas and worldview.

6. IMAGE DESCRIPTION
Write a detailed description for an artistic illustration representing
the main idea of the poem.
Do not put Urdu or English text inside the illustration.

Return the result using exactly these headings:

ENGLISH_TRANSLATION
ENGLISH_SUMMARY
URDU_SUMMARY
DIFFICULT_WORDS
IQBAL_PERSONALITY
IMAGE_DESCRIPTION
"""

    return ask_ai(prompt)


def make_book_introduction():

    prompt = """
Write an introduction for an educational bilingual ebook about
five poems from Allama Muhammad Iqbal's Bang-e-Dara.

Write approximately 500 words.

Include:
- who Iqbal was
- the importance of poetry in his thought
- the purpose of studying these five poems
- the value of reading the Urdu original with English translation
- how poetry reveals personality and philosophy

Write the introduction in English followed by Urdu.
"""

    return ask_ai(prompt)


def make_final_analysis(poems_information):

    prompt = f"""
You are an expert on Allama Muhammad Iqbal.

Below is information extracted from five poems from Bang-e-Dara:

{poems_information}

Write a final comparative analysis.

Discuss:

1. Common themes
2. Iqbal's concept of human personality
3. Selfhood / Khudi
4. Courage and action
5. Hope and spiritual development
6. Relationship between individual and society
7. What these poems collectively reveal about Iqbal

Write first in English and then in Urdu.

Do not claim that an idea occurs in a poem unless it is supported
by the supplied material.
"""

    return ask_ai(prompt)