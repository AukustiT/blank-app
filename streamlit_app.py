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
col1.metric("Asiakashankintahinta (CPA)", f"{cpa:.2f} €")
col2.metric("Voitto per myynti", f"{voitto:.2f} €", delta=f"{voitto:.2f} €")

# Visuaalinen palaute
if voitto > 0:
    st.success(f"✅ VOITOLLISTA! Jää viivan alle: {voitto:.2f} €")
    st.balloons()
else:
    st.error(f"❌ TAPPIOLLISTA. Häviät per myynti: {abs(voitto):.2f} €")

# 5. Mikä pitäisi olla CTR tai CR?
st.divider()
st.subheader("Mitä vaaditaan nollatulokseen?")

needed_cr = (cpm / (10 * ctr * kate))
needed_ctr = (cpm / (10 * cr * kate))

st.write(f"• Jotta pääset omillesi nykyisellä CTR:llä ({ctr}%), konversioasteen on oltava vähintään **{needed_cr:.2f} %**.")
st.write(f"• Jotta pääset omillesi nykyisellä konversiolla ({cr}%), CTR:n on oltava vähintään **{needed_ctr:.2f} %**.")

st.caption("Kaava: CPA = CPM / (10 * CTR * CR) | Voitto = Kate - CPA")