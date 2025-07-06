# Medical-Grade Stress Detection System

## Overview

This is a comprehensive medical-grade stress detection system built with Streamlit that provides three-tier stress classification with advanced health parameter analysis. The system integrates multiple medical components including classification models, parameter analysis, report generation, and clinical insights to deliver a complete healthcare monitoring solution.

## System Architecture

The application follows a modular architecture with clear separation of concerns:

- **Frontend**: Streamlit-based web interface for user interaction and data visualization
- **Backend**: Python-based medical processing modules with specialized components
- **Data Processing**: Medical parameter validation and analysis with clinical reference ranges
- **Machine Learning**: RandomForest-based stress classification model with medical-grade parameters
- **Reporting**: Comprehensive medical report generation system

## Key Components

### Core Medical Modules

1. **MedicalStressClassifier** (`medical_classifier.py`)
   - Three-tier stress classification system
   - RandomForest model with 200 estimators optimized for medical data
   - Medical parameter weights based on clinical significance
   - Feature importance tracking for clinical interpretation

2. **MedicalParameterAnalyzer** (`medical_parameters.py`)
   - Clinical reference ranges for adult parameters
   - Parameter weight assignments based on medical importance
   - Clinical interpretation system for vital signs

3. **MedicalReportGenerator** (`medical_reports.py`)
   - Comprehensive medical report templates
   - Multiple report types (Comprehensive Assessment, Stress Summary, Vital Signs Analysis)
   - Medical terminology integration

4. **MedicalInsightsEngine** (`medical_insights.py`)
   - Clinical knowledge base for medical insights
   - Evidence-based intervention protocols
   - Physiological stress indicator analysis

5. **MedicalDataValidator** (`data_validator.py`)
   - Medical-grade data validation with clinical ranges
   - Critical threshold monitoring
   - Validation history tracking

### Data Management

- **Session Management**: Patient history tracking and current session monitoring
- **Parameter Monitoring**: Simplified essential health tracking (heart rate, blood pressure, sleep duration, stress symptoms)
- **Validation System**: Comprehensive data validation with medical reference ranges

### User Interface

- **Streamlit Frontend**: Wide layout with expandable sidebar
- **Interactive Dashboards**: Real-time parameter visualization
- **Medical Reports**: Formatted clinical documentation
- **Patient History**: Session-based tracking system

## Data Flow

1. **Data Input**: Health parameters entered through Streamlit interface
2. **Validation**: Medical data validator ensures parameter integrity
3. **Analysis**: Parameter analyzer processes data against clinical ranges
4. **Classification**: ML model classifies stress levels (three-tier system)
5. **Insights**: Medical insights engine generates clinical interpretations
6. **Reporting**: Report generator creates comprehensive medical documentation
7. **Visualization**: Results displayed through interactive Plotly charts

## External Dependencies

### Core Libraries
- **Streamlit**: Web application framework
- **Pandas/NumPy**: Data processing and numerical computations
- **Scikit-learn**: Machine learning model implementation
- **Plotly**: Interactive data visualization
- **Joblib**: Model serialization and loading

### Medical-Specific Features
- Clinical reference ranges for vital signs
- Medical terminology integration
- Evidence-based intervention protocols
- HIPAA-compliant data handling considerations

## Deployment Strategy

The application is designed for deployment on Replit with the following considerations:

- **Single-file execution**: Main application in `app.py`
- **Modular imports**: Medical components loaded as separate modules
- **Resource caching**: Streamlit cache for medical system initialization
- **Session persistence**: State management for patient data
- **Real-time processing**: Immediate analysis and feedback

## Changelog

- July 06, 2025: Initial setup
- July 06, 2025: Simplified parameter structure to 5 essential health indicators (heart rate, systolic/diastolic blood pressure, sleep duration, stress symptoms) per user request
- July 06, 2025: Removed medical reports tab to streamline interface

## User Preferences

Preferred communication style: Simple, everyday language.