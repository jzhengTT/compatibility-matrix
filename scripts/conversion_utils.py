#!/usr/bin/env python3
"""
Shared utility functions for compatibility data conversion.
Used by both db_to_json.py and excel_to_json.py.
"""

import os
import re
from datetime import datetime, timezone
from typing import Dict, Set

import pandas as pd

from config import DEVICE_MAPPING, MODEL_MAPPING


def create_model_id(model_name: str) -> str:
    """Create a kebab-case ID from model name."""
    return model_name.lower().replace('.', '-').replace('_', '-').replace(' ', '-')


def get_model_config(model_name: str) -> Dict:
    """Get model configuration, with fallback for unknown models."""
    config = MODEL_MAPPING.get(model_name)
    if config:
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


def save_new_entries_to_file(new_models: Set[str], new_devices: Set[str]) -> None:
    """
    Save new models and devices to a separate file for manual review.
    Creates a file called 'new_entries.txt' in the scripts directory.
    """
    if not new_models and not new_devices:
        return

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, 'new_entries.txt')

    with open(output_file, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("NEW MODELS AND DEVICES DETECTED\n")
        f.write("=" * 80 + "\n")
        f.write(f"Generated at: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
        f.write("\nThese entries need to be added to config.py manually.\n")
        f.write("=" * 80 + "\n\n")

        if new_devices:
            f.write(f"NEW DEVICES ({len(new_devices)}):\n")
            f.write("-" * 80 + "\n")
            f.write("Add these entries to the DEVICE_MAPPING dictionary in config.py:\n\n")
            for device in sorted(new_devices):
                display_name = device.capitalize()
                f.write(f"    '{device}': '{display_name}',\n")
            f.write("\n")

        if new_models:
            f.write(f"NEW MODELS ({len(new_models)}):\n")
            f.write("-" * 80 + "\n")
            f.write("Add these entries to the MODEL_MAPPING dictionary in config.py:\n\n")
            for model in sorted(new_models):
                f.write(f"    '{model}': {{\n")
                f.write(f"        'display_name': '{model}',\n")
                f.write(f"        'family': 'Other',  # TODO: Update with correct family\n")
                f.write(f"        'tasks': ['Unknown']  # TODO: Update with correct tasks\n")
                f.write(f"    }},\n\n")

        f.write("=" * 80 + "\n")
        f.write("INSTRUCTIONS:\n")
        f.write("=" * 80 + "\n")
        f.write("1. Review the entries above\n")
        f.write("2. Update display names, families, and tasks as needed\n")
        f.write("3. Copy the entries to the appropriate section in config.py\n")
        f.write("4. Delete or archive this file once you've updated config.py\n")

    print(f"\n{'='*80}")
    print(f"WARNING: New entries detected and saved to: {output_file}")
    print(f"{'='*80}")


def update_config_file(new_devices: Set[str] = None, new_models: Set[str] = None) -> None:
    """
    Update config.py with new devices and models.

    Args:
        new_devices: Set of new device names to add to DEVICE_MAPPING
        new_models: Set of new model names to add to MODEL_MAPPING
    """
    if not new_devices and not new_models:
        return

    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, 'config.py')

    # Read the current config file
    with open(config_path, 'r') as f:
        content = f.read()

    # Add new devices to DEVICE_MAPPING
    if new_devices:
        # Find the DEVICE_MAPPING dictionary
        device_mapping_pattern = r"(DEVICE_MAPPING = \{[^}]*)(})"

        # Generate new device entries
        new_entries = []
        for device in sorted(new_devices):
            display_name = device.capitalize()
            new_entries.append(f"    '{device}': '{display_name}',")

        # Insert new entries before the closing brace
        def replace_device_mapping(match):
            existing_content = match.group(1)
            closing_brace = match.group(2)

            # Ensure existing content ends with a comma and newline
            content = existing_content.rstrip()
            if not content.endswith(','):
                content += ','

            return content + '\n' + '\n'.join(new_entries) + '\n' + closing_brace

        content = re.sub(device_mapping_pattern, replace_device_mapping, content, flags=re.DOTALL)

        print(f"\nAdded {len(new_devices)} new device(s) to config.py:")
        for device in sorted(new_devices):
            print(f"  - {device}")

    # Add new models to MODEL_MAPPING
    if new_models:
        # Find the MODEL_MAPPING dictionary (ends before the script closes)
        model_mapping_pattern = r"(MODEL_MAPPING = \{[^}]*)(}\s*\n)"

        # Generate new model entries
        new_entries = []
        for model in sorted(new_models):
            new_entries.append(f"\n    # Auto-added model")
            new_entries.append(f"    '{model}': {{")
            new_entries.append(f"        'display_name': '{model}',")
            new_entries.append(f"        'family': 'Other',")
            new_entries.append(f"        'tasks': ['Unknown']")
            new_entries.append(f"    }},")

        # Insert new entries before the closing brace
        def replace_model_mapping(match):
            existing_content = match.group(1)
            closing_brace = match.group(2)

            # Ensure existing content ends with a comma
            content = existing_content.rstrip()
            if not content.endswith(','):
                content += ','

            return content + '\n'.join(new_entries) + '\n' + closing_brace

        content = re.sub(model_mapping_pattern, replace_model_mapping, content, flags=re.DOTALL)

        print(f"\nAdded {len(new_models)} new model(s) to config.py:")
        for model in sorted(new_models):
            print(f"  - {model}")
        print("\nPlease review the auto-generated model configurations and update them with proper display names, families, and tasks.")

    # Write back to config.py
    with open(config_path, 'w') as f:
        f.write(content)

    print(f"\nconfig.py has been updated successfully.")
