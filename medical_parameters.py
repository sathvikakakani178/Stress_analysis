import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any

class MedicalParameterAnalyzer:
    """
    Medical parameter analysis with clinical reference ranges and interpretations
    """
    
    def __init__(self):
        self.reference_ranges = self._initialize_reference_ranges()
        self.parameter_weights = self._initialize_parameter_weights()
        self.clinical_interpretations = self._initialize_clinical_interpretations()
    
    def _initialize_reference_ranges(self):
        """
        Initialize medical reference ranges for adult parameters
        """
        return {
            'heart_rate': {
                'normal': (60, 100),
                'low': (40, 60),
                'high': (100, 180),
                'critical_low': (0, 40),
                'critical_high': (180, 300),
                'unit': 'bpm'
            },
            'breathing_rate': {
                'normal': (12, 20),
                'low': (8, 12),
                'high': (20, 30),
                'critical_low': (0, 8),
                'critical_high': (30, 50),
                'unit': 'breaths/min'
            },
            'bp_systolic': {
                'normal': (90, 120),
                'low': (80, 90),
                'high': (120, 140),
                'critical_low': (0, 80),
                'critical_high': (140, 250),
                'unit': 'mmHg'
            },
            'bp_diastolic': {
                'normal': (60, 80),
                'low': (40, 60),
                'high': (80, 90),
                'critical_low': (0, 40),
                'critical_high': (90, 150),
                'unit': 'mmHg'
            },
            'temperature': {
                'normal': (36.1, 37.2),
                'low': (35.0, 36.1),
                'high': (37.2, 38.0),
                'critical_low': (30.0, 35.0),
                'critical_high': (38.0, 45.0),
                'unit': '°C'
            },
            'oxygen_saturation': {
                'normal': (95, 100),
                'low': (90, 95),
                'high': (100, 100),
                'critical_low': (70, 90),
                'critical_high': (100, 100),
                'unit': '%'
            },
            'sleep_duration': {
                'normal': (7, 9),
                'low': (5, 7),
                'high': (9, 11),
                'critical_low': (0, 5),
                'critical_high': (11, 24),
                'unit': 'hours'
            },
            'sound_level': {
                'normal': (30, 60),
                'low': (20, 30),
                'high': (60, 80),
                'critical_low': (0, 20),
                'critical_high': (80, 120),
                'unit': 'dB'
            },
            'caffeine_intake': {
                'normal': (0, 400),
                'low': (0, 100),
                'high': (400, 600),
                'critical_low': (0, 0),
                'critical_high': (600, 1000),
                'unit': 'mg'
            }
        }
    
    def _initialize_parameter_weights(self):
        """
        Initialize clinical significance weights for each parameter
        """
        return {
            'heart_rate': 0.35,
            'bp_systolic': 0.25,
            'bp_diastolic': 0.20,
            'sleep_duration': 0.15,
            'stress_symptoms': 0.05
        }
    
    def _initialize_clinical_interpretations(self):
        """
        Initialize clinical interpretations for parameter ranges
        """
        return {
            'heart_rate': {
                'normal': 'Heart rate within normal limits',
                'low': 'Bradycardia - slower than normal heart rate',
                'high': 'Tachycardia - faster than normal heart rate',
                'critical_low': 'Severe bradycardia - immediate medical attention required',
                'critical_high': 'Severe tachycardia - immediate medical attention required'
            },
            'breathing_rate': {
                'normal': 'Respiratory rate within normal limits',
                'low': 'Bradypnea - slower than normal breathing rate',
                'high': 'Tachypnea - faster than normal breathing rate',
                'critical_low': 'Severe bradypnea - immediate medical attention required',
                'critical_high': 'Severe tachypnea - immediate medical attention required'
            },
            'bp_systolic': {
                'normal': 'Systolic blood pressure within normal limits',
                'low': 'Hypotension - lower than normal blood pressure',
                'high': 'Hypertension - higher than normal blood pressure',
                'critical_low': 'Severe hypotension - immediate medical attention required',
                'critical_high': 'Severe hypertension - immediate medical attention required'
            },
            'bp_diastolic': {
                'normal': 'Diastolic blood pressure within normal limits',
                'low': 'Low diastolic pressure',
                'high': 'Elevated diastolic pressure',
                'critical_low': 'Critically low diastolic pressure',
                'critical_high': 'Critically high diastolic pressure'
            },
            'temperature': {
                'normal': 'Body temperature within normal limits',
                'low': 'Hypothermia - below normal body temperature',
                'high': 'Fever - elevated body temperature',
                'critical_low': 'Severe hypothermia - immediate medical attention required',
                'critical_high': 'High fever - immediate medical attention required'
            },
            'oxygen_saturation': {
                'normal': 'Oxygen saturation within normal limits',
                'low': 'Mild hypoxemia - slightly low oxygen levels',
                'high': 'Oxygen saturation optimal',
                'critical_low': 'Severe hypoxemia - immediate medical attention required',
                'critical_high': 'Oxygen saturation optimal'
            },
            'sleep_duration': {
                'normal': 'Sleep duration within recommended range',
                'low': 'Sleep deprivation - insufficient sleep',
                'high': 'Excessive sleep duration',
                'critical_low': 'Severe sleep deprivation',
                'critical_high': 'Excessive sleep - possible underlying condition'
            },
            'sound_level': {
                'normal': 'Environmental noise within acceptable limits',
                'low': 'Quiet environment',
                'high': 'Elevated noise levels - potential stressor',
                'critical_low': 'Extremely quiet environment',
                'critical_high': 'Harmful noise levels - hearing protection recommended'
            }
        }
    
    def _categorize_parameter_value(self, value: float, parameter: str) -> str:
        """
        Categorize a parameter value based on medical reference ranges
        """
        if parameter not in self.reference_ranges:
            return 'unknown'
        
        ranges = self.reference_ranges[parameter]
        
        if ranges['critical_low'][0] <= value < ranges['critical_low'][1]:
            return 'critical_low'
        elif ranges['low'][0] <= value < ranges['low'][1]:
            return 'low'
        elif ranges['normal'][0] <= value <= ranges['normal'][1]:
            return 'normal'
        elif ranges['high'][0] < value <= ranges['high'][1]:
            return 'high'
        elif ranges['critical_high'][0] < value <= ranges['critical_high'][1]:
            return 'critical_high'
        else:
            return 'out_of_range'
    
    def _calculate_stress_impact(self, parameter: str, category: str, value: float) -> str:
        """
        Calculate the impact of a parameter on stress levels
        """
        if category == 'normal':
            return 'Minimal impact on stress'
        
        impact_mappings = {
            'heart_rate': {
                'low': 'Low impact - may indicate relaxation or fitness',
                'high': 'High impact - elevated heart rate increases stress',
                'critical_low': 'Critical impact - severe bradycardia affects circulation',
                'critical_high': 'Critical impact - severe tachycardia indicates high stress'
            },
            'breathing_rate': {
                'low': 'Low impact - slow breathing may indicate relaxation',
                'high': 'Moderate impact - rapid breathing indicates stress response',
                'critical_low': 'Critical impact - dangerously slow breathing',
                'critical_high': 'Critical impact - severe respiratory distress'
            },
            'bp_systolic': {
                'low': 'Moderate impact - low blood pressure may cause fatigue',
                'high': 'High impact - elevated blood pressure indicates stress',
                'critical_low': 'Critical impact - severe hypotension',
                'critical_high': 'Critical impact - severe hypertension'
            },
            'bp_diastolic': {
                'low': 'Low impact - slightly low diastolic pressure',
                'high': 'Moderate impact - elevated diastolic pressure',
                'critical_low': 'Critical impact - dangerously low diastolic pressure',
                'critical_high': 'Critical impact - dangerously high diastolic pressure'
            },
            'temperature': {
                'low': 'Moderate impact - hypothermia affects metabolism',
                'high': 'Moderate impact - fever indicates physiological stress',
                'critical_low': 'Critical impact - severe hypothermia',
                'critical_high': 'Critical impact - dangerous hyperthermia'
            },
            'oxygen_saturation': {
                'low': 'High impact - low oxygen levels increase stress',
                'high': 'Minimal impact - optimal oxygen levels',
                'critical_low': 'Critical impact - severe hypoxemia',
                'critical_high': 'Minimal impact - optimal oxygen levels'
            },
            'sleep_duration': {
                'low': 'High impact - sleep deprivation increases stress',
                'high': 'Moderate impact - excessive sleep may indicate issues',
                'critical_low': 'Critical impact - severe sleep deprivation',
                'critical_high': 'High impact - excessive sleep duration'
            },
            'sound_level': {
                'low': 'Minimal impact - quiet environment',
                'high': 'Moderate impact - noise pollution increases stress',
                'critical_low': 'Minimal impact - very quiet environment',
                'critical_high': 'High impact - harmful noise levels'
            }
        }
        
        return impact_mappings.get(parameter, {}).get(category, 'Unknown impact')
    
    def _generate_recommendations(self, parameter: str, category: str, value: float) -> str:
        """
        Generate medical recommendations based on parameter values
        """
        if category == 'normal':
            return 'Continue current health practices'
        
        recommendations = {
            'heart_rate': {
                'low': 'Monitor for symptoms; consider cardiac evaluation if symptomatic',
                'high': 'Practice relaxation techniques; consider cardiovascular evaluation',
                'critical_low': 'Seek immediate medical attention',
                'critical_high': 'Seek immediate medical attention'
            },
            'breathing_rate': {
                'low': 'Monitor consciousness level; evaluate for respiratory depression',
                'high': 'Practice deep breathing exercises; evaluate for underlying causes',
                'critical_low': 'Seek immediate medical attention',
                'critical_high': 'Seek immediate medical attention'
            },
            'bp_systolic': {
                'low': 'Increase fluid intake; monitor for dizziness',
                'high': 'Reduce sodium intake; increase physical activity; monitor regularly',
                'critical_low': 'Seek immediate medical attention',
                'critical_high': 'Seek immediate medical attention'
            },
            'bp_diastolic': {
                'low': 'Monitor for symptoms; ensure adequate hydration',
                'high': 'Lifestyle modifications; regular monitoring',
                'critical_low': 'Seek immediate medical attention',
                'critical_high': 'Seek immediate medical attention'
            },
            'temperature': {
                'low': 'Warm environment; monitor for shivering',
                'high': 'Hydration; rest; monitor for fever symptoms',
                'critical_low': 'Seek immediate medical attention',
                'critical_high': 'Seek immediate medical attention'
            },
            'oxygen_saturation': {
                'low': 'Evaluate breathing; consider oxygen therapy',
                'high': 'Continue current practices',
                'critical_low': 'Seek immediate medical attention',
                'critical_high': 'Continue current practices'
            },
            'sleep_duration': {
                'low': 'Improve sleep hygiene; establish regular sleep schedule',
                'high': 'Evaluate for sleep disorders; maintain regular schedule',
                'critical_low': 'Seek medical evaluation for sleep disorders',
                'critical_high': 'Seek medical evaluation for excessive sleepiness'
            },
            'sound_level': {
                'low': 'Current environment is optimal',
                'high': 'Reduce noise exposure; use hearing protection',
                'critical_low': 'Current environment is optimal',
                'critical_high': 'Immediate hearing protection required'
            }
        }
        
        return recommendations.get(parameter, {}).get(category, 'Consult healthcare provider')
    
    def analyze_parameter(self, parameter: str, value: float) -> Dict[str, Any]:
        """
        Analyze a single parameter and provide medical interpretation
        """
        if parameter not in self.reference_ranges:
            return {
                'status': 'unknown',
                'value': value,
                'normal_range': 'Unknown',
                'interpretation': 'Parameter not recognized',
                'stress_impact': 'Unknown impact',
                'recommendation': 'Consult healthcare provider'
            }
        
        # Categorize the value
        category = self._categorize_parameter_value(value, parameter)
        
        # Get reference range
        ranges = self.reference_ranges[parameter]
        normal_range = f"{ranges['normal'][0]}-{ranges['normal'][1]} {ranges['unit']}"
        
        # Get interpretation
        interpretation = self.clinical_interpretations[parameter].get(category, 'Unknown status')
        
        # Calculate stress impact
        stress_impact = self._calculate_stress_impact(parameter, category, value)
        
        # Generate recommendations
        recommendation = self._generate_recommendations(parameter, category, value)
        
        return {
            'status': category,
            'value': f"{value} {ranges['unit']}",
            'normal_range': normal_range,
            'interpretation': interpretation,
            'stress_impact': stress_impact,
            'recommendation': recommendation,
            'clinical_weight': self.parameter_weights.get(parameter, 0.0)
        }
    
    def analyze_parameters(self, patient_data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """
        Analyze multiple parameters and provide comprehensive medical interpretation
        """
        results = {}
        
        # Analyze each numerical parameter
        for parameter in self.reference_ranges.keys():
            if parameter in patient_data:
                results[parameter] = self.analyze_parameter(parameter, patient_data[parameter])
        
        # Handle stress symptoms separately
        if 'stress_symptoms' in patient_data:
            symptoms = patient_data['stress_symptoms']
            symptoms_count = len(symptoms) if symptoms else 0
            
            if symptoms_count == 0:
                status = 'normal'
                interpretation = 'No stress symptoms reported'
                stress_impact = 'Minimal impact on stress'
                recommendation = 'Continue current wellness practices'
            elif symptoms_count <= 2:
                status = 'low'
                interpretation = 'Few stress symptoms present'
                stress_impact = 'Low impact on stress levels'
                recommendation = 'Monitor symptoms and practice stress reduction techniques'
            elif symptoms_count <= 4:
                status = 'high'
                interpretation = 'Multiple stress symptoms present'
                stress_impact = 'Moderate to high impact on stress levels'
                recommendation = 'Implement stress management strategies and consider professional support'
            else:
                status = 'critical_high'
                interpretation = 'Significant stress symptom burden'
                stress_impact = 'High impact on stress levels and overall wellbeing'
                recommendation = 'Seek professional medical or psychological evaluation'
            
            results['stress_symptoms'] = {
                'status': status,
                'value': f"{symptoms_count} symptoms: {', '.join(symptoms) if symptoms else 'None'}",
                'normal_range': '0-2 symptoms',
                'interpretation': interpretation,
                'stress_impact': stress_impact,
                'recommendation': recommendation,
                'clinical_weight': self.parameter_weights.get('stress_symptoms', 0.0)
            }
        
        return results
    
    def calculate_parameter_correlation(self, measurements: List[Dict]) -> Dict[str, float]:
        """
        Calculate correlations between parameters across multiple measurements
        """
        if len(measurements) < 2:
            return {}
        
        # Extract parameter data
        parameter_data = {}
        for param in self.reference_ranges.keys():
            parameter_data[param] = []
            for measurement in measurements:
                if param in measurement['data']:
                    parameter_data[param].append(measurement['data'][param])
        
        # Calculate correlations
        correlations = {}
        parameters = list(parameter_data.keys())
        
        for i, param1 in enumerate(parameters):
            for j, param2 in enumerate(parameters[i+1:], i+1):
                if len(parameter_data[param1]) > 1 and len(parameter_data[param2]) > 1:
                    # Calculate correlation coefficient
                    correlation = np.corrcoef(parameter_data[param1], parameter_data[param2])[0, 1]
                    correlations[f"{param1}_vs_{param2}"] = correlation
        
        return correlations
    
    def generate_parameter_summary(self, analysis_results: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate a comprehensive summary of parameter analysis
        """
        normal_count = 0
        abnormal_count = 0
        critical_count = 0
        high_impact_count = 0
        
        critical_parameters = []
        abnormal_parameters = []
        recommendations = []
        
        for param, result in analysis_results.items():
            status = result['status']
            
            if status == 'normal':
                normal_count += 1
            elif status in ['critical_low', 'critical_high']:
                critical_count += 1
                critical_parameters.append(param)
            else:
                abnormal_count += 1
                abnormal_parameters.append(param)
            
            # Check for high impact parameters
            if 'High impact' in result['stress_impact'] or 'Critical impact' in result['stress_impact']:
                high_impact_count += 1
            
            # Collect recommendations
            if result['recommendation'] != 'Continue current health practices':
                recommendations.append(f"{param}: {result['recommendation']}")
        
        total_parameters = len(analysis_results)
        
        return {
            'total_parameters': total_parameters,
            'normal_count': normal_count,
            'abnormal_count': abnormal_count,
            'critical_count': critical_count,
            'high_impact_count': high_impact_count,
            'critical_parameters': critical_parameters,
            'abnormal_parameters': abnormal_parameters,
            'recommendations': recommendations,
            'overall_status': self._determine_overall_status(normal_count, abnormal_count, critical_count, total_parameters)
        }
    
    def _determine_overall_status(self, normal: int, abnormal: int, critical: int, total: int) -> str:
        """
        Determine overall health status based on parameter analysis
        """
        if critical > 0:
            return 'Critical - Immediate medical attention required'
        elif abnormal > total * 0.5:
            return 'Concerning - Multiple parameters outside normal range'
        elif abnormal > 0:
            return 'Caution - Some parameters need attention'
        else:
            return 'Normal - All parameters within acceptable range'
