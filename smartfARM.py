import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import requests

# Set up I2C bus and ADS1115 ADC
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)

# Initialize analog input for soil moisture sensor
chan = AnalogIn(ads, ADS.P0)

# API endpoint for sending alerts
API_ENDPOINT = "http://your-server-endpoint/api/alert"

# Function to read soil moisture level
def read_soil_moisture():
    return chan.value  # Read raw ADC value

# Function to check soil moisture level and send alert if too low
def monitor_soil_moisture():
    moisture_level = read_soil_moisture()

    # Convert ADC value to percentage (adjust according to sensor and soil type)
    moisture_percentage = (moisture_level / 65535.0) * 100.0

    print(f"Soil Moisture Level: {moisture_percentage:.2f}%")

    # Threshold example: send alert if moisture is below 30%
    if moisture_percentage < 30.0:
        alert_data = {
            'sensor': 'Soil Moisture Sensor',
            'message': 'Low soil moisture detected!',
            'moisture_level': moisture_percentage
        }
        try:
            # Send alert to API endpoint
            response = requests.post(API_ENDPOINT, json=alert_data)
            if response.status_code == 200:
                print("Alert sent successfully!")
            else:
                print(f"Failed to send alert. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error sending alert: {str(e)}")

# Main loop to continuously monitor soil moisture
def main():
    while True:
        monitor_soil_moisture()
        time.sleep(300)  # Check every 5 minutes (adjust as needed)

if __name__ == "__main__":
    main()
