class WorkflowEditor {
  constructor(dataflow, customNodes) {
    this.dataflow = dataflow;
    this.customNodes = customNodes;
    this.temporary;
    this.editor;
    this.initEditor();
  }

  initEditor() {
    // Créer l'éditeur Drawflow
    const editor = new Drawflow(document.getElementById("drawflow"));
    editor.reroute = true;
    editor.start();
    editor.import(this.dataflow);
    this.editor=editor;
    // Créer la barre d'options pour les nœuds personnalisés
    const optionsBar = document.getElementById("options-bar");
    this.customNodes.component.forEach((node) => {
      const nodeElement = document.createElement("div");
      nodeElement.classList.add("drag-drawflow");
      nodeElement.setAttribute("draggable", "true");
      nodeElement.setAttribute("data-node", node.name);
      nodeElement.innerHTML = node.icon;
      optionsBar.appendChild(nodeElement);
    });

    // Écouteurs d'événements pour le glisser-déposer
    const elements = document.getElementsByClassName("drag-drawflow");
    for (const element of elements) {
      element.addEventListener("dragstart", (event) => {
        event.dataTransfer.setData("node", event.target.getAttribute("data-node"));
        this.temporary=event.target.getAttribute("data-node");
      });
    }

    // Gérer l'événement de dépose dans l'éditeur
    editor.precanvas.addEventListener("drop", (event) => {
      event.preventDefault();
      //const data = event.dataTransfer.getData("node");
      const data = this.temporary;
      const posX = event.clientX;
      const posY = event.clientY;
      console.log('data'+data);
      //get index in customNodes have object with the same name 
      const index = this.customNodes.component.findIndex((node) => node.name === data);
      console.log(index)
      console.log(this.customNodes)
      this.addNodeToEditor(data, posX, posY,editor,this.customNodes.component[index].input,this.customNodes.component[index].output,this.customNodes.component[index].params,this.customNodes.component[index].html);
    });

    editor.precanvas.addEventListener("dragover", (event) => {
      event.preventDefault();
    });
  }

  addNodeToEditor(nodeName, posX, posY, editor,input,output,params,html) {
    // 
      editor.addNode(
        nodeName,
        input,
        output,
        posX,
        posY,
        nodeName,
        params,
        html
      );


}
zoomEvent(editor){
  let ed=editor;
  document.querySelector('.zoom_in').addEventListener('click',function(){
    ed.zoom_in();
  })
  document.querySelector('.zoom_out').addEventListener('click',function(){
    ed.zoom_out()
  })
}
}
// Exemple de nœuds personnalisés
// Exemple de données de flux de travail
const dataflow= {}

// Initialiser l'éditeur de flux de travail avec les données de flux de travail et les nœuds personnalisés
const workflowEditor = new WorkflowEditor(dataflow, customNodes);
console.log('lol'+workflowEditor.editor)
workflowEditor.zoomEvent(workflowEditor.editor)

  