import streamlit as st, pandas as pd, os
from data import load, header
st.set_page_config(layout="wide")
header("Students")
d = load()
d["Name"] = d["Last Name"] + ", " + d["First Name"]
d["T"] = pd.to_datetime(d["Timestamp"], format="%m/%d/%y %H:%M")
a, b = st.columns(2)
a.subheader("5 most recent accepted offers")
a.dataframe(d[d["Level"] == "Acceptance"].iloc[::-1].head(5)[["Name", "Company", "Position", "Final Salary"]].rename(columns={"Final Salary": "Salary"}), hide_index=True)
b.subheader("5 most recently active students")
b.dataframe(d.iloc[::-1].drop_duplicates("Name").head(5)[["Name", "Level", "Company", "Position", "Timestamp"]], hide_index=True)
d["Name"] = d["Last Name"] + ", " + d["First Name"]
d["T"] = pd.to_datetime(d["Timestamp"], format="%m/%d/%y %H:%M")
n = st.selectbox("Student", sorted(d["Name"].unique()))
u = d[d["Name"] == n]["UnityID"].iloc[0]
s = d[d["UnityID"] == u]
i = s[s["Level"] == "Interview"]
c1, c2, c3 = st.columns(3)
p = f"Employment_Tracker_2027_Synthetic/avatars/{u}.png"
if os.path.exists(p):
    c1.image(p, width=150)
else:
    c1.write("No avatar on file")
c2.metric("Total interviews", len(i))
c3.write(i["Interview Round "].value_counts())
st.dataframe(i[["Company", "Position", "Interview Round ", "Timestamp"]], hide_index=True)
for l, t, c in [("Offer", "Offers", ["Company", "Position"]), ("Acceptance", "Accepted offers", ["Company", "Position", "Final Salary", "Bonus", "Job City", "Job State"])]:
    o = s[s["Level"] == l]
    st.subheader(f"{t}: {len(o)}")
    if o.empty:
        st.write("None reported")
    else:
        st.dataframe(o[c], hide_index=True)
