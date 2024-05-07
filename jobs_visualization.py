import re

import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("jobs.csv")

all_technologies = []
for tech_list in df["technologies"]:
    if isinstance(tech_list, str):
        technologies = tech_list.split(",")
        english_technologies = [
            tech.strip()
            for tech in technologies
            if re.match(r"^[a-zA-Z0-9 ]+$", tech)
        ]
        all_technologies.extend(english_technologies)

technology_counts = pd.Series(all_technologies).value_counts()

top_technologies = technology_counts.head(10)

plt.figure(figsize=(20, 6))
top_technologies.plot(kind="bar", color="skyblue")
plt.title("Top 10 Most In-Demand Technologies")
plt.xlabel("Technology")
plt.ylabel("Number of Job")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

plt.savefig("technology_histogram.png")
plt.show()
