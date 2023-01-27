
description = "Country Data"
def run():
    import streamlit as st
    import pandas as pd
    import plotly.express as px


    # Countries
    df = pd.DataFrame(px.data.gapminder())
    clist = df['country'].unique()

    country = st.selectbox("Select a country:", clist)

    col1, col2 = st.columns(2)

    fig = px.line(df[df['country'] == country],
        x="year", y="gdpPercap", title="GDP per Capita")
    col1.plotly_chart(fig, use_container_width=True)

    fig = px.line(df[df['country'] == country],
        x="year", y="pop", title="Population Growth")
    col2.plotly_chart(fig, use_container_width=True)


# This code allows you to run the app standalone
# as well as part of a library of apps
if __name__ == "__main__":
    run()
