# 444-personal-fin

## System Description

## Entity list with attributes

| Column | Data Type | Constraints | Description |
| --- | --- | --- | --- |
| purchase_id | SERIAL | PRIMARY KEY | Unique identifier for each purchase |
| item_name | VARCHAR(100) | NOT NULL | Name of the purchase |
| amount | NUMERIC(10,2) | NOT NULL, CHECK(amount > 0) | Cost of the purchase |
| category_id | INT | NOT NULL, FK → categories(category_id) | Category assigned to the purchase |
| purchase_date | DATE | NOT NULL | Date of the transaction |
| notes | TEXT | NULL | Optional notes |


## Relationships description

## Page-by-page plan

## Validation rules

## ERD diagram
![Personal Finance ERD](ERD.png)
