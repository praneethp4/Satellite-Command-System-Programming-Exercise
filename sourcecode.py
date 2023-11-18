import logging
import time

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Custom exceptions
class CommandError(Exception):
    #Base class for command errors
    pass

class InvalidDirectionError(CommandError):
    #exception for invalid rotation,panel activation/deactivation error,data collection error
    def __init__(self, direction):
        super().__init__(f"Invalid rotation: {direction}. Please use 'North'/'South'/'East'/'West'.")

class ActivationError(CommandError):
    def __init__(self, message="Error in solar panel activation"):
        super().__init__(message)

class DeactivationError(CommandError):
    def __init__(self, message="Error in solar panel deactivation"):
        super().__init__(message)

class DataCollectionError(CommandError):
    def __init__(self, message="Error in data collection"):
        super().__init__(message)

# Command interface
class SatelliteCommand:
    #Interface for satellite commands
    def execute(self):
        #Execute the satellite command
        pass

# Receiver class (Satellite)
class Satellite:
    def __init__(self):
        #initialization
        self.orientation = "North"
        self.solarpanels = "Inactive"
        self.datacollected = 0
        self.command_history = []
    def show_state(self):
        #Display the current state
        logger.info(f"Orientation: {self.orientation}")
        logger.info(f"Solar Panels: {self.solarpanels}")
        logger.info(f"Data Collected: {self.datacollected}")
    def update_state(self, command):
        #Updated state after execution
        self.command_history.append(command)

# Concrete command for initialization
class initialize(SatelliteCommand):
    #Command to initialize the satellite
    def __init__(self, satellite):
        #Initialize the command with a satellite instance
        self.satellite = satellite
    def execute(self):
        #Execute the initialization command
        logger.info("Initializing satellite.....")
        self._set_default_values()
        self.satellite.update_state(self)
    def _set_default_values(self):
        #Set default values for the satellite
        self.satellite.orientation = "North"
        self.satellite.solarpanels = "Inactive"
        self.satellite.datacollected = 0

# Concrete command for rotation
class rotate(SatelliteCommand):
    #Command to rotate the satellite
    VALID_DIRECTIONS = ["North", "South", "East", "West"]

    def __init__(self, satellite, direction):
        #Initialize the command with a satellite instance and rotation direction
        self.satellite = satellite
        self.direction = direction
    def execute(self):
        #Execute the rotation command with retries
        retries = 3
        for attempt in range(retries):
            try:
                self._validate_direction()
                if self.direction == self.satellite.orientation:
                    logger.info(f"Satellite is already in {self.direction} direction ")
                    break
                logger.info(f"Rotating the satellite to {self.direction}...")
                self.satellite.orientation = self.direction
                self.satellite.update_state(self)
                break  # Break out of the retry loop on success
            except InvalidDirectionError as e:
                logger.error(f"Error in rotate: {e}")
                raise e
            except Exception as e:
                logger.error(f"Unexpected error in rotate: {e}")
                if attempt < retries - 1:
                    logger.warning("Retrying...")
                    time.sleep(1)  # Delay before the next attempt
                else:
                    raise e
    def _validate_direction(self):
        #Validate the rotation direction
        if self.direction not in self.VALID_DIRECTIONS:
            raise InvalidDirectionError(self.direction)

# Concrete command for activating solar panels
class activatepanels(SatelliteCommand):
    #Command to activate solar panels
    def __init__(self, satellite):
        #Initialize the command with a satellite instance
        self.satellite = satellite
    def execute(self):
        #Execute the solar panel activation command with retries
        retries = 3
        for attempt in range(retries):
            try:
                logger.info("Activating solar panels...")
                self.satellite.solarpanels = "Active"
                self.satellite.update_state(self)
                break  # Break out of the retry loop on success
            except Exception as e:
                logger.error(f"Error in activatePanels: {e}")
                if attempt < retries - 1:
                    logger.warning("Retrying...")
                    time.sleep(1)  # Introduce a delay before the next attempt

# Concrete command for deactivating solar panels
class deactivatepanels(SatelliteCommand):
    #Command to deactivate solar panels
    def __init__(self, satellite):
        #Initialize the command with a satellite instance
        self.satellite = satellite
    def execute(self):
        #Execute the solar panel deactivation command with retries
        retries = 3
        for attempt in range(retries):
            try:
                logger.info("Deactivating solar panels...")
                self.satellite.solarpanels = "Inactive"
                self.satellite.update_state(self)
                break  # Break out of the retry loop on success
            except Exception as e:
                logger.error(f"Error in deactivatepanels: {e}")
                if attempt < retries - 1:
                    logger.warning("Retrying...")
                    time.sleep(1)  # Introduce a delay before the next attempt

# Concrete command for collecting data
class collectdata(SatelliteCommand):
    #Command to collect data
    def __init__(self, satellite):
        #Initialize the command with a satellite instance
        self.satellite = satellite
    def execute(self):
        #Execute the data collection command with retries
        retries = 3
        for attempt in range(retries):
            try:
                self._validate_solarpanels()
                logger.info("Collecting data...")
                self._increment_datacollected()
                self.satellite.update_state(self)
                break  # Break out of the retry loop on success
            except ValueError as e:
                logger.warning(f"Warning in collectdata: {e}")
                if attempt < retries - 1:
                    logger.warning("Retrying...")
                    time.sleep(1)  # Introduce a delay before the next attempt
                else:
                    raise DataCollectionError(e)
    def _validate_solarpanels(self):
        #Validate that solar panels are active for data collection
        if self.satellite.solarpanels != "Active":
            raise ValueError("Cannot collect data. Solar panels are inactive.")
    def _increment_datacollected(self):
        #Increment 'Data Collected' if solar panels are active
        self.satellite.datacollected += 10

# Client code
def initialize_satellite():
    #Initialize the satellite
    my_satellite = Satellite()
    init_command = initialize(my_satellite)
    init_command.execute()
    my_satellite.show_state()
    return my_satellite
def execute_commands():
    #Execute a sequence of commands on the satellite
    try:
        # Execute commands
        satellite = initialize_satellite()
        while True:
            # Commands to be executed
            command_str = input("Enter command (rotate(direction)/activate/deactivate/collect/exit): ")
            if command_str == "exit":
                break
            if "rotate" in command_str:
                if command_str=="rotate(North)":
                    command = rotate(satellite, "North")
                elif command_str=="rotate(South)":
                    command = rotate(satellite, "South")
                elif command_str=="rotate(East)":
                    command = rotate(satellite, "East")
                elif command_str=="rotate(West)":
                    command = rotate(satellite, "West")
                else:
                    logger.warning("Invalid command. Please enter rotate/activate/deactivate/collect/exit.")
                    continue
            elif command_str == "activate":
                command = activatepanels(satellite)
            elif command_str == "deactivate":
                command = deactivatepanels(satellite)
            elif command_str == "collect":
                command = collectdata(satellite)
            else:
                logger.warning("Invalid command. Please enter rotate/activate/deactivate/collect/exit.")
                continue
            try:
                command.execute()
                satellite.show_state()
            except CommandError as e:
                logger.error(f"Error executing command: {e}")
            except Exception as e:
                logger.error(f"Unexpected error executing command: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
if __name__ == "__main__":
    execute_commands()
