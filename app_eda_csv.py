import streamlit as st
import pandas as pd

# Настройка страницы (широкая, заголовок вкладки)
st.set_page_config(page_title="EDA Dashboard", page_icon="📊", layout="wide")

# --- СТИЛИ (чуть-чуть CSS для красоты) ---
st.markdown("""
<style>
    .stMetric {
        border: 1px solid rgba(128, 128, 128, 0.3); 
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
    }
</style>
""", unsafe_allow_html=True)

# --- БОКОВАЯ ПАНЕЛЬ (Sidebar) ---
with st.sidebar:
    st.header("⚙️ Настройки")
    
    # Принимаем несколько файлов! accept_multiple_files=True
    uploaded_files = st.file_uploader("Загрузите CSV файлы", type=['csv'], accept_multiple_files=True)
    
    selected_file_name = None
    selected_file = None
    
    # Если загружен хотя бы один файл, показываем переключатель
    if uploaded_files:
        # Собираем названия загруженных файлов
        file_names = [f.name for f in uploaded_files]
        # Создаем выпадающий список для выбора
        selected_file_name = st.selectbox("Выберите файл для анализа:", file_names)
        
        # Находим объект файла по выбранному названию
        selected_file = next((f for f in uploaded_files if f.name == selected_file_name), None)

# Главный заголовок
st.title("📊 Анализ данных (EDA)")

# Если файл выбран, работаем с ним
if selected_file is not None:
    # Показываем название файла, который сейчас анализируем
    st.caption(f"📂 Текущий файл: `{selected_file_name}`")
    
    df = pd.read_csv(selected_file)
    rows, cols = df.shape

    # --- БЛОК 1: KPI КАРТОЧКИ ---
    st.markdown("### 📈 Основные метрики")
    
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Всего строк", rows)
    col2.metric("Всего колонок", cols)
    
    full_dups = df.duplicated().sum()
    
    if full_dups > 0:
        col3.metric("Дубликатов", full_dups)
    else:
        col3.metric("Дубликатов", "0 ✅")
        
    total_cells = rows * cols
    total_missing = df.isna().sum().sum()
    missing_pct = round((total_missing / total_cells) * 100, 2)
    col4.metric("Пропусков всего", f"{missing_pct}%")

    st.markdown("---")

    # --- БЛОК 2: ПРОСМОТР ДАННЫХ И ПРОПУСКОВ ---
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.subheader("👀 Первые 5 строк")
        st.dataframe(df.head(), use_container_width=True)

    with col_right:
        st.subheader("🧹 Качество данных (Пропуски)")
        column_info = []
        for col in df.columns:
            missing_count = df[col].isna().sum()
            missing_percent = round((missing_count / rows) * 100, 2)
            dtype = df[col].dtype
            column_info.append({
                'Колонка': col,
                'Тип': dtype,
                'Пропусков': missing_count,
                '% пропусков': missing_percent
            })
        info_df = pd.DataFrame(column_info)
        st.dataframe(info_df, use_container_width=True)

    # --- БЛОК 3: СТАТИСТИКА (В СПРОЙЛЕРЕ) ---
    st.markdown("---")
    st.subheader("📚 Подробная статистика")
    
    with st.expander("Статистика по ЧИСЛОВЫМ колонкам"):
        st.dataframe(df.describe().T, use_container_width=True)
        
    with st.expander("Статистика по ТЕКСТОВЫМ колонкам"):
        text_stats = df.describe(include='object').T
        if not text_stats.empty:
            st.dataframe(text_stats[['count', 'unique', 'top', 'freq']], use_container_width=True)
        else:
            st.write("Текстовых колонок не найдено.")

else:
    # Если файлы не загружены, показываем заглушку
    st.info("👈 Пожалуйста, загрузите один или несколько CSV-файлов в боковой панели слева.")
