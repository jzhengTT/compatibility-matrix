#!/usr/bin/env python3
"""
Convert compatibility.xlsx to JSON format following the mock-model-data.json schema.
Only includes compatibility information, no performance metrics.
A model-device pair is "Supported" if it has any non-zero, non-null metric,
otherwise it is marked as "Not Supported".

Configuration (device mappings, task mappings, etc.) is in config.py
"""

import json
import os
from datetime import datetime, timezone
from typing import Dict, Set, Tuple

import pandas as pd

from config import DEVICE_MAPPING, MODELS_CONFIG


def create_model_id(model_name: str) -> str:
    """Create a kebab-case ID from model name."""
    return model_name.lower().replace('.', '-').replace('_', '-').replace(' ', '-')


def get_model_config(model_name: str) -> Dict:
    """Get model configuration, with fallback for unknown models."""
    config = MODELS_CONFIG.get(model_name)
    if config:
        return {
            'display_name': config['display_name'],
            'family': config['family'],
            'tasks': config['tasks'],
        }

    print(f"Warning: Model '{model_name}' not found in MODELS_CONFIG. Please add it to config.py")
    return {
        'display_name': model_name,
        'family': 'Other',
        'tasks': ['Unknown'],
    }


def create_model_entry(model_name: str) -> Dict:
    """Create a new model entry with configuration."""
    config = get_model_config(model_name)
    return {
        'id': create_model_id(model_name),
        'display_name': config['display_name'],
        'family': config['family'],
        'tasks': config['tasks'],
        'compatibility': [],
    }


def print_summary(
    unique_model_names: Set[str],
    unique_device_names: Set[str],
    total_supported: int,
    total_not_supported: int,
    model_count: int,
    output_path: str,
) -> None:
    """Print conversion summary with unique names."""
    print(f"Successfully converted {model_count} models to JSON format")
    print(f"  - {total_supported} Supported combinations")
    print(f"  - {total_not_supported} Not Supported combinations")
    print(f"Output written to {output_path}")

    separator = "=" * 60

    print(f"\n{separator}")
    print(f"UNIQUE MODEL NAMES ({len(unique_model_names)}):")
    print(separator)
    for model in sorted(unique_model_names):
        print(f"  - {model}")

    print(f"\n{separator}")
    print(f"UNIQUE DEVICE NAMES ({len(unique_device_names)}):")
    print(separator)
    for device in sorted(unique_device_names):
        mapped_name = DEVICE_MAPPING.get(device, device)
        if mapped_name != device:
            print(f"  - {device} -> {mapped_name}")
        else:
            print(f"  - {device}")


def convert_excel_to_json(excel_path: str, output_path: str) -> None:
    """Convert compatibility Excel file to JSON format."""
    print(f"Reading {excel_path}...")
    df = pd.read_excel(excel_path)

    # Filter out rows with null model or device names
    df = df[df['ml_model_name'].notna() & df['device_name'].notna()]

    # Get all model-device combinations
    all_combinations = df[['ml_model_name', 'device_name']].drop_duplicates()

    # Filter for valid compatibility data (non-zero and non-null metrics)
    valid_data = df[(df['metric_value'].notna()) & (df['metric_value'] != 0)]

    # Get unique model-device combinations that are supported
    supported_combinations: Set[Tuple[str, str]] = set(
        tuple(row) for row in valid_data[['ml_model_name', 'device_name']].drop_duplicates().values
    )

    # Collect unique names for summary
    unique_model_names: Set[str] = set(all_combinations['ml_model_name'])
    unique_device_names: Set[str] = set(all_combinations['device_name'])

    # Build models dictionary
    models_dict: Dict[str, Dict] = {}

    for _, row in all_combinations.iterrows():
        model_name = row['ml_model_name']
        device_name = row['device_name']

        if model_name not in models_dict:
            models_dict[model_name] = create_model_entry(model_name)

        is_supported = (model_name, device_name) in supported_combinations
        hardware_name = DEVICE_MAPPING.get(device_name, device_name)

        models_dict[model_name]['compatibility'].append({
            'hardware': hardware_name,
            'status': 'Supported' if is_supported else 'Not Supported',
        })

    # Sort models by ID for consistent output
    models_list = sorted(models_dict.values(), key=lambda x: x['id'])

    output_data = {
        'metadata': {
            'generated_at': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'source': 'compatibility.xlsx',
            'schema_version': '1.0',
        },
        'models': models_list,
    }

    print(f"Writing to {output_path}...")
    with open(output_path, 'w') as f:
        json.dump(output_data, f, indent=2)

    total_supported = len(supported_combinations)
    total_not_supported = len(all_combinations) - total_supported

    print_summary(
        unique_model_names,
        unique_device_names,
        total_supported,
        total_not_supported,
        len(models_list),
        output_path,
    )


if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    convert_excel_to_json(
        excel_path=os.path.join(project_root, 'data', 'compatibility.xlsx'),
        output_path=os.path.join(project_root, 'data', 'compatibility.json'),
    )
