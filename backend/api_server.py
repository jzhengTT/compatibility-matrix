#!/usr/bin/env python3
"""
Flask API Server for Compatibility Matrix
Fetches compatibility data from S3 and serves it to the frontend.
"""

import os
import json
import time
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure CORS
cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(',')
CORS(app, origins=cors_origins)

# Configuration
S3_BUCKET = os.getenv('AWS_S3_BUCKET', 'ttdata-data-pipeline-compatibility-matrix-raw')
S3_KEY = os.getenv('AWS_S3_KEY', 'data/compatibility.json')
CACHE_TTL = int(os.getenv('CACHE_TTL_SECONDS', '300'))  # Default 5 minutes
API_PORT = int(os.getenv('API_PORT', '8000'))

# In-memory cache
cache = {
    'data': None,
    'timestamp': None,
    'ttl': CACHE_TTL
}


def get_s3_client():
    """Create and return an S3 client with configured credentials."""
    try:
        return boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION', 'us-east-1')
        )
    except NoCredentialsError:
        app.logger.error("AWS credentials not found")
        return None


def fetch_from_s3():
    """
    Fetch compatibility data from S3.
    Returns the JSON data or None if an error occurs.
    """
    s3_client = get_s3_client()

    if not s3_client:
        return None

    try:
        app.logger.info(f"Fetching data from S3: s3://{S3_BUCKET}/{S3_KEY}")

        response = s3_client.get_object(Bucket=S3_BUCKET, Key=S3_KEY)
        data = json.loads(response['Body'].read().decode('utf-8'))

        app.logger.info(f"Successfully fetched data from S3 ({len(json.dumps(data))} bytes)")
        return data

    except ClientError as e:
        error_code = e.response['Error']['Code']
        app.logger.error(f"S3 ClientError: {error_code} - {e}")
        return None
    except Exception as e:
        app.logger.error(f"Unexpected error fetching from S3: {e}")
        return None


def get_cached_data():
    """
    Get data from cache if still valid, otherwise fetch from S3 and update cache.
    Returns the data or None if an error occurs.
    """
    current_time = time.time()

    # Check if cache is valid
    if (cache['data'] is not None and
        cache['timestamp'] is not None and
        (current_time - cache['timestamp']) < cache['ttl']):

        cache_age = int(current_time - cache['timestamp'])
        app.logger.info(f"Returning cached data (age: {cache_age}s, TTL: {cache['ttl']}s)")
        return cache['data']

    # Cache is invalid or empty, fetch from S3
    app.logger.info("Cache miss or expired, fetching fresh data from S3")
    data = fetch_from_s3()

    if data is not None:
        # Update cache
        cache['data'] = data
        cache['timestamp'] = current_time
        app.logger.info("Cache updated with fresh data")

    return data


@app.route('/api/compatibility', methods=['GET'])
def get_compatibility():
    """
    API endpoint to get compatibility data.
    Returns JSON data from S3 (cached) or error response.
    """
    try:
        data = get_cached_data()

        if data is None:
            return jsonify({
                'error': 'Failed to fetch compatibility data from S3',
                'message': 'Please check server logs for details'
            }), 503

        return jsonify(data), 200

    except Exception as e:
        app.logger.error(f"Error in /api/compatibility: {e}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'cache_age': int(time.time() - cache['timestamp']) if cache['timestamp'] else None,
        'cache_ttl': cache['ttl']
    }), 200


@app.route('/api/cache/clear', methods=['POST'])
def clear_cache():
    """Clear the cache (useful for testing/debugging)."""
    cache['data'] = None
    cache['timestamp'] = None
    app.logger.info("Cache cleared manually")
    return jsonify({'message': 'Cache cleared successfully'}), 200


if __name__ == '__main__':
    # Log configuration on startup
    app.logger.info(f"Starting Compatibility Matrix API Server")
    app.logger.info(f"S3 Bucket: {S3_BUCKET}")
    app.logger.info(f"S3 Key: {S3_KEY}")
    app.logger.info(f"Cache TTL: {CACHE_TTL} seconds")
    app.logger.info(f"CORS Origins: {cors_origins}")
    app.logger.info(f"API Port: {API_PORT}")

    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=API_PORT,
        debug=True
    )
