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
### 💰 1. Dashboard
#### Displays
* High‑level financial metrics (total purchases, total bills, total spending)
* Summary of upcoming bills within the next billing window
* Aggregated monthly bill totals

#### User Actions
* Navigate to other pages
* Review overall spending and upcoming obligations

### 🛒 2. Log Purchase
#### Displays
* Form for entering a new purchase
* Inputs for item name, amount, category, notes
* Multi‑select for assigning tags

#### User Actions
* Submit a new purchase
* Attach one or more tags
* Add optional notes

### 📅 3. Recurring Bills
#### Displays
* Form for adding a recurring bill
* Inputs for bill name, amount, due day, frequency, notes

#### User Actions
* Add a new recurring bill
* Specify billing frequency and due day
* Save bill to the database

### 📈 4. View Spending
#### Displays
* Spending summary filtered by tag
* Category‑level spending totals
* Visual breakdown of spending
* Monthly bill obligations
* Full list of purchases with tag labels

#### User Actions
* Filter spending by tag
* Review category totals
* Inspect all purchases
* Compare spending across categories

### 🗂 5. Manage Purchases
#### Displays
* Table of all purchases with IDs, categories, and amounts
* Control for selecting a purchase to delete

#### User Actions
* Review all purchases
* Select a purchase by ID
* Delete a purchase

### 🏷️ 6. Tags (Tag Management)
#### Displays
* Form for creating a new tag (name, color, description)
* Table of existing tags
* Control for selecting a tag to delete

#### User Actions
* Add a new tag
* Assign color and optional description
* View all tags
* Delete a tag


## Validation rules

### Purchases
* item_name: required, ≤100 chars
* amount: required, numeric, >0
* category_id: required, must exist in categories
* purchase_date: required, valid date
* tags: optional, but each must exist in tags table

### Recurring Bills
* bill_name: required
* amount: required, >0
* frequency: must be weekly/monthly/yearly
* next_due_date: required, valid date

### Tags
* tag_name: required, unique, ≤50 chars
### purchase_tags 
* No duplicate pairs
* purchase_id must exist
* tag_id must exist

## ERD diagram
![Personal Finance ERD](ERD.png)
