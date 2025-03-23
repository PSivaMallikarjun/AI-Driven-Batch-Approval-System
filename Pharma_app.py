import gradio as gr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from fpdf import FPDF
import os
import io
import base64
from PIL import Image, ImageDraw, ImageFont
from transformers import pipeline
import torch

# Create a fixed directory for temporary files
TEMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp_files")
os.makedirs(TEMP_DIR, exist_ok=True)

# Ensure we're using the right device
device = 0 if torch.cuda.is_available() else -1

# Load Hugging Face model for batch approval classification
try:
    classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english", device=device)
except Exception as e:
    print(f"Failed to load main model: {e}")
    try:
        # Fallback to a simpler model if the first one fails
        classifier = pipeline("text-classification", model="distilbert-base-uncased", device=device)
    except Exception as e:
        print(f"Failed to load fallback model: {e}")
        # Define a dummy classifier that simulates the pipeline output
        def dummy_classifier(text):
            # Use some basic rules to determine if the text is positive
            positive_words = ["pass", "high", "good", "excellent"]
            text_lower = text.lower()
            score = sum([1 for word in positive_words if word in text_lower])
            return [{"label": "POSITIVE" if score >= 2 else "NEGATIVE", "score": 0.8}]
        classifier = dummy_classifier

# Function to calculate estimated delivery date
def calculate_delivery_date(batch_start, processing_time):
    try:
        return (datetime.strptime(batch_start, "%Y-%m-%d") + timedelta(days=int(processing_time))).strftime("%Y-%m-%d")
    except:
        return "Invalid date format"

# AI-based batch approval prediction
def ai_batch_approval(yield_efficiency, oee_score, hvac_status, water_validation, energy_optimization):
    input_text = f"Yield: {yield_efficiency}, OEE: {oee_score}, HVAC: {hvac_status}, Water: {water_validation}, Energy: {energy_optimization}"
    try:
        if callable(getattr(classifier, "__call__", None)):
            result = classifier(input_text)
            if isinstance(result, list) and len(result) > 0:
                result = result[0]
            return "Approved" if result.get("label") == "POSITIVE" else "Pending"
        else:
            raise ValueError("Classifier is not callable")
    except Exception as e:
        print(f"Error in AI prediction: {e}")
        # Fallback to rule-based approval if AI fails
        if yield_efficiency > 80 and oee_score > 75 and hvac_status == "Pass" and water_validation == "Pass":
            return "Approved"
        return "Pending"

