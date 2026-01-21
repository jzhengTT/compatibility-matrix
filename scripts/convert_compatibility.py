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
from typing import Dict, Set

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


def get_performance_metrics(df: pd.DataFrame, model_name: str, device_name: str) -> Dict:
    """Extract performance metrics for a model-device pair."""
    # Define the metrics we want to include
    target_metrics = ['mean_ttft_ms', 'ttft', 'mean_tps', 'accuracy_check']

    # Filter data for this specific model-device combination
    pair_data = df[
        (df['ml_model_name'] == model_name) &
        (df['device_name'] == device_name) &
        (df['metric_name'].isin(target_metrics)) &
        (df['metric_value'].notna())
    ]

    metrics = {}
    for _, row in pair_data.iterrows():
        metric_name = row['metric_name']
        metric_value = row['metric_value']

        # Convert metric value to appropriate type
        if metric_name == 'accuracy_check':
            # Treat non-zero values as True, zero/null as False
            metrics[metric_name] = bool(metric_value != 0)
        else:
            # Keep numeric metrics as numbers
            metrics[metric_name] = float(metric_value)

    return metrics


def convert_excel_to_json(excel_path: str, output_path: str) -> None:
    """Convert compatibility Excel file to JSON format."""
    print(f"Reading {excel_path}...")
    df = pd.read_excel(excel_path)

    # Filter out rows with null model or device names
    df = df[df['ml_model_name'].notna() & df['device_name'].notna()]

    # Get unique model names from the data
    unique_model_names: Set[str] = set(df['ml_model_name'].unique())

    # Get unique device names from the data
    unique_device_names: Set[str] = set(df['device_name'].unique())

    # Build models dictionary
    models_dict: Dict[str, Dict] = {}

    total_supported = 0
    total_not_supported = 0

    # For each model, create entries for ALL hardware platforms
    for model_name in unique_model_names:
        models_dict[model_name] = create_model_entry(model_name)

        # Create an entry for each hardware platform
        for device_name, hardware_name in DEVICE_MAPPING.items():
            # Get performance metrics for this model-device pair
            metrics = get_performance_metrics(df, model_name, device_name)

            # Build compatibility entry
            compatibility_entry = {
                'hardware': hardware_name,
                'status': 'Supported' if metrics else 'Not Supported',
            }

            # Add metrics if available
            if metrics:
                compatibility_entry['metrics'] = metrics
                total_supported += 1
            else:
                total_not_supported += 1

            models_dict[model_name]['compatibility'].append(compatibility_entry)

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
