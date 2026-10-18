from flask import Flask, render_template, request
import csv
import io

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_data():
    if 'file' not in request.files:
        return render_template('index.html', error="No file uploaded.")
    
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', error="No selected file.")

    try:
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_reader = csv.DictReader(stream)
        
        valid_count = 0
        dropped_count = 0
        total_temp = 0.0
        
        # New lists to hold data for the graph
        timestamps = []
        temperatures = []

        for row in csv_reader:
            try:
                temp = float(row['temperature'])
                
                if 0 <= temp <= 100:
                    valid_count += 1
                    total_temp += temp
                    # Save the valid data points for the graph
                    timestamps.append(row['timestamp'])
                    temperatures.append(temp)
                else:
                    dropped_count += 1
            except (ValueError, KeyError):
                dropped_count += 1

        if valid_count > 0:
            avg_temp = round(total_temp / valid_count, 2)
        else:
            avg_temp = 0.0

        # Pass the lists to the frontend using the render_template function
        return render_template(
            'index.html', 
            success=True, 
            valid_count=valid_count, 
            dropped_count=dropped_count, 
            average_temp=avg_temp,
            timestamps=timestamps,
            temperatures=temperatures
        )

    except Exception as e:
        return render_template('index.html', error=f"Failed to process file: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True, port=5000)