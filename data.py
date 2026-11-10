import pandas as pd, streamlit as st
from concurrent.futures import ThreadPoolExecutor
B = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQMk3nbQ7vxzEh7IZU7tFqdei8TNIfIvsAA3I353lnfwXJvg-FkM82yHvaOjBWkdfAK2kgyhdXKeAO9/pub?single=true&output=csv&gid="
G = ["315357094", "1480312646"]
def get(g):
    for _ in range(3):
        try:
            return pd.read_csv(B + g)
        except Exception:
            pass
    return pd.read_csv(B + g)
@st.cache_data
def roster():
    r = get("756781838")
    r.columns = [c.strip() for c in r.columns]
    return r
@st.cache_data(show_spinner="Loading data...")
def load():
    with ThreadPoolExecutor() as ex:
        f = list(ex.map(get, G))
    f[0]["Live"], f[1]["Live"] = False, True
    d = pd.concat(f, ignore_index=True)
    d.columns = [c.strip() for c in d.columns]
    d = d.rename(columns={"Interview Round": "Interview Round ", "Working Conditions": "Working Conditions "})
    for c in ["Company", "Position", "Department", "How did you hear about the job?"]:
        s = d[c].str.strip()
        d[c] = s.str.lower().map(s.groupby(s.str.lower()).agg(lambda x: x.value_counts().index[0]))
    d["Timestamp"] = pd.to_datetime(d["Timestamp"], format="mixed").dt.strftime("%m/%d/%y %H:%M")
    return d
def header(t):
    st.markdown("<style>[data-testid='stDataFrame'] canvas{filter:brightness(.7) contrast(3)}[data-testid*='VegaLite'] text{fill:#111 !important}</style>", unsafe_allow_html=True)
    a, b = st.columns([5, 1])
    a.title(t)
    b.image("logo.jpg", width=150)
