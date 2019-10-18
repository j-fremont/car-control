# car-control

L'objectif est de récupérer une voiture télécommandée et de la piloter à distance via une app web.

Matériel : une voiture télécommandée HS (moteurs bons mais chip TX-RX douteux), un Raspberry, une webcam, un dongle wifi.

Sur la voiture : Rpi, camera, motorshield (moteur), servo-moteur (direction).

La caméra capture une image par seconde.

Un serveur Flask sur le Rpi :
- un service GET pour récupèrer la dernière image capturée par la webcam.
- des services POST pour commander les moteurs.

Sur le PC, une app React :
- qui récupère et affiche l'image récuperée via le service.
- qui donne des contrôles pour appeler les services de commande des moteurs.

Le plus, récupérer la télécommande PS4 au lieu des contrôles de l'app React.

## Préparation et échauffement

Exploration de la GPIO du Raspberry, avec le blink d'une led.

### Flash d'une carte SD avec une image Raspbian

```
$ dd bs=4M if=2018-11-13-raspbian-stretch-lite.img of=/dev/sdb conv=fsync
```

Pour changer le clavier en AZERTY.
```
$ sudo raspi-config
```

Dans Localisation Options, Change Keyboard Layout, Conserver le choix par défaut "Generic 105-Key (Intl) PC", puis sélectionner le choix "French". Sélectionner le clavier "The default for the keyboard layout", et sélectionner le choix "No compose key".

Dans Interfacing Options, activer le serveur SSH.

Dans Network Options, Wi-fi, entrer le SSID et le PSK.

```
$ sudo apt-get install python-pip
$ sudo apt-get install git
```

### Quelques tests du GPIO du Rpi en C

Sur une carte SD Raspbian, récupérer la librairie C WiringPi.

```
$ ssh pi@192.168.1.62
[raspberrypi]$ git clone git://git.drogon.net/wiringPi
[raspberrypi]$ cd wiringPi
[raspberrypi]$ git pull origin
[raspberrypi]./build
```

Code de blink.c
```
#include "../wiringPi/wiringPi/wiringPi.h"

int main (void)
{
  wiringPiSetup() ;
  pinMode(0, OUTPUT) ;
  for (;;)
  {
    digitalWrite(0, HIGH);
    delay(500) ;
    digitalWrite(0, LOW);
    delay(500) ;
  }
  return 0 ;
}
```

```
[raspberrypi]$ gcc blink.c -pthread -lwiringPi -lcrypt -lm -lrt -o blink
```

