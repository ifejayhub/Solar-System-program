# Solar System Information Program

This program displays information about planets in our solar system and allows users to query this information using natural language.

## Features

- Stores information about planets: name, mass, distance from the Sun, and moons
- Processes natural language queries about planets
- Object-oriented design with appropriate classes
- Data persistence using JSON file
- Input validation
- Comprehensive test suite

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/ifejayhub/Solar-System-program.git
   cd Solar-System-program
   ```

2. No additional dependencies are required as the program uses only Python standard libraries.

## Usage

Run the program using Python:

```
python main.py
```

This will launch the text-based interface where you can ask questions about planets.

### Example Queries

- "Tell me everything about Saturn"
- "How massive is Neptune?"
- "Is Pluto in the list of planets?"
- "How many moons does Earth have?"
- "List all planets"

## Project Structure

- `main.py`: Main program file containing the PlanetApp class
- `planet.py`: Contains Moon and Planet classes
- `solar_system.py`: Contains SolarSystem class
- `query_processor.py`: Contains QueryProcessor class
- `test_solar_system.py`: Unit tests
- `planet_data.json`: Data file (auto-generated if not present)
- `test_plan.md`: Test plan documentation

## Implementation Details

### Classes

- **Moon**: Represents a moon with name and optional diameter
- **Planet**: Represents a planet with its properties (name, mass, distance from Sun, moons)
- **SolarSystem**: Contains and manages a collection of planets
- **QueryProcessor**: Processes natural language queries about planets
- **PlanetApp**: Main application class that ties everything together

### Data Storage

Planet data is stored in a JSON file (`planet_data.json`) and loaded when the program starts. If the file doesn't exist, default data is created.

## Testing

Run unit tests with:

```
python -m unittest test_solar_system.py
```

The test plan is documented in `test_plan.md`.
