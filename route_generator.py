"""
GPX Route Generator Module
Creates optimized GPX files for cycling routes based on athlete requirements
"""
import gpxpy
import gpxpy.gpx
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import random
import math


class RouteGenerator:
    """Generate cycling routes based on athlete requirements"""
    
    def __init__(self):
        self.geolocator = Nominatim(user_agent="maptraining")
        
    def geocode_location(self, location_str):
        """Convert location string to coordinates"""
        try:
            location = self.geolocator.geocode(location_str)
            if location:
                return (location.latitude, location.longitude)
            return None
        except Exception as e:
            print(f"Geocoding error: {e}")
            return None
    
    def generate_circular_route(self, start_coords, distance_km, difficulty='medium'):
        """
        Generate a circular route from start point
        
        Args:
            start_coords: Tuple of (latitude, longitude)
            distance_km: Total distance in kilometers
            difficulty: Route difficulty ('easy', 'medium', 'hard')
        
        Returns:
            List of coordinate tuples
        """
        route_points = [start_coords]
        current_point = start_coords
        remaining_distance = distance_km
        
        # Calculate number of segments (more segments = smoother route)
        num_segments = max(8, int(distance_km / 2))
        segment_distance = distance_km / num_segments
        
        # Generate route in a circular pattern with some randomness
        for i in range(num_segments - 1):
            # Calculate angle for circular route
            angle = (2 * math.pi * i / num_segments) + random.uniform(-0.3, 0.3)
            
            # Add elevation variation based on difficulty
            elevation_factor = {'easy': 0.5, 'medium': 1.0, 'hard': 1.5}.get(difficulty, 1.0)
            
            # Calculate next point
            bearing = math.degrees(angle)
            next_point = self._calculate_destination(current_point, bearing, segment_distance)
            route_points.append(next_point)
            current_point = next_point
        
        # Add final point back to start
        route_points.append(start_coords)
        
        return route_points
    
    def _calculate_destination(self, start_point, bearing, distance_km):
        """Calculate destination point given start point, bearing and distance"""
        lat1 = math.radians(start_point[0])
        lon1 = math.radians(start_point[1])
        bearing_rad = math.radians(bearing)
        
        # Earth radius in km
        R = 6371.0
        
        lat2 = math.asin(
            math.sin(lat1) * math.cos(distance_km / R) +
            math.cos(lat1) * math.sin(distance_km / R) * math.cos(bearing_rad)
        )
        
        lon2 = lon1 + math.atan2(
            math.sin(bearing_rad) * math.sin(distance_km / R) * math.cos(lat1),
            math.cos(distance_km / R) - math.sin(lat1) * math.sin(lat2)
        )
        
        return (math.degrees(lat2), math.degrees(lon2))
    
    def create_gpx_file(self, route_points, filename, athlete_name='Athlete', route_name='Training Route'):
        """
        Create GPX file from route points
        
        Args:
            route_points: List of (latitude, longitude) tuples
            filename: Output filename
            athlete_name: Name of the athlete
            route_name: Name of the route
        """
        # Create GPX object
        gpx = gpxpy.gpx.GPX()
        
        # Set metadata
        gpx.name = route_name
        gpx.description = f'Optimized training route for {athlete_name}'
        gpx.author_name = 'Maptraining'
        
        # Create track
        gpx_track = gpxpy.gpx.GPXTrack()
        gpx_track.name = route_name
        gpx.tracks.append(gpx_track)
        
        # Create segment
        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)
        
        # Add points to segment
        base_time = datetime.now()
        for i, (lat, lon) in enumerate(route_points):
            # Estimate time based on 20 km/h average speed
            time_offset = timedelta(hours=(i * 0.5 / 20))
            point = gpxpy.gpx.GPXTrackPoint(
                latitude=lat,
                longitude=lon,
                time=base_time + time_offset,
                elevation=100 + random.uniform(-50, 150)  # Simulated elevation
            )
            gpx_segment.points.append(point)
        
        # Save to file
        with open(filename, 'w') as f:
            f.write(gpx.to_xml())
        
        return filename
    
    def optimize_route_for_athlete(self, start_location, distance_km, athlete_profile):
        """
        Create optimized route based on athlete profile
        
        Args:
            start_location: Starting location string or coordinates
            distance_km: Desired distance in km
            athlete_profile: Dict with athlete preferences
                - difficulty: 'easy', 'medium', 'hard'
                - terrain: 'flat', 'rolling', 'hilly'
                - name: Athlete name
        
        Returns:
            Tuple of (route_points, metadata)
        """
        # Geocode start location if string
        if isinstance(start_location, str):
            # Check if it's coordinate string like "48.8566, 2.3522"
            if ',' in start_location:
                try:
                    parts = [float(x.strip()) for x in start_location.split(',')]
                    if len(parts) == 2:
                        coords = tuple(parts)
                    else:
                        raise ValueError("Invalid coordinate format")
                except ValueError:
                    # Not coordinates, try geocoding
                    coords = self.geocode_location(start_location)
                    if not coords:
                        raise ValueError(f"Could not geocode location: {start_location}")
            else:
                coords = self.geocode_location(start_location)
                if not coords:
                    raise ValueError(f"Could not geocode location: {start_location}")
        else:
            coords = start_location
        
        difficulty = athlete_profile.get('difficulty', 'medium')
        
        # Generate route
        route_points = self.generate_circular_route(coords, distance_km, difficulty)
        
        # Calculate route statistics
        total_distance = sum(
            geodesic(route_points[i], route_points[i+1]).kilometers
            for i in range(len(route_points) - 1)
        )
        
        metadata = {
            'start_location': coords,
            'total_distance': round(total_distance, 2),
            'estimated_time': round(total_distance / 20, 2),  # hours at 20 km/h
            'difficulty': difficulty,
            'num_points': len(route_points)
        }
        
        return route_points, metadata
