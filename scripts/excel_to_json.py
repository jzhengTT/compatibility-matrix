#!/usr/bin/env python3
"""
Convert Excel compatibility data to JSON format following the mock-model-data.json schema.
Only includes compatibility information with performance metrics.
A model-device pair is "Supported" if it has any non-zero, non-null metric,
otherwise it is marked as "Not Supported".

Configuration (device mappings, task mappings, etc.) is in config.py
"""

import json
import os
from datetime import datetime, timezone
from typing import Dict, Set, Tuple

import pandas as pd

from config import DEVICE_MAPPING, MODEL_MAPPING
from conversion_utils import (
    create_model_entry,
    get_performance_metrics,
    print_summary,
    update_config_file,
)


def discover_new_entries(df: pd.DataFrame) -> Tuple[Set[str], Set[str]]:
    """
    Find models and devices in the Excel data that are not in config mappings.
    Returns (new_models, new_devices).
    """
    excel_model_names = set(df['ml_model_name'].unique())
    excel_device_names = set(df['device_name'].unique())

    new_models = excel_model_names - set(MODEL_MAPPING.keys())
    new_devices = excel_device_names - set(DEVICE_MAPPING.keys())

    return new_models, new_devices


def register_new_entries(new_models: Set[str], new_devices: Set[str]) -> Dict[str, str]:
    """
    Register new models and devices, updating config as needed.
    Returns a temporary mapping of new devices to their display names.
    """
    new_device_mappings = {}

    if new_models:
        print(f"\nFound {len(new_models)} new model(s) in Excel:")
        for model in sorted(new_models):
            print(f"  - {model}")

    if new_devices:
        print(f"\nFound {len(new_devices)} new device(s) in Excel:")
        for device in sorted(new_devices):
            display_name = device.capitalize()
            new_device_mappings[device] = display_name
            print(f"  - {device} -> {display_name}")

    if new_devices or new_models:
        update_config_file(new_devices=new_devices, new_models=new_models)

    return new_device_mappings


def build_compatibility_entry(
    df: pd.DataFrame, model_name: str, device_name: str, hardware_name: str
) -> Tuple[Dict, bool]:
    """
    Build a compatibility entry for a model-device pair.
    Returns (entry_dict, is_supported).
    """
    metrics = get_performance_metrics(df, model_name, device_name)
    is_supported = bool(metrics)

    entry = {
        'hardware': hardware_name,
        'status': 'Supported' if is_supported else 'Not Supported',
    }
    if metrics:
        entry['metrics'] = metrics

    return entry, is_supported


def convert_excel_to_json(excel_path: str, output_path: str) -> None:
    """Convert compatibility Excel file to JSON format."""
    print(f"Reading {excel_path}...")
    df = pd.read_excel(excel_path)

    # Filter out rows with null model or device names
    df = df[df['ml_model_name'].notna() & df['device_name'].notna()]

    new_models, new_devices = discover_new_entries(df)
    new_device_mappings = register_new_entries(new_models, new_devices)

    # Combine existing and new entries (without mutating originals)
    unique_model_names = set(MODEL_MAPPING.keys()) | new_models
    all_device_mappings = {**DEVICE_MAPPING, **new_device_mappings}
    unique_device_names = set(all_device_mappings.keys())

    models_dict: Dict[str, Dict] = {}
    total_supported = 0
    total_not_supported = 0

    for model_name in unique_model_names:
        models_dict[model_name] = create_model_entry(model_name)

        for device_name, hardware_name in all_device_mappings.items():
            entry, is_supported = build_compatibility_entry(df, model_name, device_name, hardware_name)
            models_dict[model_name]['compatibility'].append(entry)

            if is_supported:
                total_supported += 1
            else:
                total_not_supported += 1

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

    excel_path = os.path.join(project_root, 'data', 'compatibility.xlsx')
    output_path = os.path.join(project_root, 'data', 'compatibility.json')

    print("Converting Excel data to JSON...")
    print()

    convert_excel_to_json(excel_path=excel_path, output_path=output_path)
