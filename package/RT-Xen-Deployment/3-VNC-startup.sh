#!/bin/sh
/opt/TurboVNC/bin/vncserver
/opt/TurboVNC/bin/vncserver -kill :1
sed -i '/#!\/bin\/sh/a \/usr\/bin\/xfce4-terminal --geometry=90x30 --show-menubar --show-borders --show-scrollbar --font=10' /root/.vnc/xstartup.turbovnc
/opt/TurboVNC/bin/vncserver
/opt/TurboVNC/bin/vncserver
