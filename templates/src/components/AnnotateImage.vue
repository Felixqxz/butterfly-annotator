<template>
  <b-container>
    <b-row class="mb-2">
      <b-col cols="12">
        <router-link :to="'/bank/' + bankId">Back to bank</router-link>
      </b-col>
    </b-row>
    <b-row class="justify-content-between mb-2">
      <b-col cols="1">
        <b-button @click="previousImage()" :disabled="!hasPreviousImage">
          Previous
        </b-button>
      </b-col>
      <b-col cols="1">
        <b-button @click="saveAnnotations()">
          Save
        </b-button>
      </b-col>
      <b-col cols="1">
        <b-button @click="nextImage()" :disabled="!hasNextImage">
          Next
        </b-button>
      </b-col>
    </b-row>
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

class Polygon {
  constructor(dots, i) {
    this.dots = dots
    this.i = i
  }
}

export default {
  name: 'AnnotateImage',
  data() {
    return {
      imageData: null,
      availablePolygons: [],
      selectedPolygon: -1,
      bitButtonDisabled: true,
      annotations: [],
      hasPreviousImage: false,
      hasNextImage: false,
      bankId: -1,
    }
  },
  watch: {
    $route(to, from) {
      // used to remove old canvas
      if (to !== from) {
        const toRemove = document.getElementById('defaultCanvas0')
        if (toRemove) {
          toRemove.parentNode.removeChild(toRemove)
        }
        this.hasNextImage = false
        this.hasPreviousImage = false
        this.availablePolygons = []
        this.selectedPolygon = -1
        this.bitButtonDisabled = true
        this.annotations = []
        this.initializeAll()
      }
    },
  },
  methods: {
    ...mapActions({fetchImageData: 'fetchImageData', sendAnnotations: 'sendAnnotations'}),
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
        this.annotations.push({polygon: this.availablePolygons[this.selectedPolygon], description: selected})
      }
    },
    previousImage() {
      const path = '/annotate/' + this.imageData.hasPrevious
      this.$router.push({path})
      this.$router.go()
    },
    nextImage() {
      const path = '/annotate/' + this.imageData.hasNext
      this.$router.push({path})
      this.$router.go()
    },
    serializePoints(p) {
      return p.map(v => Math.round(v.x) + ',' + Math.round(v.y)).join(';')
    },
    saveAnnotations() {
      const annotations = this.annotations.map(annotation => {
        return {
          'id': -1,
          'points': this.serializePoints(annotation.polygon.dots),
          'tag': annotation.description,
        }
      })
      this.sendAnnotations({
        data: {
          imageId: this.$route.params.imageId,
          annotations
        },
      })
    },
    initializeAll() {
      const t = this
      const script = p5 => {
        // draws lines that connect all (i, i + 1) dots and closes the shape if close is true
        const connectDotsOpen = (color, dots, close) => {
          p5.stroke(color)
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
          p5.noStroke()
          p5.fill(color)
          dots.forEach(dot => p5.ellipse(dot.x, dot.y, MOUSE_RAD))
        }

        // the radius around a point we allow
        const EPS = 15
        // the disk following the mouse
        const MOUSE_RAD = 9
        const MOUSE_STROKE_WEIGHT = 2
        // general stroke weight
        const STROKE_WEIGHT = 4

        // the key to be pressed to delete a polygon
        const DELETE_KEY = p5.SHIFT

        // we will build a color sequence that always assigns the same color to a given index
        // (color(0), color(1), ..., color(n), ...)
        const colorSequence = i => p5.color((16 * i) % 256, (128 * i) % 256, (30 * i) % 256)

        // returns the closest point constituting a polygon in an `EPS` radius
        // to the mouse
        // TODO: this doesn't return the closest point, it returns the first in radius
        const closestPointInRadius = () => {
          const mousePosition = p5.createVector(p5.mouseX, p5.mouseY)
          for (let i = 0; i < t.availablePolygons.length; ++i) {
            const polygon = t.availablePolygons[i]
            for (let j = 0; j < polygon.dots.length; ++j) {
              const dot = polygon.dots[j]
              if (closeEnough(dot, mousePosition)) {
                return { dot, polygon: i, dotIdx: j }
              }
            }
          }
          return null
        }

        // returns the closest line constituting a polygon in a right angle `EPS` distance
        // to the mouse
        const closestLineInRadius = () => {
          const mousePosition = p5.createVector(p5.mouseX, p5.mouseY)
          let polygonArgmin = -1
          let dotsArgmin = -1
          let minDist = Number.POSITIVE_INFINITY
          for (let i = 0; i < t.availablePolygons.length; ++i) {
            const polygon = t.availablePolygons[i]
            for (let j = 0; j < polygon.dots.length; ++j) {
              const pointA = polygon.dots[j]
              const pointB = polygon.dots[(j + 1) % polygon.dots.length] // cycle back to close
              const numerator = (pointB.x - pointA.x) * (pointA.y - mousePosition.y)
                - (pointA.x - mousePosition.x) * (pointB.y - pointA.y)
              const endDist = Math.abs(numerator) / pointB.dist(pointA)
              if (endDist < minDist) {
                minDist = endDist
                polygonArgmin = i
                dotsArgmin = i
              }
            }
          }
          return {polygon: polygonArgmin, dotsIdx: dotsArgmin, distance: minDist}
        }

        // allows to check if the mouse is within the canvas
        const mouseInCanvas = () => 0 < p5.mouseX && p5.mouseX < t.imageData.width
            && 0 < p5.mouseY && p5.mouseY < t.imageData.height

        // returns true if the two provided points are considered to be close enough
        // so that they are at the same position, provided the tolerance radius `EPS`
        // (used for the user's mouse and another point)
        const closeEnough = (a, b) => a.dist(b) < EPS

        // displays a polygon
        const display = (color, polygon) => connectDotsOpen(color, polygon.dots, true)

        // next polygon index
        const nextIndex = () => t.availablePolygons.length > 0 
          ? t.availablePolygons[t.availablePolygons.length - 1].i + 1
          : 0

        // variables
        let currentPoints = []
        let annotateImage = undefined
        let movedPoint = null

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
          // currently displacing a point
          if (movedPoint) {
            t.availablePolygons[movedPoint.polygon].dots[movedPoint.dotIdx] = p5.createVector(p5.mouseX, p5.mouseY)
          }
          // draw all existing polygons
          t.availablePolygons.forEach(polygon => display(colorSequence(polygon.i), polygon))
          // draw the current polygon being drawn
          if (currentPoints.length > 0) {
            const color = colorSequence(nextIndex())
            connectDotsOpen(color, currentPoints, false)
            // connect the last point to the mouse's position
            p5.stroke(color)
            const last = currentPoints[currentPoints.length - 1]
            p5.line(last.x, last.y, p5.mouseX, p5.mouseY)
          }
          p5.strokeWeight(MOUSE_STROKE_WEIGHT)
          p5.fill(colorSequence(t.availablePolygons.length))
          p5.ellipse(p5.mouseX, p5.mouseY, MOUSE_RAD)

          // select cursor
          if (p5.keyIsDown(DELETE_KEY)) {
            p5.cursor(p5.HAND)
          } else {
            const closest = closestPointInRadius()
            if (closest) {
              p5.cursor(p5.MOVE)
            } else {
              p5.cursor(p5.ARROW)
            }
          }
        }

        // TODO: sometimes it's not the closest polygon that gets deleted

        p5.mousePressed = () => {
          if (!mouseInCanvas()) {
            return
          }

          const closest = closestPointInRadius()
          // no close point, or already creating a polygon
          if (!closest || currentPoints.length > 0) {
            return
          }

          movedPoint = closest
        }

        p5.mouseReleased = () => {
          if (mouseInCanvas()) {
            // if the user hasn't started drawing any polygon
            const position = p5.createVector(p5.mouseX, p5.mouseY)
            // was displacing a point
            if (movedPoint) {
              movedPoint = null
              return
            }
            // is deleting a polygon
            if (p5.keyIsDown(DELETE_KEY)) {
              const closest = closestLineInRadius()
              if (closest && closest.distance < EPS) {
                t.availablePolygons.splice(closest.polygon, 1)
              }
              return
            }
            // start polygon
            if (currentPoints.length === 0) {
              currentPoints.push(position)
              return
            }
            // if the user has only put 1 or 2 points so far
            if (currentPoints.length <= 2) {
              const first = currentPoints[0]
              if (closeEnough(first, position)) {
                currentPoints.pop()
              } else {
                // two points
                if (currentPoints.length === 2) {
                  const second = currentPoints[1]
                  // remove point as usual
                  if (closeEnough(second, position)) {
                    currentPoints.pop()
                  } else {
                    currentPoints.push(position)
                  }
                } else {
                  // only one point => add the new one
                  currentPoints.push(position)
                }
              }
              return
            }
            // two points at least
            // check if closing polygon
            const first = currentPoints[0]
            if (closeEnough(first, position)) {
              // add a new polygon!
              t.availablePolygons.push(new Polygon(currentPoints,
                nextIndex()))
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
        this.bankId = this.imageData.bankId
        this.hasNextImage = this.imageData.hasNext !== -1
        this.hasPreviousImage = this.imageData.hasPrevious !== -1
        this.imageData.annotations.forEach((annotation, i) => {
          let points = []
          annotation.regionInfo.split(';').forEach(rawPoint => {
            const rawCoord = rawPoint.split(',')
            points.push(new P5.Vector(parseInt(rawCoord[0]), parseInt(rawCoord[1])))
          })
          this.availablePolygons.push(new Polygon(points, i))
        })
        const p5canvas = new P5(script, 'canvas')
      })
    },
  },
  mounted() {
    this.initializeAll()
  },
}
</script>

<style scoped>
</style>