import streamlit as st
import json
import os

st.set_page_config(layout="wide")
st.markdown(
    """
    <style>
    .main-title { font-size: 32px; font-weight: bold; color: #FFFFFF; margin-bottom: 5px; }
    .subtitle { font-size: 14px; color: #8E8E93; margin-bottom: 25px; }
    </style>
    <div class="main-title">Интерактивный Роадмап и Бэклог проекта KitchMind</div>
    <div class="subtitle">Панель синхронизации: Таймлайн (Диаграмма Ганта), зависимости, роли команды и подробное техническое задание (ТЗ) для каждого таска</div>
    """,
    unsafe_allow_html=True
)

STATE_FILE = "backlog_state.json"

ROLE_MAP = {
    "TASK-1.1": "UI/UX",
    "TASK-1.2": "Backend",
    "TASK-1.3": "Mobile Dev",
    "TASK-1.4": "Backend",
    "TASK-1.5": "Backend",
    "TASK-1.6": "Data Science",
    "TASK-1.7": "Data Science",
    "TASK-1.8": "Mobile Dev",
    "TASK-1.9": "Backend",
    "TASK-2.1": "Data Science",
    "TASK-2.2": "UI/UX",
    "TASK-3.1": "Backend",
    "TASK-3.2": "Data Science"
}

ROLE_COLORS = {
    "Data Science": "#FFD60A", 
    "Backend": "#8E8E93",      
    "Mobile Dev": "#FFFFFF",  
    "UI/UX": "#E5E5EA"      
}

