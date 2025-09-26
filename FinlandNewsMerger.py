import pandas as pd

def extract_numeric_day(date_string):
    """
    Extracts the numeric day from a date string like '13 February'.
    Assumes the format 'Day Month'.
    """
    try:
        return int(date_string.split(" ")[0])  # Extracts only the day as an integer
    except (ValueError, IndexError):
        return 0  # Fallback for unexpected formats

def merge_story_groups(input_csv, output_csv="merged_stories_finland.csv", output_excel="merged_stories_finland.xlsx"):
    """
    Reads the chained news CSV, merges articles within each story group,
    and saves the merged stories into CSV & Excel files.
    """
    # Load chained news articles
    df = pd.read_csv(input_csv)

    merged_stories = []
    for group_id, group in df.groupby("Story Group ID"):
        # Extract unique dates & sort numerically
        date_objects = sorted(set(group["Date"]), key=extract_numeric_day)
        
        # Convert sorted dates back to their original format
        sorted_dates = ", ".join(date_objects)

        # Collect headlines and content for the story group
        headlines = " | ".join(group["Headline"])
        full_story = "\n\n".join(group.apply(lambda row: f"({row['Date']}) {row['Headline']}:\n{row['Content']}", axis=1))

        # Store the merged data
        merged_stories.append([group_id, sorted_dates, headlines, full_story])

    # Convert to DataFrame
    merged_df = pd.DataFrame(merged_stories, columns=["Story Group ID", "Dates", "Headlines", "Merged Content"])

    # Save to CSV
    merged_df.to_csv(output_csv, index=False, encoding="utf-8")

    # Save to Excel
    merged_df.to_excel(output_excel, index=False)

    print(f"\n✅ Merged stories saved to {output_csv} and {output_excel}\n")

def main():
    input_csv = "chained_news_finland.csv"  # Ensure this file exists
    merge_story_groups(input_csv)

if __name__ == "__main__":
    main()
