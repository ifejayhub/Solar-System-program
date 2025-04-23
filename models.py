class Moon:
    def __init__(self, name, diameter):
        self.name = name
        self.diameter = diameter


class Planet:
    def __init__(self, name, mass, distance_from_sun):
        self.name = name
        self.mass = mass
        self.distance_from_sun = distance_from_sun
        self.moons = []

    def add_moon(self, moon):
        self.moons.append(moon)

    def get_moon_count(self):
        return len(self.moons)

    def __str__(self):
        """Provide a string representation of the planet."""
        moon_names = (
            ", ".join([moon.name for moon in self.moons]) if self.moons else "No moons"
        )
        return (
            f"Planet: {self.name}\n"
            f"Mass: {self.mass} × 10^24 kg\n"
            f"Distance from Sun: {self.distance_from_sun} million km\n"
            f"Moons: {moon_names}"
        )


class SolarSystem:
    def __init__(self):
        self.planets = []

    def add_planet(self, planet):
        self.planets.append(planet)

    def get_all_planet_names(self):
        return [planet.name for planet in self.planets]

    def get_planet_by_name(self, name):
        for planet in self.planets:
            if planet.name.lower() == name.lower():
                return planet
        return None

    def save_to_file(self, file_path):
        # Placeholder for saving to file
        pass

    def load_from_file(self, file_path):
        # Placeholder for loading from file
        return False
