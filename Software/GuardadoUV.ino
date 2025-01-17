#include <Wire.h>
#include <SPI.h>
#include <LoRa.h>
#include <SFE_BMP180.h>

#define CS 18   // Pin de CS del módulo LoRa
#define RST 14  // Pin de Reset del módulo LoRa
#define IRQ 7   // Pin del IRQ del módulo LoRa
#define LED 25  // Pin del LED onboard

#define SERIAL_BAUDRATE 115200  // Velocidad del Puerto Serie
#define INTERVAL_TIME_TX 600000   // Cantidad de Segundos entre cada TX

#define ALTITUDE 0.0

#define LORA_FREQUENCY 915000000  // Frecuencia en Hz a la que se quiere transmitir.
#define LORA_SYNC_WORD 0xF3       // Byte value to use as the sync word, defaults to 0x12
#define LORA_POWER 17             // TX power in dB, defaults to 17. Supported values are 2 to 20 for PA_OUTPUT_PA_BOOST_PIN, and 0 to 14 for PA_OUTPUT_RFO_PIN.
#define LORA_SPREAD_FACTOR 7      // Spreading factor, defaults to 7. Supported values are between 6 and 12 (En Argentina se puede utilizar entre 7 a 10)
#define LORA_SIG_BANDWIDTH 125E3  // Signal bandwidth in Hz, defaults to 125E3. Supported values are 7.8E3, 10.4E3, 15.6E3, 20.8E3, 31.25E3, 41.7E3, 62.5E3, 125E3, 250E3, and 500E3
#define LORA_CODING_RATE 5        // Denominator of the coding rate, defaults to 5. Supported values are between 5 and 8, these correspond to coding rates of 4/5 and 4/8. The coding rate numerator is fixed at 4.

#define RESET_OLED 16

SFE_BMP180 bmp;

double baseline;
double T, P, A;
unsigned int pktNumber = 0;
double bitRate;

int UVOUT = 13;    //Output from the sensor
int REF_3V3 = 14;  //3.3V power on the ESP32 board

void setup() {
  pinMode(UVOUT, INPUT);
  pinMode(REF_3V3, INPUT);
  pinMode(LED, OUTPUT);
  pinMode(RESET_OLED,OUTPUT);
  Serial.begin(SERIAL_BAUDRATE);

  pinMode(RST, OUTPUT);
  digitalWrite(RST, HIGH);

  digitalWrite(RESET_OLED,HIGH); //Coloca el pin de reset del OLED en alto
  delay(1000);
  digitalWrite(RESET_OLED,LOW);

  //Inicializar módulo LoRa
  LoRa.setPins(CS, RST, IRQ);

  while (!LoRa.begin(LORA_FREQUENCY)) {
    Serial.println(".");
    delay(500);
  }

  LoRa.setTxPower(LORA_POWER);
  LoRa.setSpreadingFactor(LORA_SPREAD_FACTOR);
  LoRa.setSignalBandwidth(LORA_SIG_BANDWIDTH);
  LoRa.setCodingRate4(LORA_CODING_RATE);
  LoRa.setSyncWord(LORA_SYNC_WORD);
  LoRa.enableCrc();

  // Calculo del BitRate = (SF * (BW / 2 ^ SF)) * (4.0 / CR)
  bitRate = (LORA_SPREAD_FACTOR * (LORA_SIG_BANDWIDTH / pow(2, LORA_SPREAD_FACTOR))) * (4.0 / LORA_CODING_RATE);

  Serial.println("LoRa OK!");

  // Si el BMP180 no inicializa, no arranca la placa y el led onboard queda encendido!
  
}


void loop() {
  char status;
  int uvLevel = averageAnalogRead(UVOUT);
  int refLevel = averageAnalogRead(REF_3V3);
  double p0;

  //Use the 3.3V power pin as a reference to get a very accurate output value from sensor
  float outputVoltage = 3.3 / refLevel * uvLevel;

  float uvIntensity = mapfloat(outputVoltage, 0.99, 2.8, 0.0, 15.0);  //Convert the voltage to a UV intensity level


  pktNumber++;
  Serial.print(pktNumber);
  Serial.print(",");
  /*Serial.print(uvLevel);
  Serial.print(",");*/
  Serial.print(outputVoltage);
  Serial.print(",");
  Serial.println(uvIntensity);

  digitalWrite(LED, HIGH);


  if (pktNumber == 255) {
    pktNumber = 0;
  }

  digitalWrite(LED, LOW);
  delay(INTERVAL_TIME_TX);
}

int averageAnalogRead(int pinToRead) {
  byte numberOfReadings = 8;
  unsigned int runningValue = 0;

  for (int x = 0; x < numberOfReadings; x++)
    runningValue += analogRead(pinToRead);
  runningValue /= numberOfReadings;

  return (runningValue);
}

float mapfloat(float x, float in_min, float in_max, float out_min, float out_max) {
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}


double getPressure()
{
  char status;
  double p0;

  // You must first get a temperature measurement to perform a pressure reading.
  
  // Start a temperature measurement:
  // If request is successful, the number of ms to wait is returned.
  // If request is unsuccessful, 0 is returned.

  status = bmp.startTemperature();
  if (status != 0)
  {
    // Wait for the measurement to complete:

    delay(status);

    // Retrieve the completed temperature measurement:
    // Note that the measurement is stored in the variable T.
    // Use '&T' to provide the address of T to the function.
    // Function returns 1 if successful, 0 if failure.

    status = bmp.getTemperature(T);
    if (status != 0)
    {
      // Start a pressure measurement:
      // The parameter is the oversampling setting, from 0 to 3 (highest res, longest wait).
      // If request is successful, the number of ms to wait is returned.
      // If request is unsuccessful, 0 is returned.

      status = bmp.startPressure(3);
      if (status != 0)
      {
        // Wait for the measurement to complete:
        delay(status);

        // Retrieve the completed pressure measurement:
        // Note that the measurement is stored in the variable P.
        // Use '&P' to provide the address of P.
        // Note also that the function requires the previous temperature measurement (T).
        // (If temperature is stable, you can do one temperature measurement for a number of pressure measurements.)
        // Function returns 1 if successful, 0 if failure.

        status = bmp.getPressure(P,T);
        if (status != 0)
        {
          p0 = bmp.sealevel(P, ALTITUDE);
          A = bmp.altitude(P, baseline);
          return(p0);
        }
        else Serial.println("error retrieving pressure measurement\n");
      }
      else Serial.println("error starting pressure measurement\n");
    }
    else Serial.println("error retrieving temperature measurement\n");
  }
  else Serial.println("error starting temperature measurement\n");
}