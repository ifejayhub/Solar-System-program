import unittest
import os
import json
from tempfile import NamedTemporaryFile
from main import Moon, Planet, SolarSystem, QueryProcessor

# Import the classes from the main program
# Assuming they're in separate files, you would import like this:
# from planet import Moon, Planet
# from solar_system import SolarSystem
# from query_processor import QueryProcessor

# For demonstration, I'll define a test class assuming the classes are imported

class TestMoon(unittest.TestCase):
    """Tests for the Moon class."""
    
    def test_moon_initialization(self):
        """Test Moon initialization with name and diameter."""
        moon = Moon("Phobos", 22)
        self.assertEqual(moon.name, "Phobos")
        self.assertEqual(moon.diameter, 22)
        
    def test_moon_initialization_without_diameter(self):
        """Test Moon initialization with just name."""
        moon = Moon("Europa")
        self.assertEqual(moon.name, "Europa")
        self.assertIsNone(moon.diameter)
        
    def test_moon_string_representation(self):
        """Test string representation of Moon."""
        moon1 = Moon("Titan", 5150)
        moon2 = Moon("Deimos")
        
        self.assertEqual(str(moon1), "Titan (diameter: 5150 km)")
        self.assertEqual(str(moon2), "Deimos")


class TestPlanet(unittest.TestCase):
    """Tests for the Planet class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.earth = Planet("Earth", 5.97, 149.6)
        self.mars = Planet("Mars", 0.642, 227.9)
        
        # Add moons to Mars
        self.mars.add_moon(Moon("Phobos", 22))
        self.mars.add_moon(Moon("Deimos", 12))
    
    def test_planet_initialization(self):
        """Test Planet initialization."""
        self.assertEqual(self.earth.name, "Earth")
        self.assertEqual(self.earth.mass, 5.97)
        self.assertEqual(self.earth.distance_from_sun, 149.6)
        self.assertEqual(len(self.earth.moons), 0)
        
    def test_add_moon(self):
        """Test adding moons to a planet."""
        moon = Moon("Moon", 3474)
        self.earth.add_moon(moon)
        
        self.assertEqual(len(self.earth.moons), 1)
        self.assertEqual(self.earth.moons[0].name, "Moon")
        
    def test_get_moon_count(self):
        """Test getting moon count."""
        self.assertEqual(self.earth.get_moon_count(), 0)
        self.assertEqual(self.mars.get_moon_count(), 2)
        
    def test_to_dict(self):
        """Test conversion to dictionary."""
        planet_dict = self.mars.to_dict()
        
        self.assertEqual(planet_dict["name"], "Mars")
        self.assertEqual(planet_dict["mass"], 0.642)
        self.assertEqual(planet_dict["distance_from_sun"], 227.9)
        self.assertEqual(len(planet_dict["moons"]), 2)
        self.assertEqual(planet_dict["moons"][0]["name"], "Phobos")
        
    def test_from_dict(self):
        """Test creation from dictionary."""
        planet_dict = {
            "name": "Jupiter",
            "mass": 1898,
            "distance_from_sun": 778.5,
            "moons": [
                {"name": "Io", "diameter": 3643},
                {"name": "Europa", "diameter": 3122}
            ]
        }
        
        jupiter = Planet.from_dict(planet_dict)
        
        self.assertEqual(jupiter.name, "Jupiter")
        self.assertEqual(jupiter.mass, 1898)
        self.assertEqual(jupiter.distance_from_sun, 778.5)
        self.assertEqual(len(jupiter.moons), 2)
        self.assertEqual(jupiter.moons[0].name, "Io")
        self.assertEqual(jupiter.moons[0].diameter, 3643)


class TestSolarSystem(unittest.TestCase):
    """Tests for the SolarSystem class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.solar_system = SolarSystem()
        
        # Add some planets
        self.solar_system.add_planet(Planet("Earth", 5.97, 149.6))
        self.solar_system.add_planet(Planet("Mars", 0.642, 227.9))
        self.solar_system.add_planet(Planet("Jupiter", 1898, 778.5))
        
    def test_add_planet(self):
        """Test adding a planet."""
        venus = Planet("Venus", 4.87, 108.2)
        self.solar_system.add_planet(venus)
        
        self.assertEqual(len(self.solar_system.planets), 4)
        self.assertEqual(self.solar_system.planets[3].name, "Venus")
        
    def test_get_planet_by_name(self):
        """Test getting a planet by name."""
        # Case-sensitive match
        planet = self.solar_system.get_planet_by_name("Mars")
        self.assertIsNotNone(planet)
        self.assertEqual(planet.name, "Mars")
        
        # Case-insensitive match
        planet = self.solar_system.get_planet_by_name("earth")
        self.assertIsNotNone(planet)
        self.assertEqual(planet.name, "Earth")
        
        # Non-existent planet
        planet = self.solar_system.get_planet_by_name("Pluto")
        self.assertIsNone(planet)
        
    def test_get_all_planet_names(self):
        """Test getting all planet names."""
        names = self.solar_system.get_all_planet_names()
        
        self.assertEqual(len(names), 3)
        self.assertIn("Earth", names)
        self.assertIn("Mars", names)
        self.assertIn("Jupiter", names)
        
    def test_save_and_load_from_file(self):
        """Test saving and loading from file."""
        # Create a temporary file
        with NamedTemporaryFile(delete=False, suffix='.json') as temp_file:
            temp_filename = temp_file.name
        
        try:
            # Save to file
            result = self.solar_system.save_to_file(temp_filename)
            self.assertTrue(result)
            
            # Create a new solar system and load from file
            new_solar_system = SolarSystem()
            result = new_solar_system.load_from_file(temp_filename)
            
            self.assertTrue(result)
            self.assertEqual(len(new_solar_system.planets), 3)
            
            # Check planet data
            earth = new_solar_system.get_planet_by_name("Earth")
            self.assertIsNotNone(earth)
            self.assertEqual(earth.mass, 5.97)
            
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_filename):
                os.remove(temp_filename)


