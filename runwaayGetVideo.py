# pip install runwayml
from runwayml import RunwayML

# The env var RUNWAYML_API_SECRET is expected to contain your API key.
client = RunwayML(api_key="key")

task = client.tasks.retrieve(id='787c5add-7542-4988-bad1-4acc3ffcec0c')
print(task)