TASKS = [
    {"id": "TASK-1.1", "sprint": "MVP (Must)", "level": "UI/UX / Прототипирование", "name": "Проектирование UI/UX дизайн-системы и экранов в Figma", "owner": "Настя", "blockers": [], "duration": 4, "start_day": 1, "color": "#FF453A", "tz": "Разработка полной дизайн-системы приложения в Figma. Входные параметры палитры: Background #121212, Surface #1E1E1E, Text Primary #FFFFFF, Text Secondary #8E8E93, Accent #E5E5EA. Функциональные цвета состояний: Норма #8E8E93, Внимание #FFD60A, Критично #FF453A. Шрифт: Inter. Отрисовка трех ключевых экранов (Главный список Холодильник, Камера, Профиль) и всплывающего оверлея подтверждения AI со скруглением углов карточек 16dp. Подготовка интерфейсных состояний для Кейсов Б и В (пустые поля дат, предупреждающие плашки)."},
    {"id": "TASK-1.2", "sprint": "MVP (Must)", "level": "Backend / Локальная БД", "name": "Архитектура и развертывание локальной БД Room", "owner": "Арсений", "blockers": [], "duration": 3, "start_day": 1, "color": "#FF453A", "tz": "Развертывание локальной структуры базы данных Room (SQLite) на устройстве. Создание основной сущности и таблицы products. Обязательные для реализации поля модели: id (INT, Primary Key, AutoIncrement), name (TEXT), category_id (INT), expiration_date (TIMESTAMP), is_opened (BOOLEAN, default false), opened_at (TIMESTAMP, NULL), datamatrix_cache (TEXT, NULL). Настройка индексов по полю expiration_date для ускорения автоматической сортировки списков. Создание сопутствующей таблицы для инкремента и учета недельных лимитов сканирования."},
    {"id": "TASK-1.3", "sprint": "MVP (Must)", "level": "Frontend / UI Камеры", "name": "Интеграция модуля камеры и захвата 5-секундного видео", "owner": "Арсений", "blockers": ["TASK-1.1"], "duration": 4, "start_day": 5, "color": "#FF453A", "tz": "Интеграция нативного CameraX API Android в интерфейс приложения. Обработка клика по центральной кнопке Плюс из Bottom Navigation. Настройка сценария захвата: при нажатии открывается видоискатель, запускается запись короткого видеопотока строго до 5 секунд. Автоматическое сохранение полученного медиафайла во временный кэш приложения. Реализация фонового скрипта для покадровой нарезки видеопотока и передачи массива изображений в пайплайн ИИ-обработки."},
    {"id": "TASK-1.4", "sprint": "MVP (Must)", "level": "Backend / Препроцессинг", "name": "Модуль валидации строк и кэширования DataMatrix в офлайне", "owner": "Арсений", "blockers": ["TASK-1.2"], "duration": 3, "start_day": 4, "color": "#FF453A", "tz": "Реализация логики безопасного офлайн-препроцессинга. Разработка бэкенд-модуля валидации считанных с камеры строк кода. Строка проверяется на соответствие стандартам кодирования Честного Знака (наличие обязательных управляющих символов, префиксов и длины структуры для отсечения смазанных кадров). Если строка валидна — запись в таблицу datamatrix_cache. Если строка повреждена — вызов интерфейсного алерта об ошибке чтения без списания недельного лимита. Интеграция с системным ConnectivityManager для отслеживания сети и фоновой отправки накопленного кэша при появлении интернета. Арсений делает эту задачу полностью самостоятельно."},
    {"id": "TASK-1.5", "sprint": "MVP (Must)", "level": "Сеть / API Честного Знака", "name": "Интеграция с API Честного Знака и экран подтверждения", "owner": "Арсений", "blockers": ["TASK-1.3", "TASK-1.4"], "duration": 4, "start_day": 9, "color": "#FF453A", "tz": "Настройка сетевого клиента для взаимодействия с официальным тестовым/продуктовым API Честного Знака. Отправка валидированной строки кода, парсинг входящего JSON-ответа. Извлечение ключевых полей: наименование продукта, состав, точная дата окончания срока годности. Передача объекта в Frontend для рендеринга модального AI-оверлея подтверждения. Реализация жесткого бизнес-правила: еженедельный лимит (10 бесплатных попыток) уменьшается строго в момент успешного клика пользователя по кнопке ОК, добавить в холодильник. Сброс лимитов — жестко каждый понедельник в 00:00."},
    {"id": "TASK-1.6", "sprint": "MVP (Must)", "level": "ИИ / On-device AI", "name": "Локальный CV-пайплайн фабричных товаров и OCR дат", "owner": "Настя", "blockers": ["TASK-1.2", "TASK-1.3"], "duration": 5, "start_day": 9, "color": "#FF453A", "tz": "Must-версия интеллектуального фоллбэка для фабричных продуктов без маркировки (например, хлеб, батон). Настина часть: сбор датасетов, обучение и оптимизация легковесных open-source моделей компьютерного зрения для классификации базовых категорий еды и OCR-моделей для распознавания напечатанного текста дат. Конвертация готовых весов в формат TFLite/ONNX. Часть Арсения: интеграция моделей на устройство через ChaquoPy/нативный движок, запуск покадрового анализа, если Шаг 1 (Честный Знак) вернул пустой результат. Распознавание дат в текстовых форматах ДД.ММ.ГГГГ и ДД.ММ.ГГ."},
    {"id": "TASK-1.7", "sprint": "MVP (Must)", "level": "ИИ / Алгоритмы", "name": "Алгоритм умного расчета средних сроков хранения", "owner": "Настя", "blockers": ["TASK-1.2", "TASK-1.5"], "duration": 3, "start_day": 13, "color": "#FF453A", "tz": "Реализация сквозной try-except логики при отсутствии жестких дат (Кейс В или клик по кнопке Не знаю срок годности). Настина часть: сбор, очистка и подготовка статического структурированного справочника средних сроков хранения для ключевых категорий продуктов. Часть Арсения: внедрение формул расчета в логику приложения. Для скоропорта (молоко, хлеб): ExpirationDate = Текущая дата устройства + константа категории. Для долгосрочных товаров: подтягивание нормативного срока хранения (например, 12 месяцев) с выводом плашки о неизвестной дате производства и немедленным принудительным переключением индикатора карточки в желтый цвет предупреждения #FFD60A."},
    {"id": "TASK-1.8", "sprint": "MVP (Must)", "level": "Frontend + Бизнес-логика", "name": "Логика вскрытия продуктов и мгновенного пересчета дат", "owner": "Арсений", "blockers": ["TASK-1.1", "TASK-1.2"], "duration": 4, "start_day": 5, "color": "#FF453A", "tz": "Реализация логики контроля открытых упаковок. На уровне Frontend: размещение на каждой карточке товара в списке Холодильник активной иконки-крышки с увеличенной зоной тача 44x44dp. При клике на иконку (или выборе чекбокса на экране подтверждения) запускается бэкенд-метод пересчета: поле is_opened меняется на true, opened_at записывает текущий таймстамп. Система считывает значение opened_storage_life для данной категории из БД и жестко перезаписывает ExpirationDate по формуле: opened_at + opened_storage_life. Интерфейс мгновенно пересортировывает список, поднимая товар наверх в соответствии с новой критичностью."},
    {"id": "TASK-1.9", "sprint": "MVP (Must)", "level": "Backend / Службы", "name": "Воркер push-уведомлений и жесткий сброс лимитов", "owner": "Арсений", "blockers": ["TASK-1.2"], "duration": 3, "start_day": 4, "color": "#FF453A", "tz": "Настройка системной фоновой службы Android с использованием WorkManager. Периодичность проверки локальной базы данных — каждые 12 часов. Воркер рассчитывает разницу во времени между текущим моментом и полем expiration_date для каждого продукта. Генерация локальных push-уведомлений происходит строго по расписанию: первый алерт среднего уровня отправляется ровно за 3 дня до просрочки, второй критический алерт — ровно за 24 часа. Тексты пушей берутся строго из регламента ToV in PRD."},
    {"id": "TASK-2.1", "sprint": "Early Access (Should/Could)", "level": "ИИ / Компьютерное зрение", "name": "Локальная CV-классификация домашней еды в контейнерах", "owner": "Настя", "blockers": ["TASK-1.6"], "duration": 6, "start_day": 16, "color": "#FFD60A", "tz": "Развитие CV-пайплайна для работы со сложными объектами. Настина часть: сбор кастомного датасета, разметка и обучение специализированной нейросети для детектирования и классификации типов домашней готовой еды через пластиковые/стеклянные контейнеры. Оптимизация весов под мобильные процессоры. Часть Арсения: интеграция обновленной ИИ-модели в пайплайн камеры. На этапе MVP алгоритм при обнаружении контейнера просто проставляет тип Домашняя еда, выводит сервисную плашку об автоматическом распознавании в будущих апдейтах и оставляет поле даты пустым для ручного ввода."},
    {"id": "TASK-2.2", "sprint": "Early Access (Should)", "level": "Frontend / Micro-animations", "name": "Сложные микроанимации switch-контроля вскрытия", "owner": "Настя", "blockers": ["TASK-1.8"], "duration": 4, "start_day": 16, "color": "#FFD60A", "tz": "Концептуальное и визуальное обновление интерфейса карточки продукта. Замена стандартной минималистичной иконки крышки из MVP на сложный кастомный элемент управления. Настина часть: художественная проработка концепции, отрисовка раскадровок и визуального стиля микроанимации общими словами без жестких ограничений кода. Элемент должен имитировать физический, плавный, тактильно приятный отрыв защитной фольги или пленки со стаканчика йогурта при выполнении жеста свайпа. Часть Арсения: техническая реализация и программирование анимации изменения геометрии и формы шейпов на фронтенде Android."},
    {"id": "TASK-3.1", "sprint": "Scaling (Could)", "level": "Бэкенд / Серверный API", "name": "Серверная БД PostgreSQL/MongoDB и глобальный справочник", "owner": "Арсений", "blockers": ["TASK-1.4"], "duration": 5, "start_day": 16, "color": "#8E8E93", "tz": "Переход от полностью изолированного локального приложения к гибридной клиент-серверной архитектуре. Настина часть: проектирование структуры, очистка и наполнение удаленных баз данных PostgreSQL / MongoDB глобальными справочниками соответствия штрихкодов, фабричных названий, составов и нормативных сроков хранения закрытой/вскрытой продукции по категориям. Часть Арсения: развертывание серверной инфраструктуры, написание защищенных эндпоинтов REST API для синхронизации локальных баз Room с сервером при обновлении глобальных каталогов."},
    {"id": "TASK-3.2", "sprint": "Scaling (Could)", "level": "ИИ / Рекомендации", "name": "ИИ-модуль динамического планирования рациона Zero Waste", "owner": "Настя", "blockers": ["TASK-3.1"], "duration": 7, "start_day": 21, "color": "#8E8E93", "tz": "Разработка интеллектуального ядра рекомендательной системы на Python. Модель должна анализировать текущие остатки продуктов в локальной БД пользователя и формировать меню. Ключевые требования: 1. Алгоритм предварительного бронирования ингредиентов под выбранные блюда с расчетом запаса их жизненного цикла. 2. Динамический автоматический пересчет и перестройка плана рецептов на лету при добавлении новых или удалении съеденных продуктов из холодильника. 3. Логирование действий пользователя (лайки, отказы от рецептов) для постоянного дообучения ИИ-модели под индивидуальные ЗОЖ-предпочтения."}
]

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def get_task_short_name(task_id):
    """Получает краткое название таска для отображения в блокерах"""
    for task in TASKS:
        if task["id"] == task_id:
            name = task["name"]
            return (name[:22] + '...') if len(name) > 22 else name
    return task_id

