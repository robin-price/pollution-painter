If installing from scratch on fresh SD do the below and be prepared to google error messages ;-) :

Install all python dependencies as root (check python / api source but flask, sds011 come to mind)

Check the conf directory for config files. Copy them to the correct places.

Copy cmdline.txt and config.txt to boot to set UART correctly (we need the 'good' UART to talk reliably to the Arduino) and enable network OTG so you can fallback access over ssh on the USB port

Install create_ap (supplied or from source) and copy create_ap.conf to /etc/ to set pi as acess point 
for reading and 'seeing' the particulate data.

Copy pollution-painter.service to /etc/systemd/system/
pollution-painter.service, check permissions, reload daemons and start / enable service to run at boot.

For webfront end install apache2
Copy conf files to /etc/apache2
Copy mycerts to /etc/ssl (needed for https so AFRAME AR will work - the first time you load page you'll have to add the cert)

Then from the project root directory copy www/html to /var/www

set your hostname to pollutionpainter

good luck!

NB if you're installing from github the project directory needs to be /home/pi/pollution_painter for the paths to work