Cablage (une led + 1 resistance 220ohm, voir le blink déjà utilisé avec l'Arduino starter kit).

Mappging des PIN du Rpi avec celles de wiringPi sur __http://wiringpi.com/pins/__.

### Quelques tests du GPIO du Rpi en Python

Raison : choix d'un serveur Flask, donc passage du C au Python.

```
[raspberrypi]$ pip install RPi.GPIO
```

Code de blink.py
```
import RPi.GPIO as GPIO
import time

pin=17

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT, initial = GPIO.HIGH)

while True:
        GPIO.output(pin, not GPIO.input(pin))
        time.sleep(0.5)
```

Le Pi clobber doit être connecté avec le fil de couleur vers le haut du bornier GPIO (3V3 et 5V power).

Dans gpio_bcm_board_rev1.png et gpio_bcm_board_rev2.png, les chiffres dans les carrés verts sont les BCM, les chiffres dans les ronds sont les BOARD.

### Installation des utilitaires pour la webcam

On installe maintenant quelques utilitaires pour la webcam sur le Raspberry.

#### Pour lire une image

Installation de fswebcam.
```
$ sudo apt-get install fswebcam
```

Capture d'une image.
```
$ fswebcam -r 640x480 --no-banner /tmp/image.jpg
```

Capture d'une image en boucle (toutes les 2 secondes).
```
$ fswebcam -r 640x480 --no-banner /tmp/image.jpg -l2
```

Parfois, la capture part en erreur avec :
```
VIDIOC_STREAMON...
Unable to use mmap
```
Débrancher/rebrancher la webcam corrige le problème (__https://www.raspberrypi.org/forums/viewtopic.php?t=13360__).
Peut-être une solution plus pérenne sur __https://www.raspberrypi.org/forums/viewtopic.php?f=28&t=35689&p=300710&hilit=bandwidth+quirk#p300710__. Pas testé.

#### Pour la video (à priori pas utilisé pour ce projet)

Installation de ffmpeg.
```
$ sudo apt-get install ffmpeg
```

Capture d'une video.
```
$ ffmpeg -t 120 -f v4l2 -framerate 25 -video_size 640x80 -i /dev/video0 output.mkv
```

#### Pour la video live (à priori pas utilisé pour ce projet)

Ou alors trouver le moyen de récupérer le flux vidéo côté PC... A voir.

Installation de mplayer.
```
$ sudo apt-get install mplayer
```

Capture d'une video.
```
$ mplayer tv:// -tv driver=v4l2
```

### Installation du serveur Flask sur le Raspberry

Toujours avec le Rpi connecté en ethernet.

```
[raspberrypi]$ pip install flask flask-cors
```

Code de server.py
Le service get_image récupère la dernière image lue par la webcam.
```
from flask import Flask, request, send_file

app = Flask(__name__)

@app.route("/get_image", methods = ['GET'])
def get_image():
        if request.method == 'GET':
                return send_file('/tmp/image.jpg', mimetype='image/jpg')

if __name__ == '__main__':
        app.run(host='0.0.0.0',port=5000,debug=True)
```

On peut tester côté PC, Curl enregistre l'image dans le répertoire local.

### Connexion du Raspberry en wifi

Avec un dongle Edimax 7811Un, pas de driver au delà d'un noyau 3.9. Mon noyau est en version 4.4.

Donc, installation du driver en manuel : __https://edimax.freshdesk.com/support/solutions/articles/14000035492-how-to-resolve-ew-7811un-built-in-driver-issues-in-linux-kernel-v3-10-or-higher__.

```
$ sudo apt-get install linux-headers-$(uname -r) build-essential dkms
$ sudo reboot
...
$ git clone https://github.com/pvaret/rtl8192cu-fixes.git
$ sudo dkms add ./rtl8192cu-fixes
$ sudo dkms install 8192cu/1.11
$ sudo depmod -a
$ sudo cp ./rtl8192cu-fixes/blacklist-native-rtl8192.conf /etc/modprobe.d/
$ sudo cp ./rtl8192cu-fixes/8192cu-disable-power-management.conf /etc/modprobe.d/
$ sudo reboot
...
$ sudo apt-get install raspberrypi-kernel-headers
$ sudo dkms add ./rtl8192cu-fixes
$ sudo dkms install 8192cu/1.11
```

### Création d'un app React sur le PC

Installer le package qui va permettre de créer une nouvelle app React.
```
$ npm install -g create-react-app
...
$ ls $NODEJS_HOME/bin
bower  create-react-app  gulp  node  npm  npx  yo  yo-complete
```

Création de l'application.
```
$ create-react-app car-ctrl
$ cd car-ctrl
[car-ctrl]$ npm install bootstrap --save
[car-ctrl]$ npm install --save reactstrap react react-dom
```

Importer le CSS de Bootstrap dans *src/index.js*.
```
import 'bootstrap/dist/css/bootstrap.min.css';
```

```xml
<App>
  <MyContainer>
    <Row>
      <Col>
        <MyMedia>
          <Media>
      <Col>
        <MyControls>
          <FormGroup>
            <Button>
            <Button>
            <Button>
```

### Contrôle des moteurs de la voiture à partir du Raspberry

Pour connaître le numérotage des PIN de la GPIO, trouver avant tout le revision code du Raspberry.
```
pi@raspberrypi:~ $ cat /proc/cpuinfo
processor	: 0
model name	: ARMv6-compatible processor rev 7 (v6l)
BogoMIPS	: 697.95
Features	: half thumb fastmult vfp edsp java tls
CPU implementer	: 0x41
CPU architecture: 7
CPU variant	: 0x0
CPU part	: 0xb76
CPU revision	: 7

Hardware	: BCM2835
Revision	: 000e
Serial		: 00000000fe901baf
```

Le revision code est 000e, soit un Rpi B rev2 suivant le tableau ici : https://www.raspberrypi.org/documentation/hardware/raspberrypi/revision-codes/README.md

![Alt text](gpio_bcm_board_rev2.png)

Avec un L293D, commande sur Conrad.

https://business.tutsplus.com/tutorials/controlling-dc-motors-using-python-with-a-raspberry-pi--cms-20051

![Alt text](l293.jpg)

L293 | RPI Blobber, moteur ou battery
- | -
1 (enable 1,2) | #25
2 (in 1) | #24
3 (out 1) | moteur arrière fil rouge
4 (gnd) | GND
5 (gnd) | GND
6 (out 2) | moteur arrière fil noir
7 (in 2) | #23
8 (vcc 2) | batterie fil rouge
9 (vcc 1) | 5v0
10 (in 4) | MOSI
11 (out 4) | moteur avant fil noir
12 (gnd) | GND
13 (gnd) | GND
14 (out 3) | moteur avant fil rouge
15 (in 3) | MISO
16 (enable 3,4) | SCLK

Le Pi clobber doit être connecté avec le fil de couleur vers le haut du bornier GPIO (3V3 et 5V power).

```
$ curl -v --request GET --location http:/192.168.1.45:5000/get_image --output image.jpg
$ curl -v --request POST --location http:/192.168.1.45:5000/forward
$ curl -v --request POST --location http:/192.168.1.62:5000/back
$ curl -v --request POST --location http:/192.168.1.62:5000/left
```

### Récuperation d'une télécommande de PS4

Connexion de la TC sur un port USB, elle est vue sur /dev/hidraw1.
