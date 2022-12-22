### Fonts Resources
1. [dejavu](https://dejavu-fonts.github.io/)
2. [eFont](http://openlab.ring.gr.jp/efont/index.html.en)

### UIFlow Supported Font list:

#### M5GFX:
 1. DejaVu9
 2. DejaVu12
 3. DejaVu18
 4. DejaVu24
 5. DejaVu40
 6. DejaVu56
 7. DejaVu72
 8. EFontCN24
 9. EFontJA24
 10. EFontKR24

#### LVGL:
1. ...

### API

#### m5 module
  - begin -- \<function\>
  - update -- \<function\>
  - getBoard -- \<function\>
  - BOARD -- \<enumerate\>
  - btnA -- \<Button\>
  - btnB -- \<Button\>
  - btnC -- \<Button\>
  - btnPWR -- \<Button\>
  - btnEXT -- \<Button\>
  - lcd -- \<Lcd\>
  - user_lcd -- \<class 'User_Lcd'\>
  - speaker -- \<Speaker\>
  - power -- \<Power\>

##### m5.begin
##### m5.update
##### m5.getBoard


#### m5.lcd -> lowlevel M5GFX draw function
  - height -- \<function\>
  - width -- \<function\>
  - getRotation -- \<function\>
  - getColorDepth -- \<function\>
  - getCursor -- \<function\>
  - setRotation -- \<function\>
  - setColorDepth -- \<function\>
  - setFont -- \<function\>
  - setTextColor -- \<function\>
  - setTextScroll -- \<function\>
  - setTextSize -- \<function\>
  - setCursor -- \<function\>
  - clear -- \<function\>
  - fillScreen -- \<function\>
  - drawPixel -- \<function\>
  - drawCircle -- \<function\>
  - fillCircle -- \<function\>
  - drawEllipse -- \<function\>
  - fillEllipse -- \<function\>
  - drawLine -- \<function\>
  - drawRect -- \<function\>
  - fillRect -- \<function\>
  - drawRoundRect -- \<function\>
  - fillRoundRect -- \<function\>
  - drawTriangle -- \<function\>
  - fillTriangle -- \<function\>
  - drawArc -- \<function\>
  - fillArc -- \<function\>
  - drawEllipseArc -- \<function\>
  - fillEllipseArc -- \<function\>
  - drawQR -- \<function\>
  - drawJpg -- \<function\>
  - drawPng -- \<function\>
  - drawBmp -- \<function\>
  - drawImage -- \<function\>
  - drawRawBuf -- \<function\>
  - print -- \<function\>
  - printf -- \<function\>
  - newCanvas -- \<function\>
  - startWrite -- \<function\>
  - endWrite -- \<function\>
  - read -- \<function\>
  - write -- \<function\>
  - close -- \<function\>

##### FONT list:
1. FONT_ASCII7 -- \<object\>
2. FONT_DejaVu9 -- \<object\>
3. FONT_DejaVu12 -- \<object\>
4. FONT_DejaVu18 -- \<object\>
5. FONT_DejaVu24 -- \<object\>
6. FONT_DejaVu40 -- \<object\>
7. FONT_DejaVu56 -- \<object\>
8. FONT_DejaVu72 -- \<object\>
9. FONT_EFontCN24 -- \<object\>
10. FONT_EFontJA24 -- \<object\>
11. FONT_EFontKR24 -- \<object\>

- ##### Color Predefine:
1. BLACK -- 0x0000
2. NAVY -- 128
3. DARKGREEN -- 32768
4. DARKCYAN -- 32896
5. MAROON -- 8388608
6. PURPLE -- 8388736
7. OLIVE -- 8421376
8. LIGHTGREY -- 12632256
9. DARKGREY -- 8421504
10. BLUE -- 255
11. GREEN -- 65280
12. CYAN -- 65535
13. RED -- 16711680
14. MAGENTA -- 16711935
15. YELLOW -- 16776960
16. WHITE -- 16777215
17. ORANGE -- 16753920
18. GREENYELLOW -- 11403055
19. PINK -- 16761035