import datalab_api, time

datalab = datalab_api.Datalab()
datalab.logging(True)

while True:
    datalab.publish("pythonapi", "light", 100)
    time.sleep(2)
