import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.style as mpl_style

def calculate_final_grade(grade_remaining, grade_final_exam, ects_completed, current_avg, total_ects, final_exam_ects):
    grade_remaining_weight = (total_ects - ects_completed - final_exam_ects) * grade_remaining
    grade_final_exam_weight = final_exam_ects * grade_final_exam
    grade_current_weight = ects_completed * current_avg

    final_grade = (grade_current_weight + grade_remaining_weight + grade_final_exam_weight) / total_ects
    return final_grade

st.title("Final Grade Calculator")

ects_completed = st.number_input("Erfüllte ECTS", min_value=0, value=35, step=1)
current_avg = st.number_input("Aktueller Durchschnitt", min_value=1.0, max_value=4.0, value=1.88, step=0.1)
total_ects = st.number_input("Gesamtanzahl ECTS", min_value=1, value=90, step=1)
final_exam_ects = st.number_input("Abschlussprüfung ECTS", min_value=0, value=20, step=1)

grades_remaining = np.arange(1.0, 4.1, 0.1)
grades_final_exam = [1.0, 1.3, 1.7, 2.0, 2.3, 2.7, 3.0, 3.3, 3.7, 4] 

final_grades = pd.DataFrame(index=grades_remaining, columns=grades_final_exam)

for grade_remaining in grades_remaining:
    for grade_final_exam in grades_final_exam:
        final_grade = calculate_final_grade(grade_remaining, grade_final_exam, ects_completed, current_avg, total_ects, final_exam_ects)
        final_grades.at[grade_remaining, grade_final_exam] = round(final_grade, 2)

st.write(final_grades)


# Add range sliders for remaining grades and Abschlussprüfung grades
remaining_grades_range = st.slider("Expected range for remaining grades", min_value=1.0, max_value=4.0, value=(1.0, 4.0), step=0.1)
abschluss_grades_range = st.slider("Expected range for Abschlussprüfung grades", min_value=1.0, max_value=4.0, value=(1.0, 4.0), step=0.1)

# Filter the DataFrame using the slider values
filtered_final_grades = final_grades.loc[remaining_grades_range[0]:remaining_grades_range[1], abschluss_grades_range[0]:abschluss_grades_range[1]]

# Transform filtered DataFrame into 1D array
filtered_final_grades_array = filtered_final_grades.to_numpy().ravel()

# Apply the dark mode style to the plot
mpl_style.use("dark_background")

# Create a histogram using matplotlib and display it using Streamlit
fig, ax = plt.subplots()
ax.hist(filtered_final_grades_array, bins='auto', edgecolor='white')
ax.set_xlabel('Final Grades')
ax.set_ylabel('Frequency')
ax.set_title('Histogram of Filtered Final Grades')

st.pyplot(fig)
