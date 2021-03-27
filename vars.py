from pydantic import BaseModel
from typing import Optional, List
from datetime import time

first_lesson = time(hour=8, minute=40)
last_lesson = time(hour=18, minute=40)

WeekDays_RU = ('понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье')
WeekDays_EN = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')
special_chars = r'[\'"<>\[\]{}!@#*$%^&(),./\\;:]'
special_chars_digit = r'[\'"<>\[\]{}!@#*$%^&(),./\\;:]'

days = {
    'monday': 'понедельник',
    'tuesday': 'вторник',
    'wednesday': 'среда',
    'thursday': 'четверг',
    'friday': 'пятница',
    'saturday': 'суббота'
}


class Time(BaseModel):
    start: str
    end: str


class Lesson(BaseModel):
    time: Time
    subgroup: str
    lesson: str
    teacher: str
    classroom: str


class Day_of_week(BaseModel):
    lessons: List[Lesson]


class Sched(BaseModel):
    monday: Optional[Day_of_week]
    tuesday: Optional[Day_of_week]
    wednesday: Optional[Day_of_week]
    thursday: Optional[Day_of_week]
    friday: Optional[Day_of_week]
    saturday: Optional[Day_of_week]
