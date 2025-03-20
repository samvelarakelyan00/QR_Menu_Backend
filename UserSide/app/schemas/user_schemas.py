from pydantic import BaseModel


class UserFeedbackSchema(BaseModel):
    horeka_client_id: int
    rating: int
    feedback_text: str


class UserScanQRSchema(BaseModel):
    horeka_client_id: int
