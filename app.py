import re
import xlrd
from time import time
from fuzzywuzzy import fuzz
from rich.progress import track
# from multiprocessing import Pool

import database
from config import *


def get_skills_from_excel(path: str, skills_count: int = 0) -> list[SkillFromJson]:
    """
    Skills_count - переменная, хранящая информацию о том, сколько навыков нужно получить из БД. 
    По умолчанию выводятся все навыки
    """

    book = xlrd.open_workbook(path) 
    sheet = book.sheet_by_index(0) # Читаем первую страницу таблицы
    tableTitles = sheet.row_values(0) # Сохраняем все заголовки колонок, чтобы по ним определить номер необходимых колонок
   
    for titleIndex in range(sheet.ncols): 
        if tableTitles[titleIndex] == 'id': # Если колонка называется id, то запоминаем номер колонки
            id_col = titleIndex
        elif tableTitles[titleIndex] == 'name':
            name_col = titleIndex
    all_ids = sheet.col_values(id_col)[1:]
    all_names = sheet.col_values(name_col)[1:]

    if not skills_count or skills_count > len(all_names): skills_count = len(all_names)

    result = [SkillFromJson(id=int(all_ids[item]), name=all_names[item]) for item in range(skills_count)]
    return result


def remove_stop_words(skills: list[SkillFromJson]) -> list[SkillsWithoutStopWords]:
    result = []
    for skill in skills:
        if isinstance(skill.name, str):
            old = skill.name[::]
            for stop in REGULAR_STOPWORDS:
                skill.name = re.sub(stop+'.*? ', ' ', skill.name.lower())  # .*? позволяет учитывать продолжение слова до пробела
            result.append(SkillsWithoutStopWords(id=skill.id, name=old.lower(), name_without_stopwords=skill.name.lower(), suspect=False))

    return result



def fuzzy_similarity(skills: list[SkillsWithoutStopWords]):
    start = time()
    count = 0

    for current in track(range(len(skills)), description="[green]Ищем похожие пары"):
        current_skill = skills[current]
        if not current_skill.suspect:  # Если навыка не является ничьим дубликатом
            couples_skills = ((skills[current], skills[comporable]) for comporable in range(current+1, len(skills)))
           
            # with Pool(4) as process:
            #     process.map_async(
            #         func=check_similar,
            #         iterable=couples_skills,
                    # error_callback=lambda error: exit(error)
            # )
            for comporable in range(current+1, len(skills)):
                comporable_skill = skills[comporable]
               
                similarity = fuzz.token_set_ratio(current_skill.name_without_stopwords, comporable_skill.name_without_stopwords)
                if similarity >= 65:
                    comporable_skill.suspect = True
                    database.add_similar_skill_to_table(data=SimilarSkill(
                        name=current_skill.name, 
                        similar_skill=comporable_skill.name,
                        similar_skills_id=comporable_skill.id,
                        percent=similarity))
                    # current_skill.duplicates.add(SimilarSkill(id=comporable_skill.id, name=comporable_skill.name, percent=similarity))
        else:
            count += 1

    print(f'Прошло времени: {time() - start} cек.\nНайдено повторений: {count}')
    return skills


if __name__ == "__main__":
    database.create_table()
    skills = get_skills_from_excel(path=SKILLS_PATH)
    skills_without_trash = remove_stop_words(skills)
    similar_skills = fuzzy_similarity(skills_without_trash) 
    # save_json(data=prepare_skills_for_save_to_json(skills=similar_skills))