"""
Configuration for compatibility conversion script.

This file contains all mappings for the conversion process.

To add a new model, simply add one entry to MODELS_CONFIG with all its properties.
To add a new device, add an entry to DEVICE_MAPPING.

After editing, run: python3 scripts/convert_compatibility.py
"""

# Device name mappings to hardware naming convention
DEVICE_MAPPING = {
    'galaxy': 'Galaxy (Wormhole)',
    'n150': 'n150 (Wormhole)',
    'n300': 'n300 (Wormhole)',
    'p150x4': 'Quietbox (Blackhole)',
    't3k': 'Loudbox (Wormhole)',
}

# Consolidated model configuration - all model info in one place
# Each model has: display_name, family, and tasks
MODELS_CONFIG = {
    # LLaMA models
    'Llama-3.1-8B-Instruct': {
        'display_name': 'LLaMA 3.1 8B Instruct',
        'family': 'LLaMA',
        'tasks': ['LLM', 'Text-Generation']
    },
    'Llama-3.2-11B-Vision-Instruct': {
        'display_name': 'LLaMA 3.2 11B Vision Instruct',
        'family': 'LLaMA',
        'tasks': ['LLM', 'Vision', 'Text-Generation']
    },
    'Llama-3.2-1B-Instruct': {
        'display_name': 'LLaMA 3.2 1B Instruct',
        'family': 'LLaMA',
        'tasks': ['LLM', 'Text-Generation']
    },
    'Llama-3.2-3B-Instruct': {
        'display_name': 'LLaMA 3.2 3B Instruct',
        'family': 'LLaMA',
        'tasks': ['LLM', 'Text-Generation']
    },
    'Llama-3.2-90B-Vision-Instruct': {
        'display_name': 'LLaMA 3.2 90B Vision Instruct',
        'family': 'LLaMA',
        'tasks': ['LLM', 'Vision', 'Text-Generation']
    },
    'Llama-3.3-70B-Instruct': {
        'display_name': 'LLaMA 3.3 70B Instruct',
        'family': 'LLaMA',
        'tasks': ['LLM', 'Text-Generation']
    },

    # Mistral models
    'Mistral-7B-Instruct-v0.3': {
        'display_name': 'Mistral 7B Instruct v0.3',
        'family': 'Mistral',
        'tasks': ['LLM', 'Text-Generation']
    },

    # Qwen models
    'QwQ-32B': {
        'display_name': 'QwQ 32B',
        'family': 'Qwen',
        'tasks': ['LLM', 'Text-Generation']
    },
    'Qwen2.5-72B-Instruct': {
        'display_name': 'Qwen 2.5 72B Instruct',
        'family': 'Qwen',
        'tasks': ['LLM', 'Text-Generation']
    },
    'Qwen2.5-7B-Instruct': {
        'display_name': 'Qwen 2.5 7B Instruct',
        'family': 'Qwen',
        'tasks': ['LLM', 'Text-Generation']
    },
    'Qwen2.5-VL-32B-Instruct': {
        'display_name': 'Qwen 2.5 VL 32B Instruct',
        'family': 'Qwen',
        'tasks': ['LLM', 'Vision', 'Text-Generation']
    },
    'Qwen2.5-VL-3B-Instruct': {
        'display_name': 'Qwen 2.5 VL 3B Instruct',
        'family': 'Qwen',
        'tasks': ['LLM', 'Vision', 'Text-Generation']
    },
    'Qwen2.5-VL-72B-Instruct': {
        'display_name': 'Qwen 2.5 VL 72B Instruct',
        'family': 'Qwen',
        'tasks': ['LLM', 'Vision', 'Text-Generation']
    },
    'Qwen2.5-VL-7B-Instruct': {
        'display_name': 'Qwen 2.5 VL 7B Instruct',
        'family': 'Qwen',
        'tasks': ['LLM', 'Vision', 'Text-Generation']
    },
    'Qwen3-32B': {
        'display_name': 'Qwen 3 32B',
        'family': 'Qwen',
        'tasks': ['LLM', 'Text-Generation']
    },
    'Qwen3-8B': {
        'display_name': 'Qwen 3 8B',
        'family': 'Qwen',
        'tasks': ['LLM', 'Text-Generation']
    },
    'Qwen3-Embedding-4B': {
        'display_name': 'Qwen 3 Embedding 4B',
        'family': 'Qwen',
        'tasks': ['NLP', 'Embedding']
    },

    # Gemma models
    'gemma-3-1b-it': {
        'display_name': 'Gemma 3 1B IT',
        'family': 'Gemma',
        'tasks': ['LLM', 'Text-Generation']
    },
    'gemma-3-4b-it': {
        'display_name': 'Gemma 3 4B IT',
        'family': 'Gemma',
        'tasks': ['LLM', 'Text-Generation']
    },

    # Embedding models
    'bge-large-en-v1.5': {
        'display_name': 'BGE Large EN v1.5',
        'family': 'BGE',
        'tasks': ['NLP', 'Embedding']
    },

    # Vision models
    'efficientnet': {
        'display_name': 'EfficientNet',
        'family': 'EfficientNet',
        'tasks': ['Vision', 'Image-Classification']
    },
    'mobilenetv2': {
        'display_name': 'MobileNet v2',
        'family': 'MobileNet',
        'tasks': ['Vision', 'Image-Classification']
    },
    'resnet-50': {
        'display_name': 'ResNet-50',
        'family': 'ResNet',
        'tasks': ['Vision', 'Image-Classification']
    },
    'segformer': {
        'display_name': 'SegFormer',
        'family': 'SegFormer',
        'tasks': ['Vision', 'Image-Segmentation']
    },
    'vit': {
        'display_name': 'ViT',
        'family': 'ViT',
        'tasks': ['Vision', 'Image-Classification']
    },
    'vovnet': {
        'display_name': 'VoVNet',
        'family': 'VoVNet',
        'tasks': ['Vision', 'Image-Classification']
    },

    # Image generation models
    'stable-diffusion-3.5-large': {
        'display_name': 'Stable Diffusion 3.5 Large',
        'family': 'Stable Diffusion',
        'tasks': ['Text-to-Image', 'Image-Generation']
    },
    'stable-diffusion-xl-base-1.0': {
        'display_name': 'Stable Diffusion XL Base 1.0',
        'family': 'Stable Diffusion',
        'tasks': ['Text-to-Image', 'Image-Generation']
    },
    'unet': {
        'display_name': 'UNet',
        'family': 'UNet',
        'tasks': ['Text-to-Image', 'Image-Generation']
    },

    # Speech models
    'whisper-large-v3': {
        'display_name': 'Whisper Large v3',
        'family': 'Whisper',
        'tasks': ['Speech-to-Text', 'NLP']
    },
}


