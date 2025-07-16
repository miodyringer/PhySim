# PhySim: Introduction

PhySim is a physics simulation framework built on top of Pygame. It provides a modular architecture for creating various types of physics scenarios, allowing you to easily define entities with properties like movement, mass, collision, and force reception.

## Features

* **Modular Design**: Built with abstract base classes (`Entity`, `Movable`, `Collision`, `Mass`, `ReceiveForce`, `Shape`) to promote reusability and extensibility.

* **Two-Phase Physics Update**: Stable and predictable physics simulation through separate calculation and application phases.

* **Collision Detection & Resolution**: Handles circle-to-circle collisions with restitution.

* **Gravitational Forces**: Supports both global (N-body) gravity and localized (constant direction) gravity.

* **Repulsive Forces**: Implement `ForceField` objects to influence other entities.

* **Screen Border Collisions**: Entities bounce off the edges of the display surface.

## Getting Started

### Prerequisites

* Python 3.x

* Pygame library: You can install it using pip:

```
pip install pygame
```

### Installation

Clone this repository:

```
git clone https://github.com/miodyringer/PhySim.git
```

## Creating a New Scenario

To create your own physics simulation:

**Make a new class inheriting from the `Scenario` class**:
   Create a new Python file (e.g., `my_custom_scenario.py`) in the `Demos/` folder or a similar structure.
