import pandas as pd
import openai
import os
from dotenv import load_dotenv

# Load OpenAI API key from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("❌ OpenAI API key is missing! Check your .env file.")

# OpenAI client setup
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def extract_numeric_day(date_string):
    """
    Extracts the numeric day from a date string like '13 February'.
    Assumes the format 'Day Month'.
    """
    try:
        return int(date_string.split(" ")[0])  # Extracts only the day as an integer
    except (ValueError, IndexError):
        return 0  # Fallback for unexpected formats

def format_dates(dates):
    """
    Ensures dates are consistently formatted as (1, 2, 3 February) in ascending order.
    """
    date_list = dates.split(", ")
    if not date_list:
        return ""

    # Extract numeric day values and sort them
    sorted_dates = sorted(date_list, key=extract_numeric_day)

    # Extract the month from the last date (e.g., "3 February")
    month = sorted_dates[-1].split(" ")[1] if " " in sorted_dates[-1] else "Unknown"

    # Extract only the numeric dates
    numeric_dates = [d.split(" ")[0] for d in sorted_dates]

    return f"({', '.join(numeric_dates)} {month})"

def get_summary_instructions(dates):
    """
    Determines the summary length instructions based on the number of attached dates.
    """
    num_dates = len(dates.split(", "))

    if num_dates == 1:
        return "Summarise the story in **1-2 sentences**."
    elif num_dates == 2:
        return "Summarise the story in **2-4 sentences**."
    else:
        return "Write a full paragraph summarising the story."

def generate_summary(headlines, full_story, dates):
    """
    Uses OpenAI's ChatGPT API to generate a complete, structured summary based on date count.
    """
    summary_instruction = get_summary_instructions(dates)

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a professional news summariser writing in British English and past tense. "
                                              "Your summaries must always be fully complete and must never be cut off."},
                {"role": "user", "content": f"{summary_instruction} Ensure the summary is concise and well-structured.\n\n"
                                            f"📝 Headlines: {headlines}\n\n📜 Full Story:\n{full_story}"
                                            f"🛑 The summary **must** be factual, clear, and use the provided token limit."}
            ],
            max_tokens=3000,  # Fixed max tokens for all summaries
            temperature=0.2,
            stop=["###", "\n\n"]
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"⚠️ Error generating summary: {e}")
        return "Summary unavailable"

def generate_headline(headlines, full_story):
    """
    Uses OpenAI to generate a merged headline summarising the key event.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert news summariser writing in British English."},
                {"role": "user", "content": f"Generate a concise, professional news headline summarising the following merged news story:\n\nHeadlines: {headlines}\n\nFull Story:\n{full_story}"}
            ],
            max_tokens=300,  # Keep headlines concise
            temperature=0.3
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"⚠️ Error generating headline: {e}")
        return "Headline unavailable"

def summarise_merged_stories(input_csv="merged_stories.csv", output_csv="summarised_stories.csv", output_excel="summarised_stories.xlsx"):
    """
    Reads the merged news stories CSV, generates summaries and headlines using ChatGPT,
    appends dates manually, and saves results in a structured format.
    """
    df = pd.read_csv(input_csv)

    summaries = []
    for _, row in df.iterrows():
        story_group_id = row["Story Group ID"]
        dates = row["Dates"]
        headlines = row["Headlines"]
        full_story = row["Merged Content"]

        print(f"📝 Processing Story Group {story_group_id}...")

        # Generate AI-based headline & summary
        merged_headline = generate_headline(headlines, full_story)
        summary = generate_summary(headlines, full_story, dates)

        # Append the manually formatted date at the end of the summary
        formatted_date = format_dates(dates)
        summary += f" {formatted_date}"

        summaries.append([story_group_id, merged_headline, summary, formatted_date])

    # Convert to DataFrame
    summary_df = pd.DataFrame(summaries, columns=["Story Group ID", "Merged Headline", "Summary", "Dates"])

    # Save to CSV
    summary_df.to_csv(output_csv, index=False, encoding="utf-8")

    # Save to Excel
    summary_df.to_excel(output_excel, index=False)

    print(f"\n✅ Summarised stories saved to {output_csv} and {output_excel}\n")

def main():
    """
    Main function to run the news summarisation process.
    """
    summarise_merged_stories()

if __name__ == "__main__":
    main()
