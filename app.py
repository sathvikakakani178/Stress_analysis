import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import datetime
from medical_classifier import MedicalStressClassifier
from medical_parameters import MedicalParameterAnalyzer
from medical_reports import MedicalReportGenerator
from medical_insights import MedicalInsightsEngine
from data_validator import MedicalDataValidator

# Initialize medical components
@st.cache_resource
def initialize_medical_system():
    """Initialize the medical-grade stress detection system"""
    classifier = MedicalStressClassifier()
    analyzer = MedicalParameterAnalyzer()
    report_generator = MedicalReportGenerator()
    insights_engine = MedicalInsightsEngine()
    validator = MedicalDataValidator()
    
    return classifier, analyzer, report_generator, insights_engine, validator

# Page Configuration
st.set_page_config(
    page_title='Medical-Grade Stress Detection System',
    page_icon='🏥',
    layout='wide',
    initial_sidebar_state='expanded'
)

# Initialize session state
if 'patient_history' not in st.session_state:
    st.session_state.patient_history = []
if 'current_session' not in st.session_state:
    st.session_state.current_session = {
        'start_time': datetime.datetime.now(),
        'measurements': []
    }

# Load medical system
classifier, analyzer, report_generator, insights_engine, validator = initialize_medical_system()

# Main Header
st.title('🏥 Medical-Grade Stress Detection System')
st.markdown('**Advanced three-tier stress classification with comprehensive health parameter analysis**')

# Sidebar for navigation and settings
with st.sidebar:
    st.header('📊 System Overview')
    
    # Current session info
    st.subheader('Current Session')
    session_duration = datetime.datetime.now() - st.session_state.current_session['start_time']
    st.metric('Session Duration', f"{session_duration.seconds // 60}m {session_duration.seconds % 60}s")
    st.metric('Total Measurements', len(st.session_state.current_session['measurements']))
    st.metric('Historical Records', len(st.session_state.patient_history))
    
    # Medical system status
    st.subheader('System Status')
    st.success('✅ Medical Classifier: Active')
    st.success('✅ Parameter Analyzer: Online')
    st.success('✅ Validation System: Ready')
    
    if st.button('🔄 Reset Session'):
        st.session_state.current_session = {
            'start_time': datetime.datetime.now(),
            'measurements': []
        }
        st.rerun()

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🔬 Medical Assessment", 
    "📊 Advanced Analytics", 
    "📈 Real-time Monitoring",
    "🧠 Clinical Insights"
])

with tab1:
    st.header('🔬 Medical-Grade Stress Assessment')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader('Essential Health Parameters')
        heart_rate = st.number_input(
            '💓 Heart Rate (bpm)', 
            min_value=40, max_value=200, value=75,
            help="Normal range: 60-100 bpm for adults"
        )
        
        blood_pressure_systolic = st.number_input(
            '🩸 Systolic Blood Pressure (mmHg)', 
            min_value=80, max_value=250, value=120,
            help="Normal range: 90-120 mmHg"
        )
        
        blood_pressure_diastolic = st.number_input(
            '🩸 Diastolic Blood Pressure (mmHg)', 
            min_value=40, max_value=150, value=80,
            help="Normal range: 60-80 mmHg"
        )
        
    with col2:
        st.subheader('Additional Indicators')
        sleep_duration = st.number_input(
            '💤 Sleep Duration (hours)', 
            min_value=0.0, max_value=24.0, value=7.5, step=0.5,
            help="Recommended: 7-9 hours for adults"
        )
        
        stress_symptoms = st.multiselect(
            '⚠️ Current Symptoms',
            ['Headache', 'Muscle Tension', 'Fatigue', 'Irritability', 
             'Difficulty Concentrating', 'Sleep Issues', 'Anxiety'],
            help="Select any symptoms currently experienced"
        )
    
    # Medical assessment button
    if st.button('🔬 Perform Medical Assessment', type='primary'):
        with st.spinner('Performing comprehensive medical analysis...'):
            time.sleep(2)
            
            # Validate parameters
            validation_result = validator.validate_parameters({
                'heart_rate': heart_rate,
                'bp_systolic': blood_pressure_systolic,
                'bp_diastolic': blood_pressure_diastolic,
                'sleep_duration': sleep_duration,
                'stress_symptoms': stress_symptoms
            })
            
            if validation_result['valid']:
                # Prepare data for classification
                patient_data = {
                    'heart_rate': heart_rate,
                    'bp_systolic': blood_pressure_systolic,
                    'bp_diastolic': blood_pressure_diastolic,
                    'sleep_duration': sleep_duration,
                    'stress_symptoms': stress_symptoms,
                    'timestamp': datetime.datetime.now()
                }
                
                # Perform classification
                classification_result = classifier.classify_stress_level(patient_data)
                
                # Store in session
                st.session_state.current_session['measurements'].append({
                    'timestamp': datetime.datetime.now(),
                    'data': patient_data,
                    'result': classification_result
                })
                
                # Display results
                st.success('✅ Medical Assessment Complete')
                
                # Results display
                col5, col6, col7 = st.columns(3)
                
                with col5:
                    stress_level = classification_result['stress_level']
                    color = {'Low': 'green', 'Medium': 'orange', 'High': 'red'}[stress_level]
                    st.markdown(f"### Stress Level: <span style='color: {color}'>{stress_level}</span>", unsafe_allow_html=True)
                    st.metric('Confidence Score', f"{classification_result['confidence']:.1%}")
                
                with col6:
                    st.metric('Risk Assessment', classification_result['risk_category'])
                    st.metric('Primary Contributing Factor', classification_result['primary_factor'])
                
                with col7:
                    st.metric('Medical Priority', classification_result['medical_priority'])
                    st.metric('Recommended Action', classification_result['action_required'])
                
                # Parameter analysis
                st.subheader('📊 Parameter Analysis')
                parameter_analysis = analyzer.analyze_parameters(patient_data)
                
                for param, analysis in parameter_analysis.items():
                    with st.expander(f"{param.replace('_', ' ').title()} Analysis"):
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.write(f"**Status:** {analysis['status']}")
                            st.write(f"**Value:** {analysis['value']}")
                            st.write(f"**Normal Range:** {analysis['normal_range']}")
                        with col_b:
                            st.write(f"**Impact on Stress:** {analysis['stress_impact']}")
                            st.write(f"**Recommendation:** {analysis['recommendation']}")
                
            else:
                st.error('❌ Parameter Validation Failed')
                for error in validation_result['errors']:
                    st.error(f"• {error}")

