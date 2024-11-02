// Reads a button attached to a MCP23XXX pin.
#include <Adafruit_MCP23X17.h>

#define BUTTON_PIN1 0  // MCP23XXX pin button is attached to
#define BUTTON_PIN2 1
#define BUTTON_PIN3 2
#define BUTTON_PIN4 3
#define BUTTON_PIN5 4
#define BUTTON_PIN6 5
#define BUTTON_PIN7 6

// only used for SPI
#define CS_PIN 6

// uncomment appropriate line
Adafruit_MCP23X17 mcp;

uint8_t row_pins[4] = {BUTTON_PIN2, BUTTON_PIN7, BUTTON_PIN6, BUTTON_PIN4};
uint8_t col_pins[3] = {BUTTON_PIN3, BUTTON_PIN1, BUTTON_PIN5};

char rc_array[4][3] = {{'1', '2', '3'}, {'4', '5', '6'}, {'7', '8', '9'}, {'*', '0', '#'}};

void setup() {
  Serial.begin(9600);

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

  for (int r = 0; r < 4; r++) {
      mcp.digitalWrite(row_pins[r], LOW);
      delay(5);
      for (int c = 0; c < 3; c++) {
          if (mcp.digitalRead(col_pins[c]) == LOW) {
            Serial.println(rc_array[r][c]);
          }
      }
      mcp.digitalWrite(row_pins[r], HIGH);
      delay(5);
    }
  }

