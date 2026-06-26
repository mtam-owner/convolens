# ConvoLens

ConvoLens is an AI Conversation Intelligence Platform for customer support analytics.

The project transforms public customer support conversations into management-ready insights using Python, NLP, LLM-assisted summarisation, risk scoring and interactive Streamlit dashboards.

## Project Objective

Customer support teams handle large volumes of conversations across social media, chat, email and call centres. These conversations contain valuable signals about recurring customer issues, complaint risk, service quality and operational priorities.

ConvoLens analyses customer support conversations to answer:

- What are customers contacting support about?
- Which issues appear most frequently?
- Which conversations show complaint or escalation risk?
- What themes should management prioritise?
- How can AI summaries support faster review and decision-making?

## Planned Features

- Customer conversation reconstruction
- Text cleaning and preprocessing
- Topic and theme extraction
- Intent and issue categorisation
- Complaint and escalation risk scoring
- AI-generated conversation summaries
- Management-ready KPIs and visualisations
- Interactive Streamlit web application

## Dataset

The project will use the public Customer Support on Twitter dataset.

The dataset contains real customer support conversations between customers and major brands. It is suitable for conversation intelligence because it includes readable customer messages, company replies and reply-chain metadata that can be used to reconstruct conversation threads.

Raw data is not committed to this repository. Users should download the dataset manually and place it inside:

```text
data/raw/