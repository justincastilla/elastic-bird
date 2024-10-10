import json
from utils import Util

# Start a connection
es_db = Util.get_connection()

# iterate through the bird json files and index them using the bulk index command
for i in range(1, 20):
    print(f"Indexing birds{i}.json")
    with open(f"./bird_partitions/birds{i}.json", "r") as json_file:
        birds = json.load(json_file)

        operations = []
        for bird in birds:
            operations.append({"index": {"_index": "bird-image-index"}})
            operations.append(bird)

        batch_size = 500

        for i in range(0, len(operations), batch_size):
            chunk = operations[i : i + batch_size]
            es_db.bulk(body=operations[i : i + batch_size])
            print(f"Indexed {min(i + batch_size, len(operations))} birds")
