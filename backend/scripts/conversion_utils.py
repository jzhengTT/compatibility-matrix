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


def _create_header() -> str:
    """Create the file header section."""
    sep = "=" * 80
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    return f"{sep}\nNEW MODELS AND DEVICES DETECTED\n{sep}\nGenerated at: {timestamp}\n\nThese entries need to be added to config.py manually.\n{sep}\n"


def _create_device_section(new_devices: Set[str]) -> str:
    """Create the device section for the file."""
    lines = [
        f"NEW DEVICES ({len(new_devices)}):",
        "-" * 80,
        "Add these entries to the DEVICE_MAPPING dictionary in config.py:\n"
    ]
    lines.extend(f"    '{device}': '{device.capitalize()}'," for device in sorted(new_devices))
    return '\n'.join(lines) + '\n'


def _create_model_section(new_models: Set[str]) -> str:
    """Create the model section for the file."""
    lines = [
        f"NEW MODELS ({len(new_models)}):",
        "-" * 80,
        "Add these entries to the MODEL_MAPPING dictionary in config.py:\n"
    ]
    for model in sorted(new_models):
        lines.extend([
            f"    '{model}': {{",
            f"        'display_name': '{model}',",
            f"        'family': 'Other',  # TODO: Update with correct family",
            f"        'tasks': ['Unknown']  # TODO: Update with correct tasks",
            "    },\n"
        ])
    return '\n'.join(lines)


def _create_instructions() -> str:
    """Create the instructions section for the file."""
    sep = "=" * 80
    return f"{sep}\nINSTRUCTIONS:\n{sep}\n1. Review the entries above\n2. Update display names, families, and tasks as needed\n3. Copy the entries to the appropriate section in config.py\n4. Delete or archive this file once you've updated config.py\n"


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
