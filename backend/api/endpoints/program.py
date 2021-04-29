from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from cruds.program import crud_program
from schemas import Program, ProgramCreate, ProgramUpdate
from utils import deps

router = APIRouter()


@router.get("/", response_model=List[Program])
async def get_programs(
        db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100
) -> Any:
    programs = crud_program.get_multi(db, skip=skip, limit=limit)
    return programs


@router.post("/", response_model=Program)
async def create_program(
        db: Session = Depends(deps.get_db), *, program_in: ProgramCreate
) -> Any:
    program = crud_program.create(db, obj_in=program_in)
    return program


@router.get("/{program_id}", response_model=Program)
async def get_program(db: Session = Depends(deps.get_db), *, program_id: int) -> Any:
    program = crud_program.get(db, program_id)
    return program


@router.put("/{program_id}", response_model=Program)
async def update_program(
        db: Session = Depends(deps.get_db),
        *,
        program_id: int,
        program_update: ProgramUpdate
) -> Any:
    program = crud_program.get(db, program_id)
    program = crud_program.update(db, db_obj=program, obj_in=program_update)
    return program

