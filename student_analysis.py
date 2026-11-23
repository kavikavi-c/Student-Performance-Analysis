import streamlit as st
import pandas as pd

st.set_page_config(page_title="Student Performance Analysis", page_icon="📊")
st.title("📊 Student Performance Analysis")
st.caption("Analyze student marks, grades and results from a CSV file.")

sample = pd.DataFrame({
    "Student": ["Kavitha", "Priya", "Arun", "Divya", "Ravi"],
    "Maths":   [88, 92, 78, 97, 68],
    "Science": [82, 88, 72, 93, 62],
    "English": [85, 90, 75, 95, 65],
})
bad_sample = pd.DataFrame({
    "Student": ["Kavitha", "Priya", "Kavitha", "Arun", "Ravi"],
    "Maths":   [88, 92, 88, 150, "abc"],
    "Science": [82, None, 82, 72, 62],
    "English": [85, 90, 85, 75, 65],
})

b1, b2 = st.columns(2)
b1.download_button("⬇️ Sample CSV", sample.to_csv(index=False),
                   file_name="sample_students.csv", mime="text/csv")
b2.download_button("⬇️ Test CSV (with errors)", bad_sample.to_csv(index=False),
                   file_name="test_students_errors.csv", mime="text/csv")

uploaded = st.file_uploader("Upload a CSV file (optional)", type="csv")

if uploaded is not None:
    try:
        raw_df = pd.read_csv(uploaded)
    except Exception:
        st.error("Could not read the file. Please upload a valid CSV.")
        st.stop()
else:
    raw_df = sample.copy()
    st.info("Showing sample data. Upload a CSV to analyze your own data.")

# ---------- Data validation ----------
raw_df.columns = raw_df.columns.astype(str).str.strip()
if "Student" not in raw_df.columns:
    st.error("The CSV must have a 'Student' column.")
    st.stop()

subjects_all = [c for c in raw_df.columns if c != "Student"]
if not subjects_all:
    st.error("The CSV needs at least one subject column.")
    st.stop()

rows_read = len(raw_df)
df = raw_df.copy()
df["Student"] = df["Student"].astype(str).str.strip()
df = df[df["Student"].ne("") & df["Student"].str.lower().ne("nan")]
blank_removed = rows_read - len(df)

before = len(df)
df = df.drop_duplicates(subset="Student", keep="first")
dup_removed = before - len(df)

numeric_all = df[subjects_all].apply(pd.to_numeric, errors="coerce")
subjects = [c for c in subjects_all if numeric_all[c].notna().any()]
ignored = [c for c in subjects_all if c not in subjects]
if not subjects:
    st.error("No numeric subject columns found.")
    st.stop()

numeric = numeric_all[subjects]
non_numeric = int(numeric.isna().sum().sum() - df[subjects].isna().sum().sum())
out_of_range = int(((numeric < 0) | (numeric > 100)).sum().sum())
numeric = numeric.where((numeric >= 0) & (numeric <= 100))
missing_total = int(numeric.isna().sum().sum())
df = df[["Student"]].join(numeric)

with st.expander("🧹 Data Quality Report", expanded=False):
    report = pd.DataFrame({
        "Check": ["Rows read", "Blank names removed", "Duplicate students removed",
                  "Non-numeric values", "Marks outside 0-100",
                  "Missing values (total)"],
        "Count": [rows_read, blank_removed, dup_removed,
                  non_numeric, out_of_range, missing_total],
    })
    st.dataframe(report, hide_index=True)
    if ignored:
        st.caption("Ignored non-numeric columns: " + ", ".join(ignored))
    fix = st.radio("Handle missing values by",
                   ["Filling with subject average", "Removing those rows"])

if fix == "Removing those rows":
    df = df.dropna(subset=subjects)
else:
    df[subjects] = df[subjects].fillna(df[subjects].mean())

if df.empty:
    st.error("No valid data left after cleaning.")
    st.stop()

if dup_removed or missing_total or blank_removed:
    st.warning("Data was cleaned. See the Data Quality Report above.")

