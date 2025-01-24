from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select, update, delete

from database.models import User, LastQuiz, OneTimeSchedule, RegularSchedule
from database import async_session_maker


def connection(method):
    async def wrapper(*args, **kwargs):
        async with async_session_maker() as session:
            try:
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()
    return wrapper

@connection
async def add_user(userdata: dict[str, Any], session: AsyncSession):
    user = User(**userdata)
    session.add(user)
    await session.commit()
    
@connection
async def update_user(userdata: dict[str, Any], session: AsyncSession):
    await session.execute(update(User).where(User.user_id == userdata['user_id']), userdata)
    await session.commit()
    

@connection
async def check_user_exist(user_id: int, session: AsyncSession):
    result = await session.execute(select(User.user_id).where(User.user_id == user_id))
    return bool(result.fetchone())

@connection
async def add_quiz(quizdata: dict[str, Any], session: AsyncSession):
    quiz = LastQuiz(
        user_id=quizdata['user_id'],
        feeling=quizdata['feeling'],
        symptoms=quizdata['symptoms'],
        blood_pressure=quizdata['blood_pressure'],
        pulse=quizdata['pulse'],
        sport=quizdata['sport'],
        food=quizdata['food'],
        emotions=quizdata['emotions'],
        criticals=quizdata['criticals'],
    )
    
    session.add(quiz)
    await session.commit()
    
@connection
async def update_quiz(quizdata: dict[str, Any], session: AsyncSession):
    quizdata = dict(
        user_id=quizdata['user_id'],
        feeling=quizdata['feeling'],
        symptoms=quizdata['symptoms'],
        blood_pressure=quizdata['blood_pressure'],
        pulse=quizdata['pulse'],
        sport=quizdata['sport'],
        food=quizdata['food'],
        emotions=quizdata['emotions'],
        criticals=quizdata['criticals'],
    )
    await session.execute(update(LastQuiz).where(LastQuiz.user_id == quizdata['user_id']), quizdata)
    await session.commit()

@connection
async def check_quiz_exist(user_id: int, session: AsyncSession):
    result = await session.execute(select(LastQuiz.user_id).where(LastQuiz.user_id == user_id))
    return bool(result.fetchone())

@connection
async def get_last_quiz(user_id: int, session: AsyncSession):
    result = await session.execute(select(LastQuiz).where(LastQuiz.user_id == user_id))
    return result.fetchone()[0]


@connection
async def add_one_time_schedule(data: dict[str, Any], session: AsyncSession):
    schedule_info = OneTimeSchedule(**data)
    session.add(schedule_info)
    await session.commit()
    

@connection
async def get_one_time_schedule(user_id: int, name: str, session: AsyncSession):
    result = await session.execute(select(OneTimeSchedule).where(OneTimeSchedule.user_id == user_id).where(OneTimeSchedule.name == name))
    return result.fetchone()[0]


@connection
async def remove_one_time_schedule(user_id: int, name: str, session: AsyncSession):
    removable_schedule = await get_one_time_schedule(user_id, name)
    await session.delete(removable_schedule)
    await session.commit()


@connection
async def add_regular_schedule(data: dict[str, Any], session: AsyncSession):
    schedule_info = RegularSchedule(**data)
    session.add(schedule_info)
    await session.commit()


@connection
async def get_regular_schedule(user_id: int, name: str, session: AsyncSession):
    result = await session.execute(select(RegularSchedule).where(RegularSchedule.user_id == user_id).where(RegularSchedule.name == name))
    return result.fetchone()[0]


@connection
async def remove_regular_schedule(user_id: int, name: str, session: AsyncSession):
    removable_schedule = await get_regular_schedule(user_id, name)
    try:
        await session.delete(removable_schedule)
        await session.commit()
    except Exception:
        pass


@connection
async def get_user(user_id: int, session: AsyncSession):
    result = await session.execute(select(User).where(User.user_id == user_id))
    return result.unique().scalars().all()[0]
