#include <ESP8266WiFi.h>
#include <ArduinoJson.h>
#include <time.h>
#include <DHT.h>

// Definitions
#define DHT_PIN D2
#define ANEMOMETER_PIN D3
#define PI 3.14159265 // pi
// Time between samples (1m).
#define DELAY_TIME 60000
#define RADIUS 105
#define DHTTYPE DHT22 // DHT 22  (AM2302)

const char *ssid     = "NETWORK";
const char *password = "PASSWORD";
const char *server = "192.168.1.110";

const int port = 5080;
const char* ntpServer = "pool.ntp.org";
WiFiClient client;

unsigned int anemometer_counter = 0;
bool measuring_delay_1 = false;

// DHT.
DHT dht(DHT_PIN, DHTTYPE);

// Used to count the interruptions on the anemometer.
void ICACHE_RAM_ATTR add_anemometer_count(){
  anemometer_counter++;
}

void setup() {
  Serial.begin(9600); // sets the serial port to 9600 baud
  WiFi.begin(ssid, password);
  Serial.println("Trying to connect...");
  while (WiFi.status() != WL_CONNECTED) {
    delay (1000);
    Serial.print(".");
  }
  Serial.println("Connected!");
  configTime(0, 0, ntpServer);
  Serial.println("Waiting for NTP time sync...");
  while (time(nullptr) < 1510644967) { // Wait for a valid time to be set
    delay(100);
  }
  Serial.println("Time synchronized");
  
  // Set the pins
  pinMode(ANEMOMETER_PIN, INPUT);
  digitalWrite(ANEMOMETER_PIN, HIGH); //internall pull-up active
  dht.begin();
}

void loop() {
  if (!measuring_delay_1) {
    // start measuring with the first delay.
    start_measuring_wind_speed();
  } else {
    // Measure wind speed.
    float wind_speed_kmh = finish_wind_speed_measurement();
    Serial.print("Wind speed: ");
    Serial.print(wind_speed_kmh);
    Serial.println("km/h");

    // Measure humidity and temperature from DHT22.
    float hum = dht.readHumidity();
    float temp= dht.readTemperature();
    Serial.print("Humidity: ");
    Serial.print(hum);
    Serial.print(" %, Temp: ");
    Serial.print(temp);
    Serial.println(" Celsius");
  
    // Direction
    int wind_dir = winddir();
    
    send_data_to_server(wind_dir, wind_speed_kmh, hum, temp);
  }
  delay(DELAY_TIME); //delay between reads.
}

void start_measuring_wind_speed() {
  // `wind_speed_measurement_period` has passed. Start measuring speed.
  anemometer_counter = 0;
  measuring_delay_1 = true;
  attachInterrupt(digitalPinToInterrupt(ANEMOMETER_PIN), add_anemometer_count, RISING);
}

float finish_wind_speed_measurement() {
  measuring_delay_1 = false;
  detachInterrupt(digitalPinToInterrupt(ANEMOMETER_PIN));
  // speed in km/h
  float wind_speed_kmh = ((2*PI*RADIUS) * anemometer_counter / DELAY_TIME) * 3.6;
  return wind_speed_kmh;
}

/*
 * Reads the wind direction:
 * 0 -> North
 * 1 -> Northeast
 * 2 -> East
 * 3 -> Southeast
 * 4 -> South
 * 5 -> Southwest
 * 6 -> West
 * 7 -> Northwest
 */
byte winddir() {
  int acc = 0;
  int wd;
  for (int i = 0; i < 20; i++) {
    wd = analogRead(0); //A0 arduino
    acc+= wd;
    delay(50);
  }
  int avg = acc / 20;
  byte wdir;
  if(avg >= 0 && avg < 84 ) {
    wdir = 3;
  } else if (avg >= 84 && avg < 207) {
    wdir = 2;
  } else if (avg >= 207 && avg < 329) {
    wdir = 1;
  } else if (avg >= 329 && avg <= 449) {
    wdir = 0;
  } else if (avg >= 450 && avg < 572) {
    wdir = 7;
  } else if (avg >= 572 && avg < 700) {
    wdir = 6;
  } else if (avg >= 700 && avg < 835) {
    wdir = 5;
  } else if (avg >= 835) {
    wdir= 4;
  }
  Serial.print("Avg analog read: ");
  Serial.print(avg);
  Serial.print("Direction: ");
  Serial.println(wdir);
  delay(1000);
  return wdir;
}

void send_data_to_server(byte wind_direction, float wind_speed, float humidity, float temperature) {
  time_t now = time(nullptr);
  tm *myTime = gmtime(&now);
  char buffer[20];
  sprintf(buffer, "%04d-%02d-%02d %02d:%02d:%02d", myTime->tm_year + 1900, myTime->tm_mon + 1, myTime->tm_mday, myTime->tm_hour, myTime->tm_min, myTime->tm_sec);
  
  if (client.connect(server, port)) { // Port 80 is the default for HTTP
    Serial.println("Connected to server");

    DynamicJsonDocument doc(1024);
    doc["date"] = buffer;
    doc["wind_direction"] = wind_direction;
    doc["wind_speed_knot"] = wind_speed;
    doc["temperature_c"] = temperature;
    doc["pressure_mbar"] = 0;
    doc["humidity"] = humidity;
    
    String postData;
    serializeJson(doc, postData);

    // Send the POST request with JSON payload
    client.println("POST /save_air_data HTTP/1.1");
    client.println("Host: " + String(server));
    client.println("Content-Type: application/json");
    client.print("Content-Length: ");
    client.println(postData.length());
    client.println();
    client.print(postData);

    // Wait for the response
    while (client.connected()) {
      String line = client.readStringUntil('\n');
      if (line == "\r") {
        break;
      }
    }
    String line = client.readStringUntil('\n');
    Serial.println("Server Response: " + line);

  } else {
    Serial.println("Failed to connect to server");
  }

  client.stop();
}
