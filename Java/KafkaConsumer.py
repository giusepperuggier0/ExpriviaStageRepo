from confluent_kafka import Consumer, KafkaException, KafkaError


conf = {
    'bootstrap.servers': 'localhost:9092',  
    'group.id': 'my-consumer-group',         
    'auto.offset.reset': 'earliest'         
}


consumer = Consumer(conf)
consumer.subscribe(['test'])

def consume_messages():
    try:
        while True:
            msg = consumer.poll(timeout=1.0)  
            if msg is None: # Cosi da non bloccarsi appena si avvia  
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print(f"Arrivati al topic: {msg.topic()} [{msg.partition()}] alla posizione {msg.offset()}")
                else:
                    raise KafkaException(msg.error())
            else:
                print(f"{msg.value().decode('utf-8')}")

    except KeyboardInterrupt:
        print("Interruzione del consumer.")
    finally:
        
        consumer.close()


consume_messages()
