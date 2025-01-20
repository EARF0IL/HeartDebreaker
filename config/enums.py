import enum


class GenderEnum(str, enum.Enum):
    MALE = 'муж'
    FEMALE = 'жен'
    
    
class BloodPressureEnum(str, enum.Enum):
    HIGH = 'высокое'
    NORMAL = 'нормальное'
    LOW = 'низкое'
    

class SportRegularityEnum(str, enum.Enum):
    OFTEN = 'часто'
    RARELY = 'редко'
    NEVER = 'никогда'
    
    
class FeelingEnum(str, enum.Enum):
    FINE = 'отлично'
    OK = 'удовлетворительно'
    BAD = 'плохо'
    

class SymptomsEnum(str, enum.Enum):
    DISCOMFORT = 'Дискомфорт в груди'
    DIZZINESS = 'Головокружение'
    SHORTNESS = 'Одышка или затрудненное дыхание'
    FATIGUE = 'Усталость или слабость'
    RATE = 'Повышенное сердцебиение'
    NO = 'Симптомы не беспокоили'
    

class FoodEnum(str, enum.Enum):
    LIGHT = 'Легкая и сбалансированная'
    HEAVY = 'Жирная, соленая и тяжелая пища'
    HUNGRY = 'Давно не питался'
    
    
class EmotionsEnum(str, enum.Enum):
    CALM = 'Спокойное'
    STRESS = 'Небольшой стресс'
    CRITICAL = 'Очень напряженное'


class CriticalStatesEnum(str, enum.Enum):
    FAINT = 'Потеря сознания'
    HEARTATTACK = 'Внезапная боль в груди'
    SUFFOCATION = 'Приступ удушья'
    NO = 'Всё в порядке'


class PhysActivityEnum(str, enum.Enum):
    LOW = 'Минимальный'
    MIDDLE = 'Средний'
    HIGH = 'Высокий'
    

class PulseEnum(str, enum.Enum):
    LOW = 'Менее 60'
    MIDDLE = '60-100'
    HIGH = 'Более 100'
    NO = 'Не могу определить'