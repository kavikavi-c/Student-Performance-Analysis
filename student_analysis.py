import streamlit as st
import pandas as pd

students = {
    "Kavitha": 85,
    "Priya": 90,
    "Arun": 75,
    "Divya": 95,
    "Ravi": 65
}

def grade(m):
    if m >= 90: return "A+"
    if m >= 80: return "A"
    if m >= 70: return "B"
    if m >= 60: return "C"
    return "D"

df = pd.DataFrame(list(students.items()), columns=["Student", "Marks"])
df["Grade"] = df["Marks"].apply(grade)
df["Result"] = df["Marks"].apply(lambda m: "Pass" if m >= 40 else "Fail")

total = df["Marks"].sum()
average = df["Marks"].mean()
top = df.loc[df["Marks"].idxmax()]
low = df.loc[df["Marks"].idxmin()]
pass_pct = (df["Result"] == "Pass").mean() * 100

st.title("📊 Student Performance Analysis")

c1, c2 = st.columns(2)
c1.metric("Total Marks", total)
c2.metric("Average", round(average, 2))

c3, c4 = st.columns(2)
c3.metric("Highest", f"{top['Student']} ({top['Marks']})")
c4.metric("Lowest", f"{low['Student']} ({low['Marks']})")

st.metric("Pass Percentage", f"{pass_pct:.0f}%")

st.subheader("Marks Chart")
st.bar_chart(df, x="Student", y="Marks")

st.subheader("Grade Distribution")
st.bar_chart(df["Grade"].value_counts())

st.subheader("Student Marks Table")
st.dataframe(df, hide_index=True)