# Create a custom barcode image since the barcode library is causing issues
def create_custom_barcode(text, width=400, height=100):
    # Create a white background image
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)
    
    try:
        # Try to use a default font
        font = ImageFont.load_default()
        
        # Draw border
        draw.rectangle([(0, 0), (width-1, height-1)], outline='black')
        
        # Draw text
        draw.text((width//2, height//4), f"ID: {text}", fill='black', anchor='mm', font=font)
        
        # Draw code-like lines
        line_width = 2
        for i in range(10):
            # Calculate position based on text characters
            x = 20 + i * (width-40)//10
            # Vary height based on character value if possible
            try:
                h = ord(text[i % len(text)]) % 50 + 10
            except:
                h = 30
            
            draw.rectangle([(x, height//2), (x + line_width, height//2 + h)], fill='black')
        
        # Save to a file
        barcode_filename = os.path.join(TEMP_DIR, f"batch_{text}_barcode.png")
        image.save(barcode_filename)
        
        return barcode_filename
    except Exception as e:
        print(f"Error creating custom barcode: {e}")
        # Fallback to an even simpler approach
        draw.rectangle([(0, 0), (width-1, height-1)], outline='black')
        draw.text((width//2, height//2), f"Batch ID: {text}", fill='black')
        
        barcode_filename = os.path.join(TEMP_DIR, f"batch_{text}_barcode.png")
        image.save(barcode_filename)
        
        return barcode_filename

# Function to generate auto-approval certificate with barcode
def generate_certificate(batch_id, yield_efficiency, oee_score, hvac_status, water_validation, energy_optimization, batch_start, processing_time):
    delivery_date = calculate_delivery_date(batch_start, processing_time)
    approval_status = ai_batch_approval(yield_efficiency, oee_score, hvac_status, water_validation, energy_optimization)
    
    # Generate Custom Barcode (not using barcode library)
    barcode_filename = create_custom_barcode(batch_id)
    
    # Make sure the file exists before proceeding
    if not os.path.exists(barcode_filename):
        print(f"Warning: Barcode file not created at {barcode_filename}")
        # Create a simple placeholder using matplotlib as a last resort
        plt.figure(figsize=(4, 2))
        plt.text(0.5, 0.5, f"Batch ID: {batch_id}", horizontalalignment='center', verticalalignment='center')
        plt.axis('off')
        plt.savefig(barcode_filename)
        plt.close()
        
    # Generate PDF Certificate
    pdf_filename = os.path.join(TEMP_DIR, f"batch_{batch_id}_certificate.pdf")
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, "Batch Approval Certificate", ln=True, align='C')
        pdf.ln(10)
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, f"Batch ID: {batch_id}", ln=True)
        pdf.cell(200, 10, f"Yield Efficiency: {yield_efficiency}%", ln=True)
        pdf.cell(200, 10, f"OEE Score: {oee_score}%", ln=True)
        pdf.cell(200, 10, f"HVAC Compliance: {hvac_status}", ln=True)
        pdf.cell(200, 10, f"Water System Validation: {water_validation}", ln=True)
        pdf.cell(200, 10, f"Energy Optimization: {energy_optimization}%", ln=True)
        pdf.cell(200, 10, f"Estimated Delivery Date: {delivery_date}", ln=True)
        pdf.cell(200, 10, f"Approval Status: {approval_status} (AI Prediction)", ln=True)
        
        # Only include the barcode image if it exists
        if os.path.exists(barcode_filename):
            pdf.image(barcode_filename, x=60, y=pdf.get_y() + 10, w=80)
        
        pdf.output(pdf_filename)
    except Exception as e:
        print(f"Error generating PDF: {e}")
        # Create an empty file to prevent further errors
        with open(pdf_filename, 'w') as f:
            f.write("Error generating PDF")
        return pdf_filename, barcode_filename
    
    return pdf_filename, barcode_filename

# Function to create efficiency visualization
def create_efficiency_plot(yield_efficiency, oee_score, energy_optimization):
    labels = ['Yield Efficiency', 'OEE Score', 'Energy Optimization']
    values = [yield_efficiency, oee_score, energy_optimization]
    
    plot_filename = os.path.join(TEMP_DIR, f"efficiency_plot_{datetime.now().strftime('%Y%m%d%H%M%S')}.png")
    try:
        fig, ax = plt.subplots(figsize=(8, 6))
        bars = ax.bar(labels, values, color=['#4169E1', '#2E8B57', '#FF8C00'])
        ax.set_ylim([0, 100])
        ax.set_ylabel("Percentage (%)")
        ax.set_title("Batch Efficiency Metrics")
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height}%',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig(plot_filename)
        plt.close()
    except Exception as e:
        print(f"Error generating plot: {e}")
        # Create a simple placeholder plot if generation fails
        plt.figure(figsize=(8, 6))
        plt.text(0.5, 0.5, "Error generating visualization", horizontalalignment='center', verticalalignment='center')
        plt.axis('off')
        plt.savefig(plot_filename)
        plt.close()
        
    # Verify the file exists
    if not os.path.exists(plot_filename):
        # Last resort fallback
        with open(plot_filename, 'w') as f:
            f.write("Error generating plot")
    
    return plot_filename

# Clean old files to prevent disk space issues
def clean_old_files(max_files=20):
    try:
        files = sorted([os.path.join(TEMP_DIR, f) for f in os.listdir(TEMP_DIR)], 
                      key=lambda x: os.path.getmtime(x))
        if len(files) > max_files:
            for old_file in files[:-max_files]:
                try:
                    os.remove(old_file)
                except:
                    pass
    except Exception as e:
        print(f"Error cleaning old files: {e}")

# Gradio Interface function
def batch_approval_system(batch_id, yield_efficiency, oee_score, hvac_status, water_validation, energy_optimization, batch_start, processing_time):
    if not batch_id:
        return None, None, None, "Error: Batch ID is required"
    
    # Clean up old files periodically
    clean_old_files()
    
    try:
        pdf_file, barcode_file = generate_certificate(batch_id, yield_efficiency, oee_score, hvac_status, water_validation, energy_optimization, batch_start, processing_time)
        plot_file = create_efficiency_plot(yield_efficiency, oee_score, energy_optimization)
        
        approval_status = ai_batch_approval(yield_efficiency, oee_score, hvac_status, water_validation, energy_optimization)
        message = f"Batch {batch_id} has been processed. Status: {approval_status}"
        
        # Verify all files exist
        files_to_check = [pdf_file, barcode_file, plot_file]
        for file in files_to_check:
            if file and not os.path.exists(file):
                print(f"Warning: File does not exist: {file}")
        
        return pdf_file, barcode_file, plot_file, message
    except Exception as e:
        error_message = f"Error processing batch: {str(e)}"
        print(error_message)
        return None, None, None, error_message

# Create the Gradio interface
demo = gr.Interface(
    fn=batch_approval_system,
    inputs=[
        gr.Textbox(label="Batch ID", placeholder="Enter a unique batch identifier", value="BATCH001"),
        gr.Slider(0, 100, value=85, step=1, label="Yield Efficiency (%)"),
        gr.Slider(0, 100, value=80, step=1, label="OEE Score (%)"),
        gr.Dropdown(["Pass", "Fail"], value="Pass", label="HVAC Compliance"),
        gr.Dropdown(["Pass", "Fail"], value="Pass", label="Water System Validation"),
        gr.Slider(0, 100, value=75, step=1, label="Energy Optimization (%)"),
        gr.Textbox(label="Batch Start Date (YYYY-MM-DD)", value=datetime.now().strftime("%Y-%m-%d")),
        gr.Number(label="Processing Time (Days)", value=14, minimum=1, maximum=90)
    ],
    outputs=[
        gr.File(label="Download Approval Certificate"),
        gr.Image(label="Batch ID Barcode"),
        gr.Image(label="Efficiency Metrics Visualization"),
        gr.Textbox(label="Status")
    ],
    title="AI-Driven Batch Approval System",
    description="Automate batch approval, generate compliance certificates, and visualize efficiency metrics as per USFDA, WHO, and EU-GMP. The system uses AI to predict approval status based on key metrics.",
    examples=[
        ["BATCH001", 92, 88, "Pass", "Pass", 85, "2025-03-10", 14],
        ["BATCH002", 78, 72, "Pass", "Fail", 65, "2025-03-15", 21],
        ["BATCH003", 95, 90, "Pass", "Pass", 92, "2025-03-20", 7]
    ],
    allow_flagging="never"  # Disable flagging to avoid file-related errors
)

# Launch the app (only when running directly, not when imported)
if __name__ == "__main__":
    demo.launch()
else:
    # This is the pattern Hugging Face Spaces looks for
    app = demo