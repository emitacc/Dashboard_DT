import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    layout="wide",
    page_title="DDashboard - Dados MRO"
)

@st.cache_data
def load_data():
    df = pd.read_parquet("Dados MRO-10_RAW.parquet")
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    return df

df = load_data()

# Sidebar para seleção de intervalo de tempo
st.sidebar.header("Filtrar por período")
start_date = st.sidebar.date_input("Data de início", df["Timestamp"].min().date())
start_time = st.sidebar.time_input("Hora de início", df["Timestamp"].min().time())
end_date = st.sidebar.date_input("Data de fim", df["Timestamp"].max().date())
end_time = st.sidebar.time_input("Hora de fim", df["Timestamp"].max().time())

# Combinar data e hora selecionadas
start_datetime = pd.to_datetime(f"{start_date} {start_time}")
end_datetime = pd.to_datetime(f"{end_date} {end_time}")

# Filtrar os dados com base na seleção do usuário
df_filtered = df[(df["Timestamp"] >= start_datetime) & (df["Timestamp"] <= end_datetime)]

# Criar o gráfico de série temporal
st.title("Série Temporal - P_PDG_AN_SUP")
fig = px.line(df_filtered, x="Timestamp", y="P_PDG_AN_SUP", title="Pressão no Ponto PDG AN SUP")
st.plotly_chart(fig, use_container_width=True)

# Exibir os dados filtrados
#st.write("### Dados Filtrados")
#df_filtered