import sys

import win32serviceutil
from win32 import win32service, servicemanager

# MySQL Configuration
MySQLHost = 'localhost'
MySQLUser = 'root'
MySQLPassword = ''
MySQLDB = 'flask-monitoring'

# MQTT Configuration
MQTTBroker = 'broker.hivemq.com'
MQTTTopic = 'bmkg/sistoringsuser'
MQTTPort = 1883


class MyService:
    """Listen to MQTT and Write to MySQL Database"""
    def stop(self):
        """Stop the service"""
        self.running = False

    def run(self):
        """Main service loop. This is where work is done!"""
        self.running = True

        from peewee import Model, MySQLDatabase, CharField, AutoField, DateTimeField, IntegerField, FloatField, BooleanField
        import paho.mqtt.client as mqtt
        import datetime

        database = MySQLDB
        user = MySQLUser
        password = MySQLPassword
        host = MySQLHost

        # Define your Peewee database connection
        db = MySQLDatabase(database, user=user, password=password,
                        host=host, port=3306)

        # Define your Peewee models
        class Data(Model):
            id = AutoField()
            gas_an = IntegerField(null=True)
            gas_di = BooleanField(null=True)
            temp = FloatField(null=True)
            hum = FloatField(null=True)
            status = CharField(max_length=30, null=True)
            time = DateTimeField(default=datetime.datetime.now)

            class Meta:
                database = db
                tablename = 'data'

        # Define MQTT callbacks
        def on_message(client, userdata, message):
            # Handle incoming message
            data = message.payload.decode('utf-8')

            # print(data)

            # Split the string into individual variables
            data_list = data.split(',')

            # Print the decoded variables
            # for var in data_list:
            #     print(var)

            # mapping for bool massage
            bool_mapping = {"true":True, "false":False, "1":True, "0":False}
            data_list[1] = bool_mapping.get(data_list[1].lower())

            # Save data to MySQL using Peewee
            new_data = Data(gas_an=data_list[0], gas_di=data_list[1], temp=data_list[2], hum=data_list[3], status=data_list[4])
            new_data.save()

        broker = MQTTBroker
        port = MQTTPort
        topic = MQTTTopic

        # Set up MQTT client
        client = mqtt.Client()
        client.on_message = on_message

        try:
            client.connect(broker, port, 60)

            # Subscribe to MQTT topic
            client.subscribe(topic)

            servicemanager.LogInfoMsg("Service listening to "+broker+" at "+str(port)+" for "+topic)

            # Start MQTT loop
            client.loop_forever()
        except Exception as e:
            # Log any errors
            servicemanager.LogErrorMsg(f"Error: {str(e)}")

class MyServiceFramework(win32serviceutil.ServiceFramework):

    _svc_name_ = 'mqttlistener'
    _svc_display_name_ = 'MQTT Listener'

    def SvcStop(self):
        """Stop the service"""
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.service_impl.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def SvcDoRun(self):
        """Start the service; does not return until stopped"""
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        self.service_impl = MyService()
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        # Run the service
        self.service_impl.run()


def init():
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(MyServiceFramework)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(MyServiceFramework)


if __name__ == '__main__':
    init()