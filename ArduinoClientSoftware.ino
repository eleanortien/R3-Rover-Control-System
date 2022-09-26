#include <Ethernet.h>
#include <EthernetUdp.h>
#include <SPI.h>
#include <Servo.h>

byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xEE };  //Assign a mac address
IPAddress compIp(169, 254, 15, 133);                  //Find IP address (put in brackets) and assign IP address
IPAddress ardIp(192, 168, 1, 243);

unsigned int localPort = 8800;  //Assign port to talk over
unsigned int pythonPort = 7000;
char packetBuffer[UDP_TX_PACKET_MAX_SIZE];  //Sent Data
String dataReq;                             //String for data
int packetSize;
EthernetUDP udp;  //Define UDP Object

//Variable setup
int lw1, lw2, lw3, rw1, rw2, rw3;
int wheels[6] = {lw1, lw2, lw3, rw1, rw2, rw3}; 

Servo servoLW1, servoLW2, servoLW3, servoRW1, servoRW2, servoRW3, servoLEDR, servoLEDB, servoLEDG;
Servo servoList [9]= {servoLW1, servoLW2, servoLW3, servoRW1, servoRW2, servoRW3, servoLEDR, servoLEDB, servoLEDG};

//Drive Pin Numbers
int leftW1 = 11;
int leftW2 = 12;
int leftW3 = 24;
int rightW1 = 25;
int rightW2 = 28;
int rightW3 = 29;
int ledRed = 33;
int ledBlue = 34;
int ledGreen = 35;


int pinList [9]={leftW1, leftW2, leftW3, rightW1, rightW2, rightW3, ledRed, ledBlue, ledGreen};
int motorSize = 9;




void setup() {
  Serial.begin(115200);        //Turn on Serial Port
  Ethernet.begin(mac, ardIp);  //Initialise Ethernet
  udp.begin(localPort);        //Start udp
  delay(1500);
  for (int pin = 0; pin < motorSize; pin++)
  {
    servoList[pin].attach(pinList[pin]);
  }
}

void loop() {
  packetSize = udp.parsePacket();  //Read packet size
  if (packetSize > 0) {
    udp.read(packetBuffer, UDP_TX_PACKET_MAX_SIZE);
    String data(packetBuffer);  //Convert data to string
    if (data.substring(0, data.indexOf("_")) == "DRIVECOMMAND")
    {
      data = data[0, data.indexOf("_") + 1];
      for (int i = 0; i < 6; i++)
      {
        int wheel = int(data[0, data.indexOf("_")]);
        wheels[i] = wheel;
        servoList[i].write(int(wheels[i]) + (1500 - 128));

      }

    }
    

    //Clear packet
    memset(packetBuffer, 0, UDP_TX_PACKET_MAX_SIZE);
  }
}














/*#include <Wifi.h>

const char* netID = "networkName";
const char* password = "networkPass";
const uint16_t serverport = 8090;
const char * host = "192.168.1.83"; 
int timedl = 500;

void setup() {
  Serial.begin(115200); //Use bps of Arduino here

  WiFi.begin(netID, password); //Open serial connection
  while (WiFi.status() != WL_CONNECTED){ //While not connected
    delay (timedl);
    Serial.println("...");
  }

Serial.print("WiFi connected with IP: ");
Serial.println(WiFi.localIP());
}

void loop() {
  // put your main code here, to run repeatedly:

}
*/