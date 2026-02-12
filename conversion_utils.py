#!/usr/bin/env python3
"""
Shared utility functions for compatibility data conversion.
Used by db_to_json.py.
"""

import os
import re
from datetime import datetime, timezone
from typing import Dict, Set

import pandas as pd

from config import DEVICE_MAPPING, MODEL_MAPPING


def create_model_id(model_name: str) -> str:
    """Create a kebab-case ID from model name."""
    return re.sub(r'[.\s_]+', '-', model_name.lower())


def get_model_config(model_name: str) -> Dict:
    """Get model configuration, with fallback for unknown models."""
    if config := MODEL_MAPPING.get(model_name):
        return {
            'display_name': config['display_name'],
            'family': config['family'],
            'tasks': config['tasks'],
        }

    print(f"Warning: Model '{model_name}' not found in MODEL_MAPPING. Please add it to config.py")
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
    new_models: Set[str] = None,
    new_devices: Set[str] = None,
) -> None:
    """Print conversion summary with unique names and warnings about new entries."""
    _print_new_entry_warnings(new_models, new_devices)
    _print_conversion_stats(model_count, total_supported, total_not_supported, output_path)
    _print_unique_names(unique_model_names, unique_device_names)


def _print_new_entry_warnings(new_models: Set[str], new_devices: Set[str]) -> None:
    """Print warnings about new models and devices."""
    for entries, label in [(new_models, 'model(s)'), (new_devices, 'device(s)')]:
        if entries:
            print(f"\n{'!'*80}")
            print(f"WARNING: Found {len(entries)} new {label} in database:")
            print(f"{'!'*80}")
            for entry in sorted(entries):
                print(f"  - {entry}")
            print(f"\nThese {label.rstrip('(s)')}s will be EXCLUDED from output until added to config.py.")


def _print_conversion_stats(model_count: int, total_supported: int,
                            total_not_supported: int, output_path: str) -> None:
    """Print conversion statistics."""
    print(f"\nSuccessfully converted {model_count} models to JSON format")
    print(f"  - {total_supported} Supported combinations")
    print(f"  - {total_not_supported} Not Supported combinations")
    print(f"Output written to {output_path}")


def _print_unique_names(unique_model_names: Set[str], unique_device_names: Set[str]) -> None:
    """Print unique model and device names."""
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
        display = f"{device} -> {mapped_name}" if mapped_name != device else device
        print(f"  - {display}")


def get_performance_metrics(df: pd.DataFrame, model_name: str, device_name: str) -> Dict:
    """Extract performance metrics for a model-device pair."""
    target_metrics = ['mean_ttft_ms', 'ttft', 'mean_tps', 'accuracy_check']

    pair_data = df[
        (df['ml_model_name'] == model_name) &
        (df['device_name'] == device_name) &
        (df['metric_name'].isin(target_metrics)) &
        (df['metric_value'].notna())
    ]

    metrics = {}
    for _, row in pair_data.iterrows():
        metric_name, metric_value = row['metric_name'], row['metric_value']
        metrics[metric_name] = (bool(metric_value != 0) if metric_name == 'accuracy_check'
                               else float(metric_value))

    return metrics


def save_new_entries_to_file(new_models: Set[str], new_devices: Set[str]) -> None:
    """
    Save new models and devices to a separate file for manual review.
    Creates a file called 'new_entries.txt' in the scripts directory.
    """
    if not new_models and not new_devices:
        return

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, 'new_entries.txt')

    sections = []
    sections.append(_create_header())

    if new_devices:
        sections.append(_create_device_section(new_devices))

    if new_models:
        sections.append(_create_model_section(new_models))

    sections.append(_create_instructions())

    with open(output_file, 'w') as f:
        f.write('\n'.join(sections))

    print(f"\n{'='*80}")
    print(f"WARNING: New entries detected and saved to: {output_file}")
    print(f"{'='*80}")


