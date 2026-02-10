"""
Training Analysis Module
Analyzes athlete training data and provides immediate feedback
"""
from datetime import datetime, timedelta
import gpxpy
import numpy as np


class TrainingAnalyzer:
    """Analyze training data and provide insights"""
    
    def __init__(self):
        self.thresholds = {
            'easy': {'max_hr_pct': 70, 'pace_factor': 1.3},
            'moderate': {'max_hr_pct': 80, 'pace_factor': 1.15},
            'hard': {'max_hr_pct': 90, 'pace_factor': 1.0},
            'intense': {'max_hr_pct': 95, 'pace_factor': 0.9}
        }
    
    def parse_gpx_training(self, gpx_file_path):
        """
        Parse GPX file and extract training data
        
        Args:
            gpx_file_path: Path to GPX file
        
        Returns:
            Dictionary with training metrics
        """
        with open(gpx_file_path, 'r') as gpx_file:
            gpx = gpxpy.parse(gpx_file)
        
        # Extract data from all tracks and segments
        points_data = []
        total_distance = 0
        total_elevation_gain = 0
        total_elevation_loss = 0
        
        prev_point = None
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    if prev_point:
                        # Calculate distance
                        distance = self._calculate_distance(
                            (prev_point.latitude, prev_point.longitude),
                            (point.latitude, point.longitude)
                        )
                        total_distance += distance
                        
                        # Calculate elevation change
                        if prev_point.elevation and point.elevation:
                            elev_change = point.elevation - prev_point.elevation
                            if elev_change > 0:
                                total_elevation_gain += elev_change
                            else:
                                total_elevation_loss += abs(elev_change)
                    
                    points_data.append({
                        'lat': point.latitude,
                        'lon': point.longitude,
                        'elevation': point.elevation,
                        'time': point.time
                    })
                    prev_point = point
        
        # Calculate duration
        if points_data and len(points_data) > 1:
            start_time = points_data[0]['time']
            end_time = points_data[-1]['time']
            if start_time and end_time:
                duration = (end_time - start_time).total_seconds() / 3600  # hours
            else:
                duration = 1.0  # default
        else:
            duration = 1.0
        
        return {
            'total_distance': total_distance / 1000,  # Convert to km
            'total_elevation_gain': total_elevation_gain,
            'total_elevation_loss': total_elevation_loss,
            'duration': duration,
            'num_points': len(points_data),
            'points': points_data
        }
    
    def _calculate_distance(self, point1, point2):
        """Calculate distance between two points in meters using Haversine formula"""
        lat1, lon1 = point1
        lat2, lon2 = point2
        
        R = 6371000  # Earth radius in meters
        phi1 = np.radians(lat1)
        phi2 = np.radians(lat2)
        delta_phi = np.radians(lat2 - lat1)
        delta_lambda = np.radians(lon2 - lon1)
        
        a = np.sin(delta_phi/2)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda/2)**2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
        
        return R * c
    
    def analyze_training_session(self, training_data, athlete_max_hr=None):
        """
        Analyze a training session and provide feedback
        
        Args:
            training_data: Dict from parse_gpx_training()
            athlete_max_hr: Athlete's maximum heart rate (optional)
        
        Returns:
            Dictionary with analysis and recommendations
        """
        distance = training_data['total_distance']
        duration = training_data['duration']
        elevation_gain = training_data['total_elevation_gain']
        
        # Calculate metrics
        avg_speed = distance / duration if duration > 0 else 0
        avg_pace = duration / distance * 60 if distance > 0 else 0  # min/km
        
        # Estimate intensity based on speed and elevation
        elevation_factor = 1 + (elevation_gain / distance / 100) if distance > 0 else 1
        
        # Classify training intensity
        if avg_speed < 15:
            intensity = 'easy'
        elif avg_speed < 20:
            intensity = 'moderate'
        elif avg_speed < 25:
            intensity = 'hard'
        else:
            intensity = 'intense'
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            intensity, distance, duration, elevation_gain
        )
        
        # Calculate training load score (TSS-like metric)
        training_load = self._calculate_training_load(
            duration, distance, elevation_gain, intensity
        )
        
        analysis = {
            'distance_km': round(distance, 2),
            'duration_hours': round(duration, 2),
            'avg_speed_kmh': round(avg_speed, 2),
            'avg_pace_min_per_km': round(avg_pace, 2),
            'elevation_gain_m': round(elevation_gain, 2),
            'intensity': intensity,
            'training_load': round(training_load, 1),
            'recommendations': recommendations
        }
        
        return analysis
    
    def _calculate_training_load(self, duration, distance, elevation, intensity):
        """Calculate training load score"""
        intensity_factors = {
            'easy': 0.5,
            'moderate': 0.7,
            'hard': 0.9,
            'intense': 1.0
        }
        
        base_load = duration * 60 * intensity_factors.get(intensity, 0.7)
        elevation_load = elevation / 10
        distance_load = distance * 2
        
        return base_load + elevation_load + distance_load
    
    def _generate_recommendations(self, intensity, distance, duration, elevation):
        """Generate training recommendations"""
        recommendations = []
        
        # Distance-based recommendations
        if distance < 20:
            recommendations.append("Consider gradually increasing your distance for better endurance")
        elif distance > 100:
            recommendations.append("Great long ride! Make sure to include recovery days")
        
        # Intensity recommendations
        if intensity == 'easy':
            recommendations.append("Good recovery pace. Perfect for building base fitness")
        elif intensity == 'intense':
            recommendations.append("High intensity session. Ensure adequate recovery before next hard effort")
        
        # Elevation recommendations
        if elevation > 1000:
            recommendations.append("Significant climbing! Excellent for building strength")
        elif elevation < 100 and distance > 30:
            recommendations.append("Consider adding some hills for varied training stimulus")
        
        # Duration recommendations
        if duration > 4:
            recommendations.append("Long endurance ride completed. Focus on nutrition and hydration recovery")
        
        return recommendations
    
    def compare_trainings(self, training_list):
        """
        Compare multiple training sessions
        
        Args:
            training_list: List of training analysis dicts
        
        Returns:
            Comparison statistics
        """
        if not training_list:
            return {}
        
        distances = [t['distance_km'] for t in training_list]
        durations = [t['duration_hours'] for t in training_list]
        speeds = [t['avg_speed_kmh'] for t in training_list]
        loads = [t['training_load'] for t in training_list]
        
        return {
            'avg_distance': round(np.mean(distances), 2),
            'avg_duration': round(np.mean(durations), 2),
            'avg_speed': round(np.mean(speeds), 2),
            'total_training_load': round(sum(loads), 1),
            'max_distance': round(max(distances), 2),
            'improvement_trend': 'increasing' if len(speeds) > 1 and speeds[-1] > speeds[0] else 'stable'
        }
