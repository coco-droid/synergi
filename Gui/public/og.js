const socket = io('http://localhost:5000');

socket.on('connect', () => {
  console.log('Connected to server');
});
socket.on('image',()=>{
  console.log('image')
})
function handleOpenGraphPreviews(bubbleAttribute) {
    const bubbles = document.querySelectorAll(`${bubbleAttribute}`);
    const processedUrls = new Set();

    bubbles.forEach(bubble => {
        if (bubble.getAttribute("og-see") === "true") return;
        const textContent = bubble.textContent;
        const urls = extractUrlsFromText(textContent);
        socket.emit('opengraph', {url:urls});
        urls.forEach(url => {
            if (!processedUrls.has(url)) {
                const ogId = generateUniqueId();
                const bubbleContent = bubble.innerHTML;
                const linkContent = createLinkContent(url, url);

                bubble.innerHTML = bubbleContent.replace(url, linkContent);
                processedUrls.add(url);
                const link = bubble.querySelector(`[og-id="${url}"]`);
                bubble.setAttribute("og-see", "true");
            }
        });
    });
}

function extractUrlsFromText(text) {
    return text.match(/https?:\/\/[^\s/$.?#].[^\s]*/g) || [];
}

function generateUniqueId() {
    return `og-${Date.now()}`;
}

function createLinkContent(url, ogId) {
    return `<a href="${url}" og-id="${ogId}">${url}</a>`;
}
/*function fetchOpenGraphData(url){
    //post url to server
    fetch(`http://localhost:5000/ogread`,
    {
        method: 'POST',
        body: JSON.stringify({url: url}), 
    }
    ).then(response => response.json())
    .then(data => {
       
    })
    .catch(error => {
        console.error(error);
    });
    
}
*/
function SSEClient(url) {
    this.eventListeners = {};

    this.eventSource = new EventSource(url);

    this.eventSource.onmessage = function(event) {
        const data = JSON.parse(event.data);

        if (data.event && this.eventListeners[data.event]) {
            this.eventListeners[data.event](data.data);
        }
    }.bind(this);

    this.addEventListener = function(event, callback) {
        this.eventListeners[event] = callback;
    };

    this.removeEventListener = function(event) {
        delete this.eventListeners[event];
    };

    this.close = function() {
        this.eventSource.close();
    };
}

var source = new EventSource("http://localhost:5000/event_synergi");
source.addEventListener('synergi_event', function(event) {
    var data = JSON.parse(event.data);
    console.log(data)
    // do what you want with this data
}, false);
