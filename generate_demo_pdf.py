from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'CredBuddha Financial Operations Policy', 0, 1, 'C')
        self.ln(10)

def create_demo_pdf():-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)
    
    text = """
CredBuddha 2026 Internal Operations Policy

1. Employee Travel Expenses
All CredBuddha employees are entitled to a daily meal allowance when traveling for business. The maximum reimbursable amount for dinner is $65.00 per day. Alcohol is strictly not reimbursable under any circumstances. Flight bookings must be made at least 14 days in advance using the corporate travel portal.

2. Software Subscriptions
If a department needs a new software tool (like GitHub Copilot or Groq API access), the manager must submit a request to the IT Procurement team. Subscriptions under $100/month are automatically approved by the system. Subscriptions over $100/month require manual review by the CTO.

3. Remote Work Equipment
Employees working fully remote are granted a one-time stipend of $500 to set up their home office. This stipend can be used for a desk, ergonomic chair, or extra monitors. Keyboards and mice are provided directly by the IT department and should not be purchased with the stipend.

4. Client Meetings
When taking a prospective client to lunch, the budget is capped at $120 total for the table. Receipts must be uploaded to the CredBuddha Expense Portal within 48 hours of the meeting.

Confidential Document - Do not distribute outside of CredBuddha.
"""
    
    # fpdf's multi_cell handles line wrapping automatically
    pdf.multi_cell(0, 10, text)
    
    pdf.output('CredBuddha_Policy_2026.pdf')
    print("Demo PDF created successfully!")

if __name__ == "__main__":
    create_demo_pdf()
