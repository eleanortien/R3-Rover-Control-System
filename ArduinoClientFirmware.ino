#include <Ethernet.h>
#include <EthernetUdp.h>
#define UDP_TX_PACKET_MAX_SIZE 34 //increase UDP size
#include <SPI.h>
#include <Servo.h>

class motor{
  public:
    Servo servo;
    int pin;
};

byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xEE };  //Assign a mac address
//IPAddress compIp(169, 254, 15, 133);                  //Find IP address (put in brackets) and assign IP address
IPAddress ardIp(192, 168, 1, 243);

unsigned int localPort = 8090;  //Assign port to talk over
//unsigned int pythonPort = 7000;
char packetBuffer[UDP_TX_PACKET_MAX_SIZE];  //Sent Data
String dataReq;                             //String for data
int packetSize;
EthernetUDP udp;  //Define UDP Object

//Variable setup
int up, low, hoist, screw, claw, swivel;
int armComps[6] = {up, low, screw, claw, hoist, swivel}; 

Servo upServo, lowServo, hoistServo, screwServo, clawServo, swivelServo;
Servo servoList [6]= {upServo, lowServo, screwServo, clawServo, hoistServo, swivelServo};
motor upMotor, lowMotor, hoistMotor, screwMotor, clawMotor, swivelMotor;
motor motors [6] = {upMotor, lowMotor, screwMotor, clawMotor, hoistMotor, swivelMotor};

//Arm Pin Numbers
int upperExt = 24;
int lowerExt= 29;
int hoistPin = 25;
int screwdriver = 11;
int clawPin = 28;
int swivelPin = 12;


int pinList [6]={upperExt, lowerExt, screwdriver, clawPin, hoistPin, swivelPin};
int motorSize = 6;




void setup() {
  Ethernet.begin(mac, ardIp);  //Initialise Ethernet
  udp.begin(localPort);        //Start udp
  delay(1500);
  for (int motor = 0; motor < motorSize; motor++)
  {
    motors[motor].servo = servoList[motor];
    motors[motor].pin = pinList[motor];
    motors[motor].servo.attach(motors[motor].pin);
  }
}

void loop() {
  packetSize = udp.parsePacket();  //Read packet size
  if (packetSize > 0) {
    udp.read(packetBuffer, UDP_TX_PACKET_MAX_SIZE);
    String data(packetBuffer);  //Convert data to string
    
    if (data.substring(0, data.indexOf("_")) == "ArmCommand")
    {
      data = data.substring(data.indexOf("_") + 1 );
      for (int i = 0; i < 6; i++)
      {
        int armPiece = int(data[0, data.indexOf("_")]);
        armComps[i] = armPiece;
        servoList[i].writeMicroseconds((int) (int(armComps[i])/255 * 1000) + 1000);
        data = data.substring(data.indexOf("_") + 1 );

      }

    }
    

    //Clear packet
    memset(packetBuffer, 0, UDP_TX_PACKET_MAX_SIZE);
  }
}
