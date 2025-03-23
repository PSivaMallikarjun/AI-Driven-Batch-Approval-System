# Module: AI-Driven Pharma Batch Approval System

## Overview
This module automates the batch approval process in pharmaceutical manufacturing. It evaluates raw materials, production parameters, equipment validation, quality assurance, and delivery status to generate an automated approval certificate based on industry standards (USFDA, WHO, EU-GMP).

## Features
- **Batch Yield & Efficiency Calculation**: Computes input material vs. output API yield.
- **Equipment Calibration & Validation**: Ensures precise calculations for flow rates, RPM, pressure differentials, and temperature monitoring.
- **OEE (Overall Equipment Effectiveness) Tracking**: Measures Availability, Performance, and Quality to optimize efficiency.
- **HVAC & Clean Room Compliance**: Monitors airflow velocity, HEPA filter pressure differentials, and particulate matter count.
- **Water System Validation**: Checks TOC, Conductivity, pH levels, and microbial contamination.
- **Energy & Utility Optimization**: Estimates steam, compressed air, and power consumption for cost control.

## System Requirements
- **Programming Language**: Python 3.8+
- **Libraries**:
  - Gradio
  - Pandas
  - NumPy
  - Datetime
- **Development Environment**:
  - Visual Studio Code / PyCharm
  - Jupyter Notebook (optional)

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/pharma-batch-approval.git
   cd pharma-batch-approval
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the application:
   ```sh
   python app.py
   ```

## Usage
- Launch the Gradio interface and input the following:
  - **Raw Material Status** (Verified/Not Verified)
  - **Production Parameters** (Optimized/Not Optimized)
  - **Equipment Check** (Calibrated/Not Calibrated)
  - **Quality Parameters** (Meets Specifications/Not Met)
  - **Delivery Status** (Ready/Not Ready)
- The system will generate:
  - **Final Batch Approval Status** (Approved/Rejected)
  - **Auto-Generated Approval Certificate**

## Expected Output
### Example Certificate:
```
Pharma Batch Approval Certificate
----------------------------------
Date: 2025-03-23 10:20:50
Raw Material Approval: Pass
Production Approval: Pass
Equipment Approval: Pass
Quality Approval: Pass
Delivery Approval: Pass
Final Batch Status: Approved
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
For any issues or contributions, contact **Siva Mallikarjun Parvatham** at **sivamallikarjun2601@gmail.com**.

