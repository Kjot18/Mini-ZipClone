import strawberry
from typing import Optional, List
from datetime import datetime

@strawberry.type
class UserType:
    id: int
    email: str
    username: str
    full_name: Optional[str]
    role: str
    created_at: datetime

@strawberry.type
class ApprovalType:
    id: int
    purchase_request_id: int
    approver: "UserType"
    status: str
    comment: Optional[str]
    stage: int
    created_at: datetime
    updated_at: Optional[datetime]

@strawberry.type
class PurchaseRequestType:
    id: int
    title: str
    description: Optional[str]
    amount: float
    currency: str
    status: str
    requester: UserType
    approvals: List[ApprovalType]
    created_at: datetime
    updated_at: Optional[datetime]

@strawberry.type
class AuthPayload:
    token: str
    user: UserType

@strawberry.input
class PurchaseRequestInput:
    title: str
    description: Optional[str] = None
    amount: float
    currency: str = "USD"

@strawberry.input
class ApprovalInput:
    purchase_request_id: int
    status: str
    comment: Optional[str] = None

@strawberry.input
class LoginInput:
    username: str
    password: str

@strawberry.input
class RegisterInput:
    username: str
    email: str
    password: str
    full_name: Optional[str] = None

