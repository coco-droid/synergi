const socket = io('http://localhost:5000');

socket.on('connect', () => {
  console.log('Connected to server');
});

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

