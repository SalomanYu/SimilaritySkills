from typing import NamedTuple
from dataclasses import astuple, dataclass

import sqlite3


SKILLS_PATH = "Data/course_skills.xlsx"
RESULT_DATABASE = "Results/skills.db"
REGULAR_STOPWORDS = (
    'имеешь', 'опыт работы', 'понимание',  'базов', 'знания', 'знание', 'отлично', 'есть опыт', 'написания', 'опыт',
    'принцип', 'умение', 'навык', 'мышление', 'обязательно', 'владение', 'приветствуется', 'уверен', 'свободно',
    'способно', 'ведение'
)

class Connection(NamedTuple):
    db: sqlite3.Connection
    cursor: sqlite3.Cursor


class SimilarSkill(NamedTuple):
    name: str
    similar_skill: str
    similar_skills_id: int
    percent: int


@dataclass
class SkillsWithoutStopWords:
    id: int
    name: str
    name_without_stopwords: str
    suspect: bool
    # duplicates: set() # Пригодится, если записывать в JSON. Сейчас ведется запись в SQL, поэтому поле не нужно

    def __iter__(self): # Добавляем возможность итерации
        return iter(astuple(self))


@dataclass
class SkillFromJson:
    id: int
    name: str
    def __iter__(self): # Добавляем возможность итерации
        return iter(astuple(self))


# def prepare_skills_for_save_to_json(skills: list[SkillsWithoutStopWords]) -> list[dict]:
#     # снизу описана анонимная функция, которая принимает на вход список классов SimilarSkill и строит из этих данных список со словарями
#     format_duplicates = lambda duplicates: [{"id": duplicate.id, "name": duplicate.name, "percent": duplicate.percent} for duplicate in duplicates]    
#     data = [{"name":skill.name, "name_without_stopwords": skill.name_without_stopwords, "duplicates": format_duplicates(skill.duplicates)} for skill in skills]

#     return data

# def save_json(data: list[dict]) -> None:
#     os.makedirs("Results", exist_ok=True)
#     with open("Results/similar_skills.json", "w") as File:
#         json.dump(data, File, indent=2, ensure_ascii=False)
    

# def check_similar(couple: tuple[SkillFromJson]):
#     print(couple)
#     current_skill, comporable_skill = couple

#     similarity = fuzz.token_set_ratio(current_skill.name_without_stopwords, comporable_skill.name_without_stopwords)
#     if similarity >= 65:
#         comporable_skill.suspect = True
#         database.add_similar_skill_to_table(data=SimilarSkill(
#             name=current_skill.name, 
#             similar_skill=comporable_skill.name,
#             similar_skills_id=comporable_skill.id,
#             percent=similarity))