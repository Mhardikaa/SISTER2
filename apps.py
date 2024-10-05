import tkinter as tk
from tkinter import scrolledtext
import paho.mqtt.client as mqtt
import time  # To track message latency
import json  # To send timestamp in the message

# MQTT Settings
BROKER = 'broker.hivemq.com'  # Public broker for demonstration
PORT = 1883

# Create MQTT Client
client = mqtt.Client()

# Callback when a message is received
def on_message(client, userdata, message):
    msg = message.payload.decode('utf-8')
    
    # Parse the message to get the timestamp
    msg_data = json.loads(msg)
    sender_message = msg_data['message']
    sender_name = msg_data['username']
    sent_time = msg_data['timestamp']
    
    # Calculate latency
    received_time = time.time()
    latency = received_time - sent_time
    
    # Display the message and latency
    subscriber_textbox.config(state=tk.NORMAL)
    subscriber_textbox.insert(tk.END, f"Received from {message.topic} by {sender_name}: {sender_message}\n")
    subscriber_textbox.insert(tk.END, f"Latency: {latency:.3f} seconds\n\n")
    subscriber_textbox.config(state=tk.DISABLED)

# Connect to the broker and start listening
def connect_mqtt():
    client.connect(BROKER, PORT)
    client.on_message = on_message
    client.loop_start()

# Publish message to the topic
def publish_message():
    msg = publisher_entry.get()
    user = username_entry.get()
    topic = topic_entry.get()
    if msg and user and topic:
        # Add timestamp to the message
        full_message = {
            "username": user,
            "message": msg,
            "timestamp": time.time()  # Send current time as timestamp
        }
        client.publish(topic, json.dumps(full_message))
        publisher_entry.delete(0, tk.END)

# Subscribe to the topic
def subscribe_topic():
    topic = topic_entry.get()
    if topic:
        client.subscribe(topic)
        subscriber_textbox.config(state=tk.NORMAL)
        subscriber_textbox.insert(tk.END, f"Subscribed to topic: {topic}\n")
        subscriber_textbox.config(state=tk.DISABLED)

# GUI Setup
root = tk.Tk()
root.title("Multi-User MQTT Publish-Subscribe with Latency")
root.geometry("600x500")

# Username Frame
username_frame = tk.Frame(root)
username_frame.pack(pady=10)

username_label = tk.Label(username_frame, text="Username:")
username_label.pack(side=tk.LEFT, padx=5)

username_entry = tk.Entry(username_frame, width=20)
username_entry.pack(side=tk.LEFT, padx=5)

# Topic Frame
topic_frame = tk.Frame(root)
topic_frame.pack(pady=10)

topic_label = tk.Label(topic_frame, text="Topic:")
topic_label.pack(side=tk.LEFT, padx=5)

topic_entry = tk.Entry(topic_frame, width=30)
topic_entry.pack(side=tk.LEFT, padx=5)

# Publisher Frame
publisher_frame = tk.Frame(root)
publisher_frame.pack(pady=10)

publisher_label = tk.Label(publisher_frame, text="Message:")
publisher_label.pack(side=tk.LEFT, padx=5)

publisher_entry = tk.Entry(publisher_frame, width=30)
publisher_entry.pack(side=tk.LEFT, padx=5)

publisher_button = tk.Button(publisher_frame, text="Publish", command=publish_message)
publisher_button.pack(side=tk.LEFT, padx=5)

# Subscriber Frame
subscriber_frame = tk.Frame(root)
subscriber_frame.pack(pady=10)

subscriber_label = tk.Label(subscriber_frame, text="Subscriber Log:")
subscriber_label.pack()

subscriber_textbox = scrolledtext.ScrolledText(subscriber_frame, width=60, height=15, state=tk.DISABLED)
subscriber_textbox.pack(pady=5)

# Subscribe Button
subscribe_button = tk.Button(root, text="Subscribe", command=subscribe_topic)
subscribe_button.pack(pady=10)

# Start MQTT connection
connect_mqtt()

# Run the GUI loop
root.mainloop()

# Stop MQTT loop on exit
client.loop_stop()
client.disconnect()
