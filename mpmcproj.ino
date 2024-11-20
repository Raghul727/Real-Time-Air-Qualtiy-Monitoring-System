#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <DHT.h>

#define SCREEN_WIDTH 128 // OLED display width
#define SCREEN_HEIGHT 64  // OLED display height
#define OLED_RESET -1     // Reset pin
#define DHTPIN 2          // DHT11 data pin
#define DHTTYPE DHT11     // DHT 11
#define MQ135_PIN A0      // MQ-135 analog pin

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  
  // Initialize the OLED display
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("SSD1306 alloc failed"));
    while (true); // Loop forever if the display is not found
  }
  
  // Initialize the DHT11 sensor
  dht.begin();
  
  display.clearDisplay();
}

void loop() {
  // Read DHT11 sensor
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  
  // Read MQ-135 sensor
  int mq135Value = analogRead(MQ135_PIN);

  // Check for DHT read failures
  if (isnan(h) || isnan(t)) {
    Serial.println("DHT read fail!");
    return;
  }

  // Print values to Serial
  Serial.print("T: "); // Temperature
  Serial.print(t);
  Serial.print("C, H: "); // Humidity
  Serial.print(h);
  Serial.print("%, MQ135: "); // MQ-135 value
  Serial.println(mq135Value);

  // Display readings on the OLED
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  
  // Display Temperature
  display.setCursor(0, 0);
  display.print("T: ");
  display.print(t);
  display.print("C");

  // Display Humidity
  display.setCursor(0, 10);
  display.print("H: ");
  display.print(h);
  display.print("%");

  // Display MQ135 Value
  display.setCursor(0, 20);
  display.print("MQ135: ");
  display.println(mq135Value);
  
  // Display air quality category
  String quality;
  if (mq135Value < 300) {
    quality = "Good";
  } else if (mq135Value < 700) {
    quality = "Mod.";
  } else {
    quality = "Poor";
  }

  display.setCursor(0, 40);
  display.print("Qual: ");
  display.println(quality);
  
  display.display(); // Update the display
  delay(2000); // Wait for 2 seconds before the next reading
}
