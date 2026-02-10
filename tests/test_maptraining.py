#!/usr/bin/env python3
"""
Test script for Maptraining
Demonstrates route generation and training analysis
"""
from pathlib import Path
import os
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from route_generator import RouteGenerator
from training_analyzer import TrainingAnalyzer


TEST_OUTPUT_DIR = PROJECT_ROOT / "samples" / "test_outputs"
TEST_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def test_route_generation():
    """Test route generation functionality"""
    print("=" * 60)
    print("Testing Route Generation")
    print("=" * 60)
    
    generator = RouteGenerator()
    
    # Test 1: Generate route from Paris
    print("\nTest 1: Generating 30km route from Paris...")
    try:
        athlete_profile = {
            'name': 'Test Athlete',
            'difficulty': 'medium',
            'terrain': 'rolling'
        }
        
        route_points, metadata = generator.optimize_route_for_athlete(
            "Paris, France",
            30,
            athlete_profile
        )
        
        print(f"✓ Route generated successfully!")
        print(f"  - Distance: {metadata['total_distance']} km")
        print(f"  - Estimated time: {metadata['estimated_time']} hours")
        print(f"  - Difficulty: {metadata['difficulty']}")
        print(f"  - Number of GPS points: {metadata['num_points']}")
        
        # Create GPX file
        filename = TEST_OUTPUT_DIR / "test_route_paris.gpx"
        generator.create_gpx_file(
            route_points,
            str(filename),
            'Test Athlete',
            'Paris 30km Training Route'
        )
        print(f"✓ GPX file created: {filename}")
        
        # Clean up
        if filename.exists():
            filename.unlink()
            print(f"✓ Test file cleaned up")
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False
    
    # Test 2: Generate different difficulty levels
    print("\nTest 2: Testing different difficulty levels...")
    for difficulty in ['easy', 'medium', 'hard']:
        try:
            athlete_profile['difficulty'] = difficulty
            route_points, metadata = generator.optimize_route_for_athlete(
                (48.8566, 2.3522),  # Paris coordinates
                20,
                athlete_profile
            )
            print(f"✓ {difficulty.capitalize()} route: {metadata['total_distance']} km")
        except Exception as e:
            print(f"✗ Error with {difficulty}: {e}")
            return False
    
    print("\n✓ All route generation tests passed!")
    return True


def test_training_analysis():
    """Test training analysis functionality"""
    print("\n" + "=" * 60)
    print("Testing Training Analysis")
    print("=" * 60)
    
    analyzer = TrainingAnalyzer()
    generator = RouteGenerator()
    
    # Create a sample GPX file for testing
    print("\nCreating sample training file...")
    try:
        athlete_profile = {
            'name': 'Test Athlete',
            'difficulty': 'medium',
            'terrain': 'rolling'
        }
        
        route_points, _ = generator.optimize_route_for_athlete(
            (48.8566, 2.3522),
            40,
            athlete_profile
        )
        
        test_file = TEST_OUTPUT_DIR / "test_training.gpx"
        generator.create_gpx_file(
            route_points,
            str(test_file),
            'Test Athlete',
            'Test Training'
        )
        print(f"✓ Sample GPX file created: {test_file}")
        
        # Test analysis
        print("\nAnalyzing training data...")
        training_data = analyzer.parse_gpx_training(str(test_file))
        print(f"✓ GPX parsed successfully")
        print(f"  - Distance: {training_data['total_distance']:.2f} km")
        print(f"  - Duration: {training_data['duration']:.2f} hours")
        print(f"  - Elevation gain: {training_data['total_elevation_gain']:.2f} m")
        print(f"  - Number of points: {training_data['num_points']}")
        
        # Perform analysis
        print("\nPerforming analysis...")
        analysis = analyzer.analyze_training_session(training_data)
        print(f"✓ Analysis completed")
        print(f"  - Average speed: {analysis['avg_speed_kmh']} km/h")
        print(f"  - Intensity: {analysis['intensity']}")
        print(f"  - Training load: {analysis['training_load']}")
        print(f"  - Recommendations: {len(analysis['recommendations'])} provided")
        
        for i, rec in enumerate(analysis['recommendations'], 1):
            print(f"    {i}. {rec}")
        
        # Clean up
        if test_file.exists():
            test_file.unlink()
            print(f"\n✓ Test file cleaned up")
        
        print("\n✓ All training analysis tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_geocoding():
    """Test geocoding functionality"""
    print("\n" + "=" * 60)
    print("Testing Geocoding")
    print("=" * 60)
    
    generator = RouteGenerator()
    
    test_locations = [
        "Paris, France",
        "Lyon, France",
        "Marseille, France"
    ]
    
    print("\nTesting geocoding for various locations...")
    for location in test_locations:
        try:
            coords = generator.geocode_location(location)
            if coords:
                print(f"✓ {location}: {coords[0]:.4f}, {coords[1]:.4f}")
            else:
                print(f"✗ Could not geocode: {location}")
                return False
        except Exception as e:
            print(f"✗ Error geocoding {location}: {e}")
            return False
    
    print("\n✓ All geocoding tests passed!")
    return True


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("MAPTRAINING TEST SUITE")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Geocoding", test_geocoding()))
    results.append(("Route Generation", test_route_generation()))
    results.append(("Training Analysis", test_training_analysis()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print("\n❌ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
