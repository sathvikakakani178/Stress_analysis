# Medical-Grade Stress Detection System

## Overview

This is a comprehensive medical-grade stress detection system built with Streamlit that provides three-tier stress classification (Low, Medium, High) with advanced health parameter analysis. The system integrates multiple medical components including classification models, parameter analysis, and clinical insights to deliver a complete healthcare monitoring solution.

## Features

- **🏥 Medical Assessment**: Simplified 5-parameter input for stress analysis
- **📊 Advanced Analytics**: Data visualization and trend analysis
- **📡 Real-time Monitoring**: Live vital signs simulation
- **🧠 Clinical Insights**: Medical recommendations and analysis

## Installation

1. Clone or download all files to your local directory
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Local Development
```bash
streamlit run app.py
```

### Streamlit Cloud Deployment
1. Upload all files to a GitHub repository
2. Connect your repository to Streamlit Cloud
3. Deploy with the following settings:
   - Main file: `app.py`
   - Python version: 3.9+
   - Requirements file: `requirements.txt`

## File Structure

```
deployment_package/
├── app.py                    # Main Streamlit application
├── medical_classifier.py     # ML-based stress classification
├── medical_parameters.py     # Parameter analysis with clinical ranges
├── medical_insights.py       # Clinical insights generation
├── data_validator.py         # Medical data validation
├── medical_reports.py        # Report generation system
├── requirements.txt          # Python dependencies
├── .streamlit/
│   └── config.toml          # Streamlit configuration
└── README.md                # This file
```

## Usage

1. **Medical Assessment**: Enter your health parameters (heart rate, blood pressure, sleep duration, stress symptoms)
2. **View Results**: Get immediate three-tier stress classification with medical analysis
3. **Advanced Analytics**: Explore trends and correlations in your data
4. **Real-time Monitoring**: Simulate live vital signs monitoring
5. **Clinical Insights**: Review personalized medical recommendations

## Health Parameters

The system analyzes 5 essential health indicators:
- **Heart Rate**: Normal range 60-100 bpm
- **Systolic Blood Pressure**: Normal range 90-140 mmHg
- **Diastolic Blood Pressure**: Normal range 60-90 mmHg
- **Sleep Duration**: Recommended 7-9 hours
- **Stress Symptoms**: Self-reported severity (None, Mild, Moderate, Severe)

## Stress Classification

- **Low Stress**: Normal parameters, low risk
- **Medium Stress**: Some parameters outside normal range, moderate risk
- **High Stress**: Multiple parameters concerning, high risk requiring attention

## Medical Disclaimer

This system is for educational and research purposes only. Always consult qualified healthcare professionals for medical advice, diagnosis, or treatment decisions.

## Technical Details

- **Framework**: Streamlit for web interface
- **ML Model**: RandomForest classifier with 200 estimators
- **Data Processing**: Pandas and NumPy for numerical analysis
- **Visualization**: Plotly for interactive charts
- **Validation**: Comprehensive medical data validation system

## System Requirements

- Python 3.9 or higher
- Internet connection for Streamlit Cloud deployment
- Modern web browser for optimal experience

## Support

For technical issues or questions about the system, please refer to the Streamlit documentation or contact the development team.