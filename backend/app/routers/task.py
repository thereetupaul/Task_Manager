from fastapi import Depends, FastAPI,Response,status, HTTPException, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models,schemas,oauth2
from sqlalchemy.orm import joinedload, contains_eager

router=APIRouter(
    prefix="/tasks",
    tags=['Tasks']
)


@router.get("/", response_model=List[schemas.TaskOut])
def get_posts(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
   
    if current_user.role == "admin":
        # Admin can see all tasks
        tasks = db.query(models.Task).join(models.Task.owner).options(contains_eager(models.Task.owner)).all()
    else:
        # Regular users can only see their own tasks
        tasks = db.query(models.Task).join(models.Task.owner).options(contains_eager(models.Task.owner)).filter(models.Task.owner_id == current_user.id).all()

    return tasks


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.TaskOut)
def create_posts(task:schemas.TaskCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
  
    new_task = models.Task(owner_id = current_user.id, **task.dict())  #unpacking the dictionary using **
    db.add(new_task)
    db.commit()
    db.refresh(new_task)    
    return new_task


@router.get("/{id}", response_model=schemas.TaskOut)
def get_post(id:int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    
    task = db.query(models.Task).join(models.Task.owner).options(contains_eager(models.Task.owner)).filter(models.Task.id == id).first()
    
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"task with id: {id} was not found")
    
    # Allow access if user is admin or task owner
    if current_user.role != "admin" and task.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this task")
    
    return task



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    
    task_query = db.query(models.Task).filter(models.Task.id ==id)

    task = task_query.first()

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"task with id: {id} does not exist")
    
    # Allow deletion if user is admin or task owner
    if current_user.role != "admin" and task.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    task_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.TaskOut)
def update_post(id:int, updated_task:schemas.TaskCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    task_query = db.query(models.Task).filter(models.Task.id ==id)

    task = task_query.first()

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"task with id: {id} does not exist")

    # Allow update if user is admin or task owner   
    if current_user.role != "admin" and task.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    task_query.update(updated_task.dict(),synchronize_session=False)
    db.commit()

    return task_query.first()
