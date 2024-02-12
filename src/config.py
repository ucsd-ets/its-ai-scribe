import yaml

secrets = yaml.safe_load(open("../secrets.yml"))

OPENAI_API_KEY=secrets['openai']['api_key']
MODEL='gpt-3.5-turbo'