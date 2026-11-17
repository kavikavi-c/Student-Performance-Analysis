import streamlit as st
import pandas as pd

subjects = ["Maths", "Science", "English"]

df = pd.DataFrame({
    "Student": ["Kavitha", "Priya", "Arun", "Divya", "Ravi"],
    "Maths":   [88, 92, 78, 97, 68],
    "Science": [82, 88, 72, 93, 62],
    "English": [85, 90, 75, 95, 65],
})

df["Marks"] = df[subjects].mean(axis=1).round().astype(int)

def grade(m):
    if m >= 90: return "A+"
    if m >= 80: return "A"
    if m >= 70: return "B"
    if m >= 60: return "C"
    return "D"

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

st.subheader("Subject-wise Average")
st.bar_chart(df[subjects].mean())

st.subheader("Subject Toppers")
toppers = pd.DataFrame({
    "Subject": subjects,
    "Topper": [df.loc[df[s].idxmax(), "Student"] for s in subjects],
    "Marks": [df[s].max() for s in subjects],
})
st.dataframe(toppers, hide_index=True)

st.subheader("Student-wise Subject Marks")
st.bar_chart(df.set_index("Student")[subjects])

st.subheader("Grade Distribution")
st.bar_chart(df["Grade"].value_counts())

st.subheader("Student Marks Table")
st.dataframe(df, hide_index=True)
