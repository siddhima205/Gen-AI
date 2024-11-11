import time
from runwayml import RunwayML

client = RunwayML(api_key="key")

# Create a new image-to-video task using the "gen3a_turbo" model
task = client.image_to_video.create(
  model='gen3a_turbo',
  # Point this at your own image file
  prompt_image='https://www.shutterstock.com/shutterstock/photos/2460826719/display_1500/stock-photo-a-sleek-classic-ballpoint-pen-with-a-black-grip-and-silver-body-lies-on-a-pure-white-surface-2460826719.jpg',
)
task_id = task.id

# Poll the task until it's complete
time.sleep(10)  # Wait for a second before polling
task = client.tasks.retrieve(task_id)
while task.status not in ['SUCCEEDED', 'FAILED']:
  time.sleep(10)  # Wait for ten seconds before polling
  task = client.tasks.retrieve(task_id)

print('Task complete:', task)