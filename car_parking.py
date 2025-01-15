from abc import ABC, abstractmethod
from typing import List, Dict, Optional

# --- Models ---


class Vehicle:
    def __init__(self, license_plate: str, vehicle_type: str):
        self.license_plate = license_plate
        self.vehicle_type = vehicle_type


class ParkingSpot:
    def __init__(self, spot_id: int, spot_type: str):
        self.spot_id = spot_id
        self.spot_type = spot_type
        self.is_occupied = False
        self.vehicle: Optional[Vehicle] = None

    def park_vehicle(self, vehicle: Vehicle):
        self.is_occupied = True
        self.vehicle = vehicle

    def remove_vehicle(self):
        self.is_occupied = False
        self.vehicle = None


# --- Interfaces ---
class ParkingStrategy(ABC):
    @abstractmethod
    def find_spot(self, vehicle: Vehicle, spots: List[ParkingSpot]) -> Optional[ParkingSpot]:
        pass


# --- Concrete Strategies ---
class DefaultParkingStrategy(ParkingStrategy):
    def find_spot(self, vehicle: Vehicle, spots: List[ParkingSpot]) -> Optional[ParkingSpot]:
        for spot in spots:
            if not spot.is_occupied and spot.spot_type == vehicle.vehicle_type:
                return spot
        return None


# --- Parking Lot ---
class ParkingLot:
    def __init__(self, name: str, parking_spots: List[ParkingSpot], strategy: ParkingStrategy):
        self.name = name
        self.parking_spots = parking_spots
        self.strategy = strategy

    def park_vehicle(self, vehicle: Vehicle) -> bool:
        spot = self.strategy.find_spot(vehicle, self.parking_spots)
        if spot:
            spot.park_vehicle(vehicle)
            print(f"Vehicle {vehicle.license_plate} parked at spot {
                  spot.spot_id}")
            return True
        print(f"No parking spot available for vehicle {vehicle.license_plate}")
        return False

    def remove_vehicle(self, license_plate: str):
        for spot in self.parking_spots:
            if spot.is_occupied and spot.vehicle.license_plate == license_plate:
                print(f"Vehicle {license_plate} removed from spot {
                      spot.spot_id}")
                spot.remove_vehicle()
                return True
        print(f"Vehicle {license_plate} not found in the parking lot")
        return False

    def display_parking_status(self):
        for spot in self.parking_spots:
            status = "Occupied" if spot.is_occupied else "Available"
            print(f"Spot {spot.spot_id}: {status} ({spot.spot_type})")


# --- Main ---
if __name__ == "__main__":

    parking_spots = [
        ParkingSpot(1, "Car"),
        ParkingSpot(2, "Car"),
        ParkingSpot(3, "Bike"),
        ParkingSpot(4, "Bike"),
        ParkingSpot(5, "Truck"),
    ]

    strategy = DefaultParkingStrategy()
    parking_lot = ParkingLot("Central Parking Lot", parking_spots, strategy)

    vehicle1 = Vehicle("ABC123", "Car")
    vehicle2 = Vehicle("XYZ789", "Bike")
    vehicle3 = Vehicle("LMN456", "Truck")

    parking_lot.park_vehicle(vehicle1)
    parking_lot.park_vehicle(vehicle2)
    parking_lot.park_vehicle(vehicle3)

    print("\nParking Status:")
    parking_lot.display_parking_status()

    print("\nRemoving Vehicle ABC123:")
    parking_lot.remove_vehicle("ABC123")

    # Display parking status again
    print("\nParking Status:")
    parking_lot.display_parking_status()
