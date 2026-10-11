from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font("Helvetica", "B", 16)
pdf.cell(0, 10, "HR Policy Manual - TestCorp India Pvt Ltd", ln=True)
pdf.set_font("Helvetica", size=11)
pdf.ln(5)

sections = [
    ("1. Working Hours",
     "Employees are expected to work 9.5 hours per day, 6 days a week. "
     "There is no fixed overtime policy. Employees may be asked to work "
     "additional hours without extra compensation at management discretion."),

    ("2. Salary and Wages",
     "Salaries are paid on the last day of the month via bank transfer. "
     "The company follows applicable minimum wage guidelines. "
     "There is no formal equal pay policy documented."),

    ("3. Provident Fund",
     "EPF is deducted at 12% of basic salary for all confirmed employees. "
     "Contract staff and employees on probation (first 6 months) are not "
     "enrolled in EPF until confirmation."),

    ("4. Gratuity",
     "Gratuity is payable after 5 years of continuous service. "
     "The rate is 10 days wages per year of service. "
     "Gratuity is paid within 90 days of separation."),

    ("5. Maternity Leave",
     "Female employees are entitled to 12 weeks of paid maternity leave "
     "for first and second child. No creche facility is currently provided. "
     "Nursing breaks are not formally defined in this policy."),

    ("6. Termination and Retrenchment",
     "The company may terminate employment with 1 month notice or pay "
     "in lieu. Retrenchment compensation will be as per management decision. "
     "No formal grievance redressal committee exists currently."),

    ("7. Health and Safety",
     "The company is committed to workplace safety. Employees must follow "
     "safety guidelines. No formal safety committee has been constituted. "
     "First aid boxes are available at reception."),

    ("8. Leave Policy",
     "Employees are entitled to 15 days casual leave per year. "
     "Annual leave accrues at 1 day per 30 working days. "
     "Leave encashment is not permitted on resignation."),
]

for title, body in sections:
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, title, ln=True)
    pdf.set_font("Helvetica", size=10)
    pdf.multi_cell(0, 6, body)
    pdf.ln(4)

pdf.output("test_hr_policy.pdf")
print("Created: test_hr_policy.pdf")
