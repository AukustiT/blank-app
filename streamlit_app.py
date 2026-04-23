import streamlit as st
import numpy as np

st.set_page_config(page_title="Break-even Explorer", layout="centered")

st.title("🎯 Nollatuloksen Metsästäjä")
st.write("Aseta kiinteät arvot ja katso, millaisen CTR/Konversio-suhteen tarvitset.")

# 1. Kiinteät syötteet sivupalkkiin
st.sidebar.header("Kiinteät arvot")
kate = st.sidebar.number_input("Tuotteen kate (€)", value=15.50, step=0.10)
cpm = st.sidebar.number_input("CPM (Hinta 1000 näyttökerralle)", value=10.0, step=0.5)

# Lasketaan vaadittu "yhdistelmäprosentti" (CTR * CR)
# Kaava: Kate * (CTR/100) * (CR/100) = CPM / 1000
# => CTR * CR = CPM / (10 * Kate)
target_product = cpm / (10 * kate)

st.divider()

# 2. Yhteinen slider, joka liukuu break-even -käyrällä
st.subheader("Break-even tasapaino")
st.write(f"Jotta pääset nollatulokseen katteella **{kate}€** ja CPM:llä **{cpm}€**...")

# Slider, joka edustaa "painotusta" CTR:n ja CR:n välillä
balance = st.slider("Säädä painotusta (Vasemmalla kova CTR, oikealla kova konversio)", 
                   min_value=0.1, max_value=0.9, value=0.5, step=0.01, help="Tämä liikuttaa sinua pitkin nollatuloksen käyrää.")

# Lasketaan parit siten, että ne osuvat nollatulokseen
# Käytetään logaritmista skaalaa, jotta liike on luonnollinen
ctr_target = np.sqrt(target_product) * (balance / 0.5)
cr_target = target_product / ctr_target

# Näytetään tulokset
c1, c2 = st.columns(2)
with c1:
    st.metric("Vaadittu CTR %", f"{ctr_target:.2f} %")
    st.caption("Mainoksen tehokkuus")

with c2:
    st.metric("Vaadittu Konversio %", f"{cr_target:.2f} %")
    st.caption("Kaupan tehokkuus")

# Lasketaan CPC tässä pisteessä
cpc = cpm / (1000 * (ctr_target / 100))
st.info(f"Tässä pisteessä klikkaus maksaa **{cpc:.2f} €**. Jos konversiosi on **{cr_target:.2f} %**, jokainen kauppa maksaa tarkalleen **{kate} €**.")

# 3. Visuaalinen selite
st.divider()
st.write("### Miten tämä toimii?")
st.write(f"Nollatulokseen tarvitset yhdistelmän, jossa `CTR * CR = {target_product:.4f}`.")

if balance < 0.4:
    st.warning("👉 **Strategia:** Sinulla on todella kova CTR. Voit pärjätä heikommallakin verkkokaupalla, koska liikenne on halpaa.")
elif balance > 0.6:
    st.warning("👉 **Strategia:** Mainoksesi on kallis (pieni CTR), mutta verkkokauppasi on kone! Tarvitset kovan konversion kattaaksesi kulut.")
else:
    st.success("👉 **Strategia:** Tasapainoinen tilanne. Molemmat osa-alueet suoriutuvat tasaisesti.")

st.caption("Tämä laskuri näyttää vain nollatuloksen. Kaikki tästä ylöspäin on puhdasta voittoa.")