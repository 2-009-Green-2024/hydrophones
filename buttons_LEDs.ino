// Reads a button attached to a MCP23XXX pin.
// INSTALL MCP23017 ADAFRUIT LIBRARY
#include <Adafruit_MCP23X17.h>
#include <Adafruit_NeoPixel.h>

// MCP23XXX pin button is attached to
#define BUTTON_PIN1 0  
#define BUTTON_PIN2 1  
#define BUTTON_PIN3 2  
#define BUTTON_PIN4 3  
#define BUTTON_PIN5 4  
#define BUTTON_PIN6 5  
#define BUTTON_PIN7 6 

// Which pin on the Arduino is connected to the NeoPixels?
// On a Trinket or Gemma we suggest changing this to 1:
#define LED_PIN  14

// How many NeoPixels are attached to the Arduino?
#define LED_COUNT 12

// Declare our NeoPixel strip object:
Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_RGBW + NEO_KHZ800);

uint32_t magenta = strip.Color(255, 0, 255);

// only used for SPI
#define CS_PIN 6

Adafruit_MCP23X17 mcp;

uint8_t row_pins[4] = {BUTTON_PIN2, BUTTON_PIN7, BUTTON_PIN6, BUTTON_PIN4};
uint8_t col_pins[3] = {BUTTON_PIN3, BUTTON_PIN1, BUTTON_PIN5};

char keypad_array[4][3] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}, {10, 0, 11}};
static const char *message_array[4][3] = {{"SOS", "GOING UP", "GOING DOWN"}, {"LOW OXYGEN", "CHECK-IN", "COME LOOK"}, {"no msg", "no msg", "no msg"}, {"no msg", "no msg", "no msg"}};


void setup() {
  Serial.begin(9600);

  strip.begin();
  strip.show(); // Initialize all pixels to 'off'
  strip.setBrightness(32);

  // uncomment appropriate mcp.begin
  if (!mcp.begin_I2C()) {
  //if (!mcp.begin_SPI(CS_PIN)) {
    Serial.println("Error.");
    while (1);
  }
  for (int r = 0; r < 4; r++) {
    mcp.pinMode(row_pins[r], OUTPUT);
    mcp.digitalWrite(row_pins[r], HIGH);
    }
  for (int c = 0; c < 3; c++) {
    mcp.pinMode(col_pins[c], INPUT_PULLUP);
    }
  Serial.println("Looping...");

}

void loop() {
  strip.clear(); // Set all pixel colors to 'off'

  for (int r = 0; r < 4; r++) {
      mcp.digitalWrite(row_pins[r], LOW);
      delay(5);
      for (int c = 0; c < 3; c++) {
          if (mcp.digitalRead(col_pins[c]) == LOW) {
            Serial.println(keypad_array[r][c]);
            Serial.println(message_array[r][c]);
            strip.fill(magenta, 0, keypad_array[r][c]);
            strip.show();
          }
      }
      mcp.digitalWrite(row_pins[r], HIGH);
      delay(5);
    }
  }

