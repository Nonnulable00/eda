import streamlit as st
import pandas as pd

# Настройка страницы (широкая, заголовок вкладки)
st.set_page_config(page_title="EDA Dashboard", page_icon="📊", layout="wide")

# --- СТИЛИ (чуть-чуть CSS для красоты) ---
# Увеличиваем шрифт и делаем фон чуть темнее в боковой панели
st.markdown("""
<style>
    .stMetric { border: 1px solid #e0e0e0; border-radius: 10px; padding: 15px; background-color: #f9f9f9; }
</style>
""", unsafe_allow_html=True)

# --- БОКОВАЯ ПАНЕЛЬ (Sidebar) ---
with st.sidebar:
    st.header("⚙️ Настройки")
    uploaded_file = st.file_uploader("Загрузите CSV файл", type=['csv'])
    st.markdown("---")
    st.write("💡 **Tip:** Это веб-приложение автоматически ищет пропуски, дубликаты и аномалии в данных.")

# Главный заголовок
st.title("📊 Интеллектуальный анализ данных (EDA)")

# Если файл загружен, работаем
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    rows, cols = df.shape

    # --- БЛОК 1: KPI КАРТОЧКИ ---
    st.markdown("### 📈 Основные метрики")
    
    # Разбиваем экран на 4 колонки
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Всего строк", rows)
    col2.metric("Всего колонок", cols)
    
    full_dups = df.duplicated().sum()
    
    if full_dups > 0:
        col3.metric("Дубликатов", full_dups)
    else:
        col3.metric("Дубликатов", "0 ✅")
        
    # Считаем процент пропусков по всей таблице
    total_cells = rows * cols
    total_missing = df.isna().sum().sum()
    missing_pct = round((total_missing / total_cells) * 100, 2)
    col4.metric("Пропусков всего", f"{missing_pct}%")

    st.markdown("---")

    # --- БЛОК 2: ПРОСМОТР ДАННЫХ И ПРОПУСКОВ ---
    col_left, col_right = st.columns([1, 1]) # Две колонки одинаковой ширины

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
    
    # Expander делает блок сворачиваемым
    with st.expander("Развернуть статистику по ЧИСЛОВЫМ колонкам"):
        st.dataframe(df.describe().T, use_container_width=True)
        
    with st.expander("Развернуть статистику по ТЕКСТОВЫМ колонкам"):
        text_stats = df.describe(include='object').T
        if not text_stats.empty:
            st.dataframe(text_stats[['count', 'unique', 'top', 'freq']], use_container_width=True)
        else:
            st.write("Текстовых колонок не найдено.")

else:
    # Если файл не загружен, показываем красивую заглушку
    st.info("👈 Пожалуйста, загрузите CSV-файл в боковой панели слева.")