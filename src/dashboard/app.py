import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))

import json
import pandas as pd
import streamlit as st
from src.models.predict import score_transaction
from src.simulator.transaction_simulator import generate_transaction

st.set_page_config(page_title="FraudLens AI", layout="wide")
st.title("FraudLens AI — Real-Time Fraud Detection Dashboard")
st.caption("Production-style ML engineering portfolio project")

if "history" not in st.session_state:
    st.session_state.history = []
if "alerts" not in st.session_state:
    st.session_state.alerts = []

col1, col2, col3, col4 = st.columns(4)

if st.button("Generate & Score Transaction"):
    txn = generate_transaction()
    try:
        score = score_transaction(txn)
    except FileNotFoundError:
        st.error("Model not found. Run: python -m src.data.load_data --generate-demo && python -m src.models.train_model")
        st.stop()
    record = {**txn, **score}
    st.session_state.history.insert(0, record)
    if score["risk_level"] in {"MEDIUM", "HIGH"} or score["prediction_label"] == 1:
        st.session_state.alerts.insert(0, {"status": "OPEN", "analyst_notes": "", **record})

history = pd.DataFrame(st.session_state.history)
alerts = pd.DataFrame(st.session_state.alerts)

if history.empty:
    col1.metric("Total Transactions", 0)
    col2.metric("Fraud Alerts", 0)
    col3.metric("Average Risk Score", "0")
    col4.metric("High Risk", 0)
    st.info("Click 'Generate & Score Transaction' to start a local demo.")
else:
    col1.metric("Total Transactions", len(history))
    col2.metric("Fraud Alerts", len(alerts))
    col3.metric("Average Risk Score", round(history["final_risk_score"].mean(), 2))
    col4.metric("High Risk", int((history["risk_level"] == "HIGH").sum()))

    tab1, tab2, tab3 = st.tabs(["Real-Time Monitor", "Alert Investigation", "Model Explainability"])

    with tab1:
        st.subheader("Real-Time Transaction Feed")
        st.dataframe(history[["transaction_id", "customer_id", "amount", "fraud_probability", "rule_score", "final_risk_score", "risk_level", "reasons"]], use_container_width=True)
        st.subheader("Risk Score Trend")
        st.line_chart(history["final_risk_score"][::-1])

    with tab2:
        st.subheader("Fraud Investigator Queue")
        if alerts.empty:
            st.success("No open fraud alerts in the local demo session.")
        else:
            st.dataframe(alerts[["transaction_id", "customer_id", "amount", "risk_level", "final_risk_score", "status", "reasons"]], use_container_width=True)
            selected = st.selectbox("Select alert transaction", alerts["transaction_id"].tolist())
            alert = alerts[alerts["transaction_id"] == selected].iloc[0].to_dict()
            st.markdown(f"**Transaction:** `{selected}`")
            st.markdown(f"**Risk:** {alert['risk_level']} — {alert['final_risk_score']}")
            status = st.selectbox("Update status", ["OPEN", "UNDER_REVIEW", "CONFIRMED_FRAUD", "FALSE_POSITIVE", "CLOSED"])
            notes = st.text_area("Investigation notes")
            if st.button("Apply local status update"):
                for item in st.session_state.alerts:
                    if item["transaction_id"] == selected:
                        item["status"] = status
                        item["analyst_notes"] = notes
                st.success("Local demo alert status updated.")

    with tab3:
        st.subheader("Why was the latest transaction flagged?")
        latest = st.session_state.history[0]
        st.json(latest.get("shap_explanation", {}))
        if latest.get("reasons"):
            st.write("Rule-based risk reasons:")
            for reason in latest["reasons"]:
                st.write(f"- {reason}")
