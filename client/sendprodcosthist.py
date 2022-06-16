import csv
from fileinput import filename
import time
import datetime
import json


from azure.eventhub import EventHubProducerClient, EventData
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

keyVaultName = "kvml2by1"
KVUri = f"https://{keyVaultName}.vault.azure.net"

credential = DefaultAzureCredential()
client = SecretClient(vault_url=KVUri, credential=credential)

secretName = "productcosthist"
retrieved_secret = client.get_secret(secretName)

#Variable of the filename
filename = "data\[Production].[ProductCostHistory].csv"


# Create a producer client to produce and publish events to the event hub.
producer = EventHubProducerClient.from_connection_string(conn_str=retrieved_secret.value, eventhub_name="productcosthist")


with open(filename) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    event_data_batch = producer.create_batch() # Create a batch. You will add events to the batch later. 
    for row in csv_reader:
        if line_count > 0: 
            reading = {'ProductID': row[0], 'StartDate': row[1], 'EndDate': row[2], 'StandardCost': row[3], 'ModifiedDate': row[4]}
            s = json.dumps(reading) # Convert the reading into a JSON string.  
            print(line_count)                  
            eventdata = EventData(s)
            eventdata.properties = {"ProductID":str(row[0]), "Year":str(datetime.datetime.utcnow().year), "Month":str(datetime.datetime.utcnow().month), "Day":str(datetime.datetime.utcnow().day)}
            event_data_batch.add(eventdata) # Add event data to the batch.                        
            line_count += 1
        else:
            line_count += 1
    print(f'Processed {line_count} lines.')

producer.send_batch(event_data_batch) # Send the batch of events to the event hub.
# Close the producer.    
print(str(datetime.datetime.utcnow()))
producer.close()