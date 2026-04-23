import streamlit as st

# Sivun asetukset
st.set_page_config(page_title="Mainonnan tuottolaskuri", page_icon="📈")

st.title("📈 Mainonnan kannattavuuslaskuri")
st.write("Säädä arvoja nähdäksesi, millaisilla luvuilla mainonta on voitollista.")

# 1. Kateasetus (Input-kenttä)
st.sidebar.header("Tuotteen tiedot")
kate = st.sidebar.number_input("Tuotteen kate (€ per myynti)", value=15.50, step=0.10)

# 2. Mainonnan muuttujat (Sliderit)
st.subheader("Säädä mainonnan lukuja")

cpm = st.slider("CPM (Hinta 1000 näyttökerralle)", min_value=0.5, max_value=100.0, value=10.0, step=0.5)
ctr = st.slider("CTR % (Mainoksen klikkausprosentti)", min_value=0.1, max_value=15.0, value=1.0, step=0.1)
cr = st.slider("Konversioprosentti % (Sivuston ostokset per kävijä)", min_value=0.1, max_value=20.0, value=2.0, step=0.1)

# 3. Laskentakaava
# Lasketaan kuinka monta näyttöä tarvitaan yhteen kauppaan:
# 1000 näyttöä tuottaa (1000 * CTR% * CR%) kauppaa.
# CPA = CPM / (10 * CTR * CR)
cpa = cpm / (10 * ctr * cr)
voitto = kate - cpa

# 4. Tulosten näyttäminen
st.divider()

col1, col2 = st.columns(2)
col1.metric("Asiakashankintahinta (