saved_data = load_state()
for t in TASKS:
    if t["id"] not in st.session_state:
        st.session_state[t["id"]] = saved_data.get(t["id"], False)

col_f1, col_f2 = st.columns(2)
with col_f1:
    filter_owner = st.selectbox("Фильтр по исполнителю", ["Все", "Настя", "Арсений"])
with col_f2:
    filter_sprint = st.selectbox("Фильтр по этапу", ["Все", "MVP (Must)", "Early Access (Should/Could)", "Scaling (Could)"])

def is_blocked(blockers):
    for b in blockers:
        if not st.session_state.get(b, False):
            return True, b
    return False, None

filtered_tasks = []
for t in TASKS:
    if filter_owner != "Все" and t["owner"] != filter_owner:
        continue
    if filter_sprint != "Все" and filter_sprint not in t["sprint"]:
        continue
    filtered_tasks.append(t)

st.markdown("<p style='font-size:20px; font-weight:bold; margin-top:20px;'>🗺️ Дорожная карта проекта (Gantt Chart)</p>", unsafe_allow_html=True)

total_days = 28
calculated_height = 60 + (len(filtered_tasks) * 44)
if calculated_height < 150:
    calculated_height = 150

timeline_html = """
<html>
 <head>
 <style>
body { background-color: #121212; margin: 0; padding: 0; font-family: sans-serif; color: #FFFFFF; }
.gantt-container { background-color: #1E1E1E; padding: 15px; border-radius: 12px; box-sizing: border-box; }
.gantt-header { display: flex; border-bottom: 1px solid #3A3A3C; padding-bottom: 8px; margin-bottom: 10px; font-size: 12px; color: #8E8E93; }
.gantt-role-col { width: 130px; min-width: 130px; font-weight: bold; color: #FFFFFF; font-size: 12px; padding-right: 10px; display: flex; align-items: center; }
.gantt-task-name { width: 260px; min-width: 260px; font-weight: bold; color: #FFFFFF; font-size: 12px; padding-right: 10px; display: flex; align-items: center; }
.gantt-days-col { display: flex; flex-grow: 1; }
.gantt-day-head { flex: 1; text-align: center; min-width: 20px; border-left: 1px solid #2C2C2E; }
.gantt-row { display: flex; height: 38px; align-items: center; border-bottom: 1px solid #2C2C2E; font-size: 13px; box-sizing: border-box; }
.gantt-row .gantt-role-col { color: #8E8E93; font-weight: normal; }
.gantt-row .gantt-task-name { color: #FFFFFF; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-weight: normal; font-size: 13px;}
.gantt-bar-area { display: flex; flex-grow: 1; position: relative; height: 24px; background-color: #121212; border-radius: 4px; }
.gantt-bar { position: absolute; height: 100%; border-radius: 4px; display: flex; align-items: center; padding-left: 8px; font-weight: bold; font-size: 11px; box-sizing: border-box; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;}
 </style>
 </head>
 <body>
 <div class="gantt-container">
 <div class="gantt-header">
 <div class="gantt-role-col">Роль</div>
 <div class="gantt-task-name">Задача</div>
 <div class="gantt-days-col">
"""

