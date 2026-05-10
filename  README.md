# CreditFlow AI - Finance Credit Follow-Up Email Agent

# Project Overview

CreditFlow AI is an AI-powered finance assistant that automatically identifies overdue invoices and generates personalized follow-up emails based on the overdue stage.

The system helps finance teams reduce manual follow-up work, maintain professional communication, and log every action for audit purposes.



# Problem Statement

Finance teams often spend a lot of time manually checking overdue invoices and sending follow-up emails. Manual follow-ups are slow, inconsistent, and difficult to track.

CreditFlow AI solves this by:
 Reading invoice data from CSV/Excel
 Detecting overdue invoices
 Selecting the correct tone based on overdue days
 Generating personalized follow-up emails
 Running in dry-run mode for safety
 Logging every action in an audit trail
 Flagging 30+ day overdue cases for finance/legal review



# Features

 CSV/Excel invoice upload
 Overdue days calculation
 Tone escalation engine
 Personalized email generation
 Dry-run/mock sending
 SQLite audit logging
 Escalation flag after 30+ days
 Streamlit dashboard
 Downloadable generated email logs
 Downloadable audit trail
 Security validation



# Tone Escalation Matrix

| Stage | Trigger | Tone | Action |
|---|---|---|---|
| 1st Follow-Up | 1-7 days overdue | Warm & Friendly | Gentle reminder |
| 2nd Follow-Up | 8-14 days overdue | Polite but Firm | Ask for payment confirmation |
| 3rd Follow-Up | 15-21 days overdue | Formal & Serious | Respond within 48 hours |
| 4th Follow-Up | 22-30 days overdue | Stern & Urgent | Final reminder |
| Escalation Flag | 30+ days overdue | Legal/Finance Review | Manual review |



# Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | Python |
| LLM | Llama 3.1 8B Instant |
| Provider | Groq API |
| Data Processing | Pandas |
| Database | SQLite |
| Config Management | python-dotenv |
| Email Mode | Dry-run / Mock Send |



# LLM Choice

# Model Used
Llama 3.1 8B Instant via Groq API

# Why this model?
 Fast response time
 Cost-effective for student projects
 Good quality for professional email generation
 Easy Python integration
 Suitable for real-time dashboard use



# Agent Framework / Architecture

This project follows an agentic workflow architecture.

# Agent Flow

1. Data Ingestion Agent  
  Reads CSV/Excel invoice records.

2. Security Validation Agent  
   Checks required fields, sanitizes text, validates email format.

3. Overdue Detection Agent  
   Calculates number of overdue days.

4. Tone Escalation Agent  
   Selects follow-up stage and tone.

5. Email Generation Agent  
   Uses LLM to generate personalized email.

6. Escalation Agent  
   Flags invoices overdue by more than 30 days.

7. Audit Logger Agent  
   Saves every generated email or escalation note.


# Architecture Diagram

```txt
CSV / Excel Upload
        |
        v
Data Ingestion Agent
        |
        v
Security Validation Agent
        |
        v
Overdue Detection Agent
        |
        v
Tone Escalation Agent
        |
        v
Email Generation Agent ----> Groq LLM
        |
        v
Dry Run / Mock Send
        |
        v
SQLite Audit Trail
        |
        v
Dashboard + Download Logs
