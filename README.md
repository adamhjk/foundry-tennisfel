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

The module contains 80 converted resources from LegendKeeper, organized into two compendium packs:

### Tennisfel Journal
Extensive world documentation including:
- **Characters & NPCs**: Player characters, important NPCs, and creatures with full biographies
- **Items & Artifacts**: Magical artifacts, equipment, and technology
- **Lore**: World mythology and legends
- **History**: Timeline and historical events
- **Geography**: Locations and settlements
- **Organizations**: Factions and groups
- **Adventures**: Campaign sessions and story arcs
- **Procedures**: Game mechanics and guides
- All with embedded images and cross-references

### Tennisfel Scenes
Maps and environments including:
- The Hollow Throne (Malthulis HQ)
- Parraldea
- Tennisfel
- Belphegor
- Map to the Mokab
- Lusty Maiden
- 6 scenes with unique maps ready for your game

## Features

- **Rich Content**: Converted from LegendKeeper with preserved formatting
- **Images**: All assets downloaded and included locally
- **Cross-References**: Resource links converted to Foundry UUID format for seamless navigation between entries
- **Secrets**: GM-only content preserved in journal entries
- **System Agnostic**: Works with any game system in Foundry VTT v12

## Usage

1. Enable the module in your world
2. Open the Compendium sidebar
3. Browse the two Tennisfel compendium packs:
   - **Tennisfel Journal** - Characters, items, lore, locations, and documentation
   - **Tennisfel Scenes** - Maps and environments
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
- 80 resources
- 16 images (6 map images + 10 content images)
- Comprehensive world documentation including characters, locations, lore, and adventures

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
- Converted 80 LegendKeeper resources
- 2 compendium packs (6 Scenes with unique maps + 74 Journal Entries)
- All content as journal entries: characters, NPCs, creatures, items, artifacts, lore, and documentation
- Downloaded and integrated 16 images including map backgrounds
- Full Prosemirror to HTML conversion with embedded images
- Foundry VTT v12 compatible
