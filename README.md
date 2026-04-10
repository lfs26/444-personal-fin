# 444-personal-fin

## System Description
The Personal Finance Tracker is a Streamlit‑based application that enables an individual user to record daily purchases, manage recurring bills, and analyze spending patterns over time. The system stores structured financial data including transaction amounts, categories, dates, and user‑defined tags that support flexible classification across multiple dimensions (e.g., “Travel,” “Work,” “Health”). Tags form a many‑to‑many relationship with purchases, enabling richer filtering and analytics. The tool is designed for users who want a simple, transparent, database‑backed way to monitor expenses and understand spending behavior without relying on external budgeting platforms.

## Entity list with attributes

### purchases
| Column | Data Type | Constraints | Description |
| --- | --- | --- | --- |
| purchase_id | SERIAL | PRIMARY KEY | Unique identifier for each purchase |
| item_name | VARCHAR(100) | NOT NULL | Name of the purchase |
| amount | NUMERIC(10,2) | NOT NULL, CHECK(amount > 0) | Cost of the purchase |
| category_id | INT | NOT NULL, FK → categories(category_id) | Category assigned to the purchase |
| purchase_date | DATE | NOT NULL | Date of the transaction |
| notes | TEXT | NULL | Optional notes |

### recurring_bills 
| Column | Data Type | Constraints | Description |
| --- | --- | --- | --- |
| bill_id | SERIAL | PRIMARY KEY | Unique identifier |
| bill_name | VARCHAR(100) | NOT NULL | Name of the bill |
| amount | NUMERIC(10,2) | NOT NULL, CHECK(amount > 0) | Amount due each cycle |
| frequency | VARCHAR(20) | NOT NULL, CHECK(frequency IN ('weekly','monthly','yearly')) | Billing cycle |
| next_due_date | DATE | NOT NULL | Next due date |
| notes | TEXT | NULL | Optional notes |

### categories
| Column | Data Type | Constraints | Description |
| --- | --- | --- | --- |
| category_id | SERIAL | PRIMARY KEY | Unique identifier |
| category_name | VARCHAR(50) | UNIQUE, NOT NULL | Category label |

### tags
| Column | Data Type | Constraints | Description |
| --- | --- | --- | --- |
| tag_id | SERIAL | PRIMARY KEY | Unique identifier |
| tag_name | VARCHAR(50) | UNIQUE, NOT NULL | User‑defined tag label |

### purchase tags
| Column | Data Type | Constraints | Description |
| --- | --- | --- | --- |
| purchase_id | INT | NOT NULL, FK → purchases(purchase_id) | Linked purchase |
| tag_id | INT | NOT NULL, FK → tags(tag_id) | Linked tag |
| UNIQUE(purchase_id, tag_id) | — | Prevents duplicate tag assignments | Ensures each tag is applied once per purchase |

## Relationships description
Purchases → Categories
Many‑to‑one

Each purchase references exactly one category via category_id.

Purchases ↔ Tags
Many‑to‑many

Implemented through purchase_tags.

A purchase may have multiple tags; a tag may apply to many purchases.

Recurring Bills
Independent entity with no foreign keys.

## Page-by-page plan

## Validation rules

## ERD diagram
![Personal Finance ERD](ERD.png)
