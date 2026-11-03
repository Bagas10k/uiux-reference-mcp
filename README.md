# UI/UX Reference MCP Server

Curated Design System Reference Library & Creative Archetype Explorer for Autonomous AI Agents via the Model Context Protocol (MCP).

**Author:** Bagas Cihuy & Hermes Agent  
**License:** MIT

---

## Overview

`uiux-reference-mcp` connects AI agents directly to a curated catalog of 100+ verified high-craft design references (SaaS landing pages, agency portfolios, high-density admin dashboards, e-commerce, and creative archetypes). It allows agents to search, view visual patterns, generate moodboards, and extract design recipes without falling back on generic AI templates.

## Features

- **Semantic Catalog Search**: Query design references by keyword, aesthetic style, industry, or curated tags.
- **Visual Asset Inspection**: Retrieve exact file paths, aspect ratios, color palettes, and structural layouts of real-world award-winning web designs.
- **Creative Archetypes**: Access 5 signature design worldviews:
  1. *Swiss Editorial Brutalism* (warm paper, compressed display typography, single bold accent).
  2. *Neo-Brutalism High Contrast* (hard offset shadows, 2.5px solid ink borders, pop colors).
  3. *Liquid Gooey & Jelly Morphing* (two-layer silhouettes, organic fluid states, zero-layout-shift).
  4. *Console-First HUD* (dense monospace tabular layouts, telemetry streams, zero-slop instruments).
  5. *Spatial Tactile & Progressive Frosted Glass* (tactile depth, progressive multi-layer blur, spring physics).
- **Component Recipes**: Proven code snippets and CSS formulas for tactile buttons, command search bars, bento grids, and interactive states.

## Available Tools

1. `uiux_search(query, category, limit)`: Search design references in the catalog.
2. `uiux_view(item_id)`: Retrieve detailed design spec, palette, and typography for a reference.
3. `uiux_reference_board(category)`: Generate a multi-asset reference board for project kickoffs.
4. `uiux_creative_archetypes()`: List the 5 signature design worldviews and token palettes.
5. `uiux_get_component_recipe(component_name)`: Get production-ready CSS/JS implementation recipes.
6. `uiux_extract_patterns(item_id)`: Extract actionable spatial grids, contrast tokens, and interaction rules from a reference.

## Installation & Configuration

### Prerequisites
- Python 3.10+
- `mcp` Python SDK: `pip install mcp`

### Connecting to Hermes Agent (`~/.hermes/config.yaml`)

```yaml
mcp_servers:
  uiux-reference:
    command: /home/ubuntu/.hermes/hermes-agent/venv/bin/python
    args:
      - /path/to/mcp-uiux-reference/server.py
    enabled: true
```
