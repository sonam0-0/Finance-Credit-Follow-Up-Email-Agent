````md
# 💰 CreditFlow AI – Smart Finance Credit Follow-Up Email Agent

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" />
  <img src="https://img.shields.io/badge/Streamlit-Frontend-red.svg" />
  <img src="https://img.shields.io/badge/LLM-Llama%203.1%208B-green.svg" />
  <img src="https://img.shields.io/badge/Groq-API-orange.svg" />
  <img src="https://img.shields.io/badge/SQLite-Database-lightgrey.svg" />
</p>

---

# 📌 Project Overview

**CreditFlow AI** is an **AI-powered Finance Credit Follow-Up Email Agent** designed to automate payment reminder workflows for overdue invoices.

The system intelligently analyzes pending invoice records, calculates overdue durations, selects appropriate communication tones, generates **personalized payment reminder emails using an LLM**, and maintains a complete **audit trail** for transparency.

This project demonstrates the application of **Agentic AI + Large Language Models (LLMs)** in solving real-world finance automation problems.

---

# 🚨 Problem Statement

In organizations, finance teams often spend a lot of time manually:

- Tracking overdue invoices
- Sending repetitive payment reminders
- Following up with customers multiple times
- Maintaining professional communication
- Managing escalations for long overdue payments

### Problems with Manual Process

❌ Time-consuming and repetitive work

❌ Inconsistent email tone

❌ Missed follow-ups

❌ Lack of tracking and auditing

❌ Delayed cash flow

To solve this problem, **CreditFlow AI** automates the complete follow-up workflow using AI.

---

# 🎯 Project Objective

The objective of this project is to build an **AI Finance Assistant Agent** that can:

✅ Read pending invoice records

✅ Detect overdue payments

✅ Decide reminder tone dynamically

✅ Generate personalized payment emails

✅ Simulate email sending safely

✅ Maintain audit logs

✅ Escalate high-risk overdue invoices

---

# ✨ Key Features

## 📂 1. Data Ingestion

The system supports:

- CSV files
- Excel files (.xlsx)

Accepted fields:

| Field | Description |
|--------|-------------|
| invoice_no | Invoice number |
| client_name | Client/customer name |
| amount | Due payment amount |
| due_date | Invoice due date |
| contact_email | Client email |
| followup_count | Number of reminders already sent |
| payment_link | Dynamic payment URL |

---

## 📅 2. Overdue Detection

The system automatically calculates:

```text
Days Overdue = Current Date - Due Date
````

This helps determine whether a reminder should be sent.

---

## 🎭 3. Tone Escalation Engine

Email tone changes automatically depending on overdue duration.

| Days Overdue | Tone                 | Action                         |
| ------------ | -------------------- | ------------------------------ |
| 1–7 Days     | Warm & Friendly      | Gentle reminder                |
| 8–14 Days    | Polite but Firm      | Request payment confirmation   |
| 15–21 Days   | Formal & Serious     | Request response within 48 hrs |
| 22–30 Days   | Stern & Urgent       | Final warning                  |
| 30+ Days     | Legal/Finance Review | Escalation                     |

### Why this matters?

It ensures:

* Professional communication
* Reduced customer friction
* Business-friendly payment recovery

---

## 🤖 4. AI-Powered Email Generation

The system uses an **LLM** to generate personalized follow-up emails.

Each generated email includes:

* Client Name
* Invoice Number
* Amount Due
* Due Date
* Overdue Days
* Payment Link

This prevents generic communication and improves professionalism.

---

## 📧 5. Dry Run / Mock Send Mode

To ensure safe testing:

✅ Emails are generated

✅ Emails are previewed

❌ No actual emails are sent

This avoids accidental communication with real clients during development.

---

## 🧾 6. Audit Trail Logging

Every activity is stored in SQLite including:

* Timestamp
* Invoice details
* Tone used
* Generated email
* Status
* Escalation actions

This improves traceability and compliance.

---

# 🏗️ System Architecture

```text
CSV / Excel Upload
        ↓
Data Ingestion Agent
        ↓
Validation Agent
        ↓
Overdue Detection Agent
        ↓
Tone Escalation Agent
        ↓
LLM Email Generation Agent
        ↓
Dry Run / Mock Send
        ↓
Audit Logger Agent
        ↓
