import binascii,paho.mqtt.client as mqtt,datetime
from uuid import getnode as get_mac

class Datalab:
    def __init__(self):
        self.host = "broker.gogoboard.org"
        self.username = str(get_mac())
        self.password = "pass"
        self.datalab_time_limit = 5
        self._datalabTimeMap = {}

        self.datalab = mqtt.Client(client_id=None, clean_session=True)
        self.datalab.username_pw_set(self.username, self.password)
        
        self.datalab.connect(self.host, port=1883, keepalive=60)
    

    def _publish(self, topic, payload):
        _result = self.datalab.publish(topic, payload)

        if _result.rc != mqtt.MQTT_ERR_SUCCESS:
            if _result.rc == mqtt.MQTT_ERR_NO_CONN:
                #? trying to reconnect
                print("ERROR: No connection ... trying to reconect")
                self.datalab.connect(self.host, port=1883, keepalive=60)
            else:
                print("ERROR:", mqtt.error_string(_result.rc))


    def on_log(self, client, userdata, level, buf):
        print("LOG :", buf)


    def logging(self, status):
        if status == True:
            self.datalab.on_log = self.on_log
        else:
            self.datalab.on_log = None

    
    def publish(self, channel, field, payload):
        tmp_topic = channel + "/" + field
        topic = "plog/"+ channel + "/" + field

        if tmp_topic in self._datalabTimeMap.keys():
            if (datetime.datetime.now() - self._datalabTimeMap[tmp_topic]).seconds > self.datalab_time_limit:
                self._publish(topic, channel + " " + field + "=" + str(payload))
                self._datalabTimeMap.update({tmp_topic:datetime.datetime.now()})
        else:
            self._publish(topic, channel + " " + field + "=" + str(payload))
            self._datalabTimeMap.update({tmp_topic:datetime.datetime.now()})