with tab2:
    st.header('📊 Advanced Medical Analytics')
    
    if st.session_state.current_session['measurements']:
        # Create comprehensive analytics dashboard
        measurements_df = pd.DataFrame([
            {
                'timestamp': m['timestamp'],
                'stress_level': m['result']['stress_level'],
                'confidence': m['result']['confidence'],
                'heart_rate': m['data']['heart_rate'],
                'bp_systolic': m['data']['bp_systolic'],
                'bp_diastolic': m['data']['bp_diastolic'],
                'sleep_duration': m['data']['sleep_duration']
            }
            for m in st.session_state.current_session['measurements']
        ])
        
        # Stress level distribution
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader('Stress Level Distribution')
            stress_counts = measurements_df['stress_level'].value_counts()
            fig_pie = px.pie(
                values=stress_counts.values,
                names=stress_counts.index,
                title="Current Session Stress Levels",
                color_discrete_map={'Low': 'green', 'Medium': 'orange', 'High': 'red'}
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.subheader('Confidence Score Trends')
            fig_confidence = px.line(
                measurements_df,
                x='timestamp',
                y='confidence',
                title="Classification Confidence Over Time",
                markers=True
            )
            st.plotly_chart(fig_confidence, use_container_width=True)
        
        # Vital signs correlation matrix
        st.subheader('Vital Signs Correlation Analysis')
        vital_signs = ['heart_rate', 'bp_systolic', 'bp_diastolic', 'sleep_duration']
        
        if len(measurements_df) > 1:
            corr_matrix = measurements_df[vital_signs].corr()
            fig_heatmap = px.imshow(
                corr_matrix,
                text_auto=True,
                aspect="auto",
                title="Vital Signs Correlation Matrix",
                color_continuous_scale='RdBu'
            )
            st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # Parameter trends
        st.subheader('Parameter Trends Analysis')
        selected_params = st.multiselect(
            'Select parameters to analyze',
            vital_signs,
            default=['heart_rate', 'bp_systolic']
        )
        
        if selected_params:
            fig_trends = make_subplots(
                rows=len(selected_params), cols=1,
                subplot_titles=selected_params,
                shared_xaxes=True
            )
            
            for i, param in enumerate(selected_params):
                fig_trends.add_trace(
                    go.Scatter(
                        x=measurements_df['timestamp'],
                        y=measurements_df[param],
                        mode='lines+markers',
                        name=param,
                        line=dict(color=px.colors.qualitative.Set1[i % len(px.colors.qualitative.Set1)])
                    ),
                    row=i+1, col=1
                )
            
            fig_trends.update_layout(height=200*len(selected_params), title="Parameter Trends Over Time")
            st.plotly_chart(fig_trends, use_container_width=True)
        
    else:
        st.info('📈 No measurements available. Please perform a medical assessment first.')

with tab3:
    st.header('📈 Real-time Medical Monitoring')
    
    st.subheader('Live Monitoring Dashboard')
    
    # Real-time simulation controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        monitoring_active = st.checkbox('🔴 Enable Live Monitoring', value=False)
        
    with col2:
        refresh_rate = st.selectbox('Refresh Rate', [1, 5, 10, 30], index=1)
        
    with col3:
        alert_threshold = st.selectbox('Alert Threshold', ['Low', 'Medium', 'High'], index=1)
    
    if monitoring_active:
        # Create placeholder for real-time data
        placeholder = st.empty()
        
        # Simulate real-time monitoring
        with placeholder.container():
            st.subheader('🔴 LIVE - Medical Monitoring Active')
            
            # Display current vital signs (simulated)
            vital_cols = st.columns(4)
            
            current_time = datetime.datetime.now()
            
            # Simulate vital signs with some variation
            base_hr = 75 + np.random.normal(0, 5)
            base_br = 16 + np.random.normal(0, 2)
            base_temp = 37.0 + np.random.normal(0, 0.3)
            base_spo2 = 98 + np.random.normal(0, 1)
            
            with vital_cols[0]:
                st.metric('Heart Rate', f'{base_hr:.0f} bpm', delta=f'{np.random.normal(0, 2):.0f}')
                
            with vital_cols[1]:
                st.metric('Respiratory Rate', f'{base_br:.0f} /min', delta=f'{np.random.normal(0, 1):.0f}')
                
            with vital_cols[2]:
                st.metric('Temperature', f'{base_temp:.1f}°C', delta=f'{np.random.normal(0, 0.1):.1f}')
                
            with vital_cols[3]:
                st.metric('SpO2', f'{base_spo2:.1f}%', delta=f'{np.random.normal(0, 0.5):.1f}')
            
            # Alert system
            if base_hr > 100 or base_hr < 60:
                st.warning('⚠️ Heart Rate Alert: Outside normal range')
            
            if base_temp > 37.5:
                st.warning('⚠️ Temperature Alert: Elevated temperature detected')
            
            if base_spo2 < 95:
                st.error('🚨 Critical Alert: Low oxygen saturation')
            
            # Live chart
            st.subheader('Live Vital Signs Chart')
            
            # Generate sample time series data
            times = pd.date_range(start=current_time - datetime.timedelta(minutes=10), 
                                 end=current_time, freq='30s')
            
            live_data = pd.DataFrame({
                'time': times,
                'heart_rate': 75 + np.random.normal(0, 5, len(times)),
                'breathing_rate': 16 + np.random.normal(0, 2, len(times)),
                'temperature': 37.0 + np.random.normal(0, 0.3, len(times))
            })
            
            fig_live = make_subplots(
                rows=3, cols=1,
                subplot_titles=['Heart Rate (bpm)', 'Respiratory Rate (/min)', 'Temperature (°C)'],
                shared_xaxes=True
            )
            
            fig_live.add_trace(
                go.Scatter(x=live_data['time'], y=live_data['heart_rate'], 
                          mode='lines', name='Heart Rate', line=dict(color='red')),
                row=1, col=1
            )
            
            fig_live.add_trace(
                go.Scatter(x=live_data['time'], y=live_data['breathing_rate'], 
                          mode='lines', name='Respiratory Rate', line=dict(color='blue')),
                row=2, col=1
            )
            
            fig_live.add_trace(
                go.Scatter(x=live_data['time'], y=live_data['temperature'], 
                          mode='lines', name='Temperature', line=dict(color='green')),
                row=3, col=1
            )
            
            fig_live.update_layout(height=600, title="Live Vital Signs Monitoring")
            st.plotly_chart(fig_live, use_container_width=True)
        
        # Auto-refresh
        time.sleep(refresh_rate)
        st.rerun()
    
    else:
        st.info('📊 Click "Enable Live Monitoring" to start real-time monitoring')
        
        # Show monitoring configuration
        st.subheader('Monitoring Configuration')
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write('**Alert Thresholds:**')
            st.write('• Heart Rate: 60-100 bpm')
            st.write('• Respiratory Rate: 12-20 /min')
            st.write('• Temperature: 36.1-37.2°C')
            st.write('• SpO2: >95%')
            
        with col2:
            st.write('**Monitoring Features:**')
            st.write('• Real-time vital signs tracking')
            st.write('• Automated alert system')
            st.write('• Trend analysis')
            st.write('• Historical data logging')

with tab4:
    st.header('🧠 Clinical Insights & Recommendations')
    
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
st.markdown('---')
st.markdown(
    '**Medical-Grade Stress Detection System** | '
    'Advanced three-tier classification with comprehensive health analysis | '
    f'Session Active: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
)
