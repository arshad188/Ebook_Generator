import os

# Put your OpenAI API key in the environment variable.
# Do NOT publish your API key or put it in a book/project you share.

API_KEY = os.getenv("OPENAI_API_KEY")

# Model used for translation, summaries and analysis
TEXT_MODEL = "gpt-5.6-luna"

# Image model
IMAGE_MODEL = "gpt-image-2"

OUTPUT_PDF = "output/iqbal_5_poems.pdf"