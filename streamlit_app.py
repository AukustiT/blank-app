import streamlit as st
import numpy as np

# Sivun tyyli ja asetukset
st.set_page_config(page_title="Nollatulos-tasapainottaja", layout="centered")

st.title("⚖️ Nollatulos-tasapainottaja")
st.write("Aseta kate ja kulut. Slider näyttää kaikki mahdolliset yhdistelmät, joilla pääset omillesi.")

# 1. Syöttökentät (Boxit)
col_a, col_b = st.columns(2)
with col_a:
    kate = st.number_input("Tuotteen kate (€)", value=15.50, step=0.10, format="%.2f")
with col_b:
    cpm = st.number_input("Cost per 1000 (CPM) (€)", value=10.0, step=0.10, format="%.2f")

# Matematiikka:
# Break-even kaava: Kate * (CTR/100) * (CR/100) = CPM / 1000
# Lyhennettynä: CTR * CR = CPM / (0.1 * Kate)
target_constant = cpm / (0.1 * kate)

# Ääripäät:
# Jos CTR = 100%, CR = target_constant / 100
# Jos CR = 100%, CTR = target_constant / 100
min_limit = target_constant / 100
max_limit = 100.0

st.divider()

# 2. "Cleanimpi" Slider
# Käytetään logaritmista skaalaa, jotta liike on luonnollinen (smooth)
st.subheader("CTR vs. Konversio -liukuhihna")
st.caption(f"Kaikki alla olevat pisteet kuluttavat tasan {kate:.2f} € mainontaan per kauppa.")

# Slider arvo 0-100 (edustaa prosentuaalista sijaintia ääripäiden välillä)
balance = st.slider("Siirrä painopistettä", 0.0, 100.0, 50.0, label_visibility="collapsed")

# Logaritminen interpolointi pisteiden välillä
# Kun balance = 0 -> CTR on 100
# Kun balance = 100 -> CTR on min_limit
log_ctr = np.log(max_limit) - (balance / 100.0) * (np.log(max_limit) - np.log(min_limit))
current_ctr = np.exp(log_ctr)
current_cr = target_constant / current_ctr

# 3. Tulosten näyttäminen
st.divider()

res_col1, res_col2 = st.columns(2)

with res_col1:
    st.markdown("### Vaadittu CTR")
    st.title(f"{current_ctr:.2f} %")
    st.progress(current_ctr / 100)

with res_col2:
    st.markdown("### Vaadittu Konversio")
    st.title(f"{current_cr:.2f} %")
    st.progress(current_cr / 100)

# Lasketaan CPC (klikinhinta) vertailun vuoksi
cpc = cpm / (1000 * (current_ctr / 100))
st.info(f"Tässä tasapainossa klikkaus maksaa **{cpc:.2f} €**. "
        f"Kun konversio on **{current_cr:.2f} %**, mainoskulu on tasan **{kate:.2f} €**.")

st.divider()
st.caption("Logiikka: Slider liikkuu pitkin nollatuloksen käyrää. Toisessa päässä mainos on täydellinen (100% CTR), "
           "toisessa päässä verkkokauppa on täydellinen (100% CR).")