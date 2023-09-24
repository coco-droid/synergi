let filepreview ,filebol,fileData,fileName;
let file_preview=document.querySelector('.file_preview');
  // Client side 
// Listen for event
/*socket.on('message', (data) => {
  displayMessage(data,'bot');
});*/
socket.on('task',(data)=>{
  displayMessage(data,'task');
})
socket.on('task_update',(data)=>{
  console.log(data);
  document.getElementById(data.id).innerHTML=data.title;
})
socket.on('opengraph_data',(data)=>{
  console.log('Trace:');
  console.log(data)
//loop into the object data[url]
for (let key in data) {
  if (data.hasOwnProperty(key)) {
    console.log(`Key: ${key}`);
    console.log(`Value: ${data[key]}\n`);
    console.log(data[key]);
  const link = document.querySelector(`[og-id="${key}"]`);
  if (link) {
      // Implement your logic to display the Open Graph data using a pop-up or tooltip
      var popup=document.createElement("div");
      popup.setAttribute("class","poppertip");
      popup.setAttribute("urlp",key)
      link.setAttribute('onmouseover',` document.querySelector('[urlp="${key}"]').setAttribute('data-show', '');`)
      link.setAttribute('onmouseout',` console.log('hijack');document.querySelector('[urlp="${key}"]').removeAttribute('data-show')`)
      var img=document.createElement("img");
      img.setAttribute("src",data[key].image);
      img.setAttribute("class","popper__image");
      var title=document.createElement("h3");
      title.setAttribute("class","popper__title");
      title.innerHTML=data[key].title;
      var description=document.createElement("p");
      description.setAttribute("class","popper__description");
      description.innerHTML=data[key].description;
      popup.appendChild(img);
      popup.appendChild(title);
      popup.appendChild(description);
      link.appendChild(popup);
      console.log('hi')
const popperInstance = Popper.createPopper(link,document.querySelector(`[url_p="${key}"]`));
  }
  }
}
})

