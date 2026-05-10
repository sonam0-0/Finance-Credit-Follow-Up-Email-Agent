import os
import re
import sqlite3
from datetime import date, datetime

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

try:
    from groq import Groq
except ImportError:
    Groq = None


load_dotenv()

DB_NAME = "Finance Credit Follow-Up Email Agen_audit.db"



# DATABASE AGENT


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            invoice_no TEXT,
            client_name TEXT,
            contact_email TEXT,
            amount REAL,
            due_date TEXT,
            days_overdue INTEGER,
            followup_count INTEGER,
            stage TEXT,
            tone TEXT,
            subject TEXT,
            email_body TEXT,
            status TEXT,
            action TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_audit(record):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO audit_log (
            timestamp, invoice_no, client_name, contact_email, amount,
            due_date, days_overdue, followup_count, stage, tone,
            subject, email_body, status, action
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, record)

    conn.commit()
    conn.close()


def get_audit_logs():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM audit_log ORDER BY id DESC", conn)
    conn.close()
    return df


# SECURITY VALIDATION AGENT


def sanitize_text(value):
    value = str(value)
    value = re.sub(r"<.*?>", "", value)
    value = value.replace("ignore previous instructions", "")
    value = value.replace("system prompt", "")
    return value.strip()


def validate_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, str(email)) is not None


def validate_dataframe(df):
    required_columns = [
        "invoice_no",
        "client_name",
        "amount",
        "due_date",
        "contact_email",
        "followup_count",
        "payment_link"
    ]

    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        return False, f"Missing columns: {missing}"

    for col in required_columns:
        df[col] = df[col].apply(sanitize_text)

    invalid_emails = df[~df["contact_email"].apply(validate_email)]

    if len(invalid_emails) > 0:
        return False, "Some contact emails are invalid."

    return True, "Data validated successfully."


# OVERDUE DETECTION AGENT


def calculate_days_overdue(due_date):
    try:
        due = pd.to_datetime(due_date).date()
        return (date.today() - due).days
    except Exception:
        return 0


# TONE ESCALATION AGENT


def get_stage_and_tone(days_overdue):
    if days_overdue <= 0:
        return "Not Due", "No Email Required", "No Action"

    if 1 <= days_overdue <= 7:
        return "1st Follow-Up", "Warm & Friendly", "Send gentle reminder"

    if 8 <= days_overdue <= 14:
        return "2nd Follow-Up", "Polite but Firm", "Ask for payment confirmation"

    if 15 <= days_overdue <= 21:
        return "3rd Follow-Up", "Formal & Serious", "Request response within 48 hours"

    if 22 <= days_overdue <= 30:
        return "4th Follow-Up", "Stern & Urgent", "Final reminder before escalation"

    return "Escalation Flag", "Legal/Finance Review", "Assign to finance manager"


# FALLBACK EMAIL GENERATOR


def fallback_email(row, days_overdue, stage, tone, action):
    invoice_no = row["invoice_no"]
    client_name = row["client_name"]
    amount = row["amount"]
    due_date = row["due_date"]
    payment_link = row["payment_link"]

    if stage == "1st Follow-Up":
        subject = f"Quick Reminder – Invoice {invoice_no} | ₹{amount} Due"
        body = f"""
Hi {client_name},

I hope you are doing well.

This is a friendly reminder that Invoice {invoice_no} for ₹{amount} was due on {due_date}.
It is currently {days_overdue} day(s) overdue.

If you have already processed the payment, please ignore this message.
Otherwise, you can complete the payment using the link below:

{payment_link}

Thank you,
Finance Team
"""

    elif stage == "2nd Follow-Up":
        subject = f"Payment Follow-Up – Invoice {invoice_no}"
        body = f"""
Dear {client_name},

This is a polite follow-up regarding Invoice {invoice_no} of ₹{amount}, which was due on {due_date}.
The payment is now {days_overdue} day(s) overdue.

Please confirm the expected payment date or complete the payment using the link below:

{payment_link}

Regards,
Finance Team
"""

    elif stage == "3rd Follow-Up":
        subject = f"IMPORTANT: Outstanding Payment – Invoice {invoice_no}"
        body = f"""
Dear {client_name},

Despite our previous reminders, Invoice {invoice_no} for ₹{amount} remains unpaid.
The invoice was due on {due_date} and is now {days_overdue} day(s) overdue.

We request your immediate attention. Continued non-payment may impact your credit terms.
Please respond within 48 hours.

Payment Link:
{payment_link}

Regards,
Finance Team
"""

    elif stage == "4th Follow-Up":
        subject = f"FINAL NOTICE – Invoice {invoice_no} – Immediate Action Required"
        body = f"""
Dear {client_name},

This is our final reminder for Invoice {invoice_no} of ₹{amount}.
The invoice was due on {due_date} and is now {days_overdue} day(s) overdue.

Failure to remit payment within 24 hours may result in escalation to the finance/legal team.

Please pay immediately using the link below:

{payment_link}

Regards,
Finance Team
"""

    else:
        subject = f"Escalation Required – Invoice {invoice_no}"
        body = f"""
Invoice {invoice_no} for {client_name} is overdue by {days_overdue} days.

Amount Due: ₹{amount}
Due Date: {due_date}
Action Required: {action}

This case requires manual finance/legal review.
No automatic email has been sent.
"""

    return subject.strip(), body.strip()


# LLM EMAIL GENERATION AGENT


def generate_email_with_llm(row, days_overdue, stage, tone, action):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key or Groq is None:
        return fallback_email(row, days_overdue, stage, tone, action)

    client = Groq(api_key=api_key)

    prompt = f"""
You are a professional Finance Credit Follow-Up Email Agent.

Your task:
Generate a payment follow-up email using ONLY the given invoice data.

Rules:
1. Do not invent any missing information.
2. Do not change invoice number, amount, due date, or payment link.
3. Keep the tone exactly as: {tone}
4. Include client name, invoice number, amount due, due date, days overdue, and payment link.
5. If stage is Escalation Flag, do not write a customer email. Write an internal finance/legal review note.
6. Return output exactly in this format:

Subject: ...
Body:
...

Invoice Data:
Client Name: {row['client_name']}
Invoice Number: {row['invoice_no']}
Amount Due: ₹{row['amount']}
Due Date: {row['due_date']}
Contact Email: {row['contact_email']}
Days Overdue: {days_overdue}
Follow-up Count: {row['followup_count']}
Payment Link: {row['payment_link']}
Stage: {stage}
Tone: {tone}
Action: {action}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You generate safe, professional, personalized finance follow-up emails."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        output = response.choices[0].message.content

        if "Subject:" in output and "Body:" in output:
            subject = output.split("Body:")[0].replace("Subject:", "").strip()
            body = output.split("Body:")[1].strip()
            return subject, body

        return fallback_email(row, days_overdue, stage, tone, action)

    except Exception:
        return fallback_email(row, days_overdue, stage, tone, action)


# MAIN AGENT WORKFLOW


def run_agent_workflow(df):
    results = []

    for _, row in df.iterrows():
        days_overdue = calculate_days_overdue(row["due_date"])
        stage, tone, action = get_stage_and_tone(days_overdue)

        if days_overdue <= 0:
            continue

        subject, body = generate_email_with_llm(
            row,
            days_overdue,
            stage,
            tone,
            action
        )

        if days_overdue > 30:
            status = "Escalated - No Email Sent"
        else:
            status = "Dry Run - Email Generated Only"

        record = (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            row["invoice_no"],
            row["client_name"],
            row["contact_email"],
            float(row["amount"]),
            row["due_date"],
            int(days_overdue),
            int(row["followup_count"]),
            stage,
            tone,
            subject,
            body,
            status,
            action
        )

        save_audit(record)

        results.append({
            "invoice_no": row["invoice_no"],
            "client_name": row["client_name"],
            "contact_email": row["contact_email"],
            "amount": row["amount"],
            "due_date": row["due_date"],
            "days_overdue": days_overdue,
            "stage": stage,
            "tone": tone,
            "subject": subject,
            "email_body": body,
            "status": status,
            "action": action
        })

    return pd.DataFrame(results)


# STREAMLIT UI


st.set_page_config(
    page_title="CreditFlow AI",
    
    layout="wide"
)

init_db()

st.title(" CreditFlow AI")
st.subheader("Finance Credit Follow-Up Email Agent")

st.info(
    "This agent reads pending invoices, detects overdue payments, chooses tone, "
    "generates personalized emails, runs in dry-run mode, logs audit trail, "
    "and flags 30+ day overdue cases for finance/legal review."
)

with st.sidebar:
    st.header("Project Details")
    st.write("**LLM:** Llama 3.1 8B Instant")
    st.write("**Provider:** Groq API")
    st.write("**Framework Style:** Agentic Workflow")
    st.write("**Mode:** Dry Run / Mock Send")
    st.write("**Database:** SQLite")

uploaded_file = st.file_uploader(
    "Upload Invoice File",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    is_valid, message = validate_dataframe(df)

    if not is_valid:
        st.error(message)
    else:
        st.success(message)

        df["days_overdue"] = df["due_date"].apply(calculate_days_overdue)
        df["stage"] = df["days_overdue"].apply(lambda x: get_stage_and_tone(x)[0])
        df["tone"] = df["days_overdue"].apply(lambda x: get_stage_and_tone(x)[1])
        df["action"] = df["days_overdue"].apply(lambda x: get_stage_and_tone(x)[2])

        st.subheader(" Invoice Dashboard")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Invoices", len(df))
        col2.metric("Overdue Invoices", len(df[df["days_overdue"] > 0]))
        col3.metric("Emails to Generate", len(df[(df["days_overdue"] > 0) & (df["days_overdue"] <= 30)]))
        col4.metric("Escalation Cases", len(df[df["days_overdue"] > 30]))

        st.dataframe(df)

        st.subheader(" Run Agent")

        if st.button("Generate Follow-Up Emails"):
            result_df = run_agent_workflow(df)

            if len(result_df) == 0:
                st.warning("No overdue invoices found.")
            else:
                st.success("Agent workflow completed successfully.")

                for _, row in result_df.iterrows():
                    with st.expander(f"{row['client_name']} | {row['invoice_no']} | {row['stage']}"):
                        st.write(f"**Email:** {row['contact_email']}")
                        st.write(f"**Days Overdue:** {row['days_overdue']}")
                        st.write(f"**Tone:** {row['tone']}")
                        st.write(f"**Status:** {row['status']}")
                        st.write(f"**Action:** {row['action']}")
                        st.write(f"**Subject:** {row['subject']}")
                        st.text_area(
                            "Generated Email / Escalation Note",
                            row["email_body"],
                            height=260
                        )

                st.download_button(
                    label="Download Generated Email Log CSV",
                    data=result_df.to_csv(index=False),
                    file_name="generated_email_log.csv",
                    mime="text/csv"
                )

st.subheader(" Audit Trail")

logs = get_audit_logs()

if len(logs) > 0:
    st.dataframe(logs)

    st.download_button(
        label="Download Audit Trail CSV",
        data=logs.to_csv(index=False),
        file_name="audit_trail.csv",
        mime="text/csv"
    )
else:
    st.info("No audit logs yet.")
