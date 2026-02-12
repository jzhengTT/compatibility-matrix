# Tenstorrent Compatibility Matrix Pipeline

Data pipeline for converting Tenstorrent compatibility data from multiple sources (PostgreSQL database and Excel files) to JSON format for the Compatibility Matrix application.

## Overview

This pipeline processes benchmark run data and converts it to a JSON format that matches the compatibility matrix schema. It supports two data sources:

1. **PostgreSQL Database**: Fetches live data from the Tenstorrent database
2. **Excel Files**: Processes local Excel files with compatibility data

## Requirements

- Python 3.7+
- pandas
- openpyxl
- psycopg2-binary
- python-dotenv
- boto3 (for S3 operations)

## Setup

1. Create a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your actual credentials
```

## Usage

### Convert Database to JSON

Fetch data from PostgreSQL and convert to JSON:

```bash
python db_to_json.py
```

This will:
- Connect to the PostgreSQL database
- Fetch compatibility data using the SQL query
- Convert it to the JSON schema format
- Output to `data/compatibility.json`

### Convert Excel to JSON

Process local Excel files:

```bash
python excel_to_json.py
```

This will:
- Read `data/compatibility.xlsx`
- Convert it to the JSON schema format
- Output to `data/compatibility.json`

### Inspect Data Structure

To inspect the Excel file structure before conversion:

```bash
python excel_to_json.py --inspect
```

This will display:
- Sheet names
- Column names and types
- Sample data
- Unique model names and devices
- Available metrics

## Configuration

The pipeline uses several configuration files:

- **[config.py](config.py)**: Central configuration (hardware mappings, model families)
- **[db_config.py](db_config.py)**: Database connection settings
- **[conversion_utils.py](conversion_utils.py)**: Shared conversion utilities

## Input Data Structure

The source data contains benchmark run information with columns:
- `github_pipeline_id` - GitHub Actions pipeline ID
- `pipeline_end_ts` - Timestamp when the pipeline ended
- `ml_model_name` - Name of the ML model (e.g., "Llama-3.1-8B-Instruct")
- `device_name` - Tenstorrent hardware device (e.g., "t3k", "n150", "p150x4")
- `isl` - Input sequence length
- `osl` - Output sequence length
- `batch_size` - Batch size used in benchmark
- `precision` - Model precision (defaults to "FP16" if not specified)
- `benchmark_run_id` - Unique ID for the benchmark run
- `step_name` - Pipeline step name
- `metric_name` - Name of the performance metric
- `metric_value` - Value of the performance metric

## Output JSON Structure

The generated JSON follows this simplified schema:

```json
{
  "metadata": {
    "generated_at": "ISO-8601 timestamp",
    "source": "database or Excel file",
    "schema_version": "1.0"
  },
  "models": [
    {
      "id": "model-id-precision",
      "display_name": "Model Name Precision",
      "family": "Model Family",
      "tasks": ["Task1", "Task2"],
      "description": "Model description",
      "links": {
        "huggingface": "https://...",
        "github": "https://..."
      },
      "editorial_notes": [],
      "parameters": "8B",
      "precision": "FP16",
      "context_window": 8192,
      "compatibility": [
        {
          "hardware": "n150 (Wormhole)",
          "status": "Supported"
        },
        {
          "hardware": "p100 (Blackhole)",
          "status": "Coming Soon",
          "estimated_availability": "Q2 2025"
        }
      ]
    }
  ]
}
```

**Note:** The schema focuses on essential compatibility information only:
- **hardware**: Display name of the hardware device
- **status**: Support status ("Supported", "Coming Soon", "Deprecated")
- **estimated_availability** (optional): Expected availability date for "Coming Soon" items

## Hardware Mapping

The pipeline maps device names to display names:
- `n300x4` → QuietBox (Wormhole)
- `p150x4` → QuietBox (Blackhole)
- `t3k` → LoudBox (Wormhole)
- `loudbox-bh` → LoudBox (Blackhole)
- `galaxy` → Galaxy (Wormhole)
- `galaxy-bh` → Galaxy (Blackhole)
- `n150` → n150 (Wormhole)
- `n300` → n300 (Wormhole)
- `p100` → p100 (Blackhole)
- `p150` → p150 (Blackhole)
- `p300` → p300 (Blackhole)

## Schema Simplification

The conversion generates a simplified, flattened schema focused on compatibility information:
- **Flattened structure**: Each model variant (e.g., "LLaMA-3 8B FP16") is a top-level entry
- **No variants nesting**: Each precision/configuration is its own model entry
- **No performance metrics**: Throughput and latency data are excluded
- **No software stack**: Framework and version details are excluded
- **Essential compatibility only**: Just hardware device, support status, and availability timeline

## Customization

You can customize the pipeline by modifying:
- `HARDWARE_MAPPING` in [config.py](config.py) - Add or modify hardware device mappings
- `TASK_MAPPING` in [config.py](config.py) - Define tasks for different model types
- `get_model_family()` - Customize model family extraction logic
- `extract_parameters()` - Customize parameter count extraction

## License

[Add license information]
