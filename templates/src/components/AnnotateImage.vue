<template>
  <b-container>
    <b-row class="justify-content-center" style="padding-bottom: 2em;">
      <div id="canvas"/>
    </b-row>
    <b-row class="mb-2">
      <b-col md="6" xs="12">
        <!-- the description part -->
        <h4>Image description</h4>
        <b-card class="mb-2">
          <p @mouseup="checkTextSelection()" id="description-selection" style="white-space: pre-line">
            {{ textDescription() }}
          </p>
        </b-card>
        <b-button @click="addDescriptionBit()" :disabled="bitButtonDisabled">Add bit</b-button>
      </b-col>
      <!-- the linking between the tags and the polygons -->
      <b-col md="6" xs="12">
        <!-- list of polygons -->
        <h4>Available region</h4>
        <b-list-group>
          <b-list-group-item v-for="polygon in availablePolygons"
                             v-bind:key="polygon.i"
                             class="no-drag"
                             :active="selectedPolygon === polygon.i"
                             @click="selectPolygon(polygon.i)">
            Polgyon number {{ polygon.i }}
          </b-list-group-item>
        </b-list-group>
      </b-col>
    </b-row>
    <b-row>
      <b-col>
        <b-list-group>
          <b-list-group-item v-for="(annotation, idx) in annotations" v-bind:key="idx">
            {{ annotation.description }}
          </b-list-group-item>
        </b-list-group>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import {mapActions} from 'vuex'
import P5 from 'p5'

export default {
  name: 'AnnotateImage',
  data() {
    return {
      description: '', // of the image
      imageData: null,
      availablePolygons: [],
      selectedPolygon: -1,
      bitButtonDisabled: true,
      annotations: [],
    }
  },
  methods: {
    ...mapActions({fetchImageData: 'fetchImageData'}),
    textDescription() {
      return this.imageData ? this.imageData.description : ''
    },
    selectPolygon(i) {
      this.selectedPolygon = i
    },
    checkTextSelection() {
      const selectedText = window.getSelection().toString().trim()
      if (!selectedText) {
        this.bitButtonDisabled = true
        return
      }
      // no overlap, proceed
      this.bitButtonDisabled = false
    },
    addDescriptionBit() {
      const selected = window.getSelection().toString().trim()
      this.bitButtonDisabled = true
      window.getSelection().empty()
      if (this.selectedPolygon !== -1) {
        this.annotations.push({ polygon: this.availablePolygons[this.selectedPolygon], description: selected })
      }
    },
  },
  mounted() {
    const t = this
    const script = p5 => {
      // draws lines that connect all (i, i + 1) dots and closes the shape if close is true
      const connectDotsOpen = (dots, close) => {
        p5.beginShape()
        for (let i = 0; i < dots.length - 1; i++) {
          const currentPoint = dots[i]
          const nextPoint = dots[i + 1]
          p5.line(currentPoint.x, currentPoint.y, nextPoint.x, nextPoint.y)
        }
        if (close) {
          // join the first and last points of the polygon
          const first = dots[0]
          const last = dots[dots.length - 1]
          p5.line(last.x, last.y, first.x, first.y)
        }
        p5.endShape()
      }

      class Polygon {
        constructor(dots, i) {
          this.dots = dots
          this.i = i
        }

        display() {
          connectDotsOpen(this.dots, true)
        }
      }

      // the radius around a point we allow
      const EPS = 15
      // the disk following the mouse
      const MOUSE_RAD = 10
      const MOUSE_STROKE_WEIGHT = 2
      // general stroke weight
      const STROKE_WEIGHT = 4

      // we will build a color sequence that always assigns the same color to a given index
      // (color(0), color(1), ..., color(n), ...)
      const colorSequence = i => {
        return p5.color((16 * i) % 256, (128 * i) % 256, (30 * i) % 256)
      }

      // allows to check if the mouse is within the canvas
      const mouseInCanvas = () => 0 < p5.mouseX && p5.mouseX < t.imageData.width
          && 0 < p5.mouseY && p5.mouseY < t.imageData.height

      // returns true if the two provided points are considered to be close enough
      // so that they are at the same position, provided the tolerance radius `EPS`
      // (used for the user's mouse and another point)
      const closeEnough = (a, b) => a.dist(b) < EPS

      // variables
      let currentPoints = []
      let annotateImage = undefined

      // P5 handling
      p5.setup = () => {
        p5.createCanvas(t.imageData.width, t.imageData.height)
        annotateImage = p5.loadImage(t.$hostname + '/api/' + t.imageData.imageUrl)
      }

      p5.draw = () => {
        p5.clear()
        p5.background(255, 204, 0) // just a default background
        // display the image to be annotated
        p5.image(annotateImage, 0, 0, t.imageData.width, t.imageData.height)
        // display all polygons
        p5.strokeWeight(STROKE_WEIGHT)
        t.availablePolygons.forEach((polygon, i) => {
          p5.stroke(colorSequence(i))
          polygon.display()
        })
        p5.stroke(colorSequence(t.availablePolygons.length))
        // draw the current polygon being drawn
        if (currentPoints.length > 0) {
          connectDotsOpen(currentPoints, false)
          // connect the last point to the mouse's position
          const last = currentPoints[currentPoints.length - 1]
          p5.line(last.x, last.y, p5.mouseX, p5.mouseY)
        }
        p5.strokeWeight(MOUSE_STROKE_WEIGHT)
        p5.fill(colorSequence(t.availablePolygons.length))
        p5.ellipse(p5.mouseX, p5.mouseY, MOUSE_RAD)
      }

      p5.mousePressed = () => {
        if (mouseInCanvas()) {
          // if the user hasn't started drawing any polygon
          const position = p5.createVector(p5.mouseX, p5.mouseY)
          if (currentPoints.length === 0) {
            currentPoints.push(position)
            return
          }
          // if the user has only put 1 or 2 points so far
          if (currentPoints.length <= 2) {
            const first = currentPoints[0]
            if (closeEnough(first, position)) {
              if (currentPoints.length === 1) {
                // just delete previous point
                currentPoints = []
              } else {
                currentPoints.pop()
              }
            } else {
              currentPoints.push(position)
            }
            return
          }
          // two points at least
          // check if closing polygon
          const first = currentPoints[0]
          if (closeEnough(first, position)) {
            // add a new polygon!
            t.availablePolygons.push(new Polygon(currentPoints, t.availablePolygons.length))
            currentPoints = []
            return
          }
          // check if the user is deleting the previous point
          const last = currentPoints[currentPoints.length - 1]
          if (closeEnough(last, position)) {
            currentPoints.pop() // remove it
            return
          }
          // otherwise, just adding a point
          currentPoints.push(position)
        }
      }
    }
    this.fetchImageData({imageId: this.$route.params.imageId}).then(res => {
      this.imageData = res.data
      const p5canvas = new P5(script, 'canvas')
    })
  },
}
</script>

<style scoped>
</style>