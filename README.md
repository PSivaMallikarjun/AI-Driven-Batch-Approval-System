---
dataset_name: "Home Loan Approval Dataset"
pretty_name: "Home Loan Approval Dataset"
license: "MIT"
task_categories:
  - financial-analysis
  - risk-assessment
  - credit-scoring
language:
  - en
size_categories:
  - 10K< rows
tags:
  - home-loan
  - credit-score
  - finance
  - risk-analysis
  - machine-learning
  - banking
num_rows: 50
dataset_repo: "SivaMallikarjun/Home-Loan-Approval-Dataset"
---

# Home Loan Approval Dataset Repository

## Overview
This repository contains structured data for analyzing and predicting home loan approvals based on various financial and creditworthiness metrics. The dataset is designed for use in financial analysis, machine learning, and risk assessment models.

## Repository Structure

- `data/`
  - `loan_applications.csv` - Contains applicant details and loan request information.
  - `income_verification.csv` - Provides details on multiple income sources for applicants.
  - `credit_scores.csv` - Includes credit scores from different agencies.
  
- `documentation/`
  - `data_dictionary.md` - Detailed explanation of dataset fields.
  - `README.md` - Overview of dataset purpose and usage instructions.

## Dataset Fields

### `loan_applications.csv`
| Application_ID | Applicant_Name | Age | Marital_Status | Dependents | Employment_Type | Years_Employed | Primary_Income | Passive_Income | Debt_Obligations | Loan_Amount_Requested | Loan_Term | Loan_Purpose | Property_Value | Credit_Score | Repayment_Worthiness_Score | Approval_Status |
|---------------|---------------|-----|----------------|------------|----------------|----------------|----------------|----------------|----------------|----------------------|----------|-------------|---------------|--------------|---------------------------|----------------|
| 1001         | John Doe      | 35  | Married        | 2          | Full-time      | 10             | 80,000         | 5,000          | 20,000          | 250,000               | 30       | House Purchase | 300,000        | 720          | 85                        | Approved       |
| 1002         | Jane Smith    | 29  | Single         | 0          | Self-employed  | 5              | 60,000         | 12,000         | 10,000          | 180,000               | 20       | Refinance      | 220,000        | 680          | 75                        | Approved       |
| 1003         | Mark Johnson  | 40  | Married        | 3          | Part-time      | 15             | 40,000         | 3,000          | 5,000           | 150,000               | 25       | Other          | 200,000        | 650          | 65                        | Rejected       |

### `income_verification.csv`
| Application_ID | Primary_Income_Source | Rental_Income | Dividend_Income | Other_Investments |
|---------------|----------------------|--------------|----------------|-----------------|
| 1001         | Salary/Wages         | 2,000        | 1,000          | 2,000           |
| 1002         | Business Profits     | 5,000        | 3,000          | 4,000           |
| 1003         | Hourly Wages         | 1,000        | 500            | 1,000           |

### `credit_scores.csv`
| Application_ID | Credit_Agency | Credit_Score | Score_Date |
|---------------|--------------|--------------|------------|
| 1001         | Equifax      | 720          | 2025-01-01 |
| 1002         | Experian     | 680          | 2025-01-02 |
| 1003         | TransUnion   | 650          | 2025-01-03 |

## Dataset Creation

### Curation Rationale
The dataset has been curated to provide insights into home loan approval processes, helping financial institutions assess loan risk based on multiple factors such as income, creditworthiness, and debt obligations.

### Source Data
This dataset is a synthetic representation of real-world home loan applications, designed for research and educational purposes.

### Data Producers
The dataset has been generated for analytical and machine learning use cases in the banking and finance sector.

## Bias, Risks, and Limitations
This dataset may not reflect real-world biases in lending decisions. Users should be mindful of ethical considerations when using the data for predictive modeling.

## Usage Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/SivaMallikarjun/home-loan-approval-dataset.git
   ```
2. Load the CSV files into a data processing tool (Python, SQL, etc.).
3. Use this dataset for home loan risk analysis and machine learning models.

## License
This dataset is available under a public license for research and educational purposes.

