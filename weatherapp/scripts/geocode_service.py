import googlemaps


class GeocodeService:
    def __init__(self, google_api_key: str):
        self.google_maps_client = googlemaps.Client(key=google_api_key)

    def get_lat_long(self, address: str) -> tuple[float, float]:
        geocode_result = self.google_maps_client.geocode(address)
        if geocode_result:
            first_result = geocode_result[0]
            geometry_location = first_result["geometry"]["location"]
            return geometry_location["lat"], geometry_location["lng"]

        raise Exception(f"Failed to geocode address: {address}")
