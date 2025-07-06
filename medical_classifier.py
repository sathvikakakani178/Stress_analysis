import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import os

class MedicalStressClassifier:
    """
    Medical-grade three-tier stress classification system
    """
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        self.feature_importance = {}
        self.medical_weights = self._initialize_medical_weights()
        
        # Initialize with a pre-trained model simulation
        self._initialize_model()
    
    def _initialize_medical_weights(self):
        """
        Initialize medical parameter weights based on clinical significance
        """
        return {
            'heart_rate': 0.35,      # High clinical significance
            'bp_systolic': 0.25,     # High clinical significance
            'bp_diastolic': 0.20,    # High clinical significance
            'sleep_duration': 0.15,  # Moderate clinical significance
            'stress_symptoms': 0.05  # Behavioral indicator
        }
    
    def _initialize_model(self):
        """
        Initialize the classification model with medical-grade parameters
        """
        # Create a sophisticated RandomForest model
        self.model = RandomForestClassifier(
            n_estimators=200,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            max_features='sqrt',
            bootstrap=True,
            random_state=42,
            class_weight='balanced'
        )
        
        # Simulate training data for the model
        self._simulate_training()
        self.is_trained = True
    
    def _simulate_training(self):
        """
        Simulate model training with medical-grade synthetic data
        """
        # Generate realistic medical training data
        np.random.seed(42)
        n_samples = 5000
        
        # Generate features with medical correlations
        data = []
        labels = []
        
        for i in range(n_samples):
            # Generate correlated medical parameters
            if i < n_samples // 3:  # Low stress
                heart_rate = np.random.normal(72, 8)
                bp_systolic = np.random.normal(115, 10)
                bp_diastolic = np.random.normal(75, 8)
                sleep_duration = np.random.normal(8, 1)
                symptoms_count = np.random.poisson(0.5)  # Few symptoms
                label = 0  # Low stress
                
            elif i < 2 * n_samples // 3:  # Medium stress
                heart_rate = np.random.normal(85, 10)
                bp_systolic = np.random.normal(130, 12)
                bp_diastolic = np.random.normal(85, 10)
                sleep_duration = np.random.normal(6, 1.5)
                symptoms_count = np.random.poisson(2)  # Moderate symptoms
                label = 1  # Medium stress
                
            else:  # High stress
                heart_rate = np.random.normal(105, 15)
                bp_systolic = np.random.normal(145, 15)
                bp_diastolic = np.random.normal(95, 12)
                sleep_duration = np.random.normal(4, 1.5)
                symptoms_count = np.random.poisson(4)  # Many symptoms
                label = 2  # High stress
            
            # Ensure medical bounds
            heart_rate = np.clip(heart_rate, 50, 180)
            bp_systolic = np.clip(bp_systolic, 90, 200)
            bp_diastolic = np.clip(bp_diastolic, 60, 120)
            sleep_duration = np.clip(sleep_duration, 2, 12)
            symptoms_count = np.clip(symptoms_count, 0, 7)
            
            data.append([
                heart_rate, bp_systolic, bp_diastolic, sleep_duration, symptoms_count
            ])
            labels.append(label)
        
        # Convert to arrays
        X = np.array(data)
        y = np.array(labels)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train the model
        self.model.fit(X_scaled, y)
        
        # Calculate feature importance
        feature_names = [
            'heart_rate', 'bp_systolic', 'bp_diastolic', 'sleep_duration', 'symptoms_count'
        ]
        
        self.feature_importance = dict(zip(feature_names, self.model.feature_importances_))
    
    def _prepare_features(self, patient_data):
        """
        Prepare features from patient data for classification
        """
        # Extract numerical features
        symptoms_count = len(patient_data.get('stress_symptoms', []))
        
        features = [
            patient_data['heart_rate'],
            patient_data['bp_systolic'],
            patient_data['bp_diastolic'],
            patient_data['sleep_duration'],
            symptoms_count
        ]
        
        return np.array(features).reshape(1, -1)
    
    def _calculate_medical_risk_score(self, patient_data):
        """
        Calculate medical risk score based on parameter deviations
        """
        risk_score = 0
        risk_factors = []
        
        # Heart rate assessment
        hr = patient_data['heart_rate']
        if hr > 100:
            risk_score += 0.3
            risk_factors.append('Tachycardia detected')
        elif hr < 60:
            risk_score += 0.2
            risk_factors.append('Bradycardia detected')
        
        # Blood pressure assessment
        bp_sys = patient_data['bp_systolic']
        bp_dia = patient_data['bp_diastolic']
        
        if bp_sys > 140 or bp_dia > 90:
            risk_score += 0.4
            risk_factors.append('Hypertension indicated')
        elif bp_sys < 90 or bp_dia < 60:
            risk_score += 0.3
            risk_factors.append('Hypotension indicated')
        

        
        # Sleep duration assessment
        sleep = patient_data['sleep_duration']
        if sleep < 6:
            risk_score += 0.15
            risk_factors.append('Sleep deprivation indicated')
        elif sleep > 10:
            risk_score += 0.1
            risk_factors.append('Excessive sleep duration')
        
        # Symptom assessment
        if 'stress_symptoms' in patient_data:
            symptom_count = len(patient_data['stress_symptoms'])
            risk_score += symptom_count * 0.1
            if symptom_count > 0:
                risk_factors.append(f'{symptom_count} stress symptoms reported')
        
        return min(risk_score, 1.0), risk_factors
    
    def _determine_medical_priority(self, stress_level, risk_score):
        """
        Determine medical priority based on stress level and risk factors
        """
        if stress_level == 'High' and risk_score > 0.7:
            return 'Critical'
        elif stress_level == 'High' or risk_score > 0.5:
            return 'High'
        elif stress_level == 'Medium' or risk_score > 0.3:
            return 'Medium'
        else:
            return 'Low'
    
    def _get_action_required(self, medical_priority, risk_factors):
        """
        Determine required actions based on medical priority
        """
        if medical_priority == 'Critical':
            return 'Immediate medical attention required'
        elif medical_priority == 'High':
            return 'Urgent medical consultation recommended'
        elif medical_priority == 'Medium':
            return 'Medical follow-up advised'
        else:
            return 'Continue monitoring'
    
    def _identify_primary_factor(self, patient_data, feature_importance):
        """
        Identify the primary contributing factor to stress
        """
        # Calculate weighted contributions
        contributions = {}
        
        # Heart rate contribution
        hr_deviation = abs(patient_data['heart_rate'] - 72) / 72
        contributions['Heart Rate'] = hr_deviation * feature_importance.get('heart_rate', 0)
        
        # Blood pressure contribution
        bp_deviation = abs(patient_data['bp_systolic'] - 115) / 115
        contributions['Blood Pressure'] = bp_deviation * feature_importance.get('bp_systolic', 0)
        
        # Sleep duration contribution
        sleep_deviation = abs(patient_data['sleep_duration'] - 8) / 8
        contributions['Sleep Duration'] = sleep_deviation * feature_importance.get('sleep_duration', 0)
        
        # Stress symptoms contribution
        symptoms_count = len(patient_data.get('stress_symptoms', []))
        contributions['Stress Symptoms'] = symptoms_count * feature_importance.get('symptoms_count', 0)
        
        # Return the factor with highest contribution
        return max(contributions, key=contributions.get)
    
    def classify_stress_level(self, patient_data):
        """
        Classify stress level using medical-grade analysis
        """
        if not self.is_trained:
            raise ValueError("Model not trained. Please train the model first.")
        
        # Prepare features
        features = self._prepare_features(patient_data)
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Get prediction and probability
        prediction = self.model.predict(features_scaled)[0]
        probabilities = self.model.predict_proba(features_scaled)[0]
        
        # Map prediction to stress level
        stress_levels = {0: 'Low', 1: 'Medium', 2: 'High'}
        stress_level = stress_levels[prediction]
        
        # Calculate confidence
        confidence = probabilities[prediction]
        
        # Calculate medical risk score
        risk_score, risk_factors = self._calculate_medical_risk_score(patient_data)
        
        # Determine medical priority
        medical_priority = self._determine_medical_priority(stress_level, risk_score)
        
        # Determine required actions
        action_required = self._get_action_required(medical_priority, risk_factors)
        
        # Identify primary contributing factor
        primary_factor = self._identify_primary_factor(patient_data, self.feature_importance)
        
        # Determine risk category
        if risk_score > 0.7:
            risk_category = 'High Risk'
        elif risk_score > 0.4:
            risk_category = 'Moderate Risk'
        else:
            risk_category = 'Low Risk'
        
        return {
            'stress_level': stress_level,
            'confidence': confidence,
            'probabilities': {
                'Low': probabilities[0],
                'Medium': probabilities[1],
                'High': probabilities[2]
            },
            'risk_score': risk_score,
            'risk_factors': risk_factors,
            'risk_category': risk_category,
            'medical_priority': medical_priority,
            'action_required': action_required,
            'primary_factor': primary_factor,
            'feature_importance': self.feature_importance
        }
    
    def get_model_info(self):
        """
        Get information about the trained model
        """
        return {
            'model_type': 'Random Forest Classifier',
            'is_trained': self.is_trained,
            'feature_importance': self.feature_importance,
            'medical_weights': self.medical_weights,
            'classes': ['Low Stress', 'Medium Stress', 'High Stress']
        }
