import requests
import os
import json
from ..memory.state_manager import StateManager

class DesignerAgent:
    def __init__(self, bus, state):
        self.bus = bus
        self.state = state
        self.hf_token = os.getenv("HF_TOKEN")

    def run(self):
        self.bus.subscribe('designer_trigger', self.handle)

    def handle(self, params):
        tier = params.get('tier')
        style = params.get('style')
        assets = self._generate_assets(style)
        self._save_assets(tier, assets)
        self.bus.publish('designer_complete', {'tier': tier, 'assets': assets})

    def _generate_assets(self, style):
        # Call Hugging Face inference for video generation
        headers = {"Authorization": f"Bearer {self.hf_token}"}
        payload = {"inputs": style, "parameters": {"height": 480, "width": 854}}
        response = requests.post(
            "https://api-inference.huggingface.co/models/stabilityai/stable-video-diffusion-img2vid",
            headers=headers,
            json=payload
        )
        return response.json()  # returns binary or URL

    def _save_assets(self, tier, assets):
        # Store in OCI object storage
        import boto3
        s3 = boto3.client('s3', endpoint_url=os.getenv("OCI_OBJECT_STORAGE_ENDPOINT"))
        bucket = os.getenv("OCI_BUCKET_NAME")
        for name, data in assets.items():
            s3.put_object(Bucket=bucket, Key=f"{tier}/templates/{name}.mogrt", Body=data['binary'])
