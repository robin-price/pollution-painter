from flask import Flask, request
import zmq
import struct

app = Flask(__name__)

@app.route('/get/pm25')
def pm25():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    socket.send_multipart([b"get_pm25"])
    message = socket.recv()
    _pm25 = struct.unpack('f', message)[0]
    socket.close()
    
    json = {
        'pm25' : _pm25
    }
    return json

@app.route('/set/brightness/<brightness>')
def brightness(brightness):
    _brightness = int(brightness)
    if 0 <= _brightness <= 100: 
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:5555")
        socket.send_multipart([b"set_brightness", struct.pack("i", _brightness)])
        message = socket.recv()
        socket.close()

    #echo
    json = {
        'brightness' : _brightness
    }
    return json

@app.route('/set/fade/<fade>')
def fade(fade):
    _fade = int(fade)
    if 0 <= _fade <= 5000: 
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:5555")
        socket.send_multipart([b"set_fade", struct.pack("i", _fade)])
        message = socket.recv()
        socket.close()

    #echo
    json = {
        'fade' : _fade
    }
    return json

@app.route('/set/refresh/<refresh>')
def refresh(refresh):
    _refresh = int(refresh)
    if 0 <= _refresh <= 1000: 
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:5555")
        socket.send_multipart([b"set_refresh", struct.pack("i", _refresh)])
        message = socket.recv()
        socket.close()

    #echo
    json = {
        'refresh' : _refresh
    }
    return json

if __name__ == '__main__':
    app.run