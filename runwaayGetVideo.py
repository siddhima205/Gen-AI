# pip install runwayml
from runwayml import RunwayML

# The env var RUNWAYML_API_SECRET is expected to contain your API key.
client = RunwayML(api_key="key_32bfc791261f4e7fb13026b7d2553fb7cf24be4d960498532bd5b7c9fd7d0868879bc0d770c88c3b3ae37a09c0d6efaf4f8d62346f843fd192c7db6bb9053324")

task = client.tasks.retrieve(id='787c5add-7542-4988-bad1-4acc3ffcec0c')
print(task)