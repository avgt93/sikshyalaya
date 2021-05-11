from typing import Any, List, Dict

from random import randint

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.config import settings

from models import User
from utils import deps
from cruds import crud_quiz, crud_question
from schemas import (
    Quiz,
    QuizCreate,
    QuizUpdate,
    QuizAnswer,
    QuizAnswerCreate,
    QuizAnswerUpdate,
    QuizQuestion,
    QuizQuestionCreate,
    QuizQuestionUpdate,
)

router = APIRouter()


@router.get("/", response_model=List[Quiz])
async def get_quiz(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    quiz = crud_quiz.get_multi(db, skip=skip, limit=limit)

    if current_user.user_type == settings.UserType.STUDENT.value:
        quiz_list = []
        for quizItem in quiz:
            if quizItem.group_id == current_user.group_id:
                quiz_list.append(quizItem)

        return quiz_list

    if current_user.user_type == settings.UserType.TEACHER.value:

        quiz_list = []
        for quizItem in quiz:
            for instructor in quizItem.instructor:
                if current_user.id == instructor.id:
                    quiz_list.append(quizItem)
        return quiz_list

    if current_user.user_type <= settings.UserType.ADMIN.value:
        return quiz


@router.post("/", response_model=QuizCreate)
async def create_quiz(
    db: Session = Depends(deps.get_db),
    *,
    obj_in: QuizCreate,
    current_user: User = Depends(deps.get_current_active_teacher_or_above),
) -> Any:
    quiz = crud_quiz.create(db, obj_in=obj_in)
    return quiz


@router.get("/{id}", response_model=Quiz)
async def get_specific_quiz(
    db: Session = Depends(deps.get_db),
    *,
    id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    if current_user.user_type == settings.UserType.STUDENT.value:
        quiz_list = await get_quiz(db=db, current_user=current_user)
        for quiz in quiz_list:
            if quiz.id == id:
                return quiz
        raise HTTPException(
            status_code=401, detail="Error ID: 133"
        )  # not accessible by the Student user

    if current_user.user_type == settings.UserType.TEACHER.value:
        quiz_list = await get_quiz(db=db, current_user=current_user)
        for quiz in quiz_list:
            if quiz.id == id:
                return quiz
        raise HTTPException(
            status_code=401, detail="Error ID: 134"
        )  # not accessible by the Teacher user

    if current_user.user_type <= settings.UserType.ADMIN.value:
        quiz = crud_quiz.get(db, id)
        return quiz


@router.put("/{id}", response_model=QuizUpdate)
async def update_quiz(
    db: Session = Depends(deps.get_db),
    *,
    id: int,
    obj_in: QuizUpdate,
    current_user: User = Depends(deps.get_current_active_teacher_or_above),
) -> Any:
    quiz = crud_quiz.get(db, id)
    quiz = crud_quiz.update(db, db_obj=quiz, obj_in=obj_in)
    return quiz


@router.get("/{quizid}/question", response_model=List[QuizQuestion])
async def get_question(
    db: Session = Depends(deps.get_db),
    *,
    quizid: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    quiz = await get_specific_quiz(db, id=quizid, current_user=current_user)
    if not quiz:
        raise HTTPException(
            status_code=404, detail="Error ID = 135"
        )  # quiz not found in database

    questions = crud_question.get_all_by_quiz_id(db, quiz_id=quiz.id)
    return questions


@router.get("/{quizid}/question/{id}", response_model=List[QuizQuestion])
async def get_specific_question(
    db: Session = Depends(deps.get_db),
    *,
    quizid: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    questions = await get_question(db, quizid=quizid, current_user=current_user)
    for question in questions:
        if question.id == id:
            return questions

    raise HTTPException(
        status_code=404, detail="Error ID: 135"
    )  # question specific to that id not found


@router.post("/{quizid}/question")
async def create_question(
    db: Session = Depends(deps.get_db),
    *,
    quizid: int,
    obj_in: QuizQuestionCreate,
    current_user: User = Depends(deps.get_current_active_teacher_or_above),
) -> Any:
    # FIXME: is this needed?
    obj_in.quiz_id = quizid
    crud_question.create(db, obj_in=obj_in)
    return {"msg": "success"}


@router.put("/{quizid}/question/{id}")
async def update_question(
    db: Session = Depends(deps.get_db),
    *,
    quizid: int,
    obj_in: QuizQuestionUpdate,
    current_user: User = Depends(deps.get_current_active_teacher_or_above),
) -> Any:
    question = crud_question.get(db, id)
    if question.quiz_id == quizid:
        question = crud_question.update(db, db_obj=question, obj_in=obj_in)
        return question
    else:
        raise HTTPException(
            status_code=401, detail="Error ID = 136"
        )  # noqa Access Denied!


# for questions to write and read files and answers to those files
