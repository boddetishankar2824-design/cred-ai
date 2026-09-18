from app.schemas import LoanEligibilityRequest, LoanEligibilityResponse

class LoanService:
    @staticmethod
    def calculate_eligibility(req: LoanEligibilityRequest) -> LoanEligibilityResponse:
        """
        Business logic to determine loan eligibility, interest rate, EMI and recommendations.
        """
        # Rule 1: Max loan limit is 12x of monthly income
        max_limit = req.monthly_income * 12
        
        # Rule 2: Interest rate based on credit score
        if req.credit_score >= 750:
            annual_rate = 10.5  # 10.5% per annum
        elif req.credit_score >= 650:
            annual_rate = 13.0
        else:
            annual_rate = 16.5
            
        # Rule 3: EMI Calculation (Standard reducing balance EMI formula)
        monthly_rate = (annual_rate / 100) / 12
        n = req.tenure_months
        
        if monthly_rate > 0:
            emi = (req.requested_amount * monthly_rate * ((1 + monthly_rate) ** n)) / (((1 + monthly_rate) ** n) - 1)
        else:
            emi = req.requested_amount / n
            
        # Eligibility decision: EMI should not exceed 50% of monthly income
        is_eligible = (emi <= (req.monthly_income * 0.5)) and (req.requested_amount <= max_limit)
        
        if is_eligible:
            recommendation = (
                f"Approved! Your requested amount of ${req.requested_amount:,.2f} is within your limit of "
                f"${max_limit:,.2f} with a competitive interest rate of {annual_rate}%."
            )
        else:
            recommendation = (
                f"Your requested amount exceeds your safe EMI limit (50% of income). "
                f"We recommend a maximum loan of ${min(max_limit, req.monthly_income * 6):,.2f}."
            )
            
        return LoanEligibilityResponse(
            is_eligible=is_eligible,
            max_loan_amount=round(max_limit, 2),
            estimated_emi=round(emi, 2),
            interest_rate=annual_rate,
            recommendation=recommendation
        )

loan_service = LoanService()
