import streamlit as st, pandas as pd
from data import load, header
st.set_page_config(layout="wide")
header("Companies")
d = load()
d["Year"] = pd.to_datetime(d["Timestamp"], format="%m/%d/%y %H:%M").dt.year
nw = d[d["Live"] & ~d["Company"].isin(d[~d["Live"]]["Company"])]
n, a, b = st.columns(3)
n.subheader("New companies to watch")
if nw.empty:
    n.write("No new companies yet")
else:
    n.dataframe(nw.groupby("Company").agg(Students=("UnityID", "nunique"), Entries=("Level", "size")))
a.subheader("Top 5 by acceptances")
a.dataframe(d[d["Level"] == "Acceptance"]["Company"].value_counts().head(5))
b.subheader("Top 5 by interviews")
b.dataframe(d[d["Level"] == "Interview"]["Company"].value_counts().head(5))
c = st.selectbox("Company", sorted(d["Company"].unique()))
y = st.selectbox("Year", ["All"] + sorted(d["Year"].unique()))
x = d[d["Company"] == c]
if y != "All":
    x = x[x["Year"] == y]
i = x[x["Level"] == "Interview"]
k = st.columns(3)
k[0].metric("Students interviewed", i["UnityID"].nunique())
k[1].metric("Total interviews", len(i))
k[2].metric("Accepted positions", (x["Level"] == "Acceptance").sum())
v = i["Position"].value_counts().reset_index()
v.columns = ["Position", "\\# of Interviews"]
p, m = st.columns([3, 2])
p.table(v.set_index("Position"))
s = pd.to_numeric(x[x["Level"] == "Acceptance"]["Final Salary"].str.replace(r"[^\d]", "", regex=True), errors="coerce")
t = f"${s.mean():,.0f}" if s.notna().any() else "No Hires"
m.markdown(f"<div style='text-align:center'>Average salary of accepted offers<div style='font-size:2.5rem'>{t}</div></div>", unsafe_allow_html=True)
x = x.assign(Name=x["Last Name"] + ", " + x["First Name"], Stage=x["Interview Round "].where(x["Level"] == "Interview", x["Level"]))
x = x.assign(Rank=x["Stage"].map({"Recruiter Screening": 1, "First Round": 2, "Second Round": 3, "Final Round": 4, "Offer": 5, "Acceptance": 6}).fillna(0))
st.subheader("Students and where they are")
st.dataframe(x.sort_values("Rank").drop_duplicates(["Name", "Position"], keep="last").sort_values("Rank", ascending=False)[["Name", "Position", "Stage"]], hide_index=True)
