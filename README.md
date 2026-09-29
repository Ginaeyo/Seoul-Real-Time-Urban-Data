# Seoul Traffic Viewer

## Project Overview

Seoul Traffic Viewer is a data visualization dashboard that displays traffic congestion information in Seoul. The system processes traffic data and presents it through a map-based interface, allowing users to easily understand traffic conditions in different districts of Seoul.

---

## Contributors

|   Name   | Student Number |     GitHub ID     |     Role     |
|----------|----------------|-------------------|--------------|
| 에르덴자야 |   2025203503   |      Ginaeyo      | Team Leader |
|   민경환  |   2023203089   |    kimmolang11    | Team Member |
|   김효중  |   2022321028   | a01056405156-ctrl | Team Member |
|  할리오나  |   2025403507   |     liuka0715     | Team Member |
|   원미혜  |   2024403150   |     today0505     | Team Member |

---

## How to Run

### Requirements

- Python 3.x

### Installation

1. Clone the repository

git clone https://github.com/Ginaeyo/seoul-traffic-viewer.git

2. Move to the project directory

cd seoul-traffic-viewer

3. Run the application

python main.py

---

## Data Used

### Main Data

- Seoul Traffic Congestion Data

### Additional Data

- Seoul District Information
- Seoul Geographic Information

The additional data will be used to improve map visualization and provide district-based traffic information.

---

## Class Design

### 1. TrafficData

#### Responsibility
Stores and manages traffic congestion information.

#### Attributes
- district
- congestion_level

#### Methods
- get_congestion()
- set_congestion()

---

### 2. TrafficAPI

#### Responsibility
Retrieves traffic data from the data source.

#### Methods
- get_data()
- update_data()

---

### 3. MapManager

#### Responsibility
Manages map display and visualization.

#### Methods
- show_map()
- update_map()

---

### 4. User

#### Responsibility
Handles user information and interactions.

#### Attributes
- name

#### Methods
- search_district()

---

### 5. MainApp

#### Responsibility
Controls the overall program flow and coordinates interactions between objects.

#### Methods
- run()
- initialize()

---

## Object Interaction

User

↓

MainApp

↓

TrafficAPI

↓

TrafficData

↓

MapManager

↓

Dashboard Visualization

### Processing Flow

1. User requests traffic information.
2. MainApp receives the request.
3. TrafficAPI retrieves traffic data.
4. TrafficData stores and processes the data.
5. MapManager visualizes the processed data.
6. The dashboard displays the final result to the user.

---

## Dashboard Features

### Seoul Traffic Map

Displays traffic congestion information on a map of Seoul.

### District Traffic Information

Shows traffic conditions for each district.

### Traffic Visualization

Visualizes traffic congestion levels using charts and indicators.

### User Interaction

Allows users to explore traffic information through the dashboard interface.

---

## GitHub Repository

Repository URL:

https://github.com/Ginaeyo/seoul-traffic-viewer

---

## Development Plan

### Phase 1
- Create project structure
- Design classes

### Phase 2
- Implement data processing classes
- Implement API connection

### Phase 3
- Implement dashboard visualization
- Integrate all components

### Phase 4
- Testing and bug fixing
- Final deployment

---

## License

This project was developed for the Object-Oriented Programming Team Project.
