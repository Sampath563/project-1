import subprocess
import sys

# Install Geopy if not installed
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import geopy
except ImportError:
    print("Geopy is not installed. Installing now...")
    install("geopy")
    import geopy

import matplotlib.pyplot as plt

class Crime:
    def __init__(self, crime_id, crime_type, latitude, longitude):
        self.crime_id = crime_id
        self.crime_type = crime_type
        self.latitude = latitude
        self.longitude = longitude

class CrimeMappingSystem:
    def __init__(self):
        self.crime_data = []
        self.options = {
            "1": self.create_crime_data,
            "2": self.read_crime_data,
            "3": self.update_crime_data,
            "4": self.delete_crime_data,
            "5": self.map_crime_locations,
            "6": self.analyze_crime_patterns,
            "7": self.exit_program
        }
        self.geolocator = geopy.Nominatim(user_agent="crime_mapping_app")

    def create_crime_data(self):
        crime_id = input("Enter crime ID: ")
        crime_type = input("Enter crime type: ")
        address = input("Enter address: ")
        location = self.geolocator.geocode(address)
        if location:
            latitude = location.latitude
            longitude = location.longitude
            new_crime = Crime(crime_id, crime_type, latitude, longitude)
            self.crime_data.append(new_crime)
            print("Crime data created successfully")
        else:
            print("Address not found. Please enter a valid address.")

    def read_crime_data(self):
        if not self.crime_data:
            print("No crime data available")
            return
        for crime in self.crime_data:
            print("Crime ID:", crime.crime_id)
            print("Crime Type:", crime.crime_type)
            print("Latitude:", crime.latitude)
            print("Longitude:", crime.longitude)
            print()

    def update_crime_data(self):
        crime_id = input("Enter crime ID to update: ")
        crime = self.find_crime_by_id(crime_id)
        if crime:
            crime_type = input("Enter new crime type: ")
            address = input("Enter new address: ")
            location = self.geolocator.geocode(address)
            if location:
                crime.crime_type = crime_type
                crime.latitude = location.latitude
                crime.longitude = location.longitude
                print("Crime data updated successfully")
            else:
                print("Address not found. Crime data not updated.")
        else:
            print("Crime ID does not exist")

    def delete_crime_data(self):
        crime_id = input("Enter crime ID to delete: ")
        crime = self.find_crime_by_id(crime_id)
        if crime:
            self.crime_data.remove(crime)
            print("Crime data deleted successfully")
        else:
            print("Crime ID does not exist")

    def map_crime_locations(self):
        if not self.crime_data:
            print("No crime data available to map")
            return
        lats = [crime.latitude for crime in self.crime_data]
        longs = [crime.longitude for crime in self.crime_data]
        plt.scatter(longs, lats, color='red', alpha=0.5)
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title('Crime Locations')
        plt.grid(True)
        plt.show()

    def analyze_crime_patterns(self):
        if not self.crime_data:
            print("No crime data available to analyze")
            return
        
        crime_count = {}
        for crime in self.crime_data:
            if crime.crime_type not in crime_count:
                crime_count[crime.crime_type] = 1
            else:
                crime_count[crime.crime_type] += 1

        print("Crime patterns:")
        for crime_type, count in crime_count.items():
            print(f"- Crime Type: {crime_type}, Count: {count}")

    def exit_program(self):
        print("Exiting program")
        exit()

    def find_crime_by_id(self, crime_id):
        for crime in self.crime_data:
            if crime.crime_id == crime_id:
                return crime
        return None

    def switch_options(self, choice):
        func = self.options.get(choice)
        if func:
            func()
        else:
            print("Invalid option")

# Example Usage
if __name__ == "__main__":
    crime_mapping_system = CrimeMappingSystem()

    while True:
        print("\nMenu:")
        print("1. Create Crime Data")
        print("2. Read Crime Data")
        print("3. Update Crime Data")
        print("4. Delete Crime Data")
        print("5. Map Crime Locations")
        print("6. Analyze Crime Patterns")
        print("7. Exit")

        choice = input("Enter your choice: ")
        crime_mapping_system.switch_options(choice)
