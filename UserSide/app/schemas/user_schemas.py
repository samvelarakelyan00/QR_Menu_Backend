from pydantic import BaseModel


class UserFeedbackSchema(BaseModel):
    horeka_client_id: int
    rating: int
    feedback_text: str


class UserScanQRSchema(BaseModel):
    horeka_client_id: int


class TipPayInfo(BaseModel):
    horeka_client_id: int
    horeka_tip_amount: float
    menu_tip_amount: float


class TipIdramLastButtonInfo(BaseModel):
    horeka_client_id: int
    horeka_tip_amount: float
    menu_tip_amount: float
