from models import Moon, Planet, SolarSystem

class QueryProcessor:
    """Class for processing natural language queries about planets."""

    def __init__(self, solar_system):
        """
        Initialize with a solar system.

        Args:
            solar_system (SolarSystem): The solar system to query
        """
        self.solar_system = solar_system

    def process_query(self, query):
        """
        Process a natural language query and return the answer.

        Args:
            query (str): The query string

        Returns:
            str: The answer to the query
        """
        query = query.lower().strip()

        # Check for planet name in query
        planet_name = None
        for name in self.solar_system.get_all_planet_names():
            if name.lower() in query:
                planet_name = name
                break

        # If planet found in query
        if planet_name:
            planet = self.solar_system.get_planet_by_name(planet_name)

            # Check for specific attribute queries
            if "mass" in query or "massive" in query:
                return f"{planet_name} has a mass of {planet.mass} × 10^24 kg."

            elif (
                "distance" in query
                or "far" in query
                or "from sun" in query
                or "from the sun" in query
            ):
                return f"{planet_name} is {planet.distance_from_sun} million km from the Sun."

            elif (
                "moon" in query
                or "moons" in query
                or "satellite" in query
                or "satellites" in query
            ):
                count = planet.get_moon_count()
                if count == 0:
                    return f"{planet_name} doesn't have any moons in our database."
                else:
                    moon_names = [moon.name for moon in planet.moons]
                    return f"{planet_name} has {count} moons in our database: {', '.join(moon_names)}."

            else:
                # Default to showing everything about the planet
                return f"Information about {planet_name}:\n{planet}"

        # Check for list presence queries
        if "in the list" in query or "included" in query:
            for name in self.solar_system.get_all_planet_names():
                if name.lower() in query:
                    return f"Yes, {name} is in the list of planets."

            # Check if Pluto specifically is mentioned
            if "pluto" in query:
                if "Pluto" in self.solar_system.get_all_planet_names():
                    return "Yes, Pluto is in the list of planets."
                else:
                    return "No, Pluto is not in the list of planets. It was reclassified as a dwarf planet in 2006."

            # If no specific planet was found in the query
            return "I couldn't identify which planet you're asking about."

        # Check for moon count queries
        if (
            "how many moons" in query or "number of moons" in query
        ) and "earth" in query:
            planet = self.solar_system.get_planet_by_name("Earth")
            if planet:
                count = planet.get_moon_count()
                return f"Earth has {count} moon{'s' if count != 1 else ''} in our database."

        # List all planets
        if "list" in query and "planet" in query:
            planets = self.solar_system.get_all_planet_names()
            return f"The planets in our solar system are: {', '.join(planets)}."

        return "I'm not sure how to answer that question. Try asking about a specific planet or attribute."


class PlanetApp:
    """Main application class for the planet information system."""

    def __init__(self, data_file="planet_data.json"):
        """Initialize the application with data file path."""
        self.solar_system = SolarSystem()
        self.data_file = data_file
        self.query_processor = QueryProcessor(self.solar_system)

    def initialize_default_data(self):
        """Create default planet data if no file exists."""
        # Mercury
        mercury = Planet("Mercury", 0.330, 57.9)

        # Venus
        venus = Planet("Venus", 4.87, 108.2)

        # Earth
        earth = Planet("Earth", 5.97, 149.6)
        earth.add_moon(Moon("Moon", 3474))

        # Mars
        mars = Planet("Mars", 0.642, 227.9)
        mars.add_moon(Moon("Phobos", 22))
        mars.add_moon(Moon("Deimos", 12))

        # Jupiter
        jupiter = Planet("Jupiter", 1898, 778.5)
        jupiter.add_moon(Moon("Io", 3643))
        jupiter.add_moon(Moon("Europa", 3122))
        jupiter.add_moon(Moon("Ganymede", 5262))
        jupiter.add_moon(Moon("Callisto", 4821))

        # Saturn
        saturn = Planet("Saturn", 568, 1434)
        saturn.add_moon(Moon("Titan", 5150))
        saturn.add_moon(Moon("Enceladus", 504))
        saturn.add_moon(Moon("Mimas", 396))

        # Uranus
        uranus = Planet("Uranus", 86.8, 2871)
        uranus.add_moon(Moon("Miranda", 472))
        uranus.add_moon(Moon("Ariel", 1158))
        uranus.add_moon(Moon("Umbriel", 1169))

        # Neptune
        neptune = Planet("Neptune", 102, 4495)
        neptune.add_moon(Moon("Triton", 2707))
        neptune.add_moon(Moon("Nereid", 340))

        # Pluto (dwarf planet, included for completeness)
        pluto = Planet("Pluto", 0.0130, 5906)
        pluto.add_moon(Moon("Charon", 1212))

        # Add planets to solar system
        for planet in [
            mercury,
            venus,
            earth,
            mars,
            jupiter,
            saturn,
            uranus,
            neptune,
            pluto,
        ]:
            self.solar_system.add_planet(planet)

        # Save to file
        self.solar_system.save_to_file(self.data_file)

    def load_data(self):
        """Load planet data from file or initialize default data."""
        if not self.solar_system.load_from_file(self.data_file):
            print("Creating default planet data...")
            self.initialize_default_data()

    def text_interface(self):
        """Run the text-based user interface."""
        print("\n" + "=" * 50)
        print("Welcome to the Solar System Information Program")
        print("=" * 50)
        print("\nYou can ask questions like:")
        print("- Tell me everything about Saturn")
        print("- How massive is Neptune?")
        print("- Is Pluto in the list of planets?")
        print("- How many moons does Earth have?")
        print("\nType 'exit' to quit the program.")
        print("=" * 50)

        while True:
            query = input("\nWhat would you like to know? ").strip()

            if query.lower() == "exit":
                print("Thank you for using the Solar System Information Program!")
                break

            if not query:
                continue

            answer = self.query_processor.process_query(query)
            print("\n" + answer)

    def run(self):
        """Run the application."""
        self.load_data()
        self.text_interface()


if __name__ == "__main__":
    app = PlanetApp()
    app.run()
