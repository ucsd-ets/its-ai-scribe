import os
import yaml


secrets = yaml.safe_load(open("secrets.yml"))

if os.environ.get('OPENAI_API_KEY'):
    OPENAI_API_KEY=os.environ.get('OPENAI_API_KEY')
else:
    OPENAI_API_KEY=secrets['openai']['api_key']

if os.environ.get('OPENAI_API_BASE'):
    # OPENAI_API_BASE="https://api.openai.com/v1/"
    OPENAI_API_BASE=os.environ.get('OPENAI_API_BASE')
else:
    OPENAI_API_BASE="https://api.mistral.ai/v1/"

if os.environ.get('MODEL'):
    # MODEL='gpt-3.5-turbo'
    # MODEL='gpt-4'
    MODEL=os.environ.get('MODEL')
else:
    MODEL='open-mixtral-8x7b'

CACHE_TRANSCRIPT=True