Dashboard + Reports
```

---

# 🧠 Agent Framework

## Framework Used

**Custom Multi-Agent Workflow Architecture**

This project follows an **Agentic Workflow**, where different agents perform specialized tasks independently.

### Agent Responsibilities

### 1️⃣ Data Ingestion Agent

Reads invoice records from CSV/Excel files.

### 2️⃣ Validation Agent

Checks:

* Missing fields
* Invalid email formats
* Unsafe inputs

### 3️⃣ Overdue Detection Agent

Calculates overdue duration.

### 4️⃣ Tone Escalation Agent

Selects communication tone.

### 5️⃣ Email Generation Agent

Uses LLM for email generation.

### 6️⃣ Escalation Agent

Flags invoices overdue >30 days.

### 7️⃣ Audit Logger Agent

Stores logs in SQLite.

---

# 🤖 LLM Chosen

## Model Used

### **Llama 3.1 8B Instant**

### Provider

**Groq API**

---

## Why this model?

The model was selected because:

✅ Fast response time

✅ Free and cost-effective

✅ Professional email generation

✅ Low latency

✅ Easy Python integration

✅ Suitable for real-time applications

---

## Why not alternatives?

| Model  | Reason               |
| ------ | -------------------- |
| GPT-4o | Paid API             |
| Gemini | Less prompt control  |
| Claude | Paid and unnecessary |

---

# 📝 Prompt Design

The prompt is carefully designed to reduce hallucinations and ensure consistency.

## Prompt Strategy

The model is instructed to:

* Use only provided invoice details
* Avoid inventing information
* Maintain selected communication tone
* Include all required invoice details
* Escalate high overdue cases

---

## Example Prompt

```text
Generate a professional payment reminder email.

Rules:
- Use only provided information
- Do not invent data
- Maintain selected tone

Client Name: Rajesh Kapoor
Invoice Number: INV-001
Amount Due: ₹45,000
Due Date: 2026-05-05
Days Overdue: 10
Tone: Polite but Firm
```

---

## Guardrails Applied

✅ Structured output

✅ Controlled prompting

✅ Input sanitization

✅ Reliable response format

---

# 🔐 Security Risk Mitigation

| Risk                 | Mitigation            |
| -------------------- | --------------------- |
| Prompt Injection     | Input sanitization    |
| API Key Exposure     | `.env` + `.gitignore` |
| Hallucination        | Strict prompts        |
| Invalid Emails       | Email validation      |
| Unauthorized Sending | Dry-run mode          |
| PII Exposure         | Local SQLite storage  |

---

# ⚙️ Tech Stack

| Layer           | Technology           |
| --------------- | -------------------- |
| Frontend        | Streamlit            |
| Backend         | Python               |
| LLM             | Llama 3.1 8B Instant |
| Provider        | Groq API             |
| Database        | SQLite               |
| Data Processing | Pandas               |
| Config          | python-dotenv        |
| File Support    | CSV / Excel          |

---

# 📸 Project Screenshots

## Dashboard

(Add Screenshot Here)

```md
![Dashboard](images/dashboard.png)
```

---

## Email Generation

(Add Screenshot Here)

```md
![Generated Email](images/email_generation.png)
```

---

## Audit Trail

(Add Screenshot Here)

```md
![Audit Trail](images/audit_trail.png)
```

---

# 📁 Project Structure

```text
Finance-Credit-Follow-Up-Email-Agent/
│── main.py
│── README.md
│── requirements.txt
│── sample_invoices.csv
│── .gitignore
│── images/
```

---

# 🛠️ Installation & Setup

## Step 1: Clone Repository

```bash
git clone https://github.com/sonam0-0/Finance-Credit-Follow-Up-Email-Agent.git
cd Finance-Credit-Follow-Up-Email-Agent
```

---

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 3: Create Environment File

Create `.env`

```env
GROQ_API_KEY=your_api_key_here
```

---

## Step 4: Run Application

```bash
streamlit run main.py
```

---

# 📊 Sample Dataset

```csv
invoice_no,client_name,amount,due_date,contact_email,followup_count,payment_link
INV-001,Rajesh Kapoor,45000,2026-05-05,rajesh@example.com,0,https://pay.company.com/INV-001
INV-002,Amit Sharma,32000,2026-04-30,amit@example.com,1,https://pay.company.com/INV-002
```

---

# 📤 Sample Output

### Generated Status

```text
Dry Run – Email Generated Only
Escalated – No Email Sent
```

### Sample Generated Email

Subject:
Payment Reminder – Invoice INV-001

Body:
Dear Rajesh Kapoor,

This is a reminder regarding Invoice INV-001 of ₹45,000 which is overdue by 10 days.

Please complete payment using the link below.

Regards,
Finance Team

---

# ⚠️ Challenges Faced

During development:

* Overdue calculation logic
* Tone escalation mapping
* Prompt engineering
* LLM consistency
* Audit trail implementation

---

# 🔮 Future Improvements

Planned enhancements:

* SMTP-based real email sending
* Multi-language support
* ERP integration
* Smart payment analytics
* Risk scoring system

---

# 🎯 Conclusion

CreditFlow AI demonstrates how **Agentic AI and LLMs** can automate real-world finance operations.

The system successfully:

✅ Detects overdue invoices

✅ Generates personalized payment reminders

✅ Maintains professional communication

✅ Logs actions for auditing

✅ Reduces manual effort

This project showcases the practical use of AI in business automation.

---

# 👨‍💻 Author

### **Sonam Yadav**

**B.Tech – Artificial Intelligence & Machine Learning**
**Bennett University**

```
```