//function send message
function sendMessage() {
  //get message from input
  const message = document.querySelector('.message-input').value;
  //check if message is empty
  if (!message) return;
  //display message in the chat
  //emit message to server
  if(filebol==true)
  {
    displayMessage({message: message}, 'user');
    //socket.emit('with_file', {sendMessage: message,file:fileData,name:fileName});
    fetchOnserver('http://localhost:5000/message',{sendMessage: message,file:fileData,name:fileName,haveFile:true},function(res){
      displayMessage({message:res.msg},'bot');
    })
  }
  else{
    displayMessage({message: message}, 'user');
  //socket.emit('message', {sendMessage: message});
  fetchOnserver('http://localhost:5000/message',{sendMessage: message,file:fileData,name:fileName,haveFile:false},function(res){
      displayMessage({message:res.msg},'bot');
    })
  }
  //clear input
  document.querySelector('.message-input').value = '';
}
//function display message
function displayMessage(data, type) {

  if(type=="bot"){//#9991f698
  //display message in the chat
   document.querySelector('.chat__conversation-board').innerHTML += parseMarkdownAndLatex(`
   <div class="chat__conversation-board__message-container">
          <div class="chat__conversation-board__message__context">
            <div class="chat__conversation-board__message__bubble"> <span style=" background-color: #1F71D7ff;">${data.message}</span></div>
          </div>
          <div class="chat__conversation-board__message__options">
            <button class="btn-icon chat__conversation-board__message__option-button option-item emoji-button">
              <svg class="feather feather-smile sc-dnqmqq jxshSx" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <circle cx="12" cy="12" r="10"></circle>
                <path d="M8 14s1.5 2 4 2 4-2 4-2"></path>
                <line x1="9" y1="9" x2="9.01" y2="9"></line>
                <line x1="15" y1="9" x2="15.01" y2="9"></line>
              </svg>
            </button>
            <button class="btn-icon chat__conversation-board__message__option-button option-item more-button">
              <svg class="feather feather-more-horizontal sc-dnqmqq jxshSx" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <circle cx="12" cy="12" r="1"></circle>
                <circle cx="19" cy="12" r="1"></circle>
                <circle cx="5" cy="12" r="1"></circle>
              </svg>
            </button>
          </div>
        </div>`);
      }
      else if (type=="user" && filebol==true)
      {
        document.querySelector('.chat__conversation-board').style.height="calc(100vh - 95px - 2em - .5em - 3em)"
        file_preview.style.display='none';
        document.querySelector('.chat__conversation-board').innerHTML += parseMarkdownAndLatex(`
        <div class="chat__conversation-board__message-container reversed">
          <div class="chat__conversation-board__message__context">
            <div class="chat__conversation-board__message__bubble"> <span style="background-color:#123D7Bff;">
              <div style="display:flex; padding:5px;" class='preview-chat'>
                   ${filepreview}
              </div>
              ${data.message}</span></div>
          </div>
          <div class="chat__conversation-board__message__options">
            <button class="btn-icon chat__conversation-board__message__option-button option-item emoji-button">
              <svg class="feather feather-smile sc-dnqmqq jxshSx" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <circle cx="12" cy="12" r="10"></circle>
                <path d="M8 14s1.5 2 4 2 4-2 4-2"></path>
                <line x1="9" y1="9" x2="9.01" y2="9"></line>
                <line x1="15" y1="9" x2="15.01" y2="9"></line>
              </svg>
            </button>
            <button class="btn-icon chat__conversation-board__message__option-button option-item more-button">
              <svg class="feather feather-more-horizontal sc-dnqmqq jxshSx" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <circle cx="12" cy="12" r="1"></circle>
                <circle cx="19" cy="12" r="1"></circle>
                <circle cx="5" cy="12" r="1"></circle>
              </svg>
            </button>
          </div>
        </div>
        `);
      }
      else if (type=="task"){
        /* data.tasks:
       {
        Goal:"",
        tasks:
        [
          {
            id:"",
            title:""
          },
          ...
        ]
        }
        */
       let tasks_html='';
       for(var i=0; i<=data.tasks; i++)
       {
         tasks_html+=`
         <div class="task_me">
           <span style="background-color:transparent; id="${data.tasks[i].id}">${data.tasks[i].title}</span>
           <i class="fa-solid fa-spinner fa-spin"></i>
          </div>
         `;
       }
       document.querySelector('.chat__conversation-board').innerHTML +=parseMarkdownAndLatex(`
       <div class="chat__conversation-board__message-container">
        <div class="chat__conversation-board__message__context">
          <div class="chat__conversation-board__message__bubble"> 
            <span style=" background-color: #9991f698;"><bold>Goal:</bold>${data.Goal}
              <!--task-->
              <div class="task_box">
                 ${tasks_html}
            </div>
            </span>
          </div>
        </div>
      </div>
       `);
      }
      else{//#f52cf580
        document.querySelector('.chat__conversation-board').innerHTML += parseMarkdownAndLatex(` <div class="chat__conversation-board__message-container reversed">
          <div class="chat__conversation-board__message__context">
            <div class="chat__conversation-board__message__bubble"> <span style="background-color:#123D7Bff;">${data.message}</span></div>
          </div>
          <div class="chat__conversation-board__message__options">
            <button class="btn-icon chat__conversation-board__message__option-button option-item emoji-button">
              <svg class="feather feather-smile sc-dnqmqq jxshSx" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <circle cx="12" cy="12" r="10"></circle>
                <path d="M8 14s1.5 2 4 2 4-2 4-2"></path>
                <line x1="9" y1="9" x2="9.01" y2="9"></line>
                <line x1="15" y1="9" x2="15.01" y2="9"></line>
              </svg>
            </button>
            <button class="btn-icon chat__conversation-board__message__option-button option-item more-button">
              <svg class="feather feather-more-horizontal sc-dnqmqq jxshSx" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <circle cx="12" cy="12" r="1"></circle>
                <circle cx="19" cy="12" r="1"></circle>
                <circle cx="5" cy="12" r="1"></circle>
              </svg>
            </button>
          </div>
        </div>`);
      }
      //auto scroll
      var chat_board=document.querySelector('.chat__conversation-board');
      chat_board.scrollTop=chat_board.scrollHeight;
      renderSnippet();
      function renderSnippet()
      {
        hljs.highlightAll();

// Add copy buttons to code blocks
const codeBlocks = document.querySelectorAll('code');
codeBlocks.forEach((codeBlock) => {
  const copyButton = document.createElement('button');
  copyButton.classList.add('copy-button');
  copyButton.textContent = 'Copy';

  copyButton.addEventListener('click', () => {
    const code = codeBlock.textContent;

    navigator.clipboard.writeText(code)
      .then(() => {
        copyButton.textContent = 'Copied!';
        setTimeout(() => {
          copyButton.textContent = 'Copy';
        }, 1500);
      })
      .catch((error) => {
        console.error('Copy failed:', error);
      });
  });

  codeBlock.parentNode.insertBefore(copyButton, codeBlock.parentNode.firstChild);
});
      }
      function parseMarkdownAndLatex(text) {
  // Parse Markdown tags
  text = text.replace(/<markdown>([\s\S]*?)<\/markdown>/g, function(match, p1) {
    return '<div class="markdown">' + marked(p1) + '</div>';
  });

  // Parse LaTeX tags using MathJax
  text = text.replace(/<latex>([\s\S]*?)<\/latex>/g, function(match, p1) {
    //render with mathjax before returning
    p1=MathJax.tex2chtml(p1).outerHTML;
    console.log('text:'+p1);
    return '<div class="latex">' + p1 + '</div>';
  });

  return text;
}
handleOpenGraphPreviews(".chat__conversation-board__message__bubble");

}
//listen for click on send message button
document.querySelector('.send-message-button').addEventListener('click', sendMessage);
document.querySelector('.btn').addEventListener('click', function(){
  document.querySelector('.first').style.display = "none";
  document.querySelector('#chat').style.display = "block";
}

);
document.querySelector('.fa-clock-rotate-left').onclick=function(){
  document.querySelector('.third').style.display = "flex";
  document.querySelector("#chat").style.display="none";
  socket.emit('get_history',{req:'date'});}
  socket.on('history',(data)=>{
    data=data['message'];
    console.log(data);
    for(var i=0; i<data.length; i++)
    {
      document.querySelector('.the_history').innerHTML+=`
      <div class="a_history" style="display: flex;
      border-radius: 12px;
      background: burlywood;
      padding: 9px;
      text-align: left;">
      <div style="display:flex;flex-direction: column;align-items: flex-start;">
          <span class="summary_conversation">
            ${data[i].summary}
          </span>
          <span class="date_conversation">
            ${data[i].Date}
          </span>
      </div>
      <i class="fa-solid fa-trash" date='${data[i].Date}'></i>
      </div>
      `;
    }
    document.querySelectorAll(".a_history>i").forEach((element)=>{
      element.onclick=function(){
        console.log("hi")
        socket.emit('delete_history',{date:element.getAttribute('date')});
      }
    }
    )
  });
