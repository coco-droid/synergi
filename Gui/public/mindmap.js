function mind_op(e){
  cons
  console.log("op")
  let pop=Popper.createPopper( e.target,
    document.querySelector('#mind_options_popper'));
  document.querySelector('#mind_options_popper').setAttribute("data-show","")
  pop.update();
}
function mind_cus(){
  let pop=Popper.createPopper( e.target,
    document.querySelector('#mind_custom_popper'));
  document.querySelector('#mind_custom_popper').setAttribute("data-show","")
  pop.update();
}
function click_param(t,id)
{

}
class Mindmap_render {
    constructor(element, json) {
        this.json = json;
        this.element = element;
        this.mwd = "";
        this.position_node_array = [];
        this.variation_y=100;
        this.variation_x=120;
        this.box_template= `<div class=".mind_synergie_cnt">
        <div class="mind_synergie_content">${this.json["root"].text}</div>
        <div class="mind_options">
        <span class="ellipsis-vertical" onmouseover="mind_op(e)>
        <i class="fa-solid fa-ellipsis-vertical">
        </i>
        <span class='plus' onmouseover="mind_cus(e)">
        <i class="fa-solid fa-plus">
        </i>
        </span>
        </div>
        </div>`;
    }
    render() {
        let the_nodes=this.generated_nodes();
        console.log(the_nodes)
        window.mindwired
            .init({
                el: this.element,
                ui: { width: "100%", height: "100%"
                
                }
            })
            .then((instance) => {
                this.mwd = instance;
                // install nodes here
                this.mwd.nodes(the_nodes);
            });
    }
    generated_nodes() {
        let nodes_generated;
        console.log(this.json["root"]["children"]);
        let subs_g = this.generate_sub_nodes(this.json["root"]["children"]);
        nodes_generated = {
            model: {
                type: "text",
                text:this.box_template,
            },
            view: {
                x: -20,
                y: 0,
                layout: { type: "X-AXIS" },
                edge: {
                    name: "mustache_lr",
                    color: "#9aabaf",
                    width: 1,
                },
            },
            subs: subs_g,
        };
        
        return nodes_generated;
    }
  
    generate_sub_nodes(children) {
let y_precedent_nodes_values = 0;
let x = 160;
let sub_nodes_generated = [];

if (children !== undefined && children.length !== 0) {
sub_nodes_generated = [];
for (let i = 0; i < children.length; i++) {
    // Generate a random value between -20 and 20 to add to the x position
    const randomXOffset = Math.random() * 80 - 20;
    const randomYOffset = Math.random() * 90 - 20;
    x = x + 40 + randomXOffset;

    let child_y = this.position_calculator(children.length, i, y_precedent_nodes_values);
    if (child_y !=0)
    {
        child_y=child_y+randomYOffset;
    }
    y_precedent_nodes_values = child_y;

    sub_nodes_generated.push({
        model: { text: `<div class=".mind_synergie_cnt"><div class="mind_synergie_content">${children[i].text}</div><div class="mind_options"><i class="fa-solid fa-ellipsis-vertical"></i><i class="fa-solid fa-plus"></i></div></div>` },
        view: { x: x+10, y: child_y },
        subs: this.generate_sub_nodes(children[i].children),
    });
}

return sub_nodes_generated;
}
}
    position_calculator(length, index, prevY) {
if (length === 1) {
return 0;
} else if (length === 2) {
return index === 0 ? length * this.variation_y : -length * this.variation_y;
} else {
const middleIndex = Math.floor(length / 2);
const distanceFromMiddle = index - middleIndex;

if (distanceFromMiddle === 0) {
    return 0;
}

const sign = distanceFromMiddle > 0 ? 1 : -1;
const distanceFromMiddleAbs = Math.abs(distanceFromMiddle);

// Calculating y value based on distance from the middle
const yValue = prevY + sign * distanceFromMiddleAbs * this.variation_y;

return yValue;
}
}

      
}
//test 
let json={
"root": {
  "text": "hello world",
  "children": [
    {
      "text": "hello world",
      "children": [
        {
          "text": "hello world",
          "children": [
            {
              "text": "DEFAULT"
            },
            {
              "text": "X-AXIS"
            },
            {
              "text": "Y-AXIS"
            }
          ]
        },
        {
          "text": "hello world",
          "children": [
            {
              "text": "DEFAULT"
            },
            {
              "text": "CURVE"
            },
            {
              "text": "LINE"
            }
          ]
        },
        {
          "text": "hello world",
          "children": [
            {
              "text": "DEFAULT"
            },
            {
              "text": "RECT"
            },
            {
              "text": "CIRCLE"
            }
          ]
        }
      ]
    },
    {
      "text": "hello world",
      "children": [
        {
          "text": "init"
        },
        {
          "text": "nodes"
        },
        {
          "text": "edges"
        },
        {
          "text": "export"
        },
        {
          "text": "import"
        }
      ]
    },
    {
      "text": "hello world",
      "children": [
        {
          "text": "width"
        },
        {
          "text": "height"
        },
        {
          "text": "background"
        },
        {
          "text": "color"
        },
        {
          "text": "font"
        }
      ]
    }
  ]
}
}
let mindmap_render=new Mindmap_render("#mindmap_synergie",json)
mindmap_render.render()




