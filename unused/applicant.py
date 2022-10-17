from pydantic import BaseModel
class applicant(BaseModel):
    EXT_SOURCE_2: float # 0 to 1
    EXT_SOURCE_3: float # 0 to 1
    PAYMENT_RATE: float # 0 to 1
    PA_PrLI_DELAY_DAYS_INSTALMENT__max__max: int # -110 to 2400
    CODE_GENDER_F: int # 0 or 1