// dropzone 
const supportsFileSystemAccessAPI =
  "getAsFileSystemHandle" in DataTransferItem.prototype;
const supportsWebkitGetAsEntry =
  "webkitGetAsEntry" in DataTransferItem.prototype;

const elem = document.querySelector("#chat");
//const debug = document.querySelector("body");

elem.addEventListener("dragover", (e) => {
  // Prevent navigation.
  e.preventDefault();
});

elem.addEventListener("dragenter", (e) => {
  elem.style.outline = "solid red 1px";
});

elem.addEventListener("dragleave", (e) => {
  elem.style.outline = "";
});

elem.addEventListener("drop", async (e) => {
  e.preventDefault();
  elem.style.outline = "";
  const fileHandlesPromises = [...e.dataTransfer.items]
    .filter((item) => item.kind === "file")
    .map((item) =>
      supportsFileSystemAccessAPI
        ? item.getAsFileSystemHandle()
        : supportsWebkitGetAsEntry
        ? item.webkitGetAsEntry()
        : item.getAsFile()
    );

  for await (const handle of fileHandlesPromises) {
    if (handle.kind === "directory" || handle.isDirectory) {
      console.log(`Directory: ${handle.name}`);
      //debug.textContent += `Directory: ${handle.name}\n`;
    } else {
      filebol=true;
      console.log(`File: lol ${handle.name}`);
      fileName=handle.name;
      //file preview in tippy tooltip on top of the chat conversational board
      const file = await handle.getFile();
      const reader = new FileReader();
      function typeFile(ext){
        //detect if .txt:txt.png,.doc:doc.png,.pdf:pdf.png, or it other use file.png
        if(ext[1]=="txt"){
          return "txt.png";
        }
        else if(ext[1]=="doc"){
          return "doc.png";
        }
        else if(ext[1]=="pdf"){
          return "pdf.png";
        }
        else{
          return "file.png";
        }
      }
      filepreview=`
                 <div class="file_ext" style="display:flex;align-items:center;justify-content:center;padding:1px;">
                    <img src="${typeFile(file.name.split('.'))}" style="height:100%;"/>
                  </div>
                  <div class="file_name">
                    <span style="background:transparent;margin:0;">${file.name}</span>
                    <span style="background:transparent;font-size:0.7rem;margin:0;">${file.size}</span>
                  </div>
                  <span style="height:100%;color:#ffffff4f;align-items:center;display:flex;background:transparent;">
                    <i class="fa-solid fa-xmark" id="close"></i>
                  </span>
      `;
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
        fileData = await file.arrayBuffer();
        const formData = new FormData();
        formData.append("file", file);

        fetch("http://localhost:5000/upload", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error(data.error);
            } else if (data.url) {
               console.log(data);
            }
        })
        .catch(error => {
            console.error(error);
        });
                }
  }
});
/*animation to sync bubble text box with sound */
var waveContainer = document.querySelector(".wave-container");
var wave = new SiriWave({
  container: waveContainer,
  width: 200,
  height: 100,
  style: "ios",
  amplitude: 0.5,
  frequency: 6,
  color: "#fff",
});
  function animateBubble(element,element2, audio,callback) {
    let text = element.textContent;
  element.textContent = "";
  element2.style.display="block";
  let index = 0;
  let duration = audio.duration * 1000; // Convert audio duration to milliseconds

  // Calculate the delay between displaying each character based on audio duration
  let charDelay = duration / text.length;
  audio.play()
  element.style.opacity = 1;
  wave.start();
  function typeWriter() {
    if (index < text.length) { 
      element.textContent += text.charAt(index);
      index++;
      setTimeout(typeWriter, charDelay);
      //detect when the audio finish
    } else {
      // Show wave animation and sync with audio
      element.style.opacity = 1;
      wave.start();
    }
  }
 typeWriter();
 audio.addEventListener('ended',()=>{
        //element.style.opacity = 0;
        callback();
      })
}
// Call the animateBubble function for each bubble box
let bubble1 = document.querySelector(".bubble1");
document.querySelector("#dropzonewidget > div.--dark-theme.first > div:nth-child(1) > img").onclick=function(){
  let audio1 = document.getElementById("audio1");
animateBubble(bubble1,document.querySelectorAll('.bubble_box')[0],audio1,()=>{
  var bubble2 = document.querySelector(".bubble2");
var audio2 = document.getElementById("audio2");
animateBubble(bubble2,document.querySelectorAll('.bubble_box')[1],audio2,()=>{
  console.log('finish!')
});
});}
document.querySelector("#search").onchange = function(){
  scrollonconversation(document.querySelector("#search").value);
}

