# System Architecture

## Overview

Seoul Traffic Viewer is an Object-Oriented Programming project that displays traffic congestion information for districts in Seoul.

The system consists of five main classes:

- TrafficData
- TrafficAPI
- MapManager
- User
- MainApp

---

## TrafficData

### Responsibility
Stores traffic information for each district.

### Attributes
- district
- congestionLevel
- updateTime

---

## TrafficAPI

### Responsibility
Retrieves traffic information from a data source.

### Methods
- getTrafficData()

---

## MapManager

### Responsibility
Displays the Seoul map and visualizes traffic congestion.

### Methods
- displayMap()

---

## User

### Responsibility
Handles user interaction.

### Methods
- selectDistrict()

---

## MainApp

### Responsibility
Controls the overall application flow.

### Methods
- run()

---

## Class Relationships

User
→ MainApp

MainApp
→ TrafficAPI
→ MapManager

TrafficAPI
→ TrafficData

MapManager
→ TrafficData

---

## System Flow

1. The user selects a district.
2. MainApp requests traffic data from TrafficAPI.
3. TrafficAPI returns TrafficData objects.
4. MapManager displays the traffic information.
5. The user can refresh the data.
