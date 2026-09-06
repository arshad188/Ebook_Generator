def generate_ebook():
    poems = load_poems()

    processed_poems = process_poems(poems)

    ebook = create_ebook(processed_poems)

    save_ebook(ebook)

    print("eBook created successfully!")


if __name__ == "__main__":
    generate_ebook()