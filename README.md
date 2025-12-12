# Tennisfel World Module

A comprehensive world module for Foundry VTT, featuring the Tennisfel setting converted from LegendKeeper data.

## Overview

This module provides a complete campaign setting with:
- **Scenes**: Maps and environments for your adventures
- **Actors**: NPCs, creatures, and key characters
- **Items**: Artifacts, equipment, and technology
- **Journal Entries**: Extensive lore, history, mythology, and documentation

## Installation

### Method 1: Manifest URL (Recommended)
1. In Foundry VTT, go to "Add-on Modules"
2. Click "Install Module"
3. Paste the manifest URL: `https://raw.githubusercontent.com/adamhjk/foundry-tennisfel/main/module.json`
4. Click "Install"

### Method 2: Manual Installation
1. Download the latest release zip from [Releases](https://github.com/adamhjk/foundry-tennisfel/releases)
2. Extract to your Foundry `Data/modules/` directory
3. Restart Foundry VTT
4. Enable the module in your world settings

## What's Included

The module contains 100 converted resources from LegendKeeper, organized into four compendium packs:

### Tennisfel Scenes
Maps and environments including:
- The Tennisfel Region Map
- Location-specific maps with pins and notes

### Tennisfel Actors
Characters, NPCs, and creatures including:
- Player characters
- Important NPCs
- Creatures and monsters
- Each with full biography and portraits (where available)

### Tennisfel Items
Artifacts, equipment, and technology:
- Magical artifacts
- Technological items
- Equipment with full descriptions

### Tennisfel Journal
Extensive world documentation including:
- **Lore**: World mythology and legends
- **History**: Timeline and historical events
- **Geography**: Locations and settlements
- **Organizations**: Factions and groups
- **Procedures**: Game mechanics and guides
- All with embedded images and cross-references

## Features

- **Rich Content**: Converted from LegendKeeper with preserved formatting
- **Images**: All assets downloaded and included locally
- **Cross-References**: Resource links maintained between entries
- **Secrets**: GM-only content preserved in journal entries
- **System Agnostic**: Works with any game system in Foundry VTT v12

## Usage

1. Enable the module in your world
2. Open the Compendium sidebar
3. Browse the four Tennisfel compendium packs
4. Drag and drop content into your world as needed

## Development

### Building from Source

Requirements:
- Python 3.7+
- `jq` (for Makefile version extraction)

Steps:
```bash
# Run conversion script
make all

# Create release package
make release

# Clean build artifacts
make clean

# Test release package
make test
```

### Conversion Script

The `convert.py` script handles:
- Loading LegendKeeper JSON data
- Downloading and organizing images
- Converting Prosemirror content to HTML
- Generating Foundry-compatible compendium packs

## Data Source

This module was converted from a LegendKeeper export containing:
- 100 resources
- 40+ images
- Comprehensive world documentation

## Credits

- **Module Development**: Adam Jacob
- **World Creation**: Original LegendKeeper data
- **Foundry VTT**: By Atropos

## License

This module is provided as-is for use with Foundry VTT.

## Support

For issues or questions:
- GitHub Issues: https://github.com/adamhjk/foundry-tennisfel/issues
- Foundry VTT Discord: Tag @adamhjk

## Changelog

### Version 0.1.0 (Initial Release)
- Converted 100 LegendKeeper resources
- 4 compendium packs (Scenes, Actors, Items, Journal Entries)
- Downloaded and integrated all images
- Full Prosemirror to HTML conversion
- Foundry VTT v12 compatible
