import streamlit as st
import pandas as pd

students = {
    "Kavitha": 85,
    "Priya": 90,
    "Arun": 75,
    "Divya": 95,
    "Ravi": 65
}

total = sum(students.values())
average = total / len(students)

highest = max(students, key=students.get)
lowest = min(students, key=students.get)

st.title("📊 Student Performance Analysis")

c1, c2 = st.columns(2)
c1.metric("Total Marks", total)
c2.metric("Average", round(average, 2))

c3, c4 = st.columns(2)
c3.metric("Highest", f"{highest} ({students[highest]})")
c4.metric("Lowest", f"{lowest} ({students[lowest]})")

df = pd.DataFrame(
    list(students.items()), columns=["Student", "Marks"]
)

st.subheader("Marks Chart")
st.bar_chart(df, x="Student", y="Marks")

st.subheader("Student Marks Table")
st.dataframe(df, hide_index=True)
