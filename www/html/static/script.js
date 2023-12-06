function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

const getLocation = function () {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);

    } else { 
        latTag.innerHTML = "__.___";
        longTag.innerHTML = "__.___";
    }
}
  
const showPosition = (position) => {
    let longitude = position.coords.longitude;
    let latitude = position.coords.latitude;
    console.log("latitude: " + latitude);
    console.log("longitude: " + longitude);
    latTag.innerHTML = latitude.toFixed(3);
    longTag.innerHTML = longitude.toFixed(3);
    let url = `https://u50g7n0cbj.execute-api.us-east-1.amazonaws.com/v2/latest?limit=100&page=1&offset=0&sort=desc&coordinates=${latitude.toFixed(8)}%2C${longitude.toFixed(8)}&radius=50000&order_by=lastUpdated&dumpRaw=false`;
    console.log(url);
    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log(data)
            if (data.results.length > 0) {
                console.log(data.results[0].measurements)
                data.results[0].measurements.forEach((number, index) => {
                    console.log(data.results[0].measurements[index].parameter)
                    if (data.results[0].measurements[index].parameter == "pm25") {
                        console.log(data.results[0].measurements[index].value)
                        pm25Tag.innerHTML = data.results[0].measurements[index].value
                        const testEntity = document.createElement('a-entity');
                        testEntity.setAttribute('mythreejsthing', 'color: yellow;')
                        testEntity.setAttribute('gps-entity-place', `latitude: ${latitude}; longitude: ${longitude};`)
                        testEntity.setAttribute('position', '0, 5, -5')
                        testEntity.setAttribute('scale', '20, 20');
                        scene.appendChild(testEntity)
                    }
                })
            }
        });
}

const getAirQuality = function() {
  let endpoint = `https://pollutionpainter.local/api/get/pm25`;
  console.log(endpoint);
  return fetch(endpoint)
    .then(response => response.json())
    .then(data => {
      console.log(data);
      return data;
    });
}
  
window.onload = () => {
  const latTag = document.querySelector('#latitude')
  const longTag = document.querySelector('#longitude')
  const pm25Tag = document.querySelector('#pm25')
  const scene = document.querySelector('a-scene');

  // first get current user location
  return navigator.geolocation.getCurrentPosition(function (position) {
    let longitude = position.coords.longitude;
    let latitude = position.coords.latitude;
    console.log("latitude: " + latitude);
    console.log("longitude: " + longitude);
    latTag.innerHTML = latitude.toFixed(3);
    longTag.innerHTML = longitude.toFixed(3);

    // get air quality data
    getAirQuality()
      .then((results) => {
        console.log(results)
        const pm25 = parseFloat(results["pm25"]).toPrecision(3)
        if (pm25 > 0) {
          pm25Tag.innerHTML = pm25
          const particleSystem = document.createElement('a-entity')
          particleSystem.setAttribute('id', "particles")
          particleSystem.setAttribute('position', '0 0 0')
          particleSystem.setAttribute('gps-entity-place', `latitude: ${latitude}; longitude: ${longitude};`)
          particleSystem.setAttribute('particle-system', {preset: 'dust', texture: 'https://pollutionpainter.local/static/smokeparticle.png', particleCount: pm25*100, size: 2})
          scene.appendChild(particleSystem)
          const readingARText = document.createElement('a-entity')
          readingARText.setAttribute('id', "readingARText")
          readingARText.setAttribute('position', '0 0 -3')
          readingARText.setAttribute('gps-entity-place', `latitude: ${latitude}; longitude: ${longitude};`)
          readingARText.setAttribute('text', {value: "hello"})
          readingARText.setAttribute('scale', '3 3 3')
          scene.appendChild(readingARText)
         
      }    
    });
  },
    (err) => console.error('Error in retrieving position', err),
    {
      enableHighAccuracy: true,
      maximumAge: 0,
      timeout: 27000,
    }
  );
};
  
setInterval(function() {
  //get prev pm25
  const pm25Tag = document.querySelector('#pm25')
  const prevPm25 = parseFloat(pm25Tag.textContent)
  console.log("prev pm 2.5 = " + prevPm25)
  const particleSystem = document.querySelector('#particles')
  getAirQuality()
      .then((results) => {
        console.log(results)
        const pm25 = parseFloat(results["pm25"]).toPrecision(3)
        if (pm25 > 0) {
          pm25Tag.innerHTML = pm25
          const change = ((pm25-prevPm25)/pm25)*100
          console.log("percentage change in pm25 = " + change)
          if (Math.abs(change) > 50) {
            particleSystem.removeAttribute('particle-system')
            particleSystem.setAttribute('particle-system', {preset: 'dust', texture: 'https://pollutionpainter.local/static/smokeparticle.png', particleCount: pm25*100, size: 2})
            
          }
        }
      });
    }, 10000)// every 10 secs


function screenshot() {
  const pm25Tag = document.querySelector('#pm25')
  const pm25 = pm25Tag.textContent.replace('.','-')
  document.querySelector("video").pause();
  let aScene = document
  .querySelector("a-scene")
  .components.screenshot.getCanvas("perspective");
  let frame = captureVideoFrame("video", "png");
  aScene = resizeCanvas(aScene, frame.width, frame.height);
  frame = frame.dataUri;
  mergeImages([frame, aScene]).then(b64 =>
  {
    let link = document.getElementById("download-link", "png");
    link.setAttribute("download", "pm_2-5_" + pm25 + ".png");
    link.setAttribute("href", b64);
    link.click();
  });
  document.querySelector("video").play();
}


function resizeCanvas(origCanvas, width, height)
{
    let resizedCanvas = document.createElement("canvas");
    let resizedContext = resizedCanvas.getContext("2d");

    // if (screen.width < screen.height)
    // {
    //     var w = height * (height / width);
    //     var h = width * (height / width);
    //     var offsetX = -(height - width);
    // }
    // else
    // {
    //     var w = width;
    //     var h = height;
    //     var offsetX = 0;
    // }

    var w = width;
    var h = height;
    var offsetX = 0;
    resizedCanvas.height = height;
    resizedCanvas.width = width;

    resizedContext.drawImage(origCanvas, offsetX, 0, w, h);
    return resizedCanvas.toDataURL();
}

function captureVideoFrame(video, format, width, height)
{
    if (typeof video === 'string')
    {
        video = document.querySelector(video);
    }

    format = format || 'jpeg';

    if (!video || (format !== 'png' && format !== 'jpeg'))
    {
        return false;
    }

    var canvas = document.createElement("CANVAS");

    canvas.width = width || video.videoWidth;
    canvas.height = height || video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    var dataUri = canvas.toDataURL('image/' + format);
    var data = dataUri.split(',')[1];
    var mimeType = dataUri.split(';')[0].slice(5)

    var bytes = window.atob(data);
    var buf = new ArrayBuffer(bytes.length);
    var arr = new Uint8Array(buf);

    for (var i = 0; i < bytes.length; i++)
    {
        arr[i] = bytes.charCodeAt(i);
    }

    var blob = new Blob([ arr ], { type: mimeType });
    return { blob: blob, dataUri: dataUri, format: format, width: canvas.width, height: canvas.height };
}
