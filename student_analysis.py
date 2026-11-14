
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

print("STUDENT PERFORMANCE ANALYSIS")

for name, marks in students.items():
    print(name, ":", marks)

print("Total Marks:", total)
print("Average Marks:", average)
print("Highest Scorer:", highest)
print("Lowest Scorer:", lowest)
