from flask import Flask, render_template
from datetime import datetime
import os

app = Flask(__name__)

class AirQualityData:
    def __init__(self):
        self.THRESHOLDS = {
            'temperature': {'min': 20, 'max': 35},
            'humidity': {'min': 30, 'max': 80},
            'MQ135': {'min': 50, 'max': 150}
        }
        self.DATA_FILE = 'data/sensor_data.txt'
        
    def read_latest_data(self):
        try:
            if not os.path.exists(self.DATA_FILE) or os.path.getsize(self.DATA_FILE) == 0:
                return None
            with open(self.DATA_FILE, 'r') as file:
                lines = file.readlines()
                recent_lines = lines[-5:] if len(lines) >= 5 else lines
                
                data = []
                for line in recent_lines:
                    values = [float(x) for x in line.strip().split()]
                    if len(values) == 3:
                        timestamp = datetime.now().strftime('%H:%M')
                        data.append({
                            'timestamp': timestamp,
                            'value1': values[0],
                            'value2': values[1],
                            'value3': values[2]
                        })
                
                return data
        except Exception as e:
            print(f"Error reading data file: {e}")
            return None

    def check_threshold(self, value, threshold_type):
        threshold = self.THRESHOLDS[threshold_type]
        return value < threshold['min'] or value > threshold['max']

    def get_current_data(self):
        data = self.read_latest_data()
        if not data or len(data) == 0:
            return {
                'temperature': {'value': 0, 'warning': False},
                'humidity': {'value': 0, 'warning': False},
                'MQ135': {'value': 0, 'warning': False},
                'history': [],
                'thresholds': self.THRESHOLDS
            }

        latest = data[-1]
        return {
            'temperature': {
                'value': latest['value1'],
                'warning': self.check_threshold(latest['value1'], 'temperature')
            },
            'humidity': {
                'value': latest['value2'],
                'warning': self.check_threshold(latest['value2'], 'humidity')
            },
            'MQ135': {
                'value': latest['value3'],
                'warning': self.check_threshold(latest['value3'], 'MQ135')
            },
            'history': data,
            'thresholds': self.THRESHOLDS
        }

air_quality = AirQualityData()

@app.route('/')
def index():
    data = air_quality.get_current_data()
    return render_template('index.html', data=data)

if __name__ == '__main__':
    os.makedirs('data', exist_ok=True)
    app.run(debug=True)
