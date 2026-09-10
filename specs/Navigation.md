# Navigation service specification

This file describes the navigation service's public API. The navigation service
provides paths across the project for reading and writing files.

**Summary:** The navigation service provides validated paths for other
services to use to navigate the project.

## Signature

**Name:** `NavigationService` \
**Description:** Implements paths to navigate safely around the project

## Methods

### `new`

**Type:** `classmethod` \
**Description:** Class constructor \
**Outputs:** A `NavigationService` object

### `to_data`

**Type:** `getter` \
**Description:** Returns the data directory path \
**Outputs:** A `DirectoryPath` referring to the data directory

### `to_models`

**Type:** `getter` \
**Description:** Returns the models directory path \
**Outputs:** A `DirectoryPath` referring to the models directory

### `join`

**Type:** `method` \
**Description:** Joins two paths together \
**Inputs:** A `Path` object \
**Outputs:** A `Path` object \
**Postconditions:** The outputted path must start in the service's base
directory
