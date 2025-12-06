from typing import Optional
import strawberry
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import PurchaseRequest, User, Approval, RequestStatus, ApprovalStatus, UserRole
from app.graphql.types import (
    PurchaseRequestType, UserType, ApprovalType, AuthPayload,
    PurchaseRequestInput, ApprovalInput, LoginInput, RegisterInput
)
from app.auth import (
    authenticate_user, create_access_token, create_user,
    get_user_by_username, get_user_by_id
)
from datetime import timedelta
from app.config import settings

def get_current_user_id(info) -> Optional[int]:
    """Extract user ID from request context (simplified for demo)"""
    # In production, extract from JWT token in headers
    return getattr(info.context, "user_id", None)

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def register(self, input: RegisterInput) -> AuthPayload:
        db = next(get_db())
        try:
            # Check if user exists
            if get_user_by_username(db, input.username):
                raise Exception("Username already exists")
            
            if db.query(User).filter(User.email == input.email).first():
                raise Exception("Email already exists")
            
            user = create_user(
                db=db,
                username=input.username,
                email=input.email,
                password=input.password,
                full_name=input.full_name,
                role=UserRole.USER
            )
            
            access_token = create_access_token(
                data={"sub": str(user.id), "username": user.username}
            )
            
            return AuthPayload(
                token=access_token,
                user=UserType(
                    id=user.id,
                    email=user.email,
                    username=user.username,
                    full_name=user.full_name,
                    role=user.role.value,
                    created_at=user.created_at
                )
            )
        finally:
            db.close()
    
    @strawberry.mutation
    async def login(self, input: LoginInput) -> AuthPayload:
        db = next(get_db())
        try:
            user = authenticate_user(db, input.username, input.password)
            if not user:
                raise Exception("Invalid username or password")
            
            access_token = create_access_token(
                data={"sub": str(user.id), "username": user.username}
            )
            
            return AuthPayload(
                token=access_token,
                user=UserType(
                    id=user.id,
                    email=user.email,
                    username=user.username,
                    full_name=user.full_name,
                    role=user.role.value,
                    created_at=user.created_at
                )
            )
        finally:
            db.close()
    
    @strawberry.mutation
    async def create_purchase_request(
        self,
        input: PurchaseRequestInput,
        info
    ) -> PurchaseRequestType:
        db = next(get_db())
        try:
            # Get current user (simplified - in production use JWT)
            user_id = get_current_user_id(info)
            if not user_id:
                # For demo, use first user or create default
                user = db.query(User).first()
                if not user:
                    raise Exception("No user found. Please register first.")
                user_id = user.id
            
            purchase_request = PurchaseRequest(
                title=input.title,
                description=input.description,
                amount=input.amount,
                currency=input.currency,
                status=RequestStatus.PENDING,
                requester_id=user_id
            )
            db.add(purchase_request)
            db.commit()
            db.refresh(purchase_request)
            
            # Create initial approval stage
            approver = db.query(User).filter(User.role == UserRole.MANAGER).first()
            if not approver:
                approver = db.query(User).filter(User.role == UserRole.ADMIN).first()
            
            if approver:
                approval = Approval(
                    purchase_request_id=purchase_request.id,
                    approver_id=approver.id,
                    status=ApprovalStatus.PENDING,
                    stage=1
                )
                db.add(approval)
                db.commit()
            
            return PurchaseRequestType(
                id=purchase_request.id,
                title=purchase_request.title,
                description=purchase_request.description,
                amount=purchase_request.amount,
                currency=purchase_request.currency,
                status=purchase_request.status.value,
                requester=UserType(
                    id=purchase_request.requester.id,
                    email=purchase_request.requester.email,
                    username=purchase_request.requester.username,
                    full_name=purchase_request.requester.full_name,
                    role=purchase_request.requester.role.value,
                    created_at=purchase_request.requester.created_at
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
                    for app in purchase_request.approvals
                ],
                created_at=purchase_request.created_at,
                updated_at=purchase_request.updated_at
            )
        finally:
            db.close()
    
    @strawberry.mutation
    async def approve_request(
        self,
        input: ApprovalInput,
        info
    ) -> ApprovalType:
        db = next(get_db())
        try:
            purchase_request = db.query(PurchaseRequest).filter(
                PurchaseRequest.id == input.purchase_request_id
            ).first()
            
            if not purchase_request:
                raise Exception("Purchase request not found")
            
            user_id = get_current_user_id(info)
            if not user_id:
                user = db.query(User).filter(User.role.in_([UserRole.ADMIN, UserRole.MANAGER])).first()
                if not user:
                    raise Exception("No approver found")
                user_id = user.id
            
            # Find or create approval
            approval = db.query(Approval).filter(
                Approval.purchase_request_id == input.purchase_request_id,
                Approval.approver_id == user_id
            ).first()
            
            if not approval:
                # Create new approval
                max_stage = db.query(Approval).filter(
                    Approval.purchase_request_id == input.purchase_request_id
                ).count()
                approval = Approval(
                    purchase_request_id=input.purchase_request_id,
                    approver_id=user_id,
                    status=ApprovalStatus(input.status),
                    comment=input.comment,
                    stage=max_stage + 1
                )
                db.add(approval)
            else:
                approval.status = ApprovalStatus(input.status)
                approval.comment = input.comment
            
            # Update purchase request status
            if input.status == "approved":
                # Check if all approvals are done
                pending_approvals = db.query(Approval).filter(
                    Approval.purchase_request_id == input.purchase_request_id,
                    Approval.status == ApprovalStatus.PENDING
                ).count()
                
                if pending_approvals == 0:
                    purchase_request.status = RequestStatus.APPROVED
                else:
                    purchase_request.status = RequestStatus.IN_REVIEW
            elif input.status == "denied":
                purchase_request.status = RequestStatus.DENIED
            
            db.commit()
            db.refresh(approval)
            
            return ApprovalType(
                id=approval.id,
                purchase_request_id=approval.purchase_request_id,
                approver=UserType(
                    id=approval.approver.id,
                    email=approval.approver.email,
                    username=approval.approver.username,
                    full_name=approval.approver.full_name,
                    role=approval.approver.role.value,
                    created_at=approval.approver.created_at
                ),
                status=approval.status.value,
                comment=approval.comment,
                stage=approval.stage,
                created_at=approval.created_at,
                updated_at=approval.updated_at
            )
        finally:
            db.close()

