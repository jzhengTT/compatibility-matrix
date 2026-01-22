#!/usr/bin/env python3
"""
Convert database compatibility data to JSON format following the mock-model-data.json schema.
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
    save_new_entries_to_file,
)
from db_config import execute_query


def load_data_from_database() -> pd.DataFrame:
    """Fetch compatibility data from database and return as DataFrame."""
    print("Fetching data from database...")
    try:
        results = execute_query('fetch_compatibility_data.sql')
    except Exception as e:
        print(f"Error: Failed to connect to database or execute query: {e}")
        return pd.DataFrame()

    df = pd.DataFrame(results)

    if df.empty:
        print("Error: No data returned from database")
        return df

    print(f"Loaded {len(df)} rows from database")
    return df[df['ml_model_name'].notna() & df['device_name'].notna()]


def discover_new_entries(df: pd.DataFrame) -> Tuple[Set[str], Set[str]]:
    """
    Find models and devices in the database that are not in config mappings.
    Returns (new_models, new_devices).
    """
    db_models = set(df['ml_model_name'].unique())
    db_devices = set(df['device_name'].unique())

    new_models = db_models - set(MODEL_MAPPING.keys())
    new_devices = db_devices - set(DEVICE_MAPPING.keys())

    return new_models, new_devices


def handle_new_entries(new_models: Set[str], new_devices: Set[str]) -> None:
    """
    Save new models and devices to a file for manual review.
    New entries will NOT be included in the output until added to config.py.
    """
    if new_devices or new_models:
        save_new_entries_to_file(new_models=new_models, new_devices=new_devices)

def build_compatibility_entry(
    df: pd.DataFrame,
    model_name: str,
    device_name: str,
    hardware_name: str
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


def convert_database_to_json(output_path: str) -> None:
    """
    Convert database compatibility data to JSON format.
    Only processes models and devices that are configured in config.py.
    """
    df = load_data_from_database()

    if df.empty:
        print("Stopping: Cannot proceed without data from database.")
        return

    # Check for new entries and save them to file
    new_models, new_devices = discover_new_entries(df)
    if new_models or new_devices:
        handle_new_entries(new_models, new_devices)

    # Only process configured entries
    configured_models = MODEL_MAPPING.keys()
    configured_devices = DEVICE_MAPPING

    models_dict: Dict[str, Dict] = {}
    total_supported = 0
    total_not_supported = 0

    for model_name in configured_models:
        models_dict[model_name] = create_model_entry(model_name)

        for device_name, hardware_name in configured_devices.items():
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
            'source': 'database',
            'schema_version': '1.0',
        },
        'models': models_list,
    }

    print(f"\nWriting to {output_path}...")
    with open(output_path, 'w') as f:
        json.dump(output_data, f, indent=2)

    print_summary(
        configured_models,
        set(configured_devices.keys()),
        total_supported,
        total_not_supported,
        len(models_list),
        output_path,
        new_models=new_models,
        new_devices=new_devices,
    )

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    output_path = os.path.join(project_root, 'data', 'compatibility.json')

    print("Converting database data to JSON...")
    print()

    convert_database_to_json(output_path=output_path)
