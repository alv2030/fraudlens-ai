import pandas as pd
import plotly.express as px
import streamlit as st

st.title("Customer Risk Profile")
st.caption("Customer-level fraud risk segmentation and investigation view")

transactions = st.session_state.get("history", [])

if not transactions:
    st.info("Generate transactions from the main dashboard first.")
    st.stop()

df = pd.DataFrame(transactions)

required_columns = {
    "customer_id",
    "transaction_id",
    "final_risk_score",
    "amount",
}

missing_columns = required_columns - set(df.columns)
if missing_columns:
    st.error(f"Missing required columns: {sorted(missing_columns)}")
    st.write("Available columns:", list(df.columns))
    st.stop()

customer_df = (
    df.groupby("customer_id")
    .agg(
        transaction_count=("transaction_id", "count"),
        avg_risk_score=("final_risk_score", "mean"),
        max_risk_score=("final_risk_score", "max"),
        total_amount=("amount", "sum"),
    )
    .reset_index()
)

def risk_segment(score):
    if score >= 70:
        return "High"
    if score >= 40:
        return "Medium"
    return "Low"

customer_df["risk_segment"] = customer_df["avg_risk_score"].apply(risk_segment)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Customers", len(customer_df))
c2.metric("High Risk", int((customer_df["risk_segment"] == "High").sum()))
c3.metric("Medium Risk", int((customer_df["risk_segment"] == "Medium").sum()))
c4.metric("Low Risk", int((customer_df["risk_segment"] == "Low").sum()))

st.subheader("Customer Risk Segmentation")

seg = customer_df["risk_segment"].value_counts().reset_index()
seg.columns = ["Risk", "Count"]

fig = px.bar(
    seg,
    x="Risk",
    y="Count",
    title="Customer Risk Distribution",
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Top 10 Highest Risk Customers")

top_customers = customer_df.sort_values(
    "avg_risk_score",
    ascending=False,
).head(10)

st.dataframe(top_customers, use_container_width=True)

st.subheader("Customer Risk vs Transaction Volume")

scatter = px.scatter(
    customer_df,
    x="transaction_count",
    y="avg_risk_score",
    size="total_amount",
    color="risk_segment",
    hover_data=["customer_id", "max_risk_score"],
    title="Customer Risk Profile",
)

st.plotly_chart(scatter, use_container_width=True)