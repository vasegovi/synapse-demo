import csv
from fileinput import filename
import time
import datetime
import json
import uuid
import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from azure.eventhub import EventHubProducerClient, EventData

keyVaultName = "kvml2by1"
KVUri = f"https://{keyVaultName}.vault.azure.net"

credential = DefaultAzureCredential()
client = SecretClient(vault_url=KVUri, credential=credential)



secretName = "orderheaderkv"
retrieved_secret = client.get_secret(secretName)


#Variable of the filename
filename = "data\[Sales].[SalesOrderHeader].csv"

# Create a producer client to produce and publish events to the event hub.
producer = EventHubProducerClient.from_connection_string(conn_str=retrieved_secret.value, eventhub_name="orderheader")


with open(filename) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    event_data_batch = producer.create_batch() # Create a batch. You will add events to the batch later. 
    for row in csv_reader:        
        if line_count > 0:                        
            reading = {'SalesOrderID': row[0], 'OrderDate': row[2], 'Status': row[5], 'SalesOrderNumber': row[7], 'PurchaseOrderNumber': row[8], 'AccountNumber' : row[9], 'CustomerID' : row[10], 'SalesPersonID':row[11], 'CreditCardID': row[16], 'CreditCardApprovalCode': row[17], 'TotalDue':row[22],'rowguid' : row[24], 'ModifiedDate':row[25]}
            s = json.dumps(reading) # Convert the reading into a JSON string.        
            #print(row)
            eventdata = EventData(s)
            eventdata.properties = {"SalesOrderID":str(row[0]), "Year":str(datetime.datetime.utcnow().year), "Month":str(datetime.datetime.utcnow().month), "Day":str(datetime.datetime.utcnow().day)}
            event_data_batch.add(eventdata) # Add event data to the batch.                        
            line_count += 1
        else:
            line_count += 1
    print(f'Processed {line_count} lines.')

producer.send_batch(event_data_batch) # Send the batch of events to the event hub.
# Close the producer.    
producer.close()