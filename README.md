# labelimg-container

## Build and Run

/usr/X11/bin/xhost + 192.168.5.110

docker build --tag labelimg:dev --no-cache --file Containerfile .

docker run --rm --name labelimg -e DISPLAY=192.168.5.110:0 -e XAUTHORITY=/.Xauthority --net host -e XDG_RUNTIME_DIR=/tmp/xdgr -v /tmp/.X11-unix:/tmp/.X11-unix -v ~/.Xauthority:/.Xauthority -v ~/Workspace/labelimg/imgs:/home/labelimg/imgs labelimg:dev

## Howto

- https://techsparx.com/software-development/docker/display-x11-apps.html
- https://cuneyt.aliustaoglu.biz/en/running-gui-applications-in-docker-on-windows-linux-mac-hosts/
- https://developers.google.com/webmaster-tools/search-console-api-original/v3/quickstart/quickstart-python

