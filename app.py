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
    <div class="subtitle">Панель синхронизации: Таймлайн (Диаграмма Ганта), зависимости и распределение ролей (Настя / Арсений)</div>
    """, 
    unsafe_allow_html=True
)

STATE_FILE = "backlog_state.json"

TASKS = [
    {"id": "TASK-1.1", "sprint": "MVP (Must)", "level": "UI/UX / Прототипирование", "name": "Проектирование UI/UX дизайн-системы и экранов в Figma", "owner": "Настя", "blockers": [], "duration": 4, "start_day": 1, "color": "#FF453A"},
    {"id": "TASK-1.2", "sprint": "MVP (Must)", "level": "Backend / Локальная БД", "name": "Архитектура и развертывание локальной БД Room", "owner": "Арсений", "blockers": [], "duration": 3, "start_day": 1, "color": "#FF453A"},
    {"id": "TASK-1.3", "sprint": "MVP (Must)", "level": "Frontend / UI Камеры", "name": "Интеграция модуля камеры и захвата 5-секундного видео", "owner": "Арсений", "blockers": ["TASK-1.1"], "duration": 4, "start_day": 5, "color": "#FF453A"},
    {"id": "TASK-1.4", "sprint": "MVP (Must)", "level": "Backend / Препроцессинг", "name": "Модуль валидации строк и кэширования DataMatrix в офлайне", "owner": "Арсений", "blockers": ["TASK-1.2"], "duration": 3, "start_day": 4, "color": "#FF453A"},
    {"id": "TASK-1.5", "sprint": "MVP (Must)", "level": "Сеть / API Честного Знака", "name": "Интеграция с API Честного Знака и экран подтверждения", "owner": "Арсений", "blockers": ["TASK-1.3", "TASK-1.4"], "duration": 4, "start_day": 9, "color": "#FF453A"},
    {"id": "TASK-1.6", "sprint": "MVP (Must)", "level": "ИИ / On-device AI", "name": "Локальный CV-пайплайн фабричных товаров и OCR дат", "owner": "Настя", "blockers": ["TASK-1.2", "TASK-1.3"], "duration": 5, "start_day": 9, "color": "#FF453A"},
    {"id": "TASK-1.7", "sprint": "MVP (Must)", "level": "ИИ / Алгоритмы", "name": "Алгоритм умного расчета средних сроков хранения", "owner": "Настя", "blockers": ["TASK-1.2", "TASK-1.5"], "duration": 3, "start_day": 13, "color": "#FF453A"},
    {"id": "TASK-1.8", "sprint": "MVP (Must)", "level": "Frontend + Бизнес-логика", "name": "Логика вскрытия продуктов и мгновенного пересчета дат", "owner": "Арсений", "blockers": ["TASK-1.1", "TASK-1.2"], "duration": 4, "start_day": 5, "color": "#FF453A"},
    {"id": "TASK-1.9", "sprint": "MVP (Must)", "level": "Backend / Службы", "name": "Воркер push-уведомлений и жесткий сброс лимитов", "owner": "Арсений", "blockers": ["TASK-1.2"], "duration": 3, "start_day": 4, "color": "#FF453A"},
    {"id": "TASK-2.1", "sprint": "Early Access (Should/Could)", "level": "ИИ / Компьютерное зрение", "name": "Локальная CV-классификация домашней еды в контейнерах", "owner": "Настя", "blockers": ["TASK-1.6"], "duration": 6, "start_day": 16, "color": "#FFD60A"},
    {"id": "TASK-2.2", "sprint": "Early Access (Should)", "level": "Frontend / Микроанимации", "name": "Сложные микроанимации switch-контроля вскрытия", "owner": "Настя", "blockers": ["TASK-1.8"], "duration": 4, "start_day": 16, "color": "#FFD60A"},
    {"id": "TASK-3.1", "sprint": "Scaling (Could)", "level": "Бэкенд / Серверный API", "name": "Серверная БД PostgreSQL/MongoDB и глобальный справочник", "owner": "Арсений", "blockers": ["TASK-1.4"], "duration": 5, "start_day": 16, "color": "#8E8E93"},
    {"id": "TASK-3.2", "sprint": "Scaling (Could)", "level": "ИИ / Рекомендации", "name": "ИИ-модуль динамического планирования рациона Zero Waste", "owner": "Настя", "blockers": ["TASK-3.1"], "duration": 7, "start_day": 21, "color": "#8E8E93"}
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

html_content = """
<style>
.gantt-container { background-color: #1E1E1E; padding: 15px; border-radius: 12px; font-family: sans-serif; overflow-x: auto; color: #FFFFFF; }
.gantt-header { display: flex; border-bottom: 1px solid #3A3A3C; padding-bottom: 8px; margin-bottom: 10px; font-size: 12px; color: #8E8E93; }
.gantt-label-col { width: 250px; min-width: 250px; font-weight: bold; }
.gantt-days-col { display: flex; flex-grow: 1; }
.gantt-day-head { flex: 1; text-align: center; min-width: 25px; border-left: 1px solid #2C2C2E; }
.gantt-row { display: flex; padding: 8px 0; align-items: center; border-bottom: 1px solid #2C2C2E; font-size: 13px; }
.gantt-task-name { width: 250px; min-width: 250px; color: #FFFFFF; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; padding-right: 10px; }
.gantt-bar-area { display: flex; flex-grow: 1; position: relative; height: 26px; background-color: #121212; border-radius: 6px; width: 100%; min-width: 700px; }
.gantt-bar { position: absolute; height: 100%; border-radius: 6px; display: flex; align-items: center; padding-left: 8px; font-weight: bold; font-size: 11px; }
</style>
<div class="gantt-container">
    <div class="gantt-header">
        <div class="gantt-label-col">Этап / Задача</div>
        <div class="gantt-days-col">
"""

for d in range(1, total_days + 1):
    html_content += f'<div class="gantt-day-head">д{d}</div>'
html_content += "</div></div>"

for t in filtered_tasks:
    blocked, b_id = is_blocked(t["blockers"])
    status_style = "opacity: 0.4;" if blocked else ""
    if st.session_state[t["id"]]:
        status_style = "opacity: 0.3; text-decoration: line-through;"
    
    start_pct = ((t["start_day"] - 1) / total_days) * 100
    width_pct = (t["duration"] / total_days) * 100
    
    bar_text = f"{t['id']} ({t['owner']})"
    if blocked:
        bar_text = f"🔒 Блок: {b_id}"
        bar_color = "#3A3A3C"
        text_color = "#8E8E93"
    else:
        bar_color = t["color"]
        text_color = "#121212"
        
    html_content += f"""
    <div class="gantt-row" style="{status_style}">
        <div class="gantt-task-name"><b>[{t['id']}]</b> {t['name']}</div>
        <div class="gantt-bar-area">
            <div class="gantt-bar" style="left: {start_pct}%; width: {width_pct}%; background-color: {bar_color}; color: {text_color};">
                {bar_text}
            </div>
        </div>
    </div>
    """

html_content += "</div>"

st.components.v1.html(html_content, height=450, scrolling=True)

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
    
    if blocked:
        st.checkbox(f"🔒 Задача заблокирована, пока не выполнен таск {b_id}", value=False, disabled=True, key=f"cb_dis_{t['id']}")
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
