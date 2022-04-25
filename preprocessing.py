# preprocessing.py
# script to preprocess the raw data queried from
# spotify

import os
import json
from timeit import default_timer as timer

# custom imports
from scripts.utils import output, working_on, finished
output("Loaded Modules")

def connect_streaming_history(n):
  if os.path.isfile("data/StreamingHistory.json"):
    return
  streaming_history = []
  for i in range(n):
    with open(f"data/StreamingHistory{i}.json", "r") as f:
      streaming_history.extend(json.loads(f.read()))

  # write joined streaming history
  with open(f"data/StreamingHistory.json", "w") as f:
    json.dump(streaming_history, f)

  print("> successfully written joined streaming "\
        "history to data/StreamingHistory.json")

def main():
  # connect streaming history json files
  s = working_on("Joining Streaming History")
  connect_streaming_history(5)
  finished("Joining Streaming History", timer()-s)

if __name__ == "__main__":
  main()