for d in range(1, total_days + 1):
    timeline_html += f'<div class="gantt-day-head">д{d}</div>'
timeline_html += "</div></div>"

for t in filtered_tasks:
    blocked, b_id = is_blocked(t["blockers"])
    status_style = "opacity: 0.4;" if blocked else ""
    if st.session_state[t["id"]]:
        status_style = "opacity: 0.3; text-decoration: line-through;"
        
    start_pct = ((t["start_day"] - 1) / total_days) * 100
    width_pct = (t["duration"] / total_days) * 100
    
    # Логика текста внутри бара
    if blocked:
        short_name = get_task_short_name(b_id)
        bar_text = f"🔒 {short_name}"
        bar_color = "#3A3A3C"
        text_color = "#8E8E93"
    else:
        bar_text = f"{t['id']} ({t['owner']})"
        bar_color = t["color"]
        text_color = "#121212"
        
    # Логика бейджа роли
    role = ROLE_MAP.get(t["id"], "General")
    r_color = ROLE_COLORS.get(role, "#8E8E93")
    role_badge = f'<span style="background-color: #2C2C2E; color: {r_color}; padding: 3px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; border: 1px solid {r_color}30;">{role}</span>'

    timeline_html += f"""
 <div class="gantt-row" style="{status_style}">
     <div class="gantt-role-col">{role_badge}</div>
     <div class="gantt-task-name"><b>[{t['id']}]</b> {t['name']}</div>
     <div class="gantt-bar-area">
         <div class="gantt-bar" style="left: {start_pct}%; width: {width_pct}%; background-color: {bar_color}; color: {text_color};">
             {bar_text}
         </div>
     </div>
 </div>
 """

