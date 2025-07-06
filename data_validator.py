import numpy as np
import pandas as pd
from typing import Dict, List, Any, Tuple, Optional
import re
import datetime

class MedicalDataValidator:
    """
    Medical-grade data validation system for health parameters
    """
    
    def __init__(self):
        self.validation_rules = self._initialize_validation_rules()
        self.medical_ranges = self._initialize_medical_ranges()
        self.critical_thresholds = self._initialize_critical_thresholds()
        self.validation_history = []
    
    def _initialize_validation_rules(self):
        """
        Initialize comprehensive validation rules for medical parameters
        """
        return {
            'heart_rate': {
                'type': 'numeric',
                'min_value': 30,
                'max_value': 250,
                'required': True,
                'precision': 0,
                'clinical_min': 40,
                'clinical_max': 200,
                'unit': 'bpm'
            },

            'bp_systolic': {
                'type': 'numeric',
                'min_value': 60,
                'max_value': 300,
                'required': True,
                'precision': 0,
                'clinical_min': 80,
                'clinical_max': 250,
                'unit': 'mmHg'
            },
            'bp_diastolic': {
                'type': 'numeric',
                'min_value': 30,
                'max_value': 200,
                'required': True,
                'precision': 0,
                'clinical_min': 40,
                'clinical_max': 150,
                'unit': 'mmHg'
            },

            'sleep_duration': {
                'type': 'numeric',
                'min_value': 0.0,
                'max_value': 24.0,
                'required': True,
                'precision': 1,
                'clinical_min': 2.0,
                'clinical_max': 15.0,
                'unit': 'hours'
            },

            'stress_symptoms': {
                'type': 'list',
                'allowed_values': [
                    'Headache', 'Muscle Tension', 'Fatigue', 'Irritability',
                    'Difficulty Concentrating', 'Sleep Issues', 'Anxiety',
                    'Rapid Heartbeat', 'Sweating', 'Digestive Issues'
                ],
                'required': False,
                'max_items': 10
            },

        }
    
    def _initialize_medical_ranges(self):
        """
        Initialize medical reference ranges for validation
        """
        return {
            'heart_rate': {
                'normal': (60, 100),
                'bradycardia': (40, 60),
                'tachycardia': (100, 180),
                'severe_bradycardia': (0, 40),
                'severe_tachycardia': (180, 250)
            },
            'bp_systolic': {
                'normal': (90, 120),
                'hypotension': (80, 90),
                'elevated': (120, 130),
                'hypertension_stage1': (130, 140),
                'hypertension_stage2': (140, 180),
                'hypertensive_crisis': (180, 250)
            },
            'bp_diastolic': {
                'normal': (60, 80),
                'hypotension': (40, 60),
                'elevated': (80, 85),
                'hypertension_stage1': (85, 90),
                'hypertension_stage2': (90, 120),
                'hypertensive_crisis': (120, 150)
            },

            'sleep_duration': {
                'normal': (7, 9),
                'short_sleep': (6, 7),
                'very_short_sleep': (4, 6),
                'sleep_deprivation': (0, 4),
                'long_sleep': (9, 11),
                'excessive_sleep': (11, 15)
            }
        }
    
    def _initialize_critical_thresholds(self):
        """
        Initialize critical threshold values requiring immediate attention
        """
        return {
            'heart_rate': {
                'critical_low': 40,
                'critical_high': 150,
                'emergency_low': 30,
                'emergency_high': 180
            },
            'bp_systolic': {
                'critical_low': 80,
                'critical_high': 180,
                'emergency_low': 70,
                'emergency_high': 220
            },
            'bp_diastolic': {
                'critical_low': 40,
                'critical_high': 120,
                'emergency_low': 30,
                'emergency_high': 140
            },

        }
    
    def _validate_numeric_parameter(self, parameter: str, value: Any) -> Tuple[bool, List[str]]:
        """
        Validate numeric medical parameter
        """
        errors = []
        
        if parameter not in self.validation_rules:
            errors.append(f"Unknown parameter: {parameter}")
            return False, errors
        
        rules = self.validation_rules[parameter]
        
        # Check if value is provided when required
        if rules['required'] and (value is None or value == ''):
            errors.append(f"{parameter} is required")
            return False, errors
        
        # Skip validation if not required and empty
        if not rules['required'] and (value is None or value == ''):
            return True, []
        
        # Convert to numeric
        try:
            numeric_value = float(value)
        except (ValueError, TypeError):
            errors.append(f"{parameter} must be a valid number")
            return False, errors
        
        # Check for NaN or infinite values
        if np.isnan(numeric_value) or np.isinf(numeric_value):
            errors.append(f"{parameter} contains invalid numeric value")
            return False, errors
        
        # Check absolute bounds
        if numeric_value < rules['min_value']:
            errors.append(f"{parameter} ({numeric_value}) is below minimum allowed value ({rules['min_value']})")
        
        if numeric_value > rules['max_value']:
            errors.append(f"{parameter} ({numeric_value}) is above maximum allowed value ({rules['max_value']})")
        
        # Check clinical bounds with warnings
        if numeric_value < rules['clinical_min']:
            errors.append(f"{parameter} ({numeric_value}) is below clinical minimum ({rules['clinical_min']})")
        
        if numeric_value > rules['clinical_max']:
            errors.append(f"{parameter} ({numeric_value}) is above clinical maximum ({rules['clinical_max']})")
        
        # Check precision
        if rules['precision'] == 0:
            if numeric_value != int(numeric_value):
                errors.append(f"{parameter} should be a whole number")
        else:
            decimal_places = len(str(numeric_value).split('.')[-1]) if '.' in str(numeric_value) else 0
            if decimal_places > rules['precision']:
                errors.append(f"{parameter} has too many decimal places (max {rules['precision']})")
        
        return len(errors) == 0, errors
    
    def _validate_categorical_parameter(self, parameter: str, value: Any) -> Tuple[bool, List[str]]:
        """
        Validate categorical medical parameter
        """
        errors = []
        
        if parameter not in self.validation_rules:
            errors.append(f"Unknown parameter: {parameter}")
            return False, errors
        
        rules = self.validation_rules[parameter]
        
        # Check if value is provided when required
        if rules['required'] and (value is None or value == ''):
            errors.append(f"{parameter} is required")
            return False, errors
        
        # Skip validation if not required and empty
        if not rules['required'] and (value is None or value == ''):
            return True, []
        
        # Check if value is in allowed values
        if value not in rules['allowed_values']:
            errors.append(f"{parameter} must be one of: {', '.join(rules['allowed_values'])}")
            return False, errors
        
        return True, []
    
    def _validate_list_parameter(self, parameter: str, value: Any) -> Tuple[bool, List[str]]:
        """
        Validate list-type medical parameter
        """
        errors = []
        
        if parameter not in self.validation_rules:
            errors.append(f"Unknown parameter: {parameter}")
            return False, errors
        
        rules = self.validation_rules[parameter]
        
        # Check if value is provided when required
        if rules['required'] and (value is None or len(value) == 0):
            errors.append(f"{parameter} is required")
            return False, errors
        
        # Skip validation if not required and empty
        if not rules['required'] and (value is None or len(value) == 0):
            return True, []
        
        # Ensure value is a list
        if not isinstance(value, list):
            errors.append(f"{parameter} must be a list")
            return False, errors
        
        # Check maximum number of items
        if 'max_items' in rules and len(value) > rules['max_items']:
            errors.append(f"{parameter} cannot have more than {rules['max_items']} items")
        
        # Check if all items are in allowed values
        if 'allowed_values' in rules:
            for item in value:
                if item not in rules['allowed_values']:
                    errors.append(f"{parameter} contains invalid item: {item}")
        
        return len(errors) == 0, errors
    
    def _validate_text_parameter(self, parameter: str, value: Any) -> Tuple[bool, List[str]]:
        """
        Validate text-type medical parameter
        """
        errors = []
        
        if parameter not in self.validation_rules:
            errors.append(f"Unknown parameter: {parameter}")
            return False, errors
        
        rules = self.validation_rules[parameter]
        
        # Check if value is provided when required
        if rules['required'] and (value is None or value == ''):
            errors.append(f"{parameter} is required")
            return False, errors
        
        # Skip validation if not required and empty (but allowed)
        if not rules['required'] and (value is None or value == '') and rules.get('allow_empty', False):
            return True, []
        
        # Convert to string
        if value is not None:
            str_value = str(value)
        else:
            str_value = ''
        
        # Check maximum length
        if 'max_length' in rules and len(str_value) > rules['max_length']:
            errors.append(f"{parameter} exceeds maximum length of {rules['max_length']} characters")
        
        # Basic sanitization check
        if self._contains_suspicious_content(str_value):
            errors.append(f"{parameter} contains potentially harmful content")
        
        return len(errors) == 0, errors
    
    def _contains_suspicious_content(self, text: str) -> bool:
        """
        Check for suspicious content in text fields
        """
        # Basic patterns to check for potential injection attempts
        suspicious_patterns = [
            r'<script.*?>.*?</script>',  # JavaScript
            r'javascript:',             # JavaScript URLs
            r'on\w+\s*=',              # Event handlers
            r'<iframe.*?>',            # Iframes
            r'<object.*?>',            # Objects
            r'<embed.*?>',             # Embeds
            r'data:text/html',         # Data URLs
            r'vbscript:',              # VBScript
        ]
        
        text_lower = text.lower()
        
        for pattern in suspicious_patterns:
            if re.search(pattern, text_lower):
                return True
        
        return False
    
    def _check_parameter_relationships(self, parameters: Dict[str, Any]) -> List[str]:
        """
        Check relationships between parameters for medical consistency
        """
        warnings = []
        
        # Blood pressure consistency
        if 'bp_systolic' in parameters and 'bp_diastolic' in parameters:
            systolic = parameters['bp_systolic']
            diastolic = parameters['bp_diastolic']
            
            if systolic <= diastolic:
                warnings.append("Systolic blood pressure should be higher than diastolic blood pressure")
            
            pulse_pressure = systolic - diastolic
            if pulse_pressure < 20:
                warnings.append("Pulse pressure is unusually narrow (may indicate cardiac issues)")
            elif pulse_pressure > 80:
                warnings.append("Pulse pressure is unusually wide (may indicate arterial stiffness)")
        
        # Heart rate and blood pressure relationship
        if 'heart_rate' in parameters and 'bp_systolic' in parameters:
            hr = parameters['heart_rate']
            bp = parameters['bp_systolic']
            
            if hr > 100 and bp < 90:
                warnings.append("High heart rate with low blood pressure may indicate shock or dehydration")
            elif hr < 60 and bp > 140:
                warnings.append("Low heart rate with high blood pressure may indicate medication effects")
        
        # Temperature and heart rate relationship
        if 'temperature' in parameters and 'heart_rate' in parameters:
            temp = parameters['temperature']
            hr = parameters['heart_rate']
            
            if temp > 37.5 and hr < 60:
                warnings.append("Fever with low heart rate may indicate serious infection")
            elif temp < 36.0 and hr > 100:
                warnings.append("Hypothermia with high heart rate may indicate metabolic stress")
        
        # Oxygen saturation and breathing rate
        if 'oxygen_saturation' in parameters and 'breathing_rate' in parameters:
            spo2 = parameters['oxygen_saturation']
            rr = parameters['breathing_rate']
            
            if spo2 < 95 and rr < 12:
                warnings.append("Low oxygen saturation with slow breathing may indicate respiratory depression")
            elif spo2 > 98 and rr > 25:
                warnings.append("Normal oxygen saturation with rapid breathing may indicate anxiety or metabolic issues")
        
        # Sleep and symptoms relationship
        if 'sleep_duration' in parameters and 'stress_symptoms' in parameters:
            sleep = parameters['sleep_duration']
            symptoms = parameters['stress_symptoms']
            
            if sleep < 6 and 'Sleep Issues' not in symptoms:
                warnings.append("Short sleep duration but no sleep issues reported - consider sleep quality assessment")
            elif sleep > 9 and 'Fatigue' in symptoms:
                warnings.append("Long sleep duration with fatigue may indicate sleep disorder")
        
        return warnings
    
    def _assess_critical_status(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess critical status of parameters
        """
        critical_findings = {
            'critical_parameters': [],
            'emergency_parameters': [],
            'warning_parameters': [],
            'overall_status': 'normal'
        }
        
        for param, value in parameters.items():
            if param in self.critical_thresholds and value is not None:
                try:
                    numeric_value = float(value)
                    thresholds = self.critical_thresholds[param]
                    
                    # Check emergency thresholds
                    if (numeric_value <= thresholds['emergency_low'] or 
                        numeric_value >= thresholds['emergency_high']):
                        critical_findings['emergency_parameters'].append({
                            'parameter': param,
                            'value': numeric_value,
                            'status': 'emergency',
                            'message': f'{param} at emergency level: {numeric_value}'
                        })
                        critical_findings['overall_status'] = 'emergency'
                    
                    # Check critical thresholds
                    elif (numeric_value <= thresholds['critical_low'] or 
                          numeric_value >= thresholds['critical_high']):
                        critical_findings['critical_parameters'].append({
                            'parameter': param,
                            'value': numeric_value,
                            'status': 'critical',
                            'message': f'{param} at critical level: {numeric_value}'
                        })
                        if critical_findings['overall_status'] != 'emergency':
                            critical_findings['overall_status'] = 'critical'
                    
                    # Check warning ranges
                    elif param in self.medical_ranges:
                        ranges = self.medical_ranges[param]
                        normal_range = ranges.get('normal', (0, 100))
                        
                        if not (normal_range[0] <= numeric_value <= normal_range[1]):
                            critical_findings['warning_parameters'].append({
                                'parameter': param,
                                'value': numeric_value,
                                'status': 'warning',
                                'message': f'{param} outside normal range: {numeric_value}'
                            })
                            if critical_findings['overall_status'] == 'normal':
                                critical_findings['overall_status'] = 'warning'
                
                except (ValueError, TypeError):
                    continue
        
        return critical_findings
    
    def validate_parameter(self, parameter: str, value: Any) -> Dict[str, Any]:
        """
        Validate a single medical parameter
        """
        if parameter not in self.validation_rules:
            return {
                'valid': False,
                'errors': [f"Unknown parameter: {parameter}"],
                'warnings': [],
                'parameter': parameter,
                'value': value
            }
        
        rules = self.validation_rules[parameter]
        param_type = rules['type']
        
        # Validate based on type
        if param_type == 'numeric':
            valid, errors = self._validate_numeric_parameter(parameter, value)
        elif param_type == 'categorical':
            valid, errors = self._validate_categorical_parameter(parameter, value)
        elif param_type == 'list':
            valid, errors = self._validate_list_parameter(parameter, value)
        elif param_type == 'text':
            valid, errors = self._validate_text_parameter(parameter, value)
        else:
            valid, errors = False, [f"Unknown parameter type: {param_type}"]
        
        # Generate warnings for edge cases
        warnings = []
        if valid and param_type == 'numeric' and value is not None:
            try:
                numeric_value = float(value)
                if parameter in self.medical_ranges:
                    ranges = self.medical_ranges[parameter]
                    normal_range = ranges.get('normal', (0, 100))
                    
                    if not (normal_range[0] <= numeric_value <= normal_range[1]):
                        warnings.append(f"{parameter} is outside normal range ({normal_range[0]}-{normal_range[1]})")
            except (ValueError, TypeError):
                pass
        
        return {
            'valid': valid,
            'errors': errors,
            'warnings': warnings,
            'parameter': parameter,
            'value': value,
            'expected_type': param_type,
            'rules': rules
        }
    
    def validate_parameters(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate multiple medical parameters
        """
        validation_results = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'parameter_results': {},
            'critical_assessment': {},
            'relationship_warnings': [],
            'timestamp': datetime.datetime.now()
        }
        
        # Validate each parameter
        for param, value in parameters.items():
            result = self.validate_parameter(param, value)
            validation_results['parameter_results'][param] = result
            
            if not result['valid']:
                validation_results['valid'] = False
                validation_results['errors'].extend([f"{param}: {error}" for error in result['errors']])
            
            validation_results['warnings'].extend([f"{param}: {warning}" for warning in result['warnings']])
        
        # Check parameter relationships
        if validation_results['valid']:
            relationship_warnings = self._check_parameter_relationships(parameters)
            validation_results['relationship_warnings'] = relationship_warnings
            validation_results['warnings'].extend(relationship_warnings)
        
        # Assess critical status
        critical_assessment = self._assess_critical_status(parameters)
        validation_results['critical_assessment'] = critical_assessment
        
        # Add critical findings to errors if emergency level
        if critical_assessment['overall_status'] == 'emergency':
            validation_results['valid'] = False
            for finding in critical_assessment['emergency_parameters']:
                validation_results['errors'].append(f"EMERGENCY: {finding['message']}")
        
        # Add critical findings to warnings
        for finding in critical_assessment['critical_parameters']:
            validation_results['warnings'].append(f"CRITICAL: {finding['message']}")
        
        # Store validation history
        self.validation_history.append({
            'timestamp': validation_results['timestamp'],
            'parameters': parameters,
            'result': validation_results
        })
        
        # Limit history size
        if len(self.validation_history) > 100:
            self.validation_history = self.validation_history[-100:]
        
        return validation_results
    
    def get_parameter_info(self, parameter: str) -> Dict[str, Any]:
        """
        Get detailed information about a parameter
        """
        if parameter not in self.validation_rules:
            return {'error': f"Unknown parameter: {parameter}"}
        
        rules = self.validation_rules[parameter]
        info = {
            'parameter': parameter,
            'type': rules['type'],
            'required': rules['required'],
            'validation_rules': rules
        }
        
        # Add medical ranges if available
        if parameter in self.medical_ranges:
            info['medical_ranges'] = self.medical_ranges[parameter]
        
        # Add critical thresholds if available
        if parameter in self.critical_thresholds:
            info['critical_thresholds'] = self.critical_thresholds[parameter]
        
        return info
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """
        Get summary of validation system
        """
        return {
            'total_parameters': len(self.validation_rules),
            'required_parameters': sum(1 for rule in self.validation_rules.values() if rule['required']),
            'optional_parameters': sum(1 for rule in self.validation_rules.values() if not rule['required']),
            'parameter_types': {
                'numeric': sum(1 for rule in self.validation_rules.values() if rule['type'] == 'numeric'),
                'categorical': sum(1 for rule in self.validation_rules.values() if rule['type'] == 'categorical'),
                'list': sum(1 for rule in self.validation_rules.values() if rule['type'] == 'list'),
                'text': sum(1 for rule in self.validation_rules.values() if rule['type'] == 'text')
            },
            'validation_history_count': len(self.validation_history),
            'supported_parameters': list(self.validation_rules.keys())
        }
    
    def clear_validation_history(self):
        """
        Clear validation history
        """
        self.validation_history = []
    
    def export_validation_rules(self) -> Dict[str, Any]:
        """
        Export validation rules for external use
        """
        return {
            'validation_rules': self.validation_rules,
            'medical_ranges': self.medical_ranges,
            'critical_thresholds': self.critical_thresholds,
            'export_timestamp': datetime.datetime.now().isoformat()
        }
