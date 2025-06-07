# app/utils/validators.py
from decimal import Decimal


def validate_cpf(cpf: str) -> bool:
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    for i in range(9, 11):
        value = sum(int(cpf[j]) * ((i+1)-j) for j in range(0, i))
        digit = ((value * 10) % 11) % 10
        if digit != int(cpf[i]):
            return False
    return True


def validate_cnpj(cnpj: str) -> bool:
    if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
        return False
    def calc(digits, multipliers):
        s = sum(int(d) * m for d, m in zip(digits, multipliers, strict=False))
        d = 11 - s % 11
        return '0' if d >= 10 else str(d)
    if (calc(cnpj[:12], [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]) != cnpj[12] or
        calc(cnpj[:13], [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]) != cnpj[13]):
        return False
    return True

def validate_property_areas(total: Decimal | None, farming: Decimal | None, vegetation: Decimal | None):
    if all(area is not None for area in [total, farming, vegetation]):
        if farming + vegetation > total:
            raise ValueError("Sum of areas exceeds the property's total area.")