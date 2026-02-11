# Excel to JSON Conversion Script

This script converts the Tenstorrent compatibility Excel file ([data/compatibility.xlsx](data/compatibility.xlsx)) to a JSON format that matches the schema defined in [docs/mock-model-data.json](docs/mock-model-data.json).

## Requirements

- Python 3.7+
- pandas
- openpyxl

Install dependencies:
```bash
source venv/bin/activate  # Activate virtual environment
pip install -r requirements.txt
```

## Usage

### Convert Excel to JSON

```bash
python convert_excel_to_json.py
```

This will:
- Read `data/compatibility.xlsx`
- Convert it to the JSON schema format
- Output to `data/compatibility.json`

### Inspect Excel Structure

To inspect the Excel file structure before conversion:

```bash
python convert_excel_to_json.py --inspect
```

This will display:
- Sheet names
- Column names and types
- Sample data
- Unique model names and devices
- Available metrics

## Input Data Structure

The Excel file contains benchmark run data with the following columns:
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
    "source": "compatibility.xlsx",
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

The script maps device names to display names:
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

The conversion script generates a simplified, flattened schema focused on compatibility information:
- **Flattened structure**: Each model variant (e.g., "LLaMA-3 8B FP16") is a top-level entry in the models array
- **No variants nesting**: No nested "variants" array - each precision/configuration is its own model entry
- **No performance metrics**: Throughput and latency data are excluded
- **No software stack**: Framework and version details are excluded
- **Essential compatibility only**: Just hardware device, support status, and availability timeline

This means if a model has multiple precisions (FP16, FP8, etc.), each precision appears as a separate model entry with its own compatibility list.

## Customization

You can customize the script by modifying:
- `HARDWARE_MAPPING` - Add or modify hardware device mappings
- `TASK_MAPPING` - Define tasks for different model types
- `get_model_family()` - Customize model family extraction logic
- `extract_parameters()` - Customize parameter count extraction

## Output

After successful conversion, you'll see:
```
Processing 4090 rows from Excel file...

Successfully converted Excel to JSON!
Input:  data/compatibility.xlsx
Output: data/compatibility.json
Models: 30
Variants: 30
Hardware compatibility entries: 50

Conversion complete! You can now use data/compatibility.json in your app.
```

The generated `data/compatibility.json` file is ready to be used in your Tenstorrent Compatibility Matrix application.
