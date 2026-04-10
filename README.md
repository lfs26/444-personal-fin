# 444-personal-fin

## System Description

## Entity list with attributes

purchase_id     SERIAL PRIMARY KEY

item_name       VARCHAR(100) NOT NULL
amount          NUMERIC(10,2) NOT NULL CHECK (amount > 0)
category_id     INT NOT NULL REFERENCES categories(category_id)
purchase_date   DATE NOT NULL
notes           TEXT


## Relationships description

## Page-by-page plan

## Validation rules

## ERD diagram
![Personal Finance ERD](ERD.png)