function scrollonconversation(text)
{
  var the_history=document.querySelector('.the_history');
  var a_history=document.querySelectorAll('.a_history');
  //loop to search text correspondance in elements
  for(var i=0; i<a_history.length; i++)
  {
   //detect if we have matches 
    if(a_history[i].textContent.includes(text))
    {
      //scroll on the element in  the_history
      the_history.scrollTop=a_history[i].offsetTop;
      //break the loop
      break;
    }
  }

}
function fetchOnserver(url,data,callback)
{
  // Créer un objet XMLHttpRequest
var xhr = new XMLHttpRequest();
// Configuration de la requête POST
xhr.open("POST",url, true);
// Configuration du timeout personnalisé (en millisecondes)
xhr.timeout = 150000000; // Timeout de 15 secondes
// Définir le gestionnaire d'événement pour la réponse
xhr.onreadystatechange = function () {
if (xhr.readyState === 4) { // La requête est terminée
if (xhr.status === 200) { // Le serveur a répondu avec succès
  var response = xhr.responseText;
   callback(JSON.parse(response))
} else {
console.error("Erreur de requête. Statut :", xhr.status);
}
}
};
// Gérer les erreurs de timeout
xhr.ontimeout = function () {
console.error("La requête a expiré en raison d'un timeout.");
};
// Configurer les en-têtes de la requête (si nécessaire)
xhr.setRequestHeader("Content-Type", "application/json");
// Envoyer la requête avec les données
xhr.send(JSON.stringify(data));
}