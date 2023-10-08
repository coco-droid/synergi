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
 function pop_recommend(obj){
    /*loop in the object:[{
        "name":"test",
        ""content":""
    },...]*/
    
    var textarea=document.querySelector(".message-input");
    let recommend=document.querySelector(".recommend");
    const popperInstance = Popper.createPopper(textarea,recommend,
        {
            placement:'top'
        });
    recommend.innerHTML="";
    for (var i=0; i<obj.length; i++)
    {   
        
        var name=document.createElement("button");
        name.setAttribute("class","name");
        name.innerHTML=obj[i].name;
        recommend.appendChild(name);
        //detect click on this element 
        let ohj=obj[i].name;
        name.addEventListener("click",function(){
            textarea.value+=ohj;
            textarea.focus();
            textarea.select();
            recommend.removeAttribute('data-show')
        })
    }
    recommend.setAttribute('data-show','')
 }
 function emoji_react(el,id){
    console.log('emoji one')
    var message=document.querySelector(`[data-id="${id}"]`);
    let cnt_emoji=document.querySelector('.selectemoji');
    cnt_emoji.setAttribute('data-show','')
    var popperInstance = Popper.createPopper(el,cnt_emoji,
        {
            placement:'left'
        }
    );
    var options=cnt_emoji.querySelectorAll('span');
    //loop in options to detect click on him
    options.forEach(option => {
        console.log(option)
        option.addEventListener("click", function() {
            // Code to execute when an option is clicked
            console.log('eer')
            attachinmessage(option.innerHTML,message)
        });
      
    });
    
function attachinmessage(emj,ele){
    console.log('attach')
    var emojiDiv = document.createElement("div");
    emojiDiv.setAttribute("class","emoji-react");
    var emoji=document.createElement("span");
    emoji.setAttribute("class","emoji-at");
    emoji.style.borderRadius='50%';
    emoji.style.marginTop='-8px';
    emoji.innerHTML=emj;
    emojiDiv.appendChild(emoji);
    ele.appendChild(emojiDiv);
    var popperInstances = Popper.createPopper(ele,emojiDiv,
        {
            placement:'bottom-end'
        }
    );
    emoji_end('')
    }
 }
 function emoji_end(el){
    var vbj=document.querySelector('.selectemoji');
    vbj.removeAttribute('data-show') 
 }
 function reply_react(el,id,name)
 {
    var message=document.querySelector(`[data-id="${id}"]`);
    var messageText=message.innerText;
    var first200Chars = messageText.substring(0, 200);
    previewbox(`<div style="display:flex;">
    <div style="display: flex;
    flex-direction: column;
    border-left: 2px solid #123d7b;
    padding-left: 8px;
    margin-right: 8px;">
    <span>${name}</span>
      <span>${first200Chars}</span>
    </div>
    <span style="height:100%;color:#ffffff4f;align-items:center;display:flex;background:transparent;">
    <i class="fa-solid fa-xmark" id="close"></i>
  </span>
    </div>`)
 }
 function previewbox(filepreview){
    var file_preview=document.querySelector('.file_preview')
    document.querySelector('.chat__conversation-board').style.height="calc(100vh - 95px - 2em - .5em - 5em)"
    //display file preview like a floating tooltip on top of the chat conversational board
      var chat_board=document.querySelector('.chat__conversation-panel');
      file_preview.innerHTML=filepreview;
      //get chat board height
      var chat_board_height=chat_board.offsetHeight;
      //position the file preview tooltip
      //file_preview.style.top=chat_board.offsetTop-chat_board_height-10+"px";
      file_preview.style.height=50+"px";
      //file_preview.style.left=chat_board.offsetLeft+9+"px";
      //file_preview.style.position="absolute";
      //z-index
     // file_preview.style.zIndex="1000";
      //display file preview  height: calc(100vh - 95px - 2em - .5em - 3em);
      file_preview.style.display="flex";
      document.querySelector('#close').addEventListener('click',async ()=>{
        document.querySelector('.chat__conversation-board').style.height="calc(100vh - 95px - 2em - .5em - 3em)"
        file_preview.style.display='none';
        filepreview='';
      })
 }