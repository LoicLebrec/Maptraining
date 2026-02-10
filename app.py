"""
Flask Web Application for Maptraining
Provides interface for route generation and training analysis
"""
from flask import Flask, render_template, request, send_file, jsonify, flash, redirect, url_for
import os
from datetime import datetime
from route_generator import RouteGenerator
from training_analyzer import TrainingAnalyzer
import folium
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'maptraining-secret-key-2024'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

route_gen = RouteGenerator()
analyzer = TrainingAnalyzer()


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/generate-route', methods=['GET', 'POST'])
def generate_route():
    """Generate a new training route"""
    if request.method == 'POST':
        try:
            # Get form data
            start_location = request.form.get('start_location')
            distance = float(request.form.get('distance', 20))
            difficulty = request.form.get('difficulty', 'medium')
            athlete_name = request.form.get('athlete_name', 'Athlete')
            
            # Validate inputs
            if not start_location:
                flash('Please provide a starting location', 'error')
                return redirect(url_for('generate_route'))
            
            if distance < 1 or distance > 200:
                flash('Distance must be between 1 and 200 km', 'error')
                return redirect(url_for('generate_route'))
            
            # Create athlete profile
            athlete_profile = {
                'name': athlete_name,
                'difficulty': difficulty,
                'terrain': 'rolling'
            }
            
            # Generate route
            route_points, metadata = route_gen.optimize_route_for_athlete(
                start_location, distance, athlete_profile
            )
            
            # Create GPX file
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"route_{athlete_name.replace(' ', '_')}_{timestamp}.gpx"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            route_name = f"{athlete_name}'s {distance}km Training Route"
            route_gen.create_gpx_file(route_points, filepath, athlete_name, route_name)
            
            # Create map visualization
            map_html = create_route_map(route_points, start_location)
            
            flash(f'Route generated successfully! Distance: {metadata["total_distance"]} km', 'success')
            
            return render_template('route_result.html',
                                 filename=filename,
                                 metadata=metadata,
                                 map_html=map_html,
                                 athlete_name=athlete_name)
            
        except ValueError as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('generate_route'))
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')
            return redirect(url_for('generate_route'))
    
    return render_template('generate_route.html')


@app.route('/download/<filename>')
def download_file(filename):
    """Download generated GPX file"""
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    else:
        flash('File not found', 'error')
        return redirect(url_for('index'))


@app.route('/analyze', methods=['GET', 'POST'])
def analyze_training():
    """Analyze training data"""
    if request.method == 'POST':
        try:
            # Check if file was uploaded
            if 'gpx_file' not in request.files:
                flash('No file uploaded', 'error')
                return redirect(url_for('analyze_training'))
            
            file = request.files['gpx_file']
            
            if file.filename == '':
                flash('No file selected', 'error')
                return redirect(url_for('analyze_training'))
            
            if not file.filename.endswith('.gpx'):
                flash('Please upload a GPX file', 'error')
                return redirect(url_for('analyze_training'))
            
            # Save uploaded file
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"training_{timestamp}.gpx"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Parse and analyze training
            training_data = analyzer.parse_gpx_training(filepath)
            analysis = analyzer.analyze_training_session(training_data)
            
            # Create route visualization
            if training_data['points']:
                route_points = [(p['lat'], p['lon']) for p in training_data['points']]
                map_html = create_route_map(route_points, "Training Route")
            else:
                map_html = None
            
            return render_template('analysis_result.html',
                                 analysis=analysis,
                                 map_html=map_html)
            
        except Exception as e:
            flash(f'Error analyzing training: {str(e)}', 'error')
            return redirect(url_for('analyze_training'))
    
    return render_template('analyze.html')


def create_route_map(route_points, title):
    """Create an interactive map with the route"""
    if not route_points:
        return None
    
    # Create map centered on start point
    center = route_points[0]
    m = folium.Map(location=center, zoom_start=12)
    
    # Add route line
    folium.PolyLine(
        route_points,
        color='blue',
        weight=4,
        opacity=0.7,
        popup=title
    ).add_to(m)
    
    # Add start marker
    folium.Marker(
        route_points[0],
        popup='Start',
        icon=folium.Icon(color='green', icon='play')
    ).add_to(m)
    
    # Add end marker
    folium.Marker(
        route_points[-1],
        popup='End',
        icon=folium.Icon(color='red', icon='stop')
    ).add_to(m)
    
    return m._repr_html_()


@app.route('/api/generate-route', methods=['POST'])
def api_generate_route():
    """API endpoint for route generation"""
    try:
        data = request.get_json()
        
        start_location = data.get('start_location')
        distance = float(data.get('distance', 20))
        difficulty = data.get('difficulty', 'medium')
        athlete_name = data.get('athlete_name', 'Athlete')
        
        athlete_profile = {
            'name': athlete_name,
            'difficulty': difficulty,
            'terrain': 'rolling'
        }
        
        route_points, metadata = route_gen.optimize_route_for_athlete(
            start_location, distance, athlete_profile
        )
        
        return jsonify({
            'success': True,
            'metadata': metadata,
            'route_points': route_points
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API endpoint for training analysis"""
    try:
        if 'gpx_file' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'}), 400
        
        file = request.files['gpx_file']
        
        # Save temporary file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"temp_{timestamp}.gpx"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Analyze
        training_data = analyzer.parse_gpx_training(filepath)
        analysis = analyzer.analyze_training_session(training_data)
        
        # Clean up temp file
        os.remove(filepath)
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
