//Arduino is server file
#include <Ethernet.h>
#include <EthernetUdp.h>
#include <SPI.h>
#include <Servo.h>

byte mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xEE}; //Assign a mac address
IPAddress compIp(169, 254, 15, 133); //Find IP address (put in brackets) and assign IP address
IPAddress ardIp(192, 168, 1, 243);

unsigned int localPort = 8800; //Assign port to talk over
unsigned int pythonPort = 7000;
char packetBuffer[UDP_TX_PACKET_MAX_SIZE]; //Sent Data
String dataReq; //String for data
int packetSize;
EthernetUDP udp; //Define UDP Object

void setup() {

  Serial.begin(115200); //Turn on Serial Port
  Ethernet.begin(mac, ardIp); //Initialise Ethernet
  udp.begin(localPort);//Start udp
  delay(1500);

}

void loop() {
  packetSize = udp.parsePacket();//Read packet size
  if (packetSize > 0){
    udp.read(packetBuffer, UDP_TX_PACKET_MAX_SIZE);
    String dataRequest(packetBuffer); //Convert data to string

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