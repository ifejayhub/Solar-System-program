# Solar System Information Program - Test Plan

## 1. Unit Testing

### 1.1 Moon Class Tests
- Test Moon initialization with and without diameter
- Test string representation

### 1.2 Planet Class Tests
- Test Planet initialization with all properties
- Test adding moons to a planet
- Test getting moon count
- Test string representation
- Test conversion to and from dictionary

### 1.3 SolarSystem Class Tests
- Test adding planets
- Test getting planet by name (case-insensitive)
- Test getting all planet names
- Test saving and loading from file

### 1.4 QueryProcessor Class Tests
- Test queries about specific planet properties
- Test queries about planet existence
- Test queries about moon counts
- Test handling of unknown queries

## 2. Integration Testing

### 2.1 Data Flow Tests
- Test data flow from file to application
- Test data flow from user input to response

### 2.2 End-to-End Tests
- Test common user queries
- Test edge case queries
- Test invalid inputs

## 3. User Interface Testing

### 3.1 Text Interface Tests
- Test menu display
- Test input handling
- Test response formatting
- Test exit functionality

## 4. Data Validation Tests

### 4.1 Input Validation Tests
- Test handling of empty queries
- Test handling of nonsensical queries
- Test handling of queries with special characters

## 5. Error Handling Tests

### 5.1 File Handling Tests
- Test behavior when data file is missing
- Test behavior when data file is corrupted
- Test behavior when data file is not writable
