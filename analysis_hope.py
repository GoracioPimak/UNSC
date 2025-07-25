import csv
import re
import argparse
from collections import Counter
import matplotlib.pyplot as plt

pattern_country1 = re.compile(r'^\s*[^:]+?\s+\(([^)]+)\)')
pattern_country2 = re.compile(r'representative of ([A-Za-z ,.-]+)')
pattern_hope = re.compile(r'\bhope(?:less(?:ness)?)?\b', re.IGNORECASE)


def extract_country(text: str) -> str | None:
    """Try to extract the speaking country from the given text."""
    m = pattern_country1.search(text)
    if m:
        return m.group(1).strip()
    m = pattern_country2.search(text)
    if m:
        return m.group(1).strip()
    return None


def main(csv_path: str) -> None:
    country_counter = Counter()
    year_counter = Counter()

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            text = row["content"]
            matches = pattern_hope.findall(text)
            if not matches:
                continue
            fn = row["filename"]
            year = int(fn.split("_")[1])
            year_counter[year] += len(matches)
            country = extract_country(text)
            if country:
                country_counter[country] += len(matches)

    # Plot top countries
    sorted_countries = country_counter.most_common(10)
    plt.figure(figsize=(10, 6))
    plt.bar([c for c, _ in sorted_countries],
            [n for _, n in sorted_countries], color="skyblue")
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Occurrences of hope-related words")
    plt.title("Top countries mentioning hope or hopelessness")
    plt.tight_layout()
    plt.savefig("hope_by_country.png")

    # Plot counts per year
    years = sorted(year_counter)
    counts = [year_counter[y] for y in years]
    plt.figure(figsize=(10, 6))
    plt.plot(years, counts, marker="o")
    plt.xlabel("Year")
    plt.ylabel("Occurrences of hope-related words")
    plt.title("Hope-related word usage by year")
    plt.tight_layout()
    plt.savefig("hope_by_year.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze hope-related words in UNSC speeches")
    parser.add_argument("csv", help="Path to unsc_speeches.csv")
    args = parser.parse_args()
    main(args.csv)
