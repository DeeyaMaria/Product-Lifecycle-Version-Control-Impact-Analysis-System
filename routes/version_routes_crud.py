import models
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from models import ProductVersion
from schemas import VersionCreate
from models import ChangeLog
from schemas import ChangeLogCreate
from models import Approval
from schemas import ApprovalUpdate
from fastapi import APIRouter

router = APIRouter()

@router.post("/versions/create/{product_id}")
def create_version(
    product_id: int,
    db: Session = Depends(get_db)
):

    latest_version = (
        db.query(ProductVersion)
        .filter(ProductVersion.product_id == product_id)
        .order_by(ProductVersion.id.desc())
        .first()
    )

    if latest_version is None:
        next_version = "v1.0"
    else:
        current = latest_version.version_number

        # remove "v"
        version_num = current.replace("v", "")

        major, minor = version_num.split(".")

        next_minor = int(minor) + 1

        next_version = f"v{major}.{next_minor}"

    new_version = ProductVersion(
        product_id=product_id,
        version_number=next_version,
        status="Pending"
    )

    db.add(new_version)
    db.commit()
    db.refresh(new_version)

    return {
        "message": "Version created successfully",
        "id": new_version.id,
        "version_number": next_version
    }

@router.get("/versions/{product_id}")
def get_versions(product_id: int,
                 db: Session = Depends(get_db)):

    versions = db.query(ProductVersion).filter(
        ProductVersion.product_id == product_id
    ).all()

    return versions
@router.post("/logs/create")
def create_log(log: ChangeLogCreate,
               db: Session = Depends(get_db)):

    new_log = ChangeLog(
        version_id=log.version_id,
        requirement_id=log.requirement_id,
        field_name=log.field_name,
        old_value=log.old_value,
        new_value=log.new_value,
        reason=log.reason,
        modified_by=log.modified_by
    )

    db.add(new_log)
    db.commit()
    db.refresh(new_log)

    return {
        "message": "Log created",
        "id": new_log.id
    }
@router.get("/logs/{version_id}")
def get_logs(version_id: int,
             db: Session = Depends(get_db)):

    logs = db.query(ChangeLog).filter(
        ChangeLog.version_id == version_id
    ).all()

    return logs
#approve version
@router.post("/approve")
def approve_version(
    approval: ApprovalUpdate,
    db: Session = Depends(get_db)
):

    new_approval = Approval(
        version_id=approval.version_id,
        status="Approved",
        approved_by=approval.approved_by,
        comments= approval.comments,
    )

    db.add(new_approval)

    version = db.query(ProductVersion).filter(
        ProductVersion.id == approval.version_id
    ).first()

    if version:
        version.status = "Approved"

    db.commit()

    return {
    "message": "Version Approved",
    "version_id": approval.version_id,
    "comments": approval.comments
    }
#reject version
@router.post("/reject")
def reject_version(
    approval: ApprovalUpdate,
    db: Session = Depends(get_db)
):

    new_approval = Approval(
        version_id=approval.version_id,
        status="Rejected",
        approved_by=approval.approved_by,
        comments= approval.comments,
    )

    db.add(new_approval)

    version = db.query(ProductVersion).filter(
        ProductVersion.id == approval.version_id
    ).first()

    if version:
        version.status = "Rejected"

    db.commit()

    return {"message": "Version Rejected",
            "version_id": approval.version_id,
            "comments": approval.comments}
@router.get("/compare/{version_id}")
def compare_version(version_id: int,
                    db: Session = Depends(get_db)):

    logs = db.query(ChangeLog).filter(
        ChangeLog.version_id == version_id
    ).all()

    return {
    "version_id": version_id,
    "changes": [
        {
            "field": log.field_name,
            "old": log.old_value,
            "new": log.new_value
        }
        for log in logs
    ]
}
@router.get("/approvals")
def get_approvals(db: Session = Depends(get_db)):
    return db.query(Approval).all()

