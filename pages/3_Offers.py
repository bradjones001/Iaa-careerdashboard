import streamlit as st, pandas as pd
from data import load, header
st.set_page_config(layout="wide")
header("Offers")
d = load()
d["Year"] = pd.to_datetime(d["Timestamp"], format="%m/%d/%y %H:%M").dt.year
y = st.selectbox("Year", ["All"] + sorted(d["Year"].unique()))
if y != "All":
    d = d[d["Year"] == y]
a = d[d["Level"] == "Acceptance"].copy()
a["Base"] = a["Final Salary"].str.replace(r"[^\d]", "", regex=True).astype(float)
a["Name"] = a["Last Name"] + ", " + a["First Name"]
p, q, r = st.columns(3)
p.subheader("Top 5 cities")
p.dataframe(a["Job City"].value_counts().head(5))
q.subheader("Top 5 states")
q.dataframe(a["Job State"].value_counts().head(5))
r.subheader("Top 5 earners")
r.dataframe(a.nlargest(5, "Base")[["Name", "Company", "Base"]], hide_index=True, column_config={"Base": st.column_config.NumberColumn("Salary", format="$%d")})
m, n = st.columns([1, 2])
m.metric("Offers reported", (d["Level"] == "Offer").sum())
m.metric("Accepted offers", len(a))
m.metric("Average base", f"${a['Base'].mean():,.0f}")
m.metric("Median base", f"${a['Base'].median():,.0f}")
n.subheader("Most recently accepted offers")
n.dataframe(a.iloc[::-1].head(5)[["Name", "Company", "Position", "Final Salary"]].rename(columns={"Final Salary": "Salary"}), hide_index=True)
st.dataframe(a[["First Name", "Last Name", "Company", "Position", "Final Salary", "Bonus", "Job City", "Job State"]], hide_index=True)
