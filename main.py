import json
import os

from ai_writer import (
    analyze_poem,
    make_book_introduction,
    make_final_analysis
)

from illustrations import generate_image
from ebook import create_pdf

INPUT_FILE = "poems.json"
IMAGE_FOLDER = "images"
OUTPUT_FOLDER = "output"


def load_poems():

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def main():

    os.makedirs(IMAGE_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    data = load_poems()

    print()
    print("======================================")
    print(" IQBAL BANG-E-DARA EBOOK GENERATOR")
    print("======================================")
    print()

    print("Generating introduction...")

    introduction = make_book_introduction()

    book = {
        "author": data["author"],
        "collection": data["collection"],
        "introduction": introduction,
        "poems": []
    }

    all_information = []

    total = len(data["poems"])

    for number, poem in enumerate(data["poems"], 1):

        print()
        print("--------------------------------------")
        print(f"Processing poem {number} of {total}")
        print(poem["title"])
        print("--------------------------------------")

        analysis = analyze_poem(
            poem["title"],
            poem["urdu_text"]
        )

        # For the first version, keep the AI response together.
        poem_result = {
            "title": poem["title"],
            "urdu_text": poem["urdu_text"],
            "translation": analysis,
            "english_summary": analysis,
            "urdu_summary": analysis,
            "difficult_words": analysis,
            "personality": analysis
        }

        # Create illustration
        image_file = os.path.join(
            IMAGE_FOLDER,
            f"poem_{number}.png"
        )

        try:

            print("Generating illustration...")

            generate_image(
                analysis,
                image_file
            )

            poem_result["image"] = image_file

        except Exception as e:

            print("Image generation failed:")
            print(e)

            poem_result["image"] = None

        book["poems"].append(poem_result)

        all_information.append(
            f"\nPOEM {number}\n{analysis}"
        )

    print()
    print("Generating final analysis...")

    final_analysis = make_final_analysis(
        "\n".join(all_information)
    )

    book["final_analysis"] = final_analysis

    output_file = os.path.join(
        OUTPUT_FOLDER,
        "iqbal_5_poems.pdf"
    )

    print()
    print("Creating PDF...")

    create_pdf(
        book,
        output_file
    )

    print()
    print("======================================")
    print(" EBOOK COMPLETED")
    print("======================================")
    print()
    print("Your ebook is:")
    print(output_file)


if __name__ == "__main__":
    main()