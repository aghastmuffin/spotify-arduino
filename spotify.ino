#include <LiquidCrystal.h>

const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
int redPin= 10;
int greenPin = 9;
int bluePin = 8;

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(10); // Set timeout to 10 milliseconds
  lcd.begin(16, 2);
  lcd.setCursor(0, 0);
  lcd.print("Estbsh Serial!!!!");
  lcd.setCursor(0, 1);
  lcd.print("By: Levi B(init)");
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);

}
void loop() {
    if (Serial.available() > 0) {
        String data1 = Serial.readStringUntil('\n');
        String data2 = Serial.readString();
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print(data1);
        lcd.setCursor(0, 1);
        lcd.print(data2);
    }
}
void setColor(int redValue, int greenValue, int blueValue) {
  analogWrite(redPin, redValue);
  analogWrite(greenPin, greenValue);
  analogWrite(bluePin, blueValue);
}
