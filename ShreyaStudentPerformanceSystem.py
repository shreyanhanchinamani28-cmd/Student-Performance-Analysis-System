import pandas as pd
import matplotlib.pyplot as plt

# ---------------- GOOGLE SHEET LIVE DATA ---------------- #

sheet_url = "https://docs.google.com/spreadsheets/d/1JHfqXT9heh02FFMaUFVkWjx0xrs-LaWAv4JS4_mpSt8/export?format=csv"

data = pd.read_csv(sheet_url)

print("\nSTUDENT PERFORMANCE DATA\n")
print(data)

# ---------------- RENAME COLUMNS ---------------- #

data.columns = [
    "Timestamp",
    "Student_Name",
    "USN",
    "Branch",
    "BEC801_Marks",
    "BEC801_Result",
    "BEC802_Marks",
    "BEC802_Result",
    "BEC803_Marks",
    "BEC803_Result"
]

# ---------------- CONVERT MARKS ---------------- #

data["BEC801_Marks"] = data["BEC801_Marks"].astype(int)
data["BEC802_Marks"] = data["BEC802_Marks"].astype(int)
data["BEC803_Marks"] = data["BEC803_Marks"].astype(int)

# ---------------- CALCULATE AVERAGE ---------------- #

data["Average"] = (
    data["BEC801_Marks"] +
    data["BEC802_Marks"] +
    data["BEC803_Marks"]
) / 3

# ---------------- FINAL RESULT ---------------- #

final_result = []

for i in range(len(data)):

    if (
        data["BEC801_Result"][i] == "Fail" or
        data["BEC802_Result"][i] == "Fail" or
        data["BEC803_Result"][i] == "Fail"
    ):

        final_result.append("Fail")

    else:

        final_result.append("Pass")

data["Final_Result"] = final_result

# SORT BY USN

data = data.sort_values(by="USN")
data = data.reset_index(drop=True)

# REMOVE DUPLICATE USN

data = data.drop_duplicates(subset="USN", keep="last")
data = data.reset_index(drop=True)

# ---------------- MODERN PIE CHART ---------------- #

import mplcursors

result_count = data["Final_Result"].value_counts()

result_count = result_count.reindex(["Pass", "Fail"], fill_value=0)

labels = result_count.index
sizes = result_count.values

colors = ["#00C853", "#D50000"]

explode = [0.03, 0.03]

plt.figure(figsize=(8, 8))

wedges, texts, autotexts = plt.pie(
    sizes,
    labels=labels,
    autopct='%1.1f%%',
    pctdistance=0.75,
    startangle=90,
    colors=colors,
    explode=explode,
    shadow=False,
    wedgeprops=dict(width=0.45)
)

plt.title(
    "Pass vs Fail Students",
    fontsize=18,
    fontweight='bold'
)

# CENTER TEXT

total_students = len(data)

plt.text(
    0,
    0,
    f"Total\n{total_students}",
    ha='center',
    va='center',
    fontsize=16,
    fontweight='bold'
)

plt.show()

# ---------------- INTERACTIVE BAR GRAPH ---------------- #

import mplcursors

plt.figure(figsize=(13, 6))

colors = []
marks = []

for i in range(len(data)):

    avg = round(data["Average"][i], 1)

    marks.append(avg)

    colors.append("#87CEFA")

bars = plt.bar(
    data["USN"],
    marks,
    color=colors
)


plt.title(
    "Interactive Student Performance Analysis",
    fontsize=18,
    fontweight='bold'
)

plt.xlabel("Student USN", fontsize=12)
plt.ylabel("Average Marks", fontsize=12)

plt.xticks(rotation=20)

plt.grid(
    axis='y',
    linestyle='--',
    alpha=0.4
)

# ---------------- HOVER DETAILS ---------------- #

cursor = mplcursors.cursor(bars, hover=True)

@cursor.connect("add")
def on_add(sel):
    try:
        i = int(sel.index)

        text = (
            f"Name: {data['Student_Name'][i]}\n\n"
            f"BEC801: {data['BEC801_Marks'][i]} "
            f"({data['BEC801_Result'][i]})\n"
            f"BEC802: {data['BEC802_Marks'][i]} "
            f"({data['BEC802_Result'][i]})\n"
            f"BEC803: {data['BEC803_Marks'][i]} "
            f"({data['BEC803_Result'][i]})\n\n"
            f"Average: {round(data['Average'][i], 1)}\n"
            f"Final Result: {data['Final_Result'][i]}"
        )

        sel.annotation.set_text(text)

    except:
        pass

plt.show()
# ---------------- CLEAN INTERACTIVE LINE GRAPH ---------------- #

plt.figure(figsize=(12, 6))

x_values = list(range(len(data)))

# LINE ONLY
plt.plot(
    x_values,
    data["Average"],
    linewidth=3,
    color="#5b5bd6"
)

# DOTS ONLY
dots = plt.scatter(
    x_values,
    data["Average"],
    s=80,
    color="#5b5bd6"
)

plt.title(
    "Student Performance Trend",
    fontsize=18,
    fontweight='bold'
)

plt.xlabel("Student USN", fontsize=12)
plt.ylabel("Average Percentage", fontsize=12)

plt.xticks(x_values, data["USN"], rotation=20)

plt.grid(True, linestyle='--', alpha=0.4)

# ---------------- CLICK ONLY ON DOTS ---------------- #

cursor = mplcursors.cursor(dots, hover=False)

@cursor.connect("add")
def on_add(sel):

    try:

        index = sel.index

        student = data.iloc[index]

        sel.annotation.set_text(
            f"{student['Student_Name']}\n"
            f"{round(student['Average'], 1)}%"
        )

    except:
        pass

plt.show()
# ---------------- FAILED STUDENTS ---------------- #

failed_students = data[data["Final_Result"] == "Fail"]

print("\nFAILED STUDENTS\n")

print(failed_students[["Student_Name", "USN"]])