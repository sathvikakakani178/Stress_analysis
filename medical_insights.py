import numpy as np
import pandas as pd
from typing import Dict, List, Any, Tuple
import datetime

class MedicalInsightsEngine:
    """
    Advanced medical insights generation system for clinical interpretation
    """
    
    def __init__(self):
        self.clinical_knowledge_base = self._initialize_clinical_knowledge()
        self.evidence_base = self._initialize_evidence_base()
        self.intervention_protocols = self._initialize_intervention_protocols()
    
    def _initialize_clinical_knowledge(self):
        """
        Initialize clinical knowledge base for medical insights
        """
        return {
            'stress_indicators': {
                'physiological': {
                    'heart_rate': {
                        'normal': (60, 100),
                        'stress_threshold': 100,
                        'critical_threshold': 120,
                        'clinical_significance': 'high'
                    },
                    'blood_pressure': {
                        'normal_systolic': (90, 120),
                        'normal_diastolic': (60, 80),
                        'stress_threshold': (130, 85),
                        'critical_threshold': (140, 90),
                        'clinical_significance': 'high'
                    },
                    'respiratory_rate': {
                        'normal': (12, 20),
                        'stress_threshold': 20,
                        'critical_threshold': 25,
                        'clinical_significance': 'medium'
                    },
                    'temperature': {
                        'normal': (36.1, 37.2),
                        'stress_threshold': 37.5,
                        'critical_threshold': 38.0,
                        'clinical_significance': 'medium'
                    },
                    'oxygen_saturation': {
                        'normal': (95, 100),
                        'stress_threshold': 95,
                        'critical_threshold': 92,
                        'clinical_significance': 'high'
                    }
                },
                'behavioral': {
                    'sleep_duration': {
                        'normal': (7, 9),
                        'stress_threshold': 6,
                        'critical_threshold': 4,
                        'clinical_significance': 'medium'
                    },
                    'caffeine_intake': {
                        'normal': (0, 200),
                        'stress_threshold': 300,
                        'critical_threshold': 500,
                        'clinical_significance': 'low'
                    }
                },
                'environmental': {
                    'sound_level': {
                        'normal': (30, 60),
                        'stress_threshold': 70,
                        'critical_threshold': 85,
                        'clinical_significance': 'low'
                    }
                }
            },
            'stress_correlations': {
                'cardiovascular': ['heart_rate', 'bp_systolic', 'bp_diastolic'],
                'respiratory': ['breathing_rate', 'oxygen_saturation'],
                'metabolic': ['temperature', 'sleep_duration'],
                'environmental': ['sound_level', 'caffeine_intake']
            }
        }
    
    def _initialize_evidence_base(self):
        """
        Initialize evidence-based medical literature references
        """
        return {
            'stress_physiology': [
                'Acute stress response activates the sympathetic nervous system, leading to increased heart rate and blood pressure',
                'Chronic stress is associated with cardiovascular disease, immune suppression, and metabolic dysfunction',
                'Stress-induced tachycardia typically presents as heart rate >100 bpm during non-physical stressors',
                'Elevated cortisol levels from chronic stress can lead to hypertension and insulin resistance'
            ],
            'vital_signs_stress': [
                'Respiratory rate increases during acute stress response as part of fight-or-flight mechanism',
                'Blood pressure elevation during stress is mediated by catecholamine release',
                'Sleep deprivation significantly increases stress hormone levels and sympathetic activity',
                'Environmental noise above 70 dB can trigger stress responses and elevate blood pressure'
            ],
            'intervention_evidence': [
                'Deep breathing exercises can reduce heart rate and blood pressure within minutes',
                'Regular sleep hygiene practices improve stress resilience and vital sign stability',
                'Stress management techniques show significant reduction in cardiovascular stress markers',
                'Environmental modifications can reduce physiological stress responses by 20-30%'
            ]
        }
    
    def _initialize_intervention_protocols(self):
        """
        Initialize evidence-based intervention protocols
        """
        return {
            'immediate_interventions': {
                'critical_stress': [
                    'Immediate medical evaluation',
                    'Continuous vital sign monitoring',
                    'Consider emergency services if unstable',
                    'Assess for medical emergencies'
                ],
                'high_stress': [
                    'Implement breathing exercises',
                    'Reduce environmental stressors',
                    'Monitor vital signs every 15 minutes',
                    'Consider anxiolytic if appropriate'
                ],
                'moderate_stress': [
                    'Guided relaxation techniques',
                    'Environmental noise reduction',
                    'Hydration and rest',
                    'Monitor response to interventions'
                ]
            },
            'short_term_management': {
                'cardiovascular_focus': [
                    'Daily blood pressure monitoring',
                    'Moderate exercise program',
                    'Dietary sodium reduction',
                    'Stress management counseling'
                ],
                'respiratory_focus': [
                    'Breathing exercise training',
                    'Pulmonary function assessment',
                    'Environmental allergen evaluation',
                    'Respiratory therapy if indicated'
                ],
                'sleep_focus': [
                    'Sleep hygiene optimization',
                    'Sleep study evaluation',
                    'Caffeine reduction program',
                    'Cognitive behavioral therapy for insomnia'
                ]
            },
            'long_term_strategies': {
                'lifestyle_modification': [
                    'Regular exercise program',
                    'Stress management training',
                    'Nutritional counseling',
                    'Social support enhancement'
                ],
                'medical_management': [
                    'Regular cardiovascular screening',
                    'Stress-related disorder evaluation',
                    'Medication optimization if needed',
                    'Preventive care protocols'
                ]
            }
        }
    
    def _analyze_physiological_patterns(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze physiological patterns for clinical insights
        """
        patterns = {
            'cardiovascular_pattern': self._assess_cardiovascular_pattern(patient_data),
            'respiratory_pattern': self._assess_respiratory_pattern(patient_data),
            'metabolic_pattern': self._assess_metabolic_pattern(patient_data),
            'autonomic_pattern': self._assess_autonomic_pattern(patient_data)
        }
        
        return patterns
    
    def _assess_cardiovascular_pattern(self, patient_data: Dict[str, Any]) -> str:
        """
        Assess cardiovascular pattern for stress indicators
        """
        hr = patient_data.get('heart_rate', 0)
        bp_sys = patient_data.get('bp_systolic', 0)
        bp_dia = patient_data.get('bp_diastolic', 0)
        
        findings = []
        
        if hr > 100:
            findings.append('Tachycardia present')
        elif hr < 60:
            findings.append('Bradycardia present')
        
        if bp_sys > 140 or bp_dia > 90:
            findings.append('Hypertensive response')
        elif bp_sys < 90 or bp_dia < 60:
            findings.append('Hypotensive response')
        
        # Calculate pulse pressure
        pulse_pressure = bp_sys - bp_dia
        if pulse_pressure > 60:
            findings.append('Wide pulse pressure')
        elif pulse_pressure < 30:
            findings.append('Narrow pulse pressure')
        
        if not findings:
            return 'Cardiovascular parameters within normal limits'
        
        return '; '.join(findings)
    
    def _assess_respiratory_pattern(self, patient_data: Dict[str, Any]) -> str:
        """
        Assess respiratory pattern for stress indicators
        """
        rr = patient_data.get('breathing_rate', 0)
        spo2 = patient_data.get('oxygen_saturation', 0)
        
        findings = []
        
        if rr > 20:
            findings.append('Tachypnea present')
        elif rr < 12:
            findings.append('Bradypnea present')
        
        if spo2 < 95:
            findings.append('Hypoxemia detected')
        elif spo2 < 97:
            findings.append('Mild oxygen desaturation')
        
        if not findings:
            return 'Respiratory parameters within normal limits'
        
        return '; '.join(findings)
    
    def _assess_metabolic_pattern(self, patient_data: Dict[str, Any]) -> str:
        """
        Assess metabolic pattern for stress indicators
        """
        temp = patient_data.get('temperature', 0)
        sleep = patient_data.get('sleep_duration', 0)
        
        findings = []
        
        if temp > 37.5:
            findings.append('Hyperthermia present')
        elif temp < 36.0:
            findings.append('Hypothermia present')
        
        if sleep < 6:
            findings.append('Sleep deprivation indicated')
        elif sleep > 10:
            findings.append('Excessive sleep duration')
        
        if not findings:
            return 'Metabolic parameters within normal limits'
        
        return '; '.join(findings)
    
    def _assess_autonomic_pattern(self, patient_data: Dict[str, Any]) -> str:
        """
        Assess autonomic nervous system pattern
        """
        hr = patient_data.get('heart_rate', 0)
        bp_sys = patient_data.get('bp_systolic', 0)
        rr = patient_data.get('breathing_rate', 0)
        
        # Calculate autonomic indicators
        sympathetic_score = 0
        parasympathetic_score = 0
        
        # Heart rate analysis
        if hr > 85:
            sympathetic_score += 1
        elif hr < 65:
            parasympathetic_score += 1
        
        # Blood pressure analysis
        if bp_sys > 125:
            sympathetic_score += 1
        elif bp_sys < 100:
            parasympathetic_score += 1
        
        # Respiratory rate analysis
        if rr > 18:
            sympathetic_score += 1
        elif rr < 14:
            parasympathetic_score += 1
        
        if sympathetic_score > parasympathetic_score:
            return 'Sympathetic dominance pattern'
        elif parasympathetic_score > sympathetic_score:
            return 'Parasympathetic dominance pattern'
        else:
            return 'Balanced autonomic pattern'
    
    def _identify_risk_factors(self, patient_data: Dict[str, Any], classification_result: Dict[str, Any]) -> List[str]:
        """
        Identify clinical risk factors
        """
        risk_factors = []
        
        # Cardiovascular risk factors
        if patient_data.get('heart_rate', 0) > 100:
            risk_factors.append('Tachycardia increases cardiovascular workload')
        
        if patient_data.get('bp_systolic', 0) > 140:
            risk_factors.append('Hypertension increases cardiovascular disease risk')
        
        # Respiratory risk factors
        if patient_data.get('oxygen_saturation', 0) < 95:
            risk_factors.append('Hypoxemia compromises tissue oxygenation')
        
        # Metabolic risk factors
        if patient_data.get('sleep_duration', 0) < 6:
            risk_factors.append('Sleep deprivation impairs immune function and increases stress hormones')
        
        # Stress-related risk factors
        if classification_result.get('stress_level') == 'High':
            risk_factors.append('Chronic high stress increases risk of cardiovascular and mental health disorders')
        
        # Environmental risk factors
        if patient_data.get('sound_level', 0) > 70:
            risk_factors.append('Elevated noise exposure contributes to stress and hearing damage')
        
        return risk_factors
    
    def _identify_protective_factors(self, patient_data: Dict[str, Any]) -> List[str]:
        """
        Identify protective factors
        """
        protective_factors = []
        
        # Cardiovascular protective factors
        if 60 <= patient_data.get('heart_rate', 0) <= 80:
            protective_factors.append('Resting heart rate within optimal range')
        
        if 90 <= patient_data.get('bp_systolic', 0) <= 115:
            protective_factors.append('Blood pressure within optimal range')
        
        # Respiratory protective factors
        if patient_data.get('oxygen_saturation', 0) >= 98:
            protective_factors.append('Excellent oxygen saturation levels')
        
        # Lifestyle protective factors
        if 7 <= patient_data.get('sleep_duration', 0) <= 9:
            protective_factors.append('Adequate sleep duration supports stress resilience')
        
        if patient_data.get('sound_level', 0) < 50:
            protective_factors.append('Quiet environment reduces stress burden')
        
        return protective_factors
    
    def _generate_personalized_recommendations(self, patient_data: Dict[str, Any], patterns: Dict[str, Any]) -> List[str]:
        """
        Generate personalized recommendations based on individual patterns
        """
        recommendations = []
        
        # Cardiovascular recommendations
        if 'Tachycardia' in patterns['cardiovascular_pattern']:
            recommendations.append('Practice deep breathing exercises 3-4 times daily to reduce heart rate')
            recommendations.append('Consider cardiac evaluation if tachycardia persists')
        
        if 'Hypertensive' in patterns['cardiovascular_pattern']:
            recommendations.append('Implement DASH diet principles to reduce blood pressure')
            recommendations.append('Regular blood pressure monitoring at home')
        
        # Respiratory recommendations
        if 'Tachypnea' in patterns['respiratory_pattern']:
            recommendations.append('Practice diaphragmatic breathing techniques')
            recommendations.append('Evaluate for underlying respiratory conditions')
        
        # Sleep recommendations
        if patient_data.get('sleep_duration', 0) < 7:
            recommendations.append('Establish consistent sleep schedule with 7-9 hours nightly')
            recommendations.append('Create optimal sleep environment (dark, cool, quiet)')
        
        # Stress management recommendations
        if 'Sympathetic dominance' in patterns['autonomic_pattern']:
            recommendations.append('Implement stress reduction techniques (meditation, yoga)')
            recommendations.append('Consider stress management counseling')
        
        return recommendations
    
    def analyze_trends(self, measurements: List[Dict]) -> Dict[str, Any]:
        """
        Analyze trends across multiple measurements
        """
        if len(measurements) < 2:
            return {
                'observed_trends': ['Insufficient data for trend analysis'],
                'predictive_indicators': ['Single measurement available'],
                'prognosis': 'Cannot determine trend with single measurement'
            }
        
        # Extract time series data
        timestamps = [m['timestamp'] for m in measurements]
        stress_levels = [m['result']['stress_level'] for m in measurements]
        heart_rates = [m['data']['heart_rate'] for m in measurements]
        bp_systolic = [m['data']['bp_systolic'] for m in measurements]
        
        # Analyze trends
        observed_trends = []
        predictive_indicators = []
        
        # Stress level trend
        stress_mapping = {'Low': 1, 'Medium': 2, 'High': 3}
        numeric_stress = [stress_mapping[level] for level in stress_levels]
        
        if len(set(numeric_stress)) > 1:
            if numeric_stress[-1] > numeric_stress[0]:
                observed_trends.append('Stress levels increasing over time')
                predictive_indicators.append('Risk of stress-related complications may increase')
            elif numeric_stress[-1] < numeric_stress[0]:
                observed_trends.append('Stress levels decreasing over time')
                predictive_indicators.append('Positive response to interventions indicated')
        else:
            observed_trends.append('Stress levels remain stable')
        
        # Heart rate trend
        hr_trend = np.polyfit(range(len(heart_rates)), heart_rates, 1)[0]
        if hr_trend > 2:
            observed_trends.append('Heart rate showing increasing trend')
            predictive_indicators.append('May require cardiovascular evaluation')
        elif hr_trend < -2:
            observed_trends.append('Heart rate showing decreasing trend')
            predictive_indicators.append('Possible improvement in cardiovascular stress')
        
        # Blood pressure trend
        bp_trend = np.polyfit(range(len(bp_systolic)), bp_systolic, 1)[0]
        if bp_trend > 3:
            observed_trends.append('Blood pressure showing increasing trend')
            predictive_indicators.append('Hypertension risk may be increasing')
        elif bp_trend < -3:
            observed_trends.append('Blood pressure showing decreasing trend')
            predictive_indicators.append('Blood pressure control improving')
        
        # Generate prognosis
        prognosis = self._generate_prognosis(observed_trends, predictive_indicators, measurements)
        
        return {
            'observed_trends': observed_trends,
            'predictive_indicators': predictive_indicators,
            'prognosis': prognosis
        }
    
    def _generate_prognosis(self, trends: List[str], indicators: List[str], measurements: List[Dict]) -> str:
        """
        Generate clinical prognosis based on trends
        """
        latest_stress = measurements[-1]['result']['stress_level']
        
        improving_keywords = ['decreasing', 'improving', 'positive']
        worsening_keywords = ['increasing', 'risk', 'complications']
        
        improving_count = sum(1 for trend in trends + indicators if any(keyword in trend.lower() for keyword in improving_keywords))
        worsening_count = sum(1 for trend in trends + indicators if any(keyword in trend.lower() for keyword in worsening_keywords))
        
        if improving_count > worsening_count:
            return f"Favorable prognosis with improving trends. Current {latest_stress.lower()} stress level with positive trajectory suggests good response to interventions."
        elif worsening_count > improving_count:
            return f"Concerning prognosis with worsening trends. Current {latest_stress.lower()} stress level with negative trajectory requires immediate attention and intervention."
        else:
            return f"Stable prognosis with mixed trends. Current {latest_stress.lower()} stress level requires continued monitoring and management."
    
    def generate_insights(self, patient_data: Dict[str, Any], classification_result: Dict[str, Any], session_measurements: List[Dict]) -> Dict[str, Any]:
        """
        Generate comprehensive medical insights
        """
        # Analyze physiological patterns
        patterns = self._analyze_physiological_patterns(patient_data)
        
        # Generate primary clinical findings
        primary_findings = []
        primary_findings.append(f"Stress level classified as {classification_result['stress_level']} with {classification_result['confidence']:.1%} confidence")
        primary_findings.append(f"Primary contributing factor: {classification_result['primary_factor']}")
        primary_findings.append(f"Medical priority: {classification_result['medical_priority']}")
        
        # Add pattern-based findings
        for pattern_type, pattern_result in patterns.items():
            if 'normal limits' not in pattern_result:
                primary_findings.append(f"{pattern_type.replace('_', ' ').title()}: {pattern_result}")
        
        # Identify risk factors
        risk_factors = self._identify_risk_factors(patient_data, classification_result)
        
        # Identify protective factors
        protective_factors = self._identify_protective_factors(patient_data)
        
        # Generate areas of concern
        concerns = []
        if classification_result['stress_level'] == 'High':
            concerns.append('High stress level poses risk for cardiovascular and mental health complications')
        
        if classification_result['risk_score'] > 0.6:
            concerns.append('Elevated risk score indicates need for immediate intervention')
        
        for risk_factor in classification_result.get('risk_factors', []):
            concerns.append(f"Medical concern: {risk_factor}")
        
        # Generate immediate actions
        immediate_actions = self._generate_immediate_actions(classification_result, patterns)
        
        # Generate management plans
        short_term_plan = self._generate_short_term_plan(patient_data, patterns)
        long_term_strategy = self._generate_long_term_strategy(patient_data, classification_result)
        monitoring_plan = self._generate_monitoring_plan(classification_result, patterns)
        
        # Generate personalized recommendations
        personalized_recommendations = self._generate_personalized_recommendations(patient_data, patterns)
        
        # Generate literature references
        literature_references = self._select_relevant_literature(patient_data, classification_result)
        
        return {
            'primary_findings': primary_findings,
            'risk_factors': risk_factors,
            'protective_factors': protective_factors,
            'concerns': concerns,
            'immediate_actions': immediate_actions,
            'short_term_plan': short_term_plan,
            'long_term_strategy': long_term_strategy,
            'monitoring_plan': monitoring_plan,
            'personalized_recommendations': personalized_recommendations,
            'literature_references': literature_references,
            'physiological_patterns': patterns
        }
    
    def _generate_immediate_actions(self, classification_result: Dict[str, Any], patterns: Dict[str, Any]) -> List[str]:
        """
        Generate immediate action recommendations
        """
        actions = []
        
        priority = classification_result['medical_priority']
        
        if priority == 'Critical':
            actions.extend(self.intervention_protocols['immediate_interventions']['critical_stress'])
        elif priority == 'High':
            actions.extend(self.intervention_protocols['immediate_interventions']['high_stress'])
        else:
            actions.extend(self.intervention_protocols['immediate_interventions']['moderate_stress'])
        
        # Add pattern-specific actions
        if 'Tachycardia' in patterns['cardiovascular_pattern']:
            actions.append('Implement immediate heart rate reduction techniques')
        
        if 'Hypoxemia' in patterns['respiratory_pattern']:
            actions.append('Assess and improve oxygenation immediately')
        
        return actions
    
    def _generate_short_term_plan(self, patient_data: Dict[str, Any], patterns: Dict[str, Any]) -> List[str]:
        """
        Generate short-term management plan
        """
        plan = []
        
        # Cardiovascular focus
        if 'Tachycardia' in patterns['cardiovascular_pattern'] or 'Hypertensive' in patterns['cardiovascular_pattern']:
            plan.extend(self.intervention_protocols['short_term_management']['cardiovascular_focus'])
        
        # Respiratory focus
        if 'Tachypnea' in patterns['respiratory_pattern'] or 'Hypoxemia' in patterns['respiratory_pattern']:
            plan.extend(self.intervention_protocols['short_term_management']['respiratory_focus'])
        
        # Sleep focus
        if patient_data.get('sleep_duration', 0) < 7:
            plan.extend(self.intervention_protocols['short_term_management']['sleep_focus'])
        
        return plan
    
    def _generate_long_term_strategy(self, patient_data: Dict[str, Any], classification_result: Dict[str, Any]) -> List[str]:
        """
        Generate long-term management strategy
        """
        strategy = []
        
        # Lifestyle modifications
        strategy.extend(self.intervention_protocols['long_term_strategies']['lifestyle_modification'])
        
        # Medical management if high risk
        if classification_result['risk_score'] > 0.4:
            strategy.extend(self.intervention_protocols['long_term_strategies']['medical_management'])
        
        return strategy
    
    def _generate_monitoring_plan(self, classification_result: Dict[str, Any], patterns: Dict[str, Any]) -> List[str]:
        """
        Generate monitoring plan recommendations
        """
        plan = []
        
        priority = classification_result['medical_priority']
        
        if priority == 'Critical':
            plan.append('Continuous vital sign monitoring')
            plan.append('Hourly stress level assessments')
        elif priority == 'High':
            plan.append('Vital signs every 2-4 hours')
            plan.append('Daily stress level assessments')
        else:
            plan.append('Daily vital sign checks')
            plan.append('Weekly stress level assessments')
        
        # Add specific monitoring based on patterns
        if 'cardiovascular_pattern' in patterns and 'normal' not in patterns['cardiovascular_pattern']:
            plan.append('Cardiac rhythm monitoring')
            plan.append('Blood pressure monitoring every 6 hours')
        
        if 'respiratory_pattern' in patterns and 'normal' not in patterns['respiratory_pattern']:
            plan.append('Oxygen saturation monitoring')
            plan.append('Respiratory rate assessment every 4 hours')
        
        return plan
    
    def _select_relevant_literature(self, patient_data: Dict[str, Any], classification_result: Dict[str, Any]) -> List[str]:
        """
        Select relevant literature references based on patient condition
        """
        references = []
        
        # Add stress physiology references
        references.extend(self.evidence_base['stress_physiology'][:2])
        
        # Add vital signs references if abnormal
        if patient_data.get('heart_rate', 0) > 100 or patient_data.get('bp_systolic', 0) > 130:
            references.extend(self.evidence_base['vital_signs_stress'][:2])
        
        # Add intervention references
        references.extend(self.evidence_base['intervention_evidence'][:2])
        
        return references
