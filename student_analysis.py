import streamlit as st
import pandas as pd

st.set_page_config(page_title="Student Performance Analysis", page_icon="📊")
st.title("📊 Student Performance Analysis")

sample = pd.DataFrame({
    "Student": ["Kavitha", "Priya", "Arun", "Divya", "Ravi"],
    "Maths":   [88, 92, 78, 97, 68],
    "Science": [82, 88, 72, 93, 62],
    "English": [85, 90, 75, 95, 65],
})

st.download_button(
    "⬇️ Download sample CSV",
    sample.to_csv(index=False),
    file_name="sample_students.csv",
    mime="text/csv",
)

uploaded = st.file_uploader("Upload a CSV file (optional)", type="csv")

if uploaded is not None:
    try:
        df = pd.read_csv(uploaded)
    except Exception:
        st.error("Could not read the file. Please upload a valid CSV.")
        st.stop()
else:
    df = sample.copy()
    st.info("Showing sample data. Upload a CSV to analyze your own data.")

if "Student" not in df.columns:
    st.error("The CSV must have a 'Student' column.")
    st.stop()

subjects = [c for c in df.columns if c != "Student"]
if not subjects:
    st.error("The CSV needs at least one subject column.")
    st.stop()

df[subjects] = df[subjects].apply(pd.to_numeric, errors="coerce")
df = df.dropna(subset=subjects)
if df.empty:
    st.error("No valid marks found in the file.")
    st.stop()

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

c1, c2 = st.columns(2)
c1.metric("Total Marks", int(total))
c2.metric("Average", round(average, 2))

c3, c4 = st.columns(2)
c3.metric("Highest", f"{top['Student']} ({top['Marks']})")
c4.metric("Lowest", f"{low['Student']} ({low['Marks']})")

st.metric("Pass Percentage", f"{pass_pct:.0f}%")

st.subheader("🔍 Search Student")
name = st.text_input("Type a student name")
if name:
    found = df[df["Student"].astype(str).str.contains(name, case=False, na=False)]
    if found.empty:
        st.warning("No student found.")
    else:
        st.dataframe(found, hide_index=True)

choice = st.selectbox("Or select a student", df["Student"])
row = df[df["Student"] == choice].iloc[0]
d1, d2, d3 = st.columns(3)
d1.metric("Marks", int(row["Marks"]))
d2.metric("Grade", row["Grade"])
d3.metric("Result", row["Result"])

st.subheader("Marks Chart")
st.bar_chart(df, x="Student", y="Marks")

st.subheader("Pass / Fail Chart")
st.bar_chart(df["Result"].value_counts())

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
