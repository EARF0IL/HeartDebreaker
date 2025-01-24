from datetime import datetime, time
from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, func, ForeignKey

from config import load_config
from config.enums import *


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'


class User(Base):
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    name: Mapped[str]
    gender: Mapped[GenderEnum]
    age: Mapped[int]
    heart_attacks: Mapped[int]
    blood_pressure: Mapped[BloodPressureEnum]
    is_smoking: Mapped[bool]
    sport_regularity: Mapped[SportRegularityEnum]
    
    # One-to-one
    LastQuiz: Mapped['LastQuiz'] = relationship(
        'LastQuiz',
        back_populates='User',
        uselist=False,
        lazy='joined',
        cascade="all, delete-orphan"
    )
    
    # One-to-many
    OneTimeSchedule: Mapped[list['OneTimeSchedule']] = relationship(
        'OneTimeSchedule',
        back_populates='User',
        lazy='joined',
        cascade="all, delete-orphan"
    )
    
    # One-to-many
    RegularSchedule: Mapped[list['RegularSchedule']] = relationship(
        'RegularSchedule',
        back_populates='User',
        lazy='joined',
        cascade="all, delete-orphan"
    )


class LastQuiz(Base):
    __tablename__ = 'last_quiz'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'))
    feeling: Mapped[FeelingEnum]
    symptoms: Mapped[SymptomsEnum]
    blood_pressure: Mapped[BloodPressureEnum | None]
    pulse: Mapped[PulseEnum]
    sport: Mapped[PhysActivityEnum]
    food: Mapped[FoodEnum]
    emotions: Mapped[EmotionsEnum]
    criticals: Mapped[CriticalStatesEnum]
    
    # One-to-one
    User: Mapped['User'] = relationship(
        'User',
        back_populates='LastQuiz',
        uselist=False
    )


class OneTimeSchedule(Base):
    __tablename__ = 'one_time_schedules'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'))
    name: Mapped[str]
    description: Mapped[str | None]
    time: Mapped[datetime]
    
    # Many-to-one
    User: Mapped['User'] = relationship(
        'User',
        back_populates='OneTimeSchedule',
        uselist=False
    )
    

class RegularSchedule(Base):
    __tablename__ = 'regular_schedules'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'))
    name: Mapped[str]
    description: Mapped[str | None]
    time: Mapped[time]
    
    # Many-to-one
    User: Mapped['User'] = relationship(
        'User',
        back_populates='RegularSchedule',
        uselist=False
    )