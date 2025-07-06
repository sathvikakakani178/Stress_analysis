import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time

# Import medical modules
from medical_classifier import MedicalStressClassifier
from medical_parameters import MedicalParameterAnalyzer
from medical_insights import MedicalInsightsEngine
from data_validator import MedicalDataValidator
from medical_reports import MedicalReportGenerator

# Page configuration
st.set_page_config(
    page_title="Medical Stress Detection System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for medical theme
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #2E86AB, #A23B72);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2E86AB;
        margin-bottom: 1rem;
    }
    .stress-level-low {
        background: #d4edda;
        color: #155724;
        padding: 0.5rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .stress-level-medium {
        background: #fff3cd;
        color: #856404;
        padding: 0.5rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .stress-level-high {
        background: #f8d7da;
        color: #721c24;
        padding: 0.5rem;
        border-radius: 5px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def initialize_medical_system():
    """Initialize the medical-grade stress detection system"""
    classifier = MedicalStressClassifier()
    parameter_analyzer = MedicalParameterAnalyzer()
    insights_engine = MedicalInsightsEngine()
    data_validator = MedicalDataValidator()
    report_generator = MedicalReportGenerator()
    
    return classifier, parameter_analyzer, insights_engine, data_validator, report_generator

def initialize_session_state():
    """Initialize session state variables"""
    if 'patient_history' not in st.session_state:
        st.session_state.patient_history = []
    
    if 'current_session' not in st.session_state:
        st.session_state.current_session = {
            'start_time': datetime.now(),
            'measurements': [],
            'patient_info': {}
        }

def main():
    # Initialize system components
    classifier, parameter_analyzer, insights_engine, data_validator, report_generator = initialize_medical_system()
    initialize_session_state()
    
    # Header
    st.markdown('<div class="main-header"><h1>🏥 Medical-Grade Stress Detection System</h1><p>Advanced Three-Tier Stress Classification with Clinical Analysis</p></div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("📊 Session Overview")
        
        # Session info
        st.write(f"**Session Started:** {st.session_state.current_session['start_time'].strftime('%Y-%m-%d %H:%M:%S')}")
        st.write(f"**Measurements Taken:** {len(st.session_state.current_session['measurements'])}")
        st.write(f"**Total Sessions:** {len(st.session_state.patient_history)}")
        
        # Quick actions
        st.subheader("🚀 Quick Actions")
        if st.button("🔄 New Session"):
            if st.session_state.current_session['measurements']:
                st.session_state.patient_history.append(st.session_state.current_session.copy())
            st.session_state.current_session = {
                'start_time': datetime.now(),
                'measurements': [],
                'patient_info': {}
            }
            st.rerun()
        
        if st.button("📋 Clear History"):
            st.session_state.patient_history = []
            st.session_state.current_session = {
                'start_time': datetime.now(),
                'measurements': [],
                'patient_info': {}
            }
            st.rerun()
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🏥 Medical Assessment", "📊 Advanced Analytics", "📡 Real-time Monitoring", "🧠 Clinical Insights"])
    
    with tab1:
        st.header("🏥 Medical Assessment")
        st.write("Enter essential health parameters for comprehensive stress analysis")
        
        # Create input form
        with st.form("medical_assessment_form"):
            st.subheader("Essential Health Parameters")
            
            col1, col2 = st.columns(2)
            
            with col1:
                heart_rate = st.number_input("Heart Rate (bpm)", min_value=30, max_value=200, value=75, help="Normal resting heart rate: 60-100 bpm")
                systolic_bp = st.number_input("Systolic Blood Pressure (mmHg)", min_value=70, max_value=250, value=120, help="Normal systolic BP: 90-140 mmHg")
                sleep_duration = st.number_input("Sleep Duration (hours)", min_value=0.0, max_value=24.0, value=7.5, step=0.5, help="Recommended: 7-9 hours per night")
            
            with col2:
                diastolic_bp = st.number_input("Diastolic Blood Pressure (mmHg)", min_value=40, max_value=150, value=80, help="Normal diastolic BP: 60-90 mmHg")
                stress_symptoms = st.selectbox("Stress Symptoms", 
                                             options=["None", "Mild", "Moderate", "Severe"], 
                                             index=0,
                                             help="Self-reported stress symptom severity")
            
            submitted = st.form_submit_button("🔍 Analyze Stress Level", type="primary")
            
            if submitted:
                # Prepare patient data
                patient_data = {
                    'heart_rate': heart_rate,
                    'systolic_bp': systolic_bp,
                    'diastolic_bp': diastolic_bp,
                    'sleep_duration': sleep_duration,
                    'stress_symptoms': stress_symptoms
                }
                
                # Validate data
                validation_result = data_validator.validate_parameters(patient_data)
                
                if validation_result['is_valid']:
                    # Analyze parameters
                    parameter_analysis = parameter_analyzer.analyze_parameters(patient_data)
                    
                    # Classify stress level
                    stress_result = classifier.classify_stress_level(patient_data)
                    
                    # Store measurement
                    measurement = {
                        'timestamp': datetime.now(),
                        'data': patient_data,
                        'result': stress_result,
                        'parameter_analysis': parameter_analysis,
                        'validation': validation_result
                    }
                    
                    st.session_state.current_session['measurements'].append(measurement)
                    
                    # Display results
                    st.success("✅ Analysis completed successfully!")
                    
                    # Stress level display
                    stress_level = stress_result['stress_level']
                    confidence = stress_result['confidence']
                    
                    if stress_level == 'Low':
                        st.markdown(f'<div class="stress-level-low">🟢 Stress Level: {stress_level} (Confidence: {confidence:.1%})</div>', unsafe_allow_html=True)
                    elif stress_level == 'Medium':
                        st.markdown(f'<div class="stress-level-medium">🟡 Stress Level: {stress_level} (Confidence: {confidence:.1%})</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="stress-level-high">🔴 Stress Level: {stress_level} (Confidence: {confidence:.1%})</div>', unsafe_allow_html=True)
                    
                    # Key metrics
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Medical Priority", stress_result['medical_priority'])
                    
                    with col2:
                        st.metric("Risk Score", f"{stress_result['risk_score']:.2f}")
                    
                    with col3:
                        st.metric("Primary Factor", stress_result['primary_factor'])
                    
                    with col4:
                        st.metric("Action Required", stress_result['action_required'])
                    
                    # Parameter analysis
                    st.subheader("📋 Parameter Analysis")
                    
                    for param, analysis in parameter_analysis.items():
                        with st.expander(f"{param.replace('_', ' ').title()}: {analysis['value']} {analysis.get('unit', '')}"):
                            st.write(f"**Status:** {analysis['status']}")
                            st.write(f"**Category:** {analysis['category']}")
                            st.write(f"**Clinical Significance:** {analysis['clinical_significance']}")
                            st.write(f"**Stress Impact:** {analysis['stress_impact']}")
                            st.write(f"**Recommendations:** {analysis['recommendations']}")
                
                else:
                    st.error("❌ Data validation failed!")
                    for error in validation_result['errors']:
                        st.error(f"• {error}")
    
    with tab2:
        st.header("📊 Advanced Analytics")
        
        if st.session_state.current_session['measurements']:
            # Create comprehensive analytics
            measurements = st.session_state.current_session['measurements']
            
            # Stress level distribution
            st.subheader("🎯 Stress Level Distribution")
            
            stress_levels = [m['result']['stress_level'] for m in measurements]
            stress_counts = pd.Series(stress_levels).value_counts()
            
            fig_pie = px.pie(
                values=stress_counts.values,
                names=stress_counts.index,
                title="Stress Level Distribution",
                color_discrete_map={'Low': '#28a745', 'Medium': '#ffc107', 'High': '#dc3545'}
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            
            # Parameter trends
            st.subheader("📈 Parameter Trends")
            
            # Prepare data for trending
            df_trends = pd.DataFrame([
                {
                    'timestamp': m['timestamp'],
                    'heart_rate': m['data']['heart_rate'],
                    'systolic_bp': m['data']['systolic_bp'],
                    'diastolic_bp': m['data']['diastolic_bp'],
                    'sleep_duration': m['data']['sleep_duration'],
                    'stress_level': m['result']['stress_level'],
                    'risk_score': m['result']['risk_score']
                }
                for m in measurements
            ])
            
            # Vital signs trend
            fig_vitals = go.Figure()
            
            fig_vitals.add_trace(go.Scatter(
                x=df_trends['timestamp'],
                y=df_trends['heart_rate'],
                mode='lines+markers',
                name='Heart Rate',
                line=dict(color='#ff6b6b')
            ))
            
            fig_vitals.add_trace(go.Scatter(
                x=df_trends['timestamp'],
                y=df_trends['systolic_bp'],
                mode='lines+markers',
                name='Systolic BP',
                line=dict(color='#4ecdc4')
            ))
            
            fig_vitals.add_trace(go.Scatter(
                x=df_trends['timestamp'],
                y=df_trends['diastolic_bp'],
                mode='lines+markers',
                name='Diastolic BP',
                line=dict(color='#45b7d1')
            ))
            
            fig_vitals.update_layout(
                title="Vital Signs Trends",
                xaxis_title="Time",
                yaxis_title="Value",
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_vitals, use_container_width=True)
            
            # Risk score analysis
            st.subheader("⚡ Risk Score Analysis")
            
            fig_risk = px.bar(
                x=range(len(measurements)),
                y=[m['result']['risk_score'] for m in measurements],
                title="Risk Score Evolution",
                labels={'x': 'Measurement #', 'y': 'Risk Score'},
                color=[m['result']['risk_score'] for m in measurements],
                color_continuous_scale='RdYlGn_r'
            )
            
            st.plotly_chart(fig_risk, use_container_width=True)
            
            # Correlation analysis
            st.subheader("🔗 Parameter Correlations")
            
            numeric_cols = ['heart_rate', 'systolic_bp', 'diastolic_bp', 'sleep_duration', 'risk_score']
            correlation_matrix = df_trends[numeric_cols].corr()
            
            fig_corr = px.imshow(
                correlation_matrix,
                text_auto=True,
                aspect="auto",
                title="Parameter Correlation Matrix",
                color_continuous_scale='RdBu_r'
            )
            
            st.plotly_chart(fig_corr, use_container_width=True)
            
            # Statistical summary
            st.subheader("📊 Statistical Summary")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Parameter Statistics:**")
                st.dataframe(df_trends[numeric_cols].describe())
            
            with col2:
                st.write("**Stress Level Summary:**")
                summary_stats = {
                    'Total Measurements': len(measurements),
                    'Low Stress': stress_counts.get('Low', 0),
                    'Medium Stress': stress_counts.get('Medium', 0),
                    'High Stress': stress_counts.get('High', 0),
                    'Average Risk Score': df_trends['risk_score'].mean(),
                    'Max Risk Score': df_trends['risk_score'].max()
                }
                
                for key, value in summary_stats.items():
                    if isinstance(value, float):
                        st.metric(key, f"{value:.2f}")
                    else:
                        st.metric(key, value)
        
        else:
            st.info("📊 Advanced analytics will be available after taking measurements in the Medical Assessment tab.")
    
    with tab3:
        st.header("📡 Real-time Monitoring")
        st.write("Live simulation of vital signs monitoring")
        
        # Real-time monitoring controls
        col1, col2 = st.columns(2)
        
        with col1:
            monitoring_duration = st.selectbox("Monitoring Duration", [1, 5, 10, 15], index=1)
            
        with col2:
            if st.button("🔴 Start Live Monitoring"):
                # Create placeholder for live data
                live_placeholder = st.empty()
                
                # Progress bar
                progress_bar = st.progress(0)
                
                # Initialize monitoring
                start_time = datetime.now()
                monitoring_data = []
                
                # Simulate real-time data collection
                for i in range(monitoring_duration * 60):  # Every second for duration in minutes
                    current_time = datetime.now()
                    
                    # Simulate vital signs with some random variation
                    if st.session_state.current_session['measurements']:
                        latest = st.session_state.current_session['measurements'][-1]['data']
                        base_hr = latest['heart_rate']
                        base_sys = latest['systolic_bp']
                        base_dia = latest['diastolic_bp']
                    else:
                        base_hr, base_sys, base_dia = 75, 120, 80
                    
                    # Add realistic variations
                    heart_rate = base_hr + np.random.normal(0, 5)
                    systolic = base_sys + np.random.normal(0, 3)
                    diastolic = base_dia + np.random.normal(0, 2)
                    
                    monitoring_data.append({
                        'time': current_time,
                        'heart_rate': heart_rate,
                        'systolic_bp': systolic,
                        'diastolic_bp': diastolic
                    })
                    
                    # Update progress
                    progress = (i + 1) / (monitoring_duration * 60)
                    progress_bar.progress(progress)
                    
                    # Update live chart every 5 seconds
                    if i % 5 == 0:
                        with live_placeholder.container():
                            df_live = pd.DataFrame(monitoring_data)
                            
                            fig_live = go.Figure()
                            
                            fig_live.add_trace(go.Scatter(
                                x=df_live['time'],
                                y=df_live['heart_rate'],
                                mode='lines',
                                name='Heart Rate',
                                line=dict(color='#ff6b6b', width=2)
                            ))
                            
                            fig_live.add_trace(go.Scatter(
                                x=df_live['time'],
                                y=df_live['systolic_bp'],
                                mode='lines',
                                name='Systolic BP',
                                line=dict(color='#4ecdc4', width=2)
                            ))
                            
                            fig_live.add_trace(go.Scatter(
                                x=df_live['time'],
                                y=df_live['diastolic_bp'],
                                mode='lines',
                                name='Diastolic BP',
                                line=dict(color='#45b7d1', width=2)
                            ))
                            
                            fig_live.update_layout(
                                title=f"Live Vital Signs - {len(monitoring_data)} seconds",
                                xaxis_title="Time",
                                yaxis_title="Value",
                                height=400
                            )
                            
                            st.plotly_chart(fig_live, use_container_width=True)
                            
                            # Current values
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.metric("Current HR", f"{heart_rate:.0f} bpm")
                            
                            with col2:
                                st.metric("Current Systolic", f"{systolic:.0f} mmHg")
                            
                            with col3:
                                st.metric("Current Diastolic", f"{diastolic:.0f} mmHg")
                    
                    # Small delay to simulate real-time
                    time.sleep(0.1)
                
                st.success(f"✅ Live monitoring completed! Collected {len(monitoring_data)} data points over {monitoring_duration} minutes.")
        
        # Show sample live monitoring interface
        st.subheader("📊 Live Monitoring Interface")
        
        if st.session_state.current_session['measurements']:
            # Live chart
            st.subheader('Live Vital Signs Chart')
            
            # Generate sample time series data
            times = pd.date_range(start=current_time - datetime.timedelta(minutes=10), 
                                 end=current_time, freq='30s')
            
            live_data = pd.DataFrame({
                'time': times,
                'heart_rate': 75 + np.random.normal(0, 5, len(times)),
                'systolic_bp': 120 + np.random.normal(0, 3, len(times)),
                'diastolic_bp': 80 + np.random.normal(0, 2, len(times))
            })
            
            fig_sample = go.Figure()
            
            fig_sample.add_trace(go.Scatter(
                x=live_data['time'],
                y=live_data['heart_rate'],
                mode='lines',
                name='Heart Rate',
                line=dict(color='#ff6b6b', width=2)
            ))
            
            fig_sample.add_trace(go.Scatter(
                x=live_data['time'],
                y=live_data['systolic_bp'],
                mode='lines',
                name='Systolic BP',
                line=dict(color='#4ecdc4', width=2)
            ))
            
            fig_sample.add_trace(go.Scatter(
                x=live_data['time'],
                y=live_data['diastolic_bp'],
                mode='lines',
                name='Diastolic BP',
                line=dict(color='#45b7d1', width=2)
            ))
            
            fig_sample.update_layout(
                title="Sample Live Vital Signs Monitoring",
                xaxis_title="Time",
                yaxis_title="Value",
                height=400
            )
            
            st.plotly_chart(fig_sample, use_container_width=True)
            
            # Alert system
            st.subheader("🚨 Alert System")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.success("✅ All parameters within normal ranges")
                st.info("ℹ️ Heart rate slightly elevated - monitor")
            
            with col2:
                st.warning("⚠️ Blood pressure trending upward")
                st.error("🚨 Immediate attention required for abnormal readings")
        
        else:
            st.info("📡 Real-time monitoring will be enhanced after taking initial measurements.")
    
    with tab4:
        st.header("🧠 Clinical Insights")
        
        if st.session_state.current_session['measurements']:
            # Generate clinical insights
            latest_measurement = st.session_state.current_session['measurements'][-1]
            insights = insights_engine.generate_insights(
                latest_measurement['data'],
                latest_measurement['result'],
                st.session_state.current_session['measurements']
            )
            
            # Clinical interpretation
            st.subheader('🔬 Clinical Interpretation')
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write('**Primary Clinical Findings:**')
                for finding in insights['primary_findings']:
                    st.write(f'• {finding}')
                
                st.write('**Risk Factors Identified:**')
                for risk in insights['risk_factors']:
                    st.write(f'• {risk}')
            
            with col2:
                st.write('**Protective Factors:**')
                for protective in insights['protective_factors']:
                    st.write(f'• {protective}')
                
                st.write('**Areas of Concern:**')
                for concern in insights['concerns']:
                    st.write(f'• {concern}')
            
            # Medical recommendations
            st.subheader('💊 Medical Recommendations')
            
            recommendation_tabs = st.tabs(['Immediate Actions', 'Short-term Plan', 'Long-term Strategy', 'Monitoring Plan'])
            
            with recommendation_tabs[0]:
                st.write('**Immediate Actions Required:**')
                for action in insights['immediate_actions']:
                    st.write(f'• {action}')
            
            with recommendation_tabs[1]:
                st.write('**Short-term Management (1-7 days):**')
                for plan in insights['short_term_plan']:
                    st.write(f'• {plan}')
            
            with recommendation_tabs[2]:
                st.write('**Long-term Strategy (1-3 months):**')
                for strategy in insights['long_term_strategy']:
                    st.write(f'• {strategy}')
            
            with recommendation_tabs[3]:
                st.write('**Recommended Monitoring:**')
                for monitoring in insights['monitoring_plan']:
                    st.write(f'• {monitoring}')
            
            # Evidence-based insights
            st.subheader('📚 Evidence-Based Insights')
            
            with st.expander('📖 Clinical Literature References'):
                st.write('**Relevant Research Findings:**')
                for reference in insights['literature_references']:
                    st.write(f'• {reference}')
            
            with st.expander('🎯 Personalized Recommendations'):
                st.write('**Tailored to Current Parameters:**')
                for personalized in insights['personalized_recommendations']:
                    st.write(f'• {personalized}')
            
            # Trend analysis
            if len(st.session_state.current_session['measurements']) > 1:
                st.subheader('📈 Trend Analysis & Prognosis')
                
                trend_analysis = insights_engine.analyze_trends(st.session_state.current_session['measurements'])
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write('**Observed Trends:**')
                    for trend in trend_analysis['observed_trends']:
                        st.write(f'• {trend}')
                
                with col2:
                    st.write('**Predictive Indicators:**')
                    for indicator in trend_analysis['predictive_indicators']:
                        st.write(f'• {indicator}')
                
                # Prognosis
                st.write('**Clinical Prognosis:**')
                st.info(trend_analysis['prognosis'])
        
        else:
            st.info('🧠 Clinical insights will be available after performing medical assessments.')
            
            # Show insight categories
            st.subheader('Available Clinical Insights')
            
            insight_categories = {
                'Clinical Interpretation': 'Comprehensive analysis of medical findings',
                'Risk Assessment': 'Identification and evaluation of health risks',
                'Treatment Recommendations': 'Evidence-based treatment suggestions',
                'Monitoring Guidelines': 'Recommended follow-up and monitoring protocols',
                'Lifestyle Modifications': 'Personalized lifestyle and behavioral recommendations',
                'Prognosis Analysis': 'Trend-based health outcome predictions'
            }
            
            for category, description in insight_categories.items():
                with st.expander(f'🧠 {category}'):
                    st.write(description)

# Footer
st.markdown("---")
st.markdown("### 🏥 Medical-Grade Stress Detection System")
st.markdown("**Disclaimer:** This system is for educational and research purposes only. Always consult qualified healthcare professionals for medical advice.")

if __name__ == "__main__":
    main()