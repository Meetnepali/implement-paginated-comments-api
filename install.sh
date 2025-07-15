#!/bin/bash
set -e
apt-get update
apt-get install -y python3 python3-pip python3-venv
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install fastapi==0.110.0 uvicorn==0.27.1 pydantic==1.10.14 pytest==8.1.1