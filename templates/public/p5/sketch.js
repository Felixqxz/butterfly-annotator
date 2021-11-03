class Polygon {

  constructor(dots) {
    this.dots = dots;
  }

  display() {
    beginShape();
    for (let i = 0; i < this.dots.length - 1; i++) {
      const n = this.dots[i];
      const m = this.dots[i+1];
      line(n[0], n[1], m[0], m[1]);
    }
    endShape();
  }
}

let polygons = [];
let polygons_i = 0;
let dots = [];
let dots_i = 0;
const colours = [[0,0,255], [255,0,0], [0,255,0], [255,255,0], [0,255,255], [255,0,255]];
let colour_i = 0;

let drawing = false;
const dev = 8;
const dotSize = 8
let predX, predY;

let img;

function setup() {

  var width = document.getElementById('canvas').getAttribute('width')
  var height = document.getElementById('canvas').getAttribute('height')
  img = loadImage(document.getElementById('canvas').getAttribute('image_url'))
  console.log(img)
  canvas = createCanvas(width, height);
  canvas.parent("canvas");

  button = createButton('Submit Selections');
  button.mousePressed(submitPolygons);

  button2 = createButton('Delete Polygon');
  button2.mousePressed(deletePolygon);
  
  strokeWeight(2);
}

function draw() {
  background(220);
  image(img, 0, 0, width, height)
  for (let i = 0; i < polygons_i; i++) {
    stroke(colours[i]);
    polygons[i].display();
  }
  if (drawing) {
    stroke(colours[colour_i])
    ellipse(mouseX, mouseY, dotSize);
    line(predX, predY, mouseX, mouseY);
    for (let i = 0; i < dots_i - 1; i++) {
      const n = dots[i];
      const m = dots[i+1];
      line(n[0], n[1], m[0], m[1]);
      ellipse(n[0], n[1], dotSize);
    }
    ellipse(predX, predY, dotSize);
  }

}

function mousePressed() {
  if (mouseWithInCanvas()) {
    if (drawing) {
      if (dist(dots[0][0], dots[0][1], mouseX, mouseY) < dev) {
        if (dots_i != 1) {
          predX = mouseX;
          predY = mouseY;
          dots[dots_i++] = dots[0];
          polygons[polygons_i++] = new Polygon(dots);
          colour_i++;
        } 
        dots = [];
        dots_i = 0;
        drawing = false;
      } else if (dist(predX, predY, mouseX, mouseY) < dev) {
        dots_i--;
        predX = dots[dots_i-1][0];
        predY = dots[dots_i-1][1];
      } else {
        predX = mouseX;
        predY = mouseY;
        dots[dots_i++] = [mouseX, mouseY];
      }
    } else {
      predX = mouseX;
      predY = mouseY;
      dots[dots_i++] = [mouseX, mouseY];
      drawing = true;
    }
  }
}

function mouseWithInCanvas() {
  return 0 < mouseX & mouseX < width & 0 < mouseY & mouseY < height
}


function submitPolygons() {
  var form = document.createElement('form')
  // for (let i = 0; i < polygons_i; i++) {
  //   var polygonElement = document.createElement()
    
  // }
  form.method = 'POST'
  form.submit()
}

function deletePolygon() {
  polygons_i--;
  colour_i--;
}
