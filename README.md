# disaster-damage-assessment-lookup

Helper scripts for assisting non-profit charity look up disaster related damage assessment for a given address, so they could use it as preliminary data for providing assistance.

## Overview

This helper script consists of a few customizable components that can be assembled together using a configuration file to look up disaster related damage assessment data.

### Components

**data_loader** component loads the data, applies some processing to the data, then saves them as a Dictionary with a string label and `GeoDataFrame` value. We currently support loading Excel sheets into `GeoDataFrame` and loading `geojson` into `GeoDataFrame`. To convert the excel sheet to `GeoDataFrame`, we require a column from the sheet for calling `geocode` using an API to get the coordinate of the entry.

**matcher** component consists of different kinds of matchers that take in a source `GeoDataFrame` data and match it against another `GeoDataFrame`, and output the matched and unmatched result. We currently have a match `by_address`, `by_coordinate`, and `by_fire_perimeter`

Each of these components have their configurable parameters defined in the respective `schema` folder. These configurations will be exposed and can be configured via `config/default.yaml`.

Each component can be further customized/expanded by modifying or adding to their sub-components.

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

The configuration file uses [adobe/him](https://github.com/adobe/himl). See their documentation for more detailed explanations on value interpolation.

`config/default.yaml` is an example configuration of the real world use case we have. This file could be use as a starting point and modified to meet the specific need.

#### Example, explained

![data_loader flow](https://www.plantuml.com/plantuml/dpng/VLHXRzfA4Fo-lsALJ-z9u0SO0h6UgbWbH96Y92fjeueYTBNNnCtvrhex6gmg_xrdbnZNTU9FtCxitipSYdDZXRQxJ89DhIIalSXoIHYnIjBjVp4bOYUjLuXCOYois4WMCMbC93y1cCTKvKABpF6pd1KfkxI5QzSKMQ6saXeKcIgoHKwOiopSeHDZRHyOO7Mbh7WaNB3ElBqq-pKAWsbLt9HdM2rIJJWNcTWIXiQGCHafwss9lnjM5JyJnfBULBeFzKFV7Uaq8mUQFneIXsto6gkROEL-vSKQLfVCpjLNTKaiEH8sPONXtLNL_Hlxx0CqX69_zP36CQcrfCJsEpLrr5fThmg3N4IFPGGdZTSvmP-0xginsaSa3zNgM-MQSiqH6PEgRQM-ucnS_KWISUnkgerM0XjS1pK6ih6Rxf4EgNZFK35V0eTdE1BQCTK64vRblfsumEVk-eKM6U4yZKf1GXSlfbQ7o1FMsHfgHLLkZNWFK2lEKagZloMbQmvq5Tz-izPMnFoa-k-EgGSuz42n9TJfzi4Y9qSCvffpf2ot1Mf-we4XIP55i_jcgAH2n7ANAUC1gHZBAL0tjwvomGOuyg0-uVyEgzOxGD_3nKvA3EDOGrKhqNgn0notDDQGKw1-aBOmn7lMCiPxKU0r6mpLbYGPV1_YsM0mde3b9gVN9FLgLWy_BKCGAeQxswkRZ__qXyEPDnxuuv4_dSvcmz5WYhxldOr7fmD_DFKdazdutxPvPw2TCniRuAHbeW5ss7XJui7DxOVhETw7NnprTedXpUN5zSNoI6q9gswgbJKMBy1J3xh-3MhouHpWr8CsrhMI0SxSnDOclZxrxE-fhLwtfWCFpfsXNIP_0G00)  

[data_loader diagram link](https://www.plantuml.com/plantuml/duml/VLHXRzfA4Fo-lsALJ-z9u0SO0h6UgbWbH96Y92fjeueYTBNNnCtvrhex6gmg_xrdbnZNTU9FtCxitipSYdDZXRQxJ89DhIIalSXoIHYnIjBjVp4bOYUjLuXCOYois4WMCMbC93y1cCTKvKABpF6pd1KfkxI5QzSKMQ6saXeKcIgoHKwOiopSeHDZRHyOO7Mbh7WaNB3ElBqq-pKAWsbLt9HdM2rIJJWNcTWIXiQGCHafwss9lnjM5JyJnfBULBeFzKFV7Uaq8mUQFneIXsto6gkROEL-vSKQLfVCpjLNTKaiEH8sPONXtLNL_Hlxx0CqX69_zP36CQcrfCJsEpLrr5fThmg3N4IFPGGdZTSvmP-0xginsaSa3zNgM-MQSiqH6PEgRQM-ucnS_KWISUnkgerM0XjS1pK6ih6Rxf4EgNZFK35V0eTdE1BQCTK64vRblfsumEVk-eKM6U4yZKf1GXSlfbQ7o1FMsHfgHLLkZNWFK2lEKagZloMbQmvq5Tz-izPMnFoa-k-EgGSuz42n9TJfzi4Y9qSCvffpf2ot1Mf-we4XIP55i_jcgAH2n7ANAUC1gHZBAL0tjwvomGOuyg0-uVyEgzOxGD_3nKvA3EDOGrKhqNgn0notDDQGKw1-aBOmn7lMCiPxKU0r6mpLbYGPV1_YsM0mde3b9gVN9FLgLWy_BKCGAeQxswkRZ__qXyEPDnxuuv4_dSvcmz5WYhxldOr7fmD_DFKdazdutxPvPw2TCniRuAHbeW5ss7XJui7DxOVhETw7NnprTedXpUN5zSNoI6q9gswgbJKMBy1J3xh-3MhouHpWr8CsrhMI0SxSnDOclZxrxE-fhLwtfWCFpfsXNIP_0G00)

![matcher flow](https://www.plantuml.com/plantuml/dpng/hPFDRjim48JlUee5UavwTmCZX_wS-WHDGMp5bKoKN1BBfUEyVI79XInJJHKZDuCcPtQ-7JrcHT4IVADEFG6TC2HFq4RkNF_HKeV5w_qB1Wy1jJsGGEVZSvEJTzhS_JWuQub_tktF9m2NPm2xRnG_e-9NmK1Fx5ZnDvakIlW43m-EKz7zS8-Z4dZg1eKSYxHaB2es0CHs_7So0EpHyVziEYTa4eaBf2HvnKfSVnYynb1c5CrwwJRyc28rk-zJyYV-zM9Mf9F4bcmHsl-byFeuHYWNhyFJM7GQQyv_cNur-uTUY7ZtvTII_vVs_SddqyA0s5vcUWFC5BEEBW6paeoJlITHj5OehvEifpdVDgEDutuD9i1imD74TAqDi81OYw9N4aPrHp97HyyrJu2iCIquhgjMesxHsfpR51vFoCwAMpyeWANZTGzkQC9L5-esBEpdHW0iAj76ADOnAjMREp-efviVpP0YcmhS02KUITQRiw4xoprNnfiBDAszMaCbVrkkxOxlXh8ku-rGI-19wfKSZyIs1Fy7)  

[match flow diagram link](https://www.plantuml.com/plantuml/duml/hPFDRjim48JlUee5UavwTmCZX_wS-WHDGMp5bKoKN1BBfUEyVI79XInJJHKZDuCcPtQ-7JrcHT4IVADEFG6TC2HFq4RkNF_HKeV5w_qB1Wy1jJsGGEVZSvEJTzhS_JWuQub_tktF9m2NPm2xRnG_e-9NmK1Fx5ZnDvakIlW43m-EKz7zS8-Z4dZg1eKSYxHaB2es0CHs_7So0EpHyVziEYTa4eaBf2HvnKfSVnYynb1c5CrwwJRyc28rk-zJyYV-zM9Mf9F4bcmHsl-byFeuHYWNhyFJM7GQQyv_cNur-uTUY7ZtvTII_vVs_SddqyA0s5vcUWFC5BEEBW6paeoJlITHj5OehvEifpdVDgEDutuD9i1imD74TAqDi81OYw9N4aPrHp97HyyrJu2iCIquhgjMesxHsfpR51vFoCwAMpyeWANZTGzkQC9L5-esBEpdHW0iAj76ADOnAjMREp-efviVpP0YcmhS02KUITQRiw4xoprNnfiBDAszMaCbVrkkxOxlXh8ku-rGI-19wfKSZyIs1Fy7)

In this example, in the `data_loader` component, we loaded our `intake_form` with addresses, the master database from the government with damage assessment, and the fire perimeters. Our `intake form` is loaded using the `excel` data loader, which include some preprocessing and post processing steps, as well as geocoding step that normalize our `intake_form`'s address to better match the government database. These data are loaded as GeoDataFrame into a Dictionary with the `label` as key and the `GeoDataFrame` as the value.

We then define our `matcher` steps that will be run sequentially. First we use the `by_fire_perimeter` matcher and select our `intake_form` as the source to match against the `fire_perimeters`. We also configure it to only look at `Eaton` and `PALISADES` perimeters. We also choose a `max_distance_from_fire_perimeter_meter` of `1500` meters, as structures close to the fire perimeters may also be impacted. Here the resulting `GeoDataFrame` is also saved to the same Dictionary with the `fire_perimeters_result` label we defined. We also save the result to an excel spreadsheet by defining a `save_file`.

Next, we use the `by_address` matcher and select the data annotated from the `fire_perimeters_result` as the source to match against `postfire_master_data`. We select the column name `SITEADDRESS` as the address that we want to match. The resulting `GeoDataFrame` is then saved to the Dictionary with the label `address_matching_result`. We also save the file to excel spreadsheet here.

The `address_matching_result` actually includes a lot of columns, so we added a `no_op` matcher step that simply select the column we want and save it into an `address_matching_alternative_view` excel file for easier review, while still having the original `address_matching_result` for full data.

Next, we use the `by_coordinate` matcher. Here we actually select the leftover of `by_address` matching by referencing `matcher.by_address.unmatched_label` as the source, then we match it against the `postfire_master_data`. We choose a `max_match_distance_meter` of `20` meters for determining the distance between the coordinates fetched based on `intake_form`'s address from the government database entry's coordinate. We write the distance between the two coordinates into a column named `distance`. We use `Intake #` as our `key_column_name` to check the result against `intake_form` for what was leftover. Here we also save the `GeoDataFrame` to the dictionary and the result to file.

We did the same thing with `address_matching_alternative_view` for `by_coordinate` matching as well, and created an alternative view file for it.

Finally, we did another `no_op` matcher to fetch the un-matched result from `by_coordinate` matching and output that to the file.

With these outputs, the reviewer can first look at the direct address matching result and resolve the duplicates manually. Then they will review the coordinate matching result to see if it seems like a correct match with address variation (e.g. difference in apartment number). Finally, they'll have to review the unmatched result to see if they can figure out what they are, or if it requires an onsite assessment. All of these outputs will also have information about whether or not the given entry is inside of the fire perimeter.

#### Useful configurations

##### Test with a subset of the data

If we want to test run just the first 5 row of the `intake_form`, we can add the following step to `preprocessing`.

```yaml
      preprocessing:
        - processing_type: head
          data:
            - "5"
```
