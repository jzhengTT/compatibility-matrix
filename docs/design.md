# Tenstorrent Compatibility Matrix – Engineering Design Spec

> **Audience:** Claude Code / frontend & platform engineers  
> **Purpose:** Canonical, implementation-ready design doc for the Tenstorrent Compatibility Matrix  
> **Source:** Transformed from internal Compatibility Matrix design notes

---

## Purpose & Scope

The **Compatibility Matrix** is a core component of the Tenstorrent developer experience. It enables developers, researchers, customers, and internal teams to understand:

- Which **models** are supported by Tenstorrent
- Which **Tenstorrent hardware** (hardware + cloud) is supported
- Which **software stacks and versions** are required
- **Performance characteristics** per model variant
- **Support status** and future availability timelines

This redesign replaces the existing implementation on  
https://tenstorrent.com/en/developers, which is currently out of date and difficult to scale.

The app will not contain any backend. It'll simply read from an included .json file for all the information.

The app will two routes.
1. The first route is simple the main page that contains all the search and filters.
2. The second route is a model details page that shows additional information for the model.

---

## 2. Primary User Journeys

### U1 – Browse by task
**User:** New developer  
**Goal:** Identify models by task (e.g. Text Generation)

**Acceptance Criteria**
- Filter by task updates results immediately
- Empty state explains *why* no models are shown
- Editorial context is visible at the model level

---

### U2 – Model → hardware compatibility
**User:** Developer  
**Goal:** Check if a specific model runs on specific hardware  
**Example:** *Does LLaMA-3 8B run on Blackhole p100a?*

**Acceptance Criteria**
- Search by model name
- Compatibility table clearly shows:
  - Hardware
  - Support status
  - Supported software + versions
- “Coming Soon” entries include ETA when available

---

### U3 – Hardware → supported ecosystem
**User:** Customer / Sales / Solutions  
**Goal:** Share a URL listing everything supported on a given hardware SKU

**Acceptance Criteria**
- Hardware detail page exists
- URL is stable and externally shareable
- Page lists:
  - Supported models
  - Variants
  - Software stacks + versions

---

### U4 – Performance visibility
**User:** Researcher / advanced developer  
**Goal:** Understand performance characteristics and trends

**Acceptance Criteria**
- Performance metrics shown per variant
- Historical data visualized as time series
- Units are explicit (tokens/sec, ms, etc.)

---

## Data Contract

See mock-model-data.json for JSON file that this app will consume. This JSON file is the **single source of truth** consumed by the website.

## Search and filters
The app will users to search and filter by the following

### Searchable Fields
- Model name
- Task
- Tenstorrent hardware

### Filter Facets
- Task
- Model
- Hardware
- Support status

## Possible values for search and filters
### Tasks
- LLM
- Text-to-Image
- Image-Generation
- Speech-to-Text
- Text-to-Speech
- NLP
- Vision

### Model family
- LlaMA
- DeepSeek
- Qwen
- Falcon

### Hardware
- QuietBox (Wormhole), device_name = n300x4
- QuietBox (Blackhole), device_name = p150x4
- LoudBox (Wormhole), device_name = t3k
- LoudBox (Blackhole), device_name = loudbox-bh
- Galaxy (Wormhole), device_name = galaxy
- Galaxy (Blackhole), device_name = galaxy-bh
- n150 (Wormhole), device_name = n150
- n300 (Wormhole), device_name = n300
- p100 (Blackhole), device_name = p100
- p150 (Blackhole), device_name = p150
- p300 (Blackhole), device_name = p300

### Status
- Supported
- Coming Soon
- Deprecated

## Non-Functional Requirements
- Frontend is read-only
    - Graceful fallback for:
    - Missing JSON
    - Invalid JSON
- Clear explanation of what “Supported” means