# TPS + TVQ
# CPP : Canadian pension plan (contribution)
# EI : Empolyment Insurance
# 

## BASED ON INTERNET DATA ## ---------------
FEDERAL_BRACKETS = [
    (57375, 0.15),
    (57375, 0.205),
    (63511, 0.26),
    (76390, 0.29),
    (float('inf'), 0.33),
] 

PROVINCIAL_BRACKETS = {
    "AB": [(148269, 0.10), (14110, 0.12), (19895, 0.13), (39732, 0.14), (float('inf'), 0.15)],
    "BC": [(45654, 0.0506), (45656, 0.077), (13525, 0.105), (22404, 0.1229), (49279, 0.147), (float('inf'), 0.168)],
    "ON": [(51446, 0.0505), (51446, 0.0915), (107955, 0.1116), (float('inf'), 0.1316)],
    "QC": [(51780, 0.14), (51780, 0.19), (float('inf'), 0.25)],
    "MB": [(47000, 0.108), (47000, 0.1275), (float('inf'), 0.175)],
    "SK": [(49720, 0.105), (92338, 0.125), (float('inf'), 0.145)],
    "NS": [(29590, 0.0879), (29590, 0.1495), (33820, 0.1667), (57000, 0.175), (float('inf'), 0.21)],
    "NB": [(47715, 0.094), (47716, 0.14), (19895, 0.16), (float('inf'), 0.195)],
    "PE": [(32656, 0.096), (32656, 0.1337), (float('inf'), 0.167)],
    "NL": [(43198, 0.087), (43198, 0.145), (57889, 0.158), (float('inf'), 0.178)],
    "NT": [(50597, 0.059), (50597, 0.086), (63618, 0.122), (float('inf'), 0.1405)],
    "NU": [(53268, 0.04), (53268, 0.07), (63498, 0.09), (float('inf'), 0.115)],
    "YT": [(57375, 0.064), (57375, 0.09), (52408, 0.109), (float('inf'), 0.128)],
}

# CPP as of 2024 : 5.95% on [$3500, $68500]
CPP_RATE = 0.0595
CPP_MAX_EARNINGS = 68500
CPP_EXEMPTION = 3500

# EI as of 2024 : 1.66% on insurable earnings
EI_RATE = 0.0166
EI_MAX_EARNINGS = 63200

## ------------------------------------------------

# band = income slice taxed @ a specific rate
# example (just for understanding purposes):
# 1st band : 0 to $15k > 10% tax rate
# 2nd band : $15k to $30k > 20% tax rate etc...

def _apply_brackets(income: float, brackets: list) -> float : 
    tax = 0.0
    remaining = income
    for band, rate in brackets:
        if remaining <=0:
            break
        taxable = min(remaining, band)
        tax += taxable*rate
        remaining -= taxable
    
    return round(tax, 2)



def calculate_cpp(income: float) -> float:
    insurable = max(0, min(income, CPP_MAX_EARNINGS) - CPP_EXEMPTION)
    return round(insurable*CPP_RATE, 2)


def calculate_ei(income: float) -> float: 
    insurable = min(income, EI_MAX_EARNINGS)
    return round(insurable*EI_RATE, 2)


def calculate_taxes(name:str, annual_salary: float, province: str) -> dict:
    if province not in PROVINCIAL_BRACKETS:
        raise ValueError(f"Province '{province}' not supported for now")
    
    federal_tax = _apply_brackets(annual_salary, FEDERAL_BRACKETS)
    provincial_tax = _apply_brackets(annual_salary, PROVINCIAL_BRACKETS[province])
    cpp = calculate_cpp(annual_salary)
    ei = calculate_ei(annual_salary)

    total_deductions = round(federal_tax + provincial_tax + cpp + ei, 2)
    net_annual = round(annual_salary - total_deductions, 2)
    net_monthly = round(net_annual/12, 2)


    return {
        "name": name,
        "province": province,
        "annual_salary": annual_salary,
        "federal_tax": federal_tax,
        "provincial_tax": provincial_tax,
        "cpp": cpp,
        "ei": ei,
        "total_deductions": total_deductions,
        "net_salary_annual": net_annual,
        "net_salary_monthly": net_monthly
    }