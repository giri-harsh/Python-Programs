#questions
# Load the CSV file:
# Load the employees.csv file into a Pandas DataFrame and display the first five rows.

# Basic Information:
# Print the number of rows and columns in the DataFrame, and display the column names.

# Filter Data:
# Find all employees who work in the "IT" department.

# Sort Data:
# Sort the DataFrame by Salary in descending order and display the top 5 employees with the highest salaries.

# Group and Aggregate:
# Calculate the average salary of employees in each department.

# Filter by Condition:
# Find all employees with more than 5 years of experience.

# Date Operations:
# Extract the year from the JoiningDate column and create a new column named JoiningYear.

# Count by City:
# Count the number of employees in each city.

# Add a Column:
# Add a new column named AnnualBonus that calculates the bonus as 10% of the Salary.

# Highest Salary:
# Identify the employee with the highest salary and display their details.

import pandas as pd 
import numpy as np 

df=pd.read_csv(r"C:\Users\Harsh Giri\OneDrive\Documents\!Programing Language\Python\Test Data\employees.csv")
print("Number of rows and coloums : ",df.shape)
df["Name"]
it_employee=df[df["Department"]=="IT"]["Name"]
print(it_employee)
money=df.sort_values(by="Salary",ascending=False)
print("Money : ",money)
df["Department"].value_counts()
it_depart=df[df["Department"]=="IT"]["Salary"]
it_depart.mean()

print("salary of it depart : ",it_depart.mean())
sales_depart = df[df["Department"]=="Sales"]["Salary"]
print("mean salary of Sales Depart : ",sales_depart.mean())


HR_depart=df[df["Department"]=="HR"][["Salary","Name"]]
print("mean salary of HR: ",HR_depart["Salary"].mean())
df["City"].value_counts()

highest=df.sort_values(by="Salary")
highest[["Name","Department","Salary"]]