# ---------- Filters ----------
GRADES = ["A+", "A", "B", "C", "D"]
with st.expander("🎛️ Filters", expanded=False):
    sel_students = st.multiselect("Students", df["Student"].tolist(),
                                  default=df["Student"].tolist())
    sel_subjects = st.multiselect("Subjects", subjects, default=subjects)
    sel_grades = st.multiselect("Grades", GRADES, default=GRADES)

if not sel_students or not sel_subjects or not sel_grades:
    st.warning("Please select at least one student, subject and grade.")
    st.stop()

df = df[df["Student"].isin(sel_students)].copy()
subjects = sel_subjects
df["Marks"] = df[subjects].mean(axis=1).round().astype(int)

def grade(m):
    if m >= 90: return "A+"
    if m >= 80: return "A"
    if m >= 70: return "B"
    if m >= 60: return "C"
    return "D"

df["Grade"] = df["Marks"].apply(grade)
df["Result"] = df["Marks"].apply(lambda m: "Pass" if m >= 40 else "Fail")
df = df[df["Grade"].isin(sel_grades)]

if df.empty:
    st.warning("No students match the selected filters.")
    st.stop()

total = df["Marks"].sum()
average = df["Marks"].mean()
top = df.loc[df["Marks"].idxmax()]
low = df.loc[df["Marks"].idxmin()]
pass_pct = (df["Result"] == "Pass").mean() * 100

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📈 Overview", "📐 Statistics", "🔍 Search", "📚 Subjects", "📋 Data"]
)

with tab1:
    c1, c2 = st.columns(2)
    c1.metric("Total Marks", int(total))
    c2.metric("Average", round(average, 2))
    c3, c4 = st.columns(2)
    c3.metric("Highest", f"{top['Student']} ({top['Marks']})")
    c4.metric("Lowest", f"{low['Student']} ({low['Marks']})")
    st.metric("Pass Percentage", f"{pass_pct:.0f}%")
    st.subheader("Marks Chart")
    st.bar_chart(df, x="Student", y="Marks", color="#2E7D32")
    st.subheader("Pass / Fail Chart")
    st.bar_chart(df["Result"].value_counts(), color="#1565C0")
    st.subheader("Grade Distribution")
    st.bar_chart(df["Grade"].value_counts(), color="#EF6C00")

with tab2:
    m = df["Marks"]
    modes = m.mode()
    mode_val = int(modes.iloc[0]) if not modes.empty else 0
    s1, s2 = st.columns(2)
    s1.metric("Mean", round(m.mean(), 2))
    s2.metric("Median", round(m.median(), 2))
    s3, s4 = st.columns(2)
    s3.metric("Mode", mode_val)
    s4.metric("Std Deviation", round(float(m.std()) if len(m) > 1 else 0.0, 2))

    st.subheader("Performance Distribution")
    bins = [-1, 39, 59, 69, 79, 89, 100]
    labels = ["Below 40", "40-59", "60-69", "70-79", "80-89", "90-100"]
    dist = pd.cut(m, bins=bins, labels=labels).value_counts(sort=False)
    st.bar_chart(dist, color="#6A1B9A")

    st.subheader("Subject-wise Statistics")
    stats = pd.DataFrame({
        "Mean": df[subjects].mean(),
        "Median": df[subjects].median(),
        "Mode": df[subjects].mode().iloc[0],
        "Std Dev": df[subjects].std().fillna(0),
        "Min": df[subjects].min(),
        "Max": df[subjects].max(),
    }).round(2)
    st.dataframe(stats)

with tab3:
    name = st.text_input("Type a student name")
    if name:
        found = df[df["Student"].str.contains(name, case=False, na=False)]
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

with tab4:
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

with tab5:
    st.subheader("Student Marks Table")
    st.dataframe(df, hide_index=True)
    st.download_button("⬇️ Download results CSV", df.to_csv(index=False),
                       file_name="student_results.csv", mime="text/csv")
