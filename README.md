# 🚀 Volatile Raccoon 🔥

This repository contains data management tools and datasets for the Atmospheric Metaverse project. 

## Getting Started

### Prerequisites

- Python 3.8 or higher
- SQLite 3.34+

### Installation

```bash
pip install -r requirements.txt
```

## Database Generation

To populate and clean the database, run the database initialization script:

```bash
python -m scripts.main --add-db --clean
```

## Key Directory Structure

Below is an overview of the main directories and scripts in the repository:

- `/analysis`:
    Preliminary analyses.    

- `/data`:  
    Contains raw and processed datasets used across the project.

- `/imgs`:  
    Stores project-relavant images.

- `/scripts/clean_data`:  
    Includes scripts for cleaning and preprocessing raw data files to remove sensor noise.

- `/scripts/coordinate_mapping`:  
    Handles the transformation between William Gate Building (WGB) coordinates and data coordinates.

- `/scripts/data_loader`:  
    Contains utilities for loading datasets into the application or database.

- `/scripts/processing`:  
    Provides scripts to transform data from the internal format to a format usable by the VR team, including interpolation of sensor values.

- `/scripts/vis`:  
    Contains visualisations to gain insights for the project. This is mostly for internal use only, so the documentation is not very complete.

- `/tests`: 
    Contains tests for the important functions.

## Usage

### Running a file

Run the dedicated file as a module. For instance, if we want to invoke `/scripts/vis/co2_colormap.py`, run

```bash
python -m scripts.vis.co2_colormap
```

### Running tests

`unittest` is used for testing. To run them, use

```bash
python -m unittest discover
```