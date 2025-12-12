#!/usr/bin/env python3
"""
Tennisfel LegendKeeper to Foundry VTT Converter
Converts LegendKeeper JSON data into Foundry VTT v12 compendium packs
"""

import json
import random
import string
import os
import re
import urllib.request
import urllib.parse
from pathlib import Path


def generate_id(length=16):
    """Generate a random alphanumeric ID for Foundry documents."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def download_image(url, category='images'):
    """Download image from URL and save to appropriate assets directory."""
    if not url or not url.startswith('http'):
        return None

    # Skip non-asset URLs (like legendkeeper.com pages)
    if 'assets.legendkeeper.com' not in url:
        return None

    filename = url.split('/')[-1]  # Extract UUID filename
    local_dir = f'assets/{category}'
    os.makedirs(local_dir, exist_ok=True)
    local_path = os.path.join(local_dir, filename)

    if not os.path.exists(local_path):
        try:
            print(f"Downloading: {filename} -> {category}/")
            urllib.request.urlretrieve(url, local_path)
        except Exception as e:
            print(f"Failed to download {url}: {e}")
            return None

    return f'modules/tennisfel/{local_path}'


def collect_image_urls(data):
    """Recursively extract all image URLs from the LegendKeeper data."""
    urls = set()

    def extract_urls(obj):
        if isinstance(obj, dict):
            # Check for URL keys
            if 'url' in obj and isinstance(obj['url'], str) and 'assets.legendkeeper.com' in obj['url']:
                urls.add(obj['url'])
            # Check for mapId keys (map document images)
            if 'mapId' in obj and isinstance(obj['mapId'], str) and 'assets.legendkeeper.com' in obj['mapId']:
                urls.add(obj['mapId'])
            # Recurse into dict values
            for value in obj.values():
                extract_urls(value)
        elif isinstance(obj, list):
            # Recurse into list items
            for item in obj:
                extract_urls(item)

    extract_urls(data)
    return urls


def convert_prosemirror_to_html(content, image_map, resource_id_map=None):
    """Convert Prosemirror/TipTap JSON to HTML."""
    if not content or not isinstance(content, dict):
        return ""

    if resource_id_map is None:
        resource_id_map = {}

    def process_node(node):
        if not isinstance(node, dict):
            return ""

        node_type = node.get('type', '')
        node_content = node.get('content', [])
        attrs = node.get('attrs', {})
        marks = node.get('marks', [])

        html = ""

        # Process based on node type
        if node_type == 'doc':
            # Root document node
            return ''.join(process_node(child) for child in node_content)

        elif node_type == 'heading':
            level = attrs.get('level', 2)
            inner = ''.join(process_node(child) for child in node_content)
            html = f'<h{level}>{inner}</h{level}>'

        elif node_type == 'paragraph':
            inner = ''.join(process_node(child) for child in node_content)
            html = f'<p>{inner}</p>' if inner else '<p></p>'

        elif node_type == 'text':
            text = node.get('text', '')
            # Apply marks (bold, italic, etc.)
            for mark in marks:
                mark_type = mark.get('type', '')
                if mark_type == 'strong':
                    text = f'<strong>{text}</strong>'
                elif mark_type == 'em':
                    text = f'<em>{text}</em>'
                elif mark_type == 'code':
                    text = f'<code>{text}</code>'
                elif mark_type == 'underline':
                    text = f'<u>{text}</u>'
                elif mark_type == 'strike':
                    text = f'<s>{text}</s>'
            html = text

        elif node_type == 'bulletList':
            inner = ''.join(process_node(child) for child in node_content)
            html = f'<ul>{inner}</ul>'

        elif node_type == 'orderedList':
            inner = ''.join(process_node(child) for child in node_content)
            html = f'<ol>{inner}</ol>'

        elif node_type == 'listItem':
            inner = ''.join(process_node(child) for child in node_content)
            html = f'<li>{inner}</li>'

        elif node_type == 'image':
            src = attrs.get('src', '')
            alt = attrs.get('alt', '')
            # Replace with local path if available
            if src in image_map:
                src = image_map[src]
            html = f'<img src="{src}" alt="{alt}" />'

        elif node_type == 'rule':
            html = '<hr />'

        elif node_type == 'codeBlock':
            inner = ''.join(process_node(child) for child in node_content)
            html = f'<pre><code>{inner}</code></pre>'

        elif node_type == 'blockquote':
            inner = ''.join(process_node(child) for child in node_content)
            html = f'<blockquote>{inner}</blockquote>'

        elif node_type == 'bodiedExtension':
            # LegendKeeper extensions like secrets
            ext_key = attrs.get('extensionKey', '')
            ext_title = attrs.get('parameters', {}).get('extensionTitle', 'Secret')
            inner = ''.join(process_node(child) for child in node_content)
            html = f'<div class="secret"><strong>{ext_title}:</strong> {inner}</div>'

        elif node_type == 'panel':
            panel_type = attrs.get('panelType', 'info')
            inner = ''.join(process_node(child) for child in node_content)
            html = f'<div class="panel panel-{panel_type}">{inner}</div>'

        elif node_type == 'layoutSection':
            inner = ''.join(process_node(child) for child in node_content)
            html = f'<div class="layout-section">{inner}</div>'

        elif node_type == 'layoutColumn':
            width = attrs.get('width', 50)
            inner = ''.join(process_node(child) for child in node_content)
            html = f'<div class="layout-column" style="width:{width}%">{inner}</div>'

        elif node_type == 'mention':
            # LegendKeeper mentions/links to other resources
            mention_text = attrs.get('text', '')
            resource_id = attrs.get('id', '')

            # Convert to Foundry UUID format if we have the mapping
            if resource_id in resource_id_map:
                mapping = resource_id_map[resource_id]
                foundry_id = mapping['id']
                doc_type = mapping['type']
                html = f'@UUID[{doc_type}.{foundry_id}]{{{mention_text}}}'
            else:
                # Fallback if resource not found
                html = mention_text

        elif node_type == 'inlineExtension':
            # Inline extensions like icons
            text = attrs.get('text', '')
            icon = attrs.get('parameters', {}).get('icon', '')
            html = f'<i class="{icon}"></i> {text}' if icon else text

        else:
            # Unknown node type, try to process children
            html = ''.join(process_node(child) for child in node_content)

        return html

    return process_node(content)


def classify_resource(resource):
    """Determine what type of Foundry document this resource should become."""
    # Check for map documents (Scenes)
    for doc in resource.get('documents', []):
        if doc.get('type') == 'map':
            # Check if the map document has a mapId (the actual map image)
            map_data = doc.get('map', {})
            map_id = map_data.get('mapId', '')
            if map_id and map_id.startswith('http'):
                return 'Scene'

            # Also check IMAGE properties as fallback
            for prop in resource.get('properties', []):
                if prop.get('type') == 'IMAGE':
                    url = prop.get('data', {}).get('url', '')
                    if url and url.startswith('http'):
                        return 'Scene'
            # If no image URL, treat as journal entry
            break

    # Default: Everything else becomes a Journal entry
    # (including characters, NPCs, creatures, items, artifacts, etc.)
    return 'JournalEntry'


def create_journal_entry(resource, image_map, resource_id_map=None):
    """Convert a LegendKeeper resource into a Foundry JournalEntry."""
    resource_id = generate_id()
    name = resource.get('name', 'Untitled')

    pages = []

    # Process each document as a journal page
    for doc in resource.get('documents', []):
        if doc.get('type') == 'page':
            page_id = generate_id()
            page_name = doc.get('name', 'Main')
            content = doc.get('content', {})

            html_content = convert_prosemirror_to_html(content, image_map, resource_id_map)

            page = {
                "_id": page_id,
                "name": page_name,
                "type": "text",
                "title": {
                    "show": True,
                    "level": 1
                },
                "text": {
                    "format": 1,
                    "content": html_content
                },
                "sort": len(pages)
            }
            pages.append(page)

    # If no pages, create a default one
    if not pages:
        pages.append({
            "_id": generate_id(),
            "name": "Main",
            "type": "text",
            "title": {"show": True, "level": 1},
            "text": {"format": 1, "content": "<p>No content</p>"},
            "sort": 0
        })

    # Get banner image if available
    banner_url = resource.get('banner', {}).get('url', '')
    if banner_url and banner_url in image_map:
        # Add banner as first image in first page
        pages[0]['text']['content'] = f'<img src="{image_map[banner_url]}" alt="{name}" />' + pages[0]['text']['content']

    entry = {
        "_id": resource_id,
        "name": name,
        "pages": pages,
        "folder": None,
        "sort": 0,
        "ownership": {"default": 0},
        "flags": {
            "tennisfel": {
                "legendkeeper_id": resource.get('id', ''),
                "tags": resource.get('tags', [])
            }
        }
    }

    return entry


def create_actor_entry(resource, image_map):
    """Convert a LegendKeeper resource into a Foundry Actor."""
    actor_id = generate_id()
    name = resource.get('name', 'Untitled')

    # Get IMAGE property for portrait
    img_url = "icons/svg/mystery-man.svg"  # Default Foundry icon
    for prop in resource.get('properties', []):
        if prop.get('type') == 'IMAGE':
            url = prop.get('data', {}).get('url', '')
            if url and url in image_map:
                img_url = image_map[url]
                break

    # Gather all content from documents
    biography = ""
    for doc in resource.get('documents', []):
        if doc.get('type') == 'page':
            content = doc.get('content', {})
            biography += convert_prosemirror_to_html(content, image_map)

    actor = {
        "_id": actor_id,
        "name": name,
        "type": "npc",
        "img": img_url,
        "system": {
            "biography": {
                "value": biography
            }
        },
        "prototypeToken": {
            "name": name,
            "displayName": 30,
            "actorLink": False,
            "width": 1,
            "height": 1,
            "texture": {
                "src": img_url
            }
        },
        "items": [],
        "effects": [],
        "folder": None,
        "sort": 0,
        "ownership": {"default": 0},
        "flags": {
            "tennisfel": {
                "legendkeeper_id": resource.get('id', ''),
                "tags": resource.get('tags', [])
            }
        }
    }

    return actor


def create_item_entry(resource, image_map):
    """Convert a LegendKeeper resource into a Foundry Item."""
    item_id = generate_id()
    name = resource.get('name', 'Untitled')

    # Get IMAGE property for item image
    img_url = "icons/svg/item-bag.svg"  # Default Foundry icon
    for prop in resource.get('properties', []):
        if prop.get('type') == 'IMAGE':
            url = prop.get('data', {}).get('url', '')
            if url and url in image_map:
                img_url = image_map[url]
                break

    # Gather all content from documents
    description = ""
    for doc in resource.get('documents', []):
        if doc.get('type') == 'page':
            content = doc.get('content', {})
            description += convert_prosemirror_to_html(content, image_map)

    item = {
        "_id": item_id,
        "name": name,
        "type": "equipment",
        "img": img_url,
        "system": {
            "description": {
                "value": description
            }
        },
        "effects": [],
        "folder": None,
        "sort": 0,
        "ownership": {"default": 0},
        "flags": {
            "tennisfel": {
                "legendkeeper_id": resource.get('id', ''),
                "tags": resource.get('tags', [])
            }
        }
    }

    return item


def create_scene_entry(resource, image_map):
    """Convert a LegendKeeper resource with map into a Foundry Scene."""
    scene_id = generate_id()
    name = resource.get('name', 'Untitled Scene')

    # Find map document
    map_doc = None
    for doc in resource.get('documents', []):
        if doc.get('type') == 'map':
            map_doc = doc
            break

    # Get the map image URL - first check the map document's mapId
    background_src = None
    if map_doc:
        map_data = map_doc.get('map', {})
        map_url = map_data.get('mapId', '')
        if map_url and map_url in image_map:
            background_src = image_map[map_url]

    # If not found, check IMAGE properties as fallback
    if not background_src:
        for prop in resource.get('properties', []):
            if prop.get('type') == 'IMAGE':
                url = prop.get('data', {}).get('url', '')
                if url and url in image_map:
                    background_src = image_map[url]
                    break

    scene = {
        "_id": scene_id,
        "name": name,
        "background": {
            "src": background_src
        },
        "width": 4096,
        "height": 4096,
        "padding": 0.25,
        "grid": {
            "type": 0,
            "size": 100,
            "color": "#000000",
            "alpha": 0.2
        },
        "tokens": [],
        "notes": [],
        "drawings": [],
        "lights": [],
        "sounds": [],
        "templates": [],
        "tiles": [],
        "walls": [],
        "folder": None,
        "sort": 0,
        "ownership": {"default": 0},
        "flags": {
            "tennisfel": {
                "legendkeeper_id": resource.get('id', ''),
                "tags": resource.get('tags', [])
            }
        }
    }

    return scene


def write_db_file(filename, entries):
    """Write entries to a NeDB format file (JSON-Lines)."""
    os.makedirs('packs', exist_ok=True)
    filepath = os.path.join('packs', filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        for entry in entries:
            # Write as compact JSON (no spaces, single line)
            json_str = json.dumps(entry, separators=(',', ':'), ensure_ascii=False)
            f.write(json_str + '\n')

    print(f"Wrote {len(entries)} entries to {filepath}")


def main():
    """Main conversion workflow."""
    print("Tennisfel LegendKeeper to Foundry VTT Converter")
    print("=" * 50)

    # Load LegendKeeper data
    print("\n1. Loading LegendKeeper data...")
    with open('legendkeeper/tennisfel.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    resources = data.get('resources', [])
    print(f"   Found {len(resources)} resources")

    # Collect and download images
    print("\n2. Collecting image URLs...")
    image_urls = collect_image_urls(data)
    print(f"   Found {len(image_urls)} image URLs")

    print("\n3. Downloading images...")
    image_map = {}

    # First, identify which URLs are map images
    map_urls = set()
    for resource in resources:
        for doc in resource.get('documents', []):
            if doc.get('type') == 'map':
                map_data = doc.get('map', {})
                map_id = map_data.get('mapId', '')
                if map_id:
                    map_urls.add(map_id)

    for idx, url in enumerate(image_urls, 1):
        print(f"   [{idx}/{len(image_urls)}] ", end='')

        # Determine category based on context
        if url in map_urls:
            category = 'maps'
        elif '/banner' in url.lower():
            category = 'banners'
        else:
            category = 'images'

        local_path = download_image(url, category)
        if local_path:
            image_map[url] = local_path

    print(f"   Successfully downloaded {len(image_map)} images")

    # Copy region map
    print("\n4. Copying region map...")
    os.makedirs('assets/maps', exist_ok=True)
    region_map_src = 'legendkeeper/tennisfel-region-map.webp'
    if os.path.exists(region_map_src):
        import shutil
        shutil.copy(region_map_src, 'assets/maps/tennisfel-region-map.webp')
        print("   Region map copied successfully")

    # First pass: Build resource ID mapping
    print("\n5. Building resource ID map...")
    resource_id_map = {}
    resource_foundry_ids = {}

    for resource in resources:
        legendkeeper_id = resource.get('id', '')
        foundry_id = generate_id()
        doc_type = classify_resource(resource)
        resource_id_map[legendkeeper_id] = {
            'id': foundry_id,
            'type': doc_type
        }
        resource_foundry_ids[legendkeeper_id] = {
            'foundry_id': foundry_id,
            'resource': resource,
            'doc_type': doc_type
        }

    print(f"   Created ID mapping for {len(resource_id_map)} resources")

    # Second pass: Convert resources with proper UUID links
    print("\n6. Converting resources...")
    journal_entries = []
    scenes = []

    for idx, (legendkeeper_id, data) in enumerate(resource_foundry_ids.items(), 1):
        resource = data['resource']
        foundry_id = data['foundry_id']
        doc_type = data['doc_type']
        name = resource.get('name', 'Untitled')

        print(f"   [{idx}/{len(resources)}] {name} -> {doc_type}")

        if doc_type == 'JournalEntry':
            entry = create_journal_entry(resource, image_map, resource_id_map)
            # Override the generated ID with the pre-assigned one
            entry['_id'] = foundry_id
            journal_entries.append(entry)
        elif doc_type == 'Scene':
            entry = create_scene_entry(resource, image_map)
            # Override the generated ID with the pre-assigned one
            entry['_id'] = foundry_id
            scenes.append(entry)

    # Write compendium packs
    print("\n7. Writing compendium packs...")
    write_db_file('tennisfel-journal.db', journal_entries)
    write_db_file('tennisfel-scenes.db', scenes)

    print("\n" + "=" * 50)
    print("Conversion complete!")
    print(f"  - Journal Entries: {len(journal_entries)}")
    print(f"  - Scenes: {len(scenes)}")
    print(f"  - Images downloaded: {len(image_map)}")
    print("=" * 50)


if __name__ == '__main__':
    main()
