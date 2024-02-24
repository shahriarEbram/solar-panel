import requests

# URL of the API endpoint
url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Qazvin/2023-11-06/2024-02-22?unitGroup=metric&contentType=csv&include=days&key=XYAU3D5W3UQYBN3NSQSWVVXQ4"

# Send the GET request to the API
def get_weather_history():
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        # The request was successful, so get the CSV data
        weather_data = response.content
        # Open a file to save the CSV data
        with open('weather_data.csv', 'wb') as f:
            f.write(weather_data)
    else:
        # The request was not successful, so print an error message
        print("Error:", response.status_code)
