#!/usr/bin/env python3
"""
Simple demo script to showcase Maptraining functionality
"""
import os
from route_generator import RouteGenerator
from training_analyzer import TrainingAnalyzer


def demo_route_generation():
    """Demonstrate route generation"""
    print("=" * 70)
    print("DEMO: Generating a Training Route")
    print("=" * 70)
    
    generator = RouteGenerator()
    
    # Example 1: Create a route using coordinates (works offline)
    print("\n📍 Creating a 25km route from Paris coordinates...")
    
    paris_coords = (48.8566, 2.3522)  # Paris, France
    athlete_profile = {
        'name': 'Demo Athlete',
        'difficulty': 'medium',
        'terrain': 'rolling'
    }
    
    route_points, metadata = generator.optimize_route_for_athlete(
        paris_coords,
        25,
        athlete_profile
    )
    
    print(f"\n✅ Route Generated Successfully!")
    print(f"   📏 Distance: {metadata['total_distance']} km")
    print(f"   ⏱️  Estimated Time: {metadata['estimated_time']} hours")
    print(f"   💪 Difficulty: {metadata['difficulty']}")
    print(f"   📍 GPS Points: {metadata['num_points']}")
    
    # Create GPX file
    output_file = "demo_route_paris_25km.gpx"
    generator.create_gpx_file(
        route_points,
        output_file,
        'Demo Athlete',
        'Paris 25km Training Route'
    )
    
    print(f"\n💾 GPX file created: {output_file}")
    print(f"   You can now use this file with any GPS device or cycling app!")
    
    return output_file


def demo_training_analysis(gpx_file):
    """Demonstrate training analysis"""
    print("\n" + "=" * 70)
    print("DEMO: Analyzing a Training Session")
    print("=" * 70)
    
    analyzer = TrainingAnalyzer()
    
    print(f"\n📊 Analyzing training from: {gpx_file}")
    
    # Parse the GPX file
    training_data = analyzer.parse_gpx_training(gpx_file)
    
    print(f"\n✅ Training Data Parsed:")
    print(f"   📏 Distance: {training_data['total_distance']:.2f} km")
    print(f"   ⏱️  Duration: {training_data['duration']:.2f} hours")
    print(f"   ⛰️  Elevation Gain: {training_data['total_elevation_gain']:.2f} m")
    print(f"   📉 Elevation Loss: {training_data['total_elevation_loss']:.2f} m")
    
    # Perform detailed analysis
    analysis = analyzer.analyze_training_session(training_data)
    
    print(f"\n📈 Performance Analysis:")
    print(f"   🚴 Average Speed: {analysis['avg_speed_kmh']} km/h")
    print(f"   ⏱️  Average Pace: {analysis['avg_pace_min_per_km']:.2f} min/km")
    print(f"   💪 Intensity: {analysis['intensity'].upper()}")
    print(f"   📊 Training Load: {analysis['training_load']} TSS")
    
    print(f"\n💡 Recommendations:")
    for i, rec in enumerate(analysis['recommendations'], 1):
        print(f"   {i}. {rec}")
    
    return analysis


def create_sample_routes():
    """Create sample routes for different scenarios"""
    print("\n" + "=" * 70)
    print("Creating Sample Training Routes")
    print("=" * 70)
    
    generator = RouteGenerator()
    
    scenarios = [
        {
            'name': 'Recovery Ride',
            'location': (48.8566, 2.3522),  # Paris
            'distance': 15,
            'difficulty': 'easy',
            'description': 'Short recovery ride, flat terrain'
        },
        {
            'name': 'Weekend Long Ride',
            'location': (43.6047, 1.4442),  # Toulouse
            'distance': 80,
            'difficulty': 'medium',
            'description': 'Long endurance ride'
        },
        {
            'name': 'Hill Training',
            'location': (45.7640, 4.8357),  # Lyon
            'distance': 40,
            'difficulty': 'hard',
            'description': 'Challenging hill training'
        }
    ]
    
    created_files = []
    
    for scenario in scenarios:
        print(f"\n🚴 {scenario['name']}")
        print(f"   📍 Location: {scenario['location']}")
        print(f"   📏 Distance: {scenario['distance']} km")
        print(f"   💪 Difficulty: {scenario['difficulty']}")
        print(f"   ℹ️  {scenario['description']}")
        
        athlete_profile = {
            'name': 'Sample Athlete',
            'difficulty': scenario['difficulty'],
            'terrain': 'rolling'
        }
        
        route_points, metadata = generator.optimize_route_for_athlete(
            scenario['location'],
            scenario['distance'],
            athlete_profile
        )
        
        filename = f"sample_{scenario['name'].lower().replace(' ', '_')}.gpx"
        generator.create_gpx_file(
            route_points,
            filename,
            'Sample Athlete',
            scenario['name']
        )
        
        print(f"   ✅ Created: {filename} ({metadata['total_distance']} km)")
        created_files.append(filename)
    
    return created_files


def main():
    """Run the demo"""
    print("\n" + "=" * 70)
    print("🚴 MAPTRAINING DEMO 🚴")
    print("Open Source Training Route Generator & Analyzer")
    print("=" * 70)
    
    # Demo 1: Generate a route
    gpx_file = demo_route_generation()
    
    # Demo 2: Analyze the route
    demo_training_analysis(gpx_file)
    
    # Demo 3: Create sample routes
    sample_files = create_sample_routes()
    
    print("\n" + "=" * 70)
    print("🎉 Demo Complete!")
    print("=" * 70)
    print("\n📁 Files created:")
    print(f"   - {gpx_file}")
    for f in sample_files:
        print(f"   - {f}")
    
    print("\n🌐 To use the web interface:")
    print("   1. Run: python app.py")
    print("   2. Open: http://localhost:5000")
    print("   3. Generate custom routes and analyze your training!")
    
    print("\n📚 For more information, see README.md")
    print()


if __name__ == "__main__":
    main()
