from typing import List, Optional
import strawberry
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import PurchaseRequest, User, Approval, RequestStatus
from app.graphql.types import PurchaseRequestType, UserType, ApprovalType
from app.auth import get_user_by_id

def get_db_session():
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()

@strawberry.type
class Query:
    @strawberry.field
    async def purchase_requests(
        self,
        status: Optional[str] = None,
        requester_id: Optional[int] = None
    ) -> List[PurchaseRequestType]:
        db = next(get_db())
        try:
            query = db.query(PurchaseRequest)
            
            if status:
                query = query.filter(PurchaseRequest.status == status)
            if requester_id:
                query = query.filter(PurchaseRequest.requester_id == requester_id)
            
            requests = query.order_by(PurchaseRequest.created_at.desc()).all()
            return [
                PurchaseRequestType(
                    id=req.id,
                    title=req.title,
                    description=req.description,
                    amount=req.amount,
                    currency=req.currency,
                    status=req.status.value,
                    requester=UserType(
                        id=req.requester.id,
                        email=req.requester.email,
                        username=req.requester.username,
                        full_name=req.requester.full_name,
                        role=req.requester.role.value,
                        created_at=req.requester.created_at
                    ),
                    approvals=[
                        ApprovalType(
                            id=app.id,
                            purchase_request_id=app.purchase_request_id,
                            approver=UserType(
                                id=app.approver.id,
                                email=app.approver.email,
                                username=app.approver.username,
                                full_name=app.approver.full_name,
                                role=app.approver.role.value,
                                created_at=app.approver.created_at
                            ),
                            status=app.status.value,
                            comment=app.comment,
                            stage=app.stage,
                            created_at=app.created_at,
                            updated_at=app.updated_at
                        )
                        for app in req.approvals
                    ],
                    created_at=req.created_at,
                    updated_at=req.updated_at
                )
                for req in requests
            ]
        finally:
            db.close()
    
    @strawberry.field
    async def purchase_request(self, id: int) -> Optional[PurchaseRequestType]:
        db = next(get_db())
        try:
            req = db.query(PurchaseRequest).filter(PurchaseRequest.id == id).first()
            if not req:
                return None
            
            return PurchaseRequestType(
                id=req.id,
                title=req.title,
                description=req.description,
                amount=req.amount,
                currency=req.currency,
                status=req.status.value,
                requester=UserType(
                    id=req.requester.id,
                    email=req.requester.email,
                    username=req.requester.username,
                    full_name=req.requester.full_name,
                    role=req.requester.role.value,
                    created_at=req.requester.created_at
                ),
                approvals=[
                    ApprovalType(
                        id=app.id,
                        purchase_request_id=app.purchase_request_id,
                        approver=UserType(
                            id=app.approver.id,
                            email=app.approver.email,
                            username=app.approver.username,
                            full_name=app.approver.full_name,
                            role=app.approver.role.value,
                            created_at=app.approver.created_at
                        ),
                        status=app.status.value,
                        comment=app.comment,
                        stage=app.stage,
                        created_at=app.created_at,
                        updated_at=app.updated_at
                    )
                    for app in req.approvals
                ],
                created_at=req.created_at,
                updated_at=req.updated_at
            )
        finally:
            db.close()
    
    @strawberry.field
    async def users(self) -> List[UserType]:
        db = next(get_db())
        try:
            users = db.query(User).all()
            return [
                UserType(
                    id=user.id,
                    email=user.email,
                    username=user.username,
                    full_name=user.full_name,
                    role=user.role.value,
                    created_at=user.created_at
                )
                for user in users
            ]
        finally:
            db.close()
    
    @strawberry.field
    async def approvals(
        self,
        purchase_request_id: Optional[int] = None
    ) -> List[ApprovalType]:
        db = next(get_db())
        try:
            query = db.query(Approval)
            
            if purchase_request_id:
                query = query.filter(Approval.purchase_request_id == purchase_request_id)
            
            approvals = query.order_by(Approval.stage, Approval.created_at).all()
            return [
                ApprovalType(
                    id=app.id,
                    purchase_request_id=app.purchase_request_id,
                    approver=UserType(
                        id=app.approver.id,
                        email=app.approver.email,
                        username=app.approver.username,
                        full_name=app.approver.full_name,
                        role=app.approver.role.value,
                        created_at=app.approver.created_at
                    ),
                    status=app.status.value,
                    comment=app.comment,
                    stage=app.stage,
                    created_at=app.created_at,
                    updated_at=app.updated_at
                )
                for app in approvals
            ]
        finally:
            db.close()

