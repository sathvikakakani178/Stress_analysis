import datetime
import pandas as pd
import numpy as np
from typing import Dict, List, Any
import json

class MedicalReportGenerator:
    """
    Medical report generation system for comprehensive documentation
    """
    
    def __init__(self):
        self.report_templates = self._initialize_report_templates()
        self.medical_terminology = self._initialize_medical_terminology()
    
    def _initialize_report_templates(self):
        """
        Initialize medical report templates
        """
        return {
            'Comprehensive Assessment': {
                'sections': [
                    'Patient Information',
                    'Assessment Summary',
                    'Vital Signs Analysis',
                    'Stress Level Classification',
                    'Risk Assessment',
                    'Clinical Findings',
                    'Recommendations',
                    'Follow-up Plan'
                ],
                'priority': 'high'
            },
            'Stress Level Summary': {
                'sections': [
                    'Patient Information',
                    'Stress Classification Results',
                    'Contributing Factors',
                    'Trend Analysis',
                    'Immediate Recommendations'
                ],
                'priority': 'medium'
            },
            'Vital Signs Analysis': {
                'sections': [
                    'Patient Information',
                    'Vital Signs Summary',
                    'Parameter Analysis',
                    'Correlation Analysis',
                    'Clinical Interpretation'
                ],
                'priority': 'medium'
            },
            'Risk Assessment': {
                'sections': [
                    'Patient Information',
                    'Risk Stratification',
                    'Contributing Risk Factors',
                    'Protective Factors',
                    'Risk Mitigation Strategies'
                ],
                'priority': 'high'
            }
        }
    
    def _initialize_medical_terminology(self):
        """
        Initialize medical terminology dictionary
        """
        return {
            'tachycardia': 'Rapid heart rate (>100 bpm)',
            'bradycardia': 'Slow heart rate (<60 bpm)',
            'hypertension': 'High blood pressure (>140/90 mmHg)',
            'hypotension': 'Low blood pressure (<90/60 mmHg)',
            'tachypnea': 'Rapid breathing (>20 breaths/min)',
            'bradypnea': 'Slow breathing (<12 breaths/min)',
            'hypoxemia': 'Low blood oxygen levels (<95%)',
            'hyperthermia': 'Elevated body temperature (>37.2°C)',
            'hypothermia': 'Low body temperature (<36.1°C)'
        }
    
    def _generate_patient_information_section(self, report_data: Dict[str, Any]) -> str:
        """
        Generate patient information section
        """
        generation_time = report_data['generation_time'].strftime('%Y-%m-%d %H:%M:%S')
        session_start = report_data['session_data']['start_time'].strftime('%Y-%m-%d %H:%M:%S')
        
        return f"""
## Patient Information

**Patient ID:** {report_data['patient_id']}
**Report Generated:** {generation_time}
**Assessment Session:** {session_start}
**Total Measurements:** {len(report_data['measurements'])}
**Session Duration:** {self._calculate_session_duration(report_data['session_data'])}

---
"""
    
    def _generate_assessment_summary_section(self, report_data: Dict[str, Any]) -> str:
        """
        Generate assessment summary section
        """
        if not report_data['measurements']:
            return "## Assessment Summary\n\nNo measurements available for analysis.\n\n---\n"
        
        latest_measurement = report_data['measurements'][-1]
        result = latest_measurement['result']
        
        # Calculate summary statistics
        stress_levels = [m['result']['stress_level'] for m in report_data['measurements']]
        stress_counts = pd.Series(stress_levels).value_counts()
        
        avg_confidence = np.mean([m['result']['confidence'] for m in report_data['measurements']])
        
        return f"""
## Assessment Summary

**Current Stress Level:** {result['stress_level']} (Confidence: {result['confidence']:.1%})
**Risk Category:** {result['risk_category']}
**Medical Priority:** {result['medical_priority']}

### Session Statistics
- **Low Stress:** {stress_counts.get('Low', 0)} measurements
- **Medium Stress:** {stress_counts.get('Medium', 0)} measurements  
- **High Stress:** {stress_counts.get('High', 0)} measurements
- **Average Confidence:** {avg_confidence:.1%}

### Primary Contributing Factor
{result['primary_factor']}

### Recommended Action
{result['action_required']}

---
"""
    
    def _generate_vital_signs_analysis_section(self, report_data: Dict[str, Any]) -> str:
        """
        Generate vital signs analysis section
        """
        if not report_data['measurements']:
            return "## Vital Signs Analysis\n\nNo measurements available for analysis.\n\n---\n"
        
        latest_measurement = report_data['measurements'][-1]
        data = latest_measurement['data']
        
        # Calculate vital signs statistics
        measurements_df = pd.DataFrame([m['data'] for m in report_data['measurements']])
        
        vital_signs = ['heart_rate', 'bp_systolic', 'bp_diastolic', 'breathing_rate', 
                      'temperature', 'oxygen_saturation']
        
        analysis_text = "## Vital Signs Analysis\n\n"
        
        for vital in vital_signs:
            if vital in measurements_df.columns:
                current_value = data.get(vital, 'N/A')
                mean_value = measurements_df[vital].mean()
                std_value = measurements_df[vital].std()
                
                analysis_text += f"**{vital.replace('_', ' ').title()}:**\n"
                analysis_text += f"- Current: {current_value}\n"
                analysis_text += f"- Session Average: {mean_value:.1f} ± {std_value:.1f}\n"
                analysis_text += f"- Status: {self._assess_vital_sign_status(vital, current_value)}\n\n"
        
        analysis_text += "---\n"
        return analysis_text
    
    def _generate_stress_classification_section(self, report_data: Dict[str, Any]) -> str:
        """
        Generate stress level classification section
        """
        if not report_data['measurements']:
            return "## Stress Level Classification\n\nNo measurements available for analysis.\n\n---\n"
        
        latest_result = report_data['measurements'][-1]['result']
        
        return f"""
## Stress Level Classification

### Current Classification
**Stress Level:** {latest_result['stress_level']}
**Confidence Score:** {latest_result['confidence']:.1%}

### Classification Probabilities
- **Low Stress:** {latest_result['probabilities']['Low']:.1%}
- **Medium Stress:** {latest_result['probabilities']['Medium']:.1%}
- **High Stress:** {latest_result['probabilities']['High']:.1%}

### Risk Assessment
**Risk Category:** {latest_result['risk_category']}
**Risk Score:** {latest_result['risk_score']:.2f}

### Identified Risk Factors
{self._format_risk_factors(latest_result['risk_factors'])}

---
"""
    
    def _generate_clinical_findings_section(self, report_data: Dict[str, Any]) -> str:
        """
        Generate clinical findings section
        """
        if not report_data['measurements']:
            return "## Clinical Findings\n\nNo measurements available for analysis.\n\n---\n"
        
        latest_measurement = report_data['measurements'][-1]
        result = latest_measurement['result']
        
        findings = []
        
        # Analyze risk factors for clinical significance
        for risk_factor in result['risk_factors']:
            if 'Tachycardia' in risk_factor:
                findings.append('Elevated heart rate detected - may indicate cardiovascular stress')
            elif 'Hypertension' in risk_factor:
                findings.append('Blood pressure elevation noted - requires monitoring')
            elif 'Tachypnea' in risk_factor:
                findings.append('Increased respiratory rate - possible stress response')
            elif 'Hypoxemia' in risk_factor:
                findings.append('Reduced oxygen saturation - requires immediate attention')
            elif 'Fever' in risk_factor:
                findings.append('Elevated body temperature - may indicate physiological stress')
        
        # Add general findings based on stress level
        if result['stress_level'] == 'High':
            findings.append('High stress level classification indicates significant physiological and/or psychological stress')
        elif result['stress_level'] == 'Medium':
            findings.append('Moderate stress level suggests need for intervention and monitoring')
        
        findings_text = "## Clinical Findings\n\n"
        
        if findings:
            for i, finding in enumerate(findings, 1):
                findings_text += f"{i}. {finding}\n"
        else:
            findings_text += "No significant clinical findings identified.\n"
        
        findings_text += "\n---\n"
        return findings_text
    
    def _generate_recommendations_section(self, report_data: Dict[str, Any]) -> str:
        """
        Generate recommendations section
        """
        if not report_data['measurements']:
            return "## Recommendations\n\nNo measurements available for analysis.\n\n---\n"
        
        latest_result = report_data['measurements'][-1]['result']
        
        recommendations = []
        
        # Generate recommendations based on medical priority
        if latest_result['medical_priority'] == 'Critical':
            recommendations.append('Immediate medical evaluation required')
            recommendations.append('Continuous monitoring of vital signs')
            recommendations.append('Consider emergency medical services if symptoms worsen')
        elif latest_result['medical_priority'] == 'High':
            recommendations.append('Urgent medical consultation recommended within 24 hours')
            recommendations.append('Frequent monitoring of vital signs')
            recommendations.append('Stress reduction interventions')
        elif latest_result['medical_priority'] == 'Medium':
            recommendations.append('Medical follow-up within 1-2 weeks')
            recommendations.append('Implement stress management techniques')
            recommendations.append('Monitor symptoms and vital signs regularly')
        else:
            recommendations.append('Continue current health practices')
            recommendations.append('Maintain healthy lifestyle habits')
            recommendations.append('Regular health monitoring')
        
        # Add specific recommendations based on primary factor
        primary_factor = latest_result['primary_factor']
        if 'Heart Rate' in primary_factor:
            recommendations.append('Consider cardiovascular evaluation')
            recommendations.append('Monitor heart rate regularly')
        elif 'Blood Pressure' in primary_factor:
            recommendations.append('Blood pressure monitoring and management')
            recommendations.append('Dietary modifications (reduce sodium)')
        elif 'Sleep' in primary_factor:
            recommendations.append('Sleep hygiene evaluation and improvement')
            recommendations.append('Consider sleep study if problems persist')
        
        recommendations_text = "## Recommendations\n\n"
        
        for i, recommendation in enumerate(recommendations, 1):
            recommendations_text += f"{i}. {recommendation}\n"
        
        recommendations_text += "\n---\n"
        return recommendations_text
    
    def _generate_follow_up_plan_section(self, report_data: Dict[str, Any]) -> str:
        """
        Generate follow-up plan section
        """
        if not report_data['measurements']:
            return "## Follow-up Plan\n\nNo measurements available for analysis.\n\n---\n"
        
        latest_result = report_data['measurements'][-1]['result']
        
        # Determine follow-up timeline based on medical priority
        if latest_result['medical_priority'] == 'Critical':
            timeline = 'Immediate (within hours)'
            frequency = 'Continuous monitoring'
        elif latest_result['medical_priority'] == 'High':
            timeline = 'Urgent (within 24 hours)'
            frequency = 'Daily monitoring'
        elif latest_result['medical_priority'] == 'Medium':
            timeline = 'Short-term (1-2 weeks)'
            frequency = 'Weekly monitoring'
        else:
            timeline = 'Routine (1-3 months)'
            frequency = 'Monthly monitoring'
        
        return f"""
## Follow-up Plan

### Timeline
**Next Assessment:** {timeline}
**Monitoring Frequency:** {frequency}

### Monitoring Parameters
- Vital signs (heart rate, blood pressure, respiratory rate)
- Stress level assessment
- Symptom tracking
- Sleep quality evaluation

### Alert Criteria
- Significant change in vital signs
- Worsening of stress symptoms
- Development of new symptoms
- Failure to improve with interventions

### Contact Information
**For non-urgent questions:** Consult healthcare provider
**For urgent concerns:** Contact emergency services

---
"""
    
    def _calculate_session_duration(self, session_data: Dict[str, Any]) -> str:
        """
        Calculate session duration in human-readable format
        """
        duration = datetime.datetime.now() - session_data['start_time']
        hours = duration.seconds // 3600
        minutes = (duration.seconds % 3600) // 60
        
        if hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"
    
    def _assess_vital_sign_status(self, vital_sign: str, value: Any) -> str:
        """
        Assess vital sign status based on normal ranges
        """
        if value == 'N/A':
            return 'Not available'
        
        # Reference ranges
        ranges = {
            'heart_rate': (60, 100),
            'bp_systolic': (90, 120),
            'bp_diastolic': (60, 80),
            'breathing_rate': (12, 20),
            'temperature': (36.1, 37.2),
            'oxygen_saturation': (95, 100)
        }
        
        if vital_sign in ranges:
            min_val, max_val = ranges[vital_sign]
            try:
                numeric_value = float(value)
                if min_val <= numeric_value <= max_val:
                    return 'Normal'
                elif numeric_value < min_val:
                    return 'Below normal'
                else:
                    return 'Above normal'
            except (ValueError, TypeError):
                return 'Invalid value'
        
        return 'Not assessed'
    
    def _format_risk_factors(self, risk_factors: List[str]) -> str:
        """
        Format risk factors for report display
        """
        if not risk_factors:
            return "No significant risk factors identified."
        
        formatted_factors = ""
        for i, factor in enumerate(risk_factors, 1):
            formatted_factors += f"{i}. {factor}\n"
        
        return formatted_factors
    
    def generate_report(self, report_data: Dict[str, Any], report_type: str) -> Dict[str, Any]:
        """
        Generate a comprehensive medical report
        """
        if report_type not in self.report_templates:
            raise ValueError(f"Unknown report type: {report_type}")
        
        template = self.report_templates[report_type]
        sections = template['sections']
        
        # Generate report header
        report_content = f"""
# Medical Stress Assessment Report
## {report_type}

**Generated:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Report Type:** {report_type}
**Priority:** {template['priority'].upper()}

---
"""
        
        # Generate each section
        for section in sections:
            if section == 'Patient Information':
                report_content += self._generate_patient_information_section(report_data)
            elif section == 'Assessment Summary':
                report_content += self._generate_assessment_summary_section(report_data)
            elif section == 'Vital Signs Analysis':
                report_content += self._generate_vital_signs_analysis_section(report_data)
            elif section == 'Stress Level Classification' or section == 'Stress Classification Results':
                report_content += self._generate_stress_classification_section(report_data)
            elif section == 'Clinical Findings':
                report_content += self._generate_clinical_findings_section(report_data)
            elif section == 'Recommendations' or section == 'Immediate Recommendations':
                report_content += self._generate_recommendations_section(report_data)
            elif section == 'Follow-up Plan':
                report_content += self._generate_follow_up_plan_section(report_data)
            elif section == 'Risk Assessment' or section == 'Risk Stratification':
                report_content += self._generate_risk_assessment_section(report_data)
            elif section == 'Trend Analysis':
                report_content += self._generate_trend_analysis_section(report_data)
        
        # Add medical disclaimer
        report_content += self._generate_medical_disclaimer()
        
        return {
            'content': report_content,
            'report_type': report_type,
            'generation_time': datetime.datetime.now(),
            'total_sections': len(sections)
        }
    
    def _generate_risk_assessment_section(self, report_data: Dict[str, Any]) -> str:
        """
        Generate risk assessment section
        """
        if not report_data['measurements']:
            return "## Risk Assessment\n\nNo measurements available for analysis.\n\n---\n"
        
        latest_result = report_data['measurements'][-1]['result']
        
        return f"""
## Risk Assessment

### Current Risk Level
**Risk Category:** {latest_result['risk_category']}
**Risk Score:** {latest_result['risk_score']:.2f} (0.0 = Low Risk, 1.0 = High Risk)

### Risk Stratification
{self._determine_risk_stratification(latest_result['risk_score'])}

### Contributing Risk Factors
{self._format_risk_factors(latest_result['risk_factors'])}

### Risk Mitigation Strategies
{self._generate_risk_mitigation_strategies(latest_result)}

---
"""
    
    def _generate_trend_analysis_section(self, report_data: Dict[str, Any]) -> str:
        """
        Generate trend analysis section
        """
        if len(report_data['measurements']) < 2:
            return "## Trend Analysis\n\nInsufficient data for trend analysis (minimum 2 measurements required).\n\n---\n"
        
        # Analyze trends
        measurements = report_data['measurements']
        stress_levels = [m['result']['stress_level'] for m in measurements]
        confidences = [m['result']['confidence'] for m in measurements]
        
        # Calculate trend direction
        if len(set(stress_levels)) == 1:
            trend_direction = "Stable"
        else:
            stress_mapping = {'Low': 1, 'Medium': 2, 'High': 3}
            numeric_stress = [stress_mapping[level] for level in stress_levels]
            if numeric_stress[-1] > numeric_stress[0]:
                trend_direction = "Increasing"
            else:
                trend_direction = "Decreasing"
        
        avg_confidence = np.mean(confidences)
        
        return f"""
## Trend Analysis

### Stress Level Trend
**Direction:** {trend_direction}
**Latest Level:** {stress_levels[-1]}
**Initial Level:** {stress_levels[0]}

### Confidence Trend
**Average Confidence:** {avg_confidence:.1%}
**Latest Confidence:** {confidences[-1]:.1%}

### Clinical Interpretation
{self._interpret_trend(trend_direction, stress_levels, avg_confidence)}

---
"""
    
    def _determine_risk_stratification(self, risk_score: float) -> str:
        """
        Determine risk stratification based on score
        """
        if risk_score >= 0.8:
            return "**Very High Risk** - Immediate intervention required"
        elif risk_score >= 0.6:
            return "**High Risk** - Urgent attention needed"
        elif risk_score >= 0.4:
            return "**Moderate Risk** - Regular monitoring recommended"
        elif risk_score >= 0.2:
            return "**Low-Moderate Risk** - Routine follow-up"
        else:
            return "**Low Risk** - Maintain current practices"
    
    def _generate_risk_mitigation_strategies(self, result: Dict[str, Any]) -> str:
        """
        Generate risk mitigation strategies
        """
        strategies = []
        
        if result['risk_score'] >= 0.6:
            strategies.append("Immediate medical evaluation")
            strategies.append("Stress reduction interventions")
            strategies.append("Lifestyle modifications")
        elif result['risk_score'] >= 0.4:
            strategies.append("Regular monitoring")
            strategies.append("Stress management techniques")
            strategies.append("Healthy lifestyle promotion")
        else:
            strategies.append("Preventive measures")
            strategies.append("Health maintenance")
            strategies.append("Regular check-ups")
        
        formatted_strategies = ""
        for i, strategy in enumerate(strategies, 1):
            formatted_strategies += f"{i}. {strategy}\n"
        
        return formatted_strategies
    
    def _interpret_trend(self, direction: str, stress_levels: List[str], confidence: float) -> str:
        """
        Interpret trend analysis results
        """
        if direction == "Increasing":
            return f"Stress levels are increasing over time. This trend requires attention and possible intervention. Assessment confidence: {confidence:.1%}"
        elif direction == "Decreasing":
            return f"Stress levels are decreasing over time. This positive trend suggests effective management. Assessment confidence: {confidence:.1%}"
        else:
            return f"Stress levels remain stable. Continue current monitoring and management strategies. Assessment confidence: {confidence:.1%}"
    
    def _generate_medical_disclaimer(self) -> str:
        """
        Generate medical disclaimer
        """
        return f"""
---

## Medical Disclaimer

This report is generated by an automated medical assessment system and is intended for informational purposes only. The information provided should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of qualified healthcare providers with any questions regarding medical conditions.

**Report Generated:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**System Version:** Medical-Grade Stress Detection System v1.0
**Validation Status:** Automated Analysis

---
"""
