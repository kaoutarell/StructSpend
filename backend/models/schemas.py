from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# ONBOARDING
## 1st screen info
class OnboardingInput(BaseModel):
    name: str
    annual_salary: float
    province: str

## 2nd : just an estimate of taxes
class TaxBreakdown(BaseModel):
    name: str
    province: str
    annual_salary: float
    federal_tax: float
    provincial_tax: float
    cpp: float
    ei: float
    total_deductions: float
    net_salary_annual: float
    net_salary_monthly: float


# EXPENSES
## 2nd screen info
class ExpenseItem(BaseModel):
    label: str
    amount: float

class ExpenseStrategyInput(BaseModel):
    user_id: str #uuid
    month: str
    rent: float=0
    hydro: float=0
    insurances: float=0
    internet_cable: float=0
    mobile_plan: float=0
    groceries: float=0
    transit: float=0
    misc: float=0
    other: float=0
    custom_expenses: List[ExpenseItem] = []

# results
class ExpenseStrategyResponse(BaseModel):
    id: str
    total_fixed: float
    total_custom: float
    total_expenses: float
    remaining_net: float
    created_at: datetime


