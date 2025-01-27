# disaster-damage-assessment-lookup

Helper scripts for assisting non-profit charity look up disaster related damage assessment for a given address, so they could use it as preliminary data for providing assistance.

## Getting Started

### Preparing the data

Before you can use this package, you need to obtain the following

1. Get an API key For Google Geocoding API <https://developers.google.com/maps/documentation/geocoding/get-api-key>
    1. After you obtained the key, add an `.env` file with the key in there.

        ```bash
        GOOGLE_SERVER_API_KEY=YOUR_API_KEY
        ```

2. Download the dataset you need to query the damage assessment against and save them to `input_data/`, here are a few example
    1. <https://gis.data.cnra.ca.gov/datasets/CALFIRE-Forestry::cal-fire-damage-inspection-dins-data/about>
    2. <https://data-nifc.opendata.arcgis.com/datasets/nifc::wfigs-2025-interagency-fire-perimeters-to-date/about>
3. Put the excel spreadsheet with the address you want to look up the damage assessment for inside of `input_data/`

### Running the program

It is recommended to run this package in devcontainer with Docker in Visual Studio Code. However, it should be possible to install Python directly along with requirements.txt to execute the program.

To get started with VS Code

1. Install Docker
2. Install Visual Studio Code
3. Install Visual Studio Code Dev Containers extension
4. Clone this repository and launch open in Visual Studio Code
5. Relaunch in Devcontainer

To start the program, simply run this from the project root

```bash
python -m disaster_damage_assessment_lookup.main
```

### Configuring the program

All of the configuration are located in `config/default.yaml`
