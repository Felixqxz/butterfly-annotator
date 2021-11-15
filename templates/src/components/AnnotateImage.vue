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
      <b-col cols="12">
        <b-card>
          <!-- IMPORTANT: do not mess with the paragraph! leave as is -->
          <p style="white-space: pre-wrap"
            id="description"
            @mouseup="checkTextSelection()"
            @mousedown="checkTextSelection()">
            <span v-for="bit in createChunks()" v-bind:key="bit.start">
              <description-bit v-if="bit.selected" :text="bit.text" 
                :start-index="bit.start" :click-handler="handleBitClick"></description-bit>
              <span v-else>{{ bit.text }}</span>
            </span>
          </p>
        </b-card>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12">
        <b-button @click="addTextBit()" :disabled="!canAddBit">
          Add bit
        </b-button>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import {mapActions} from 'vuex'
import P5 from 'p5'

import DescriptionBit from './DescriptionBit'

class Polygon {
  constructor(dots, i) {
    this.dots = dots
    this.i = i
  }
}

export default {
  name: 'AnnotateImage',
  components: {
    DescriptionBit,
  },
  data() {
    return {
      imageData: null,
      availablePolygons: [],
      annotations: [],
      hasPreviousImage: false,
      hasNextImage: false,
      bankId: -1,
      canAddBit: false,
      selectedBits: [],
      chunkedDescription: [],
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
        this.annotations = []
        this.selectedBits = []
        this.chunkedDescription = []
        this.canAddBit = false
        this.initializeAll()
      }
    },
  },
  methods: {
    ...mapActions({fetchImageData: 'fetchImageData', sendAnnotations: 'sendAnnotations'}),
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
      return p.map(v => Math.floor(v.x) + ',' + Math.floor(v.y)).join(';')
    },
    createChunks() {
      if (!this.imageData) {
        return []
      }
      if (this.selectedBits.length === 0) {
        return [{text: this.imageData.description, selected: false}]
      }
      let ret = []
      let previousEnd = 0
      // the code assumes that the bits are sorted by their beginning index,
      // and that there are no overlaps
      for (let i = 0; i < this.selectedBits.length; ++i) {
        const bit = this.selectedBits[i]
        // add beginning
        if (bit.start !== previousEnd) {
          ret.push({text: this.imageData.description.substring(previousEnd, bit.start), selected: false, start: previousEnd})
        }
        // add the actual selected bit
        ret.push({text: this.imageData.description.substring(bit.start, bit.end), selected: true, start: bit.start})
        previousEnd = bit.end
      }
      // add remainder, if any
      const last = this.selectedBits[this.selectedBits.length - 1]
      if (last.end !== this.imageData.description.length) {
        ret.push({text: this.imageData.description.substring(last.end), selected: false, start: last.end})
      }
      return ret
    },
    handleBitClick(start) {
      const i = this.selectedBits.findIndex(b => b.start === start)
      if (i === -1) {
        return // (not found)
      }
      this.selectedBits.splice(i, 1)
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
          annotations,
        },
      })
    },
    descriptionIndices(text) {
      const start = this.imageData.description.indexOf(text)
      const end = start + text.trim().length // (exclusive)
      return { start, end }
    },
    checkTextSelection() {
      const selection = window.getSelection()
      const rawText = selection.toString()
      const {start, end} = this.descriptionIndices(rawText)
      // trying to add an overlapping bit!
      if (this.selectedBits.some(bit => start <= bit.end && bit.start <= end)) {
        this.canAddBit = false
        return
      }
      const selectedText = rawText.trim()
      this.canAddBit = !!selectedText // coerce to boolean
    },
    addTextBit() {
      const selection = window.getSelection()
      const rawText = selection.toString()
      const selectedText = rawText.trim()
      if (!selectedText) {
        return
      }
      const {start, end} = this.descriptionIndices(rawText)
      this.selectedBits.push({ start, end })
      this.selectedBits.sort((b, a) => b.start - a.start) // first start first; should be no overlap too
      selection.empty()
      this.canAddBit = false
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
        const colorSequence = i => p5.color((16 * i) % 256, (64 * (i + 1)) % 256, (30 * i) % 256, 150)

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
        // add all annotations
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