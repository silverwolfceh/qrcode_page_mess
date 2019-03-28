Z:
cd Z:\\gitwork\\qrcode_page_mess
rmdir dist /s /q
rmdir build /s /q
pyinstaller build.spec
rmdir build /s /q
pause