class TestQueryProcessor(unittest.TestCase):
    """Tests for the QueryProcessor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.solar_system = SolarSystem()
        
        # Earth with one moon
        earth = Planet("Earth", 5.97, 149.6)
        earth.add_moon(Moon("Moon", 3474))
        
        # Mars with two moons
        mars = Planet("Mars", 0.642, 227.9)
        mars.add_moon(Moon("Phobos", 22))
        mars.add_moon(Moon("Deimos", 12))
        
        # Jupiter with no moons (for testing)
        jupiter = Planet("Jupiter", 1898, 778.5)
        
        # Add planets to solar system
        self.solar_system.add_planet(earth)
        self.solar_system.add_planet(mars)
        self.solar_system.add_planet(jupiter)
        
        self.query_processor = QueryProcessor(self.solar_system)
        
    def test_query_everything_about_planet(self):
        """Test querying everything about a planet."""
        result = self.query_processor.process_query("Tell me everything about Mars")
        
        self.assertIn("Mars", result)
        self.assertIn("0.642", result)  # Mass
        self.assertIn("227.9", result)  # Distance
        self.assertIn("Phobos", result)  # Moon
        
    def test_query_mass(self):
        """Test querying planet mass."""
        result = self.query_processor.process_query("How massive is Jupiter?")
        
        self.assertIn("Jupiter", result)
        self.assertIn("1898", result)
        
    def test_query_distance(self):
        """Test querying distance from Sun."""
        result = self.query_processor.process_query("How far is Earth from the Sun?")
        
        self.assertIn("Earth", result)
        self.assertIn("149.6", result)
        
    def test_query_moons(self):
        """Test querying about moons."""
        result = self.query_processor.process_query("How many moons does Mars have?")
        
        self.assertIn("Mars", result)
        self.assertIn("2", result)
        self.assertIn("Phobos", result)
        self.assertIn("Deimos", result)
        
        # Test planet with no moons
        result = self.query_processor.process_query("How many moons does Jupiter have?")
        
        self.assertIn("Jupiter", result)
        self.assertIn("doesn't have any moons", result)
        
    def test_query_planet_in_list(self):
        """Test querying if a planet is in the list."""
        # Existing planet
        result = self.query_processor.process_query("Is Mars in the list of planets?")
        self.assertIn("Yes", result)
        self.assertIn("Mars", result)
        
        # Non-existent planet
        result = self.query_processor.process_query("Is Pluto in the list of planets?")
        self.assertIn("No", result)
        self.assertIn("Pluto", result)
        

if __name__ == "__main__":
    unittest.main()
