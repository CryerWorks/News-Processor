import os
import re
import csv
import pandas as pd
from datetime import datetime

def read_markdown_file(md_path):
    """
    Reads a Markdown file and returns its content as a string.
    """
    with open(md_path, "r", encoding="utf-8") as file:
        return file.read()

def extract_date(md_text):
    """
    Extracts the date from the top of the document.
    Expected format: '13 February 2025'
    """
    date_pattern = r"\b\d{1,2}\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b"
    match = re.search(date_pattern, md_text)
    return match.group(0) if match else "Unknown Date"

def extract_news_section(md_text):
    """
    Extracts the 'News' section, stopping at 'Today's Opinions'.
    """
    start_marker = re.search(r"\n\s*\*\*News\*\*", md_text, re.IGNORECASE)
    end_marker = re.search(r"\n\s*\*\*Today's opinions\*\*", md_text, re.IGNORECASE)

    if start_marker and end_marker:
        return md_text[start_marker.end():end_marker.start()].strip()
    elif start_marker:
        return md_text[start_marker.end():].strip()  # Extract till end if "Today's Opinions" is missing
    else:
        return ""  # No news section found

def segment_articles(news_text):
    """
    Segments articles based on bold headlines in the Markdown format.
    """
    articles = []
    lines = news_text.split("\n")
    current_headline = None
    current_article = []

    for line in lines:
        line = line.strip()

        # Detect headlines (bold text in Markdown format)
        if line.startswith("**") and line.endswith("**"):
            if current_headline and current_article:
                articles.append((current_headline, "\n".join(current_article)))
                current_article = []
            current_headline = line.strip("**").strip()
        elif current_headline:
            current_article.append(line)

    if current_headline and current_article:
        articles.append((current_headline, "\n".join(current_article)))

    return articles

def process_markdown_files(file_paths):
    """
    Processes a list of Markdown (.md) files and compiles extracted news.
    Ensures that extracted headlines and content are strings to prevent later errors.
    """
    all_articles = []

    for file_path in file_paths:
        if file_path.endswith(".md"):
            print(f"🔍 Processing file: {os.path.basename(file_path)}")

            md_text = read_markdown_file(file_path)
            date = extract_date(md_text)
            news_section = extract_news_section(md_text)
            articles = segment_articles(news_section)

            for headline, content in articles:
                # Ensure headline and content are strings, replacing None/NaN with an empty string
                headline = str(headline) if isinstance(headline, str) else ""
                content = str(content) if isinstance(content, str) else ""

                all_articles.append([date, headline, content])

    # Sort articles chronologically based on the date
    all_articles.sort(key=lambda x: datetime.strptime(x[0], "%d %B %Y") if x[0] != "Unknown Date" else datetime.min)

    return all_articles

def save_to_csv(articles, output_filename="extracted_news.csv"):
    """
    Saves all extracted news articles into a single CSV file.
    Ensures all data is properly formatted as strings.
    """
    df = pd.DataFrame(articles, columns=["Date", "Headline", "Content"])

    # Ensure all columns are strings and replace NaN with an empty string
    df = df.astype(str).fillna("")

    df.to_csv(output_filename, index=False, encoding="utf-8")

    print(f"\n✅ Extracted news saved to {output_filename}\n")

def save_to_excel(articles, output_filename="extracted_news.xlsx"):
    """
    Saves all extracted news articles into a single Excel file.
    Ensures all data is properly formatted as strings.
    """
    df = pd.DataFrame(articles, columns=["Date", "Headline", "Content"])

    # Ensure all columns are strings and replace NaN with an empty string
    df = df.astype(str).fillna("")

    df.to_excel(output_filename, index=False)

    print(f"\n✅ Extracted news saved to {output_filename}\n")

def main():
    """
    Main function that runs when the script is executed directly.
    This function is not called when the script is imported.
    """
    # 🔧 Update this with the correct folder path
    folder_path = r"C:\Users\jonat\OneDrive\Dokumenter\CodeWorks\Mundus\MND-Generator2025\SampleMDs"

    # Process all markdown files in the folder
    all_articles = process_markdown_files([os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.md')])

    # Save results to structured files
    save_to_csv(all_articles, "extracted_news.csv")
    save_to_excel(all_articles, "extracted_news.xlsx")

if __name__ == "__main__":
    main()
