from typing import Optional

from pydantic import BaseModel


class SubscribeRequest(BaseModel):
    plan: str  


class SubscribeResponse(BaseModel):
    approval_url: str
    subscription_id: str


class SubscriptionStatusRead(BaseModel):
    plan: str
    status: str
    provider: Optional[str] = None
    current_period_end: Optional[str] = None


class MpesaStkRequest(BaseModel):
    plan: str
    phone_number: str  # any format: 07XX, 2547XX, +2547XX


class MpesaStkResponse(BaseModel):
    checkout_request_id: str
    message: str