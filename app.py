import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="SaaS Investor ssb Dashboard", layout="wide")

st.title("📊 SaaS Investor Sensesbit Dashboard")

uploaded_file = st.sidebar.file_uploader("Sube tu Excel", type=["xlsx", "xls", "csv"])

if uploaded_file:
    df_data = pd.read_excel(uploaded_file, sheet_name="Data")
    df_prices = pd.read_excel(uploaded_file, sheet_name="Prices")

    df_data["Date"] = pd.to_datetime(df_data["Date"])
    df_data["Year"] = df_data["Date"].dt.year
    df_data["Month"] = df_data["Date"].dt.month_name()

    # Filtros
    st.sidebar.header("Filtros")
    years = st.sidebar.multiselect("Años", options=sorted(df_data["Year"].unique()), default=sorted(df_data["Year"].unique()))
    months = st.sidebar.multiselect("Meses", options=df_data["Month"].unique(), default=df_data["Month"].unique())
    plans = st.sidebar.multiselect("Plan", options=df_data["Plan"].unique(), default=df_data["Plan"].unique())

    componentes = st.sidebar.multiselect(
        "Componentes Net New",
        options=["New MRR (€)", "Expansion MRR (€)", "Churned MRR (€)", "Downgraded MRR (€)"],
        default=["New MRR (€)", "Expansion MRR (€)", "Churned MRR (€)", "Downgraded MRR (€)"]
    )

    df_filtered = df_data[df_data["Year"].isin(years) & df_data["Month"].isin(months) & df_data["Plan"].isin(plans)]

    # KPIs
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Clientes activos", df_filtered["Active Customers"].iloc[-1])
    with col2:
        st.metric("MRR total", f"€{df_filtered['MRR'].iloc[-1]:,.0f}")
    with col3:
        st.metric("ARR total", f"€{df_filtered['ARR'].iloc[-1]:,.0f}")

    # Gráfico Net New filtrable
    df_melted = df_filtered.melt(id_vars=["Date"], value_vars=componentes, var_name="Tipo", value_name="Valor")

    chart = alt.Chart(df_melted).mark_area(opacity=0.6).encode(
        x="Date:T",
        y="Valor:Q",
        color="Tipo:N"
    )
    st.altair_chart(chart, use_container_width=True)
else:
    st.info("Por favor, sube un archivo Excel con las hojas 'Data' y 'Prices'.")