timeline_html += "</div></body></html>"
st.components.v1.html(timeline_html, height=calculated_height, scrolling=True)

st.markdown("<p style='font-size:20px; font-weight:bold; margin-top:30px;'>📋 Интерактивное управление бэклогом задач</p>", unsafe_allow_html=True)

state_changed = False
for t in filtered_tasks:
    blocked, b_id = is_blocked(t["blockers"])
    card_border = t["color"] if not blocked else "#3A3A3C"
    
    st.markdown(
        f"""
        <div style="background-color: #1E1E1E; border-left: 6px solid {card_border}; padding: 12px; margin-bottom: 2px; border-radius: 4px 8px 8px 4px;">
            <span style="background-color: {card_border}; color: #121212; padding: 2px 6px; font-weight: bold; border-radius: 4px; font-size: 11px; margin-right: 8px;">{t['sprint']}</span>
            <span style="color: #8E8E93; font-size: 12px; margin-right: 15px;"><b>Раздел:</b> {t['level']}</span>
            <span style="color: #FFFFFF; font-weight: bold; margin-right: 15px;">👤 Исполнитель: {t['owner']}</span>
            <p style="color: #FFFFFF; font-size: 15px; margin-top: 5px; margin-bottom: 2px;"><b>{t['id']}:</b> {t['name']}</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    with st.expander("Посмотреть подробное техническое задание (ТЗ) задачи"):
        st.write(t["tz"])
        
    if blocked:
        short_blocker_name = get_task_short_name(b_id)
        st.checkbox(f"🔒 Задача заблокирована. Ожидает: {b_id} ({short_blocker_name})", value=False, disabled=True, key=f"cb_dis_{t['id']}")
    else:
        old_val = st.session_state[t["id"]]
        new_val = st.checkbox(f"Отметить выполнение {t['id']}", value=old_val, key=f"cb_act_{t['id']}")
        if new_val != old_val:
            st.session_state[t["id"]] = new_val
            state_changed = True

if state_changed:
    current_state = {t["id"]: st.session_state[t["id"]] for t in TASKS}
    save_state(current_state)
    st.rerun()
