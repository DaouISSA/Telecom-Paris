import requests

class RobotCommunicator:
    def __init__(self, server_url):
        self.server_url = server_url

    def send_position(self, position):
        try:
            response = requests.post(f"{self.server_url}/update_position", json=position)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with server: {e}")
            return None

if __name__ == "__main__":
    server_url = "http://proj103.r2.enst.fr"
    robot_communicator = RobotCommunicator(server_url)
    
    # Example position data
    position_data = {
        "robot_id": "robot_1",
        "x": 10.0,
        "y": 20.0,
        "z": 5.0
    }
    
    response = robot_communicator.send_position(position_data)
    if response:
        print("Position updated successfully:", response)
    else:
        print("Failed to update position.")
