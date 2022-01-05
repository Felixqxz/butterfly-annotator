<template>
  <b-container @mousemove="trackMouse">
    <div class="helper">
      <b-button v-b-modal.help style="border-radius: 1rem 1rem 0 0;">Help?</b-button>
    </div>
    <b-modal id="help" hide-footer scrollable title="How to annotate images?">
      <h5>General advice:</h5>
      <ul>
        <li>
          When you first arrive here, there will be automatically generated suggestions for you of
          text bits that you could want to use for your annotations.
        </li>
        <li>
          You can delete bits by clicking the cross in their badge, and add some by selecting the bit of
          text you want and then pressing the <b-badge>Add bit</b-badge> button.
        </li>
        <li>
          Click points on the canvas to start drawing a polygon. Click the first point you've drawn
          to finish a polygon. Then, choose one of the bits of text you've chosen to associate it with
          and create a complete annotation. If you don't want to add it now, you can always press <b-badge>Escape</b-badge>
          or click elsewhere, and come back to the selection menu of the polygon by simply clicking that
          polygon again.
        </li>
        <li>
          Don't forget to press <b-badge>Save</b-badge> to make your changes effective!
        </li>
      </ul>
      <hr/>
      <h5>
        Basic commands
      </h5>
      <ul>
        <li>
          Press <b-badge>Escape</b-badge> to stop your drawing.
        </li>
        <li>
          Click the last point you've created to remove it.
        </li>
        <li>
          <b-badge>Shift + Click</b-badge> when your cursor is close enough to a polygon to delete it.
        </li>
        <li>
          Place your cursor over a point of a polygon and start dragging it (hold your mouse's left button) 
          to move it.
        </li>
        <li>
          You can Undo (<b-badge>Ctrl + Z</b-badge>) and Redo (<b-badge>Ctrl + Y</b-badge>) the following actions:
          adding a polygon, removing a polygon, moving a point in a polygon.
        </li>
      </ul>
    </b-modal>
    <b-row class="mb-2">
      <b-col cols="12">
        <router-link :to="'/bank/' + bankId">Back to bank</router-link>
      </b-col>
    </b-row>
    <!-- Previous/next image buttons -->
    <b-row class="justify-content-between mb-2">
      <b-col cols="1">
        <b-button @click="previousImage()" :disabled="!hasPreviousImage">
          Previous
        </b-button>
      </b-col>
      <b-col cols="1">
        <b-button
          content="Save the changes made to the image's annotations."
          v-tippy="{theme: 'google', arrow: true, arrowType: 'round'}"
          @click="saveAnnotations()">
          Save
        </b-button>
      </b-col>
      <b-col cols="1">
        <b-button @click="nextImage()" :disabled="!hasNextImage">
          Next
        </b-button>
      </b-col>
    </b-row>
    <!-- Undo/redo buttons -->
    <b-row class="justify-content-center mb-2">
      <b-col cols="1">
        <div
            style="display:inline-block;" 
            :content="undoDisabled ? 'Nothing to undo!' : 'Undo (Ctrl + Z)'"
            v-tippy="{arrow: true, arrowType: 'round', theme: 'google'}">
          <b-button
            :disabled="undoDisabled"
            @click="undo()"><b-icon-arrow-counterclockwise></b-icon-arrow-counterclockwise></b-button>
        </div>
      </b-col>
      <b-col cols="1">
        <div
            style="display:inline-block;" 
            :content="redoDisabled ? 'Nothing to redo!' : 'Redo (Ctrl + Y)'"
            v-tippy="{arrow: true, arrowType: 'round', theme: 'google'}">
          <b-button
            :disabled="redoDisabled"
            @click="redo()"><b-icon-arrow-clockwise></b-icon-arrow-clockwise></b-button>
        </div>
      </b-col>
    </b-row>
    <!-- P5 canvas -->
    <b-row class="justify-content-center mb-2">
      <!-- Tooltip content (invisible) -->
      <div id="tooltip-content" style="display: none">
        <div v-if="hasNoDescription">
          <p>This polygon has no description!</p>
          <p>Please choose one:</p>
          <b-form-select :id="formDummyId" :options="descriptionOptions()" size="sm" class="mb-2"></b-form-select>
          <b-button variant="primary" size="sm" onclick="addAnnotation()" :disabled="descriptionOptions().filter(b => !b.disabled).length === 0">Add!</b-button>
        </div>
        <div v-else>
          <p>This polygon has a description:</p>
          <p><em>{{ descriptionOfSelectedPolygon }}</em></p>
          <p>Last editor: <em>{{ authorOfSelectedPolygon }}</em></p>
        </div>
      </div>
      <!-- The div to track the mouse position -->
      <div id="mouse-position" style="position: absolute !important"></div>
      <!-- The canvas itself -->
      <div id="canvas"/>
    </b-row>
    <!-- text selection -->
    <b-row class="mb-2">
      <b-col cols="12">
        <b-card 
          @mouseup="checkTextSelection()"
          @mousedown="checkTextSelection()">
          <!-- IMPORTANT: do not mess with the paragraph! leave as is -->
          <p style="white-space: pre-wrap; margin-bottom: 0;"
            id="description">
            <span v-for="bit in createChunks()" v-bind:key="bit.start">
              <description-bit v-if="bit.selected" :text="bit.text" 
                :start-index="bit.start" :click-handler="handleBitClick"
                :author="bit.author"
                :suggested="bit.suggested"></description-bit>
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
import { mapActions, mapGetters } from 'vuex'
import P5 from 'p5'
import { tippy } from 'vue-tippy'

import DescriptionBit from './DescriptionBit'
import handleError from '../errors/handler'

/**
 * Represents a polygon on the image to annotate.
 */
class Polygon {
  /**
   * @param dots the dots that constitute the polygon
   * @param i its position in the `availablePolygons` array
   */
  constructor(dots, i) {
    this.dots = dots
    this.i = i
  }
}

/**
 * Represents an action that can be done or undone.
 */
class Action {
  /**
   * @param redo a function that performs the action
   * @param undo a function that cancels the action
   */
  constructor(redo, undo) {
    this.redo = redo
    this.undo = undo
  }
}

class HistoryNode {
  constructor(next, previous, action) {
    this.next = next
    this.previous = previous
    this.action = action
  }

  hasNext() {
    return this.next !== null
  }

  hasPrevious() {
    return this.previous !== null
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
      hasPreviousImage: false,
      hasNextImage: false,
      bankId: -1,
      canAddBit: false,
      selectedBits: [],
      selectedPolygon: -1,
      chunkedDescription: [],
      mousePosX: 0,
      mousePosY: 0,
      previousTippy: null,
      // data for undo/redo history
      firstHistoryNode: null,
      lastHistoryNode: null,
      currentHistoryNode: null, // points to the last action that has been DONE (its change is already effective)
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
        this.selectedBits = []
        this.chunkedDescription = []
        this.canAddBit = false
        this.selectedPolygon = -1
        if (this.previousTippy) {
          this.previousTippy.destroy()
          this.previousTippy = null
        }
        this.firstHistoryNode = null
        this.lastHistoryNode = null
        this.currentHistoryNode = null
        this.initializeAll()
      }
    },
  },
  computed: {
    ...mapGetters({user: 'currentUser'}),
    redoDisabled() {
      // lastHistoryNode still undefined
      if (!this.lastHistoryNode) {
        return true
      }
      return this.currentHistoryNode.next === this.lastHistoryNode
        || this.lastHistoryNode.previous === this.firstHistoryNode // if no history at all yet
    },
    undoDisabled() {
      if (!this.lastHistoryNode) {
        return true
      }
      return this.currentHistoryNode === this.firstHistoryNode // points to the last action done => none is done
        || this.lastHistoryNode.previous === this.firstHistoryNode // no history at all
    },
    hasNoDescription() {
      return this.selectedPolygon === -1 || !this.availablePolygons[this.selectedPolygon].hasDescription
    },
    descriptionOfSelectedPolygon() {
      if (this.hasNoDescription) {
        return ''
      }
      const search = this.availablePolygons[this.selectedPolygon].i
      const annotation = this.imageData.annotations.find(annotation => annotation.polygon && annotation.polygon.i === search)
      return this.imageData.description.substring(annotation.description.start, annotation.description.end)
    },
    authorOfSelectedPolygon() {
      if (this.hasNoDescription) {
        return ''
      }
      const search = this.availablePolygons[this.selectedPolygon].i
      return this.imageData.annotations.find(annotation => annotation.polygon && annotation.polygon.i === search).author
    },
    formDummyId() {
      return 'XXXXX'
    },
    formActualId() {
      return 'tooltip-selected-description'
    },
  },
  methods: {
    ...mapActions({fetchImageData: 'fetchImageData', sendAnnotations: 'sendAnnotations'}),
    descriptionOptions() {
      const ret = []
      for (let i = 0; i < this.selectedBits.length; ++i) {
        const bit = this.selectedBits[i]
        ret.push({
          value: i, text: this.imageData.description.substring(bit.start, bit.end), disabled: Boolean(bit.annotation),
        })
      }
      return ret
    },
    trackMouse(event) {
      this.mousePosX = event.pageX
      this.mousePosY = event.pageY
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
    addAnnotation() {
      // invalid selection?
      if (this.selectedPolygon === -1 || this.selectedBits.length === 0) {
        return
      }
      const polygon = this.availablePolygons[this.selectedPolygon]
      polygon.hasDescription = true
      const selectedDescription = document.getElementById(this.formActualId).value
      const description = this.selectedBits[selectedDescription]
      const annotation = {
        polygon,
        description,
        author: this.user.username,
      }
      description.annotation = annotation
      // add
      this.imageData.annotations.push(annotation)
      if (this.previousTippy) {
        this.previousTippy.destroy()
        this.previousTippy = null
      }
      this.selectedPolygon = -1
    },
    createTooltip() {
      // position invisible div
      const posDiv = document.getElementById('mouse-position')
      posDiv.style.left = this.mousePosX + 'px'
      posDiv.style.top = this.mousePosY + 'px'
      if (this.previousTippy) {
        this.previousTippy.destroy()
      }
      // prepare content
      const content = document.getElementById('tooltip-content').innerHTML.replace(this.formDummyId, this.formActualId)
      this.previousTippy = tippy('#mouse-position', {
        content,
        interactive: true,
      })[0]
      const t = this
      setTimeout(() => {
        if (t.previousTippy) { 
          t.previousTippy.show()
        }
      }, 100) // delay to avoid instant close
      return this.previousTippy
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
        // start field for vue keys
        if (bit.start !== previousEnd) {
          ret.push({text: this.imageData.description.substring(previousEnd, bit.start), selected: false, start: previousEnd})
        }
        // add the actual selected bit
        ret.push({
          text: this.imageData.description.substring(bit.start, bit.end), 
          selected: true, 
          start: bit.start, 
          author: bit.annotation ? bit.annotation.author : '',
          suggested: bit.suggested,
        })
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
      // find if annotation assigned
      const annotation = this.imageData.annotations.find(a => a.description.start === start)
      if (annotation) {
        annotation.toRemove = true
        annotation.description = null
        if (annotation.polygon) {
          annotation.polygon.hasDescription = false
        }
      }
    },
    saveAnnotations() {
      // filter the annotations that never were online
      const remPred = a => !(a.toRemove && !a.id)
      const annotations = this.imageData.annotations.filter(remPred).map(annotation => {
        const id = annotation.id ? annotation.id : -1 // new annotation!
        if (annotation.toRemove) {
          return {
            'id': id,
            'rem': true,
          }
        } else {
          return {
            'id': id,
            'points': annotation.polygon.dots.map(p => {
              return {
                x: Math.floor(p.x),
                y: Math.floor(p.y),
              }
            }),
            'tag': {
              'start': annotation.description.start,
              'end': annotation.description.end,
            },
          }
        }
      })
      const t = this
      this.sendAnnotations({
        data: {
          imageId: this.$route.params.imageId,
          annotations,
        },
      }).then(res => {
        t.imageData.annotations = t.imageData.annotations.filter(remPred)
        for (let i = 0; i < t.imageData.annotations.length; ++i) {
          const annot = t.imageData.annotations[i]
          annot.id = res.data.ids[i]
        }
        t.$bvToast.toast('Done.', {
          title: 'Successfully saved annotations!',
          variant: 'success',
          solid: true,
        })
      }).catch(e => handleError(this.$bvToast, 'Could not save annotations', `Cause: ${e.response.data.message}`))
    },
    descriptionIndices(text) {
      const start = this.imageData.description.indexOf(text) // TODO: what if beginning trimmed?
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
    undo() {
      if (this.undoDisabled) {
        return
      }
      const current = this.currentHistoryNode
      current.action.undo()
      this.currentHistoryNode = current.previous
    },
    redo() {
      // no history yet!
      if (this.redoDisabled) {
        return
      }
      const current = this.currentHistoryNode
      current.next.action.redo()
      this.currentHistoryNode = current.next
    },
    pushHistory(redo, undo) {
      // continuing history or branching to new history: same handling
      const node = new HistoryNode(this.lastHistoryNode, this.currentHistoryNode, new Action(redo, undo))
      this.currentHistoryNode.next = node
      this.lastHistoryNode.previous = node
      this.currentHistoryNode = node
      redo()
    },
    initializeAll() {
      const t = this
      const script = p5 => {
        // optimizes performance
        p5.disableFriendlyErrors = true

        /**
         * Draws lines that connect all `(i, i + 1)` dots and closes the shape if `close` is `true`.
         * @param color the color of the lines
         * @param dots the dots to connect
         * @param close whether the last dot should be connected to the first one
         */
        const connectDotsOpen = (color, dots, close) => {
          p5.stroke(color)
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
          p5.noStroke()
          p5.fill(color)
          for (let i = 0; i < dots.length; ++i) {
            const dot = dots[i]
            p5.ellipse(dot.x, dot.y, MOUSE_RAD)
          }
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

        // the maximal framerate (setting it to 60 had no effect)
        const MAX_FPS = 50

        // we will build a color sequence that always assigns the same color to a given index
        // (color(0), color(1), ..., color(n), ...)
        /**
         * @param i the integer representing the polygon in the sequence
         * @returns the color of the `i-th` polygon.
         */
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

        /**
         * @param search the point
         * @param polygon the polygon
         * @returns {{distance: number, index: number}} where `distance` is the distance
         * to the closest point of the provided polygon and `index` is its index in
         * `availablePolygons`.
         */
        const polygonDistance = (search, polygon) => {
          let distMin = 0
          let argMin = 0
          for (let i = 0; i < polygon.dots.length; ++i) {
            const pointA = polygon.dots[i]
            const pointB = polygon.dots[(i + 1) % polygon.dots.length] // (roll)
            const lineX = pointB.x - pointA.x
            const lineY = pointB.y - pointA.y
            const diffX = search.x - pointA.x
            const diffY = search.y - pointA.y
            const d = diffX * lineX + diffY * lineY
            const r = d / (lineX * lineX + lineY * lineY)
            
            let compX = 0.0
            let compY = 0.0
            if (r < 0) {
              compX = pointA.x
              compY = pointA.y
            } else if (r > 1) {
              compX = pointB.x
              compY = pointB.y
            } else {
              compX = pointA.x + r * lineX
              compY = pointA.y + r * lineY
            }
            const dx = search.x - compX
            const dy = search.y - compY
            const dist = dx * dx + dy * dy
            if (dist < distMin || i === 0) {
              distMin = dist
              argMin = i
            }
          }
          return { distance: distMin, index: argMin }
        }

        // returns the closest line constituting a polygon in a right angle `EPS` distance
        // to the mouse
        /**
         * @returns {{dotsIdx: number, polygon: number, distance: number}} `dotsIdx`
         * is the index of the first point constituting the line (the next one being
         * `(dotsIdx + 1) % dots.length)`, `polygon` is the position of the polygon in the
         * `availablePolygons` array, and `distance` is the distance of the mouse to that
         * line.
         */
        const closestLineInRadius = () => {
          const mousePosition = p5.createVector(p5.mouseX, p5.mouseY)
          let polygonArgmin = -1
          let dotsArgmin = -1
          let minDist = Number.POSITIVE_INFINITY
          for (let i = 0; i < t.availablePolygons.length; ++i) {
            const polygon = t.availablePolygons[i]
            const {distance, index} = polygonDistance(mousePosition, polygon)
            if (minDist > distance) {
              minDist = distance
              dotsArgmin = index
              polygonArgmin = i
            }
          }
          return {polygon: polygonArgmin, dotsIdx: dotsArgmin, distance: minDist}
        }

        /**
         * @returns `true` if the user's mouse is within the canvas.
         */
        const mouseInCanvas = () => 0 < p5.mouseX && p5.mouseX < t.imageData.width
            && 0 < p5.mouseY && p5.mouseY < t.imageData.height

        /**
         * @param u first point
         * @param v second point
         * @returns the squared distance between points `u` and `v`.
         */
        const distanceSquared = (u, v) => {
          const dx = u.x - v.x
          const dy = u.y - v.y
          return dx * dx + dy * dy
        }

        /**
         * @param a a first point
         * @param b a second point
         * @returns `true` if the two points are close enough to be considered to be
         * in "approximately" the same location
         */
        const closeEnough = (a, b) => distanceSquared(a, b) < EPS * EPS

        /**
         * Displays the provided polygon
         * @param color the color it should take
         * @param polygon the polygon object to draq
         */
        const display = (color, polygon) => connectDotsOpen(color, polygon.dots, true)

        /**
         * @returns the next index of the polygon
         */
        const nextIndex = () => t.availablePolygons.length > 0 
          ? t.availablePolygons[t.availablePolygons.length - 1].i + 1
          : 0

        /**
         * Deletes the provided polygon.
         * @param polygon the index of the polygon
         * @param history `true` if this action should be undoable (add it to history)
         */
        const deletePolygon = (polygon, history) => {
          // copy data
          const objPolygon = Object.assign({}, t.availablePolygons[polygon]) // deep copy
          objPolygon.hasDescription = false
          const copySelected = t.selectedPolygon
          const nowAnnot = t.imageData.annotations.find(a => a.polygon && a.polygon.i === polygon)
          if (nowAnnot) {
            const bit = t.selectedBits.find(b => b.annotation === nowAnnot)
            bit.annotation = null
          }
          // delete polygon
          const redo = () => {
            const annot = t.imageData.annotations.findIndex(annotation => annotation.polygon && annotation.polygon.i === objPolygon.i)
            const annotation = annot !== -1 ? t.imageData.annotations[annot] : null
            t.availablePolygons.splice(polygon, 1)
            // check if the `annot`-th annotation has not changed
            if (annotation && t.imageData.annotations.length > annot && t.imageData.annotations[annot] === annotation) {
              // remove the annotation when sending to server
              annotation.toRemove = true
              annotation.polygon = null
              if (annotation.description) {
                annotation.description.annotation = null
              }
            }
            t.selectedPolygon = -1
          }
          // repush polygon
          const undo = () => {
            const annot = t.imageData.annotations.findIndex(annotation => annotation.polygon && annotation.polygon.i === objPolygon.i)
            const annotation = annot !== -1 ? t.imageData.annotations[annot] : null
            // restore only the polygon: lose the annotation
            t.availablePolygons.splice(polygon, 0, objPolygon)
            // same as above
            if (annotation && t.imageData.annotations.length > annot && t.imageData.annotations[annot] === annotation) {
              annotation.toRemove = false
              annotation.polygon = objPolygon
              if (annotation.description) {
                annotation.description.annotation = annotation
              }
            }
            t.selectedPolygon = copySelected
          }
          if (history) {
            t.pushHistory(redo, undo)
          } else {
            redo()
          }
        }

        // variables
        let currentPoints = []
        let annotateImage = undefined
        let movedPoint = null
        let movedPointOriginalLocation = null

        // setup the canvas
        p5.setup = () => {
          // canvas
          p5.createCanvas(t.imageData.width, t.imageData.height)
          annotateImage = p5.loadImage(this.$hostname + '/api/' + t.imageData.imageUrl)
          // cap framerate
          p5.frameRate(MAX_FPS)
        }

        p5.draw = () => {
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

          // hovering and not drawing? then don't suggest new circle
          const closest = closestLineInRadius()
          if (!closest || closest.distance >= EPS || currentPoints.length > 0) {
            p5.strokeWeight(MOUSE_STROKE_WEIGHT)
            p5.fill(colorSequence(t.availablePolygons.length))
            p5.ellipse(p5.mouseX, p5.mouseY, MOUSE_RAD)
          }

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

        p5.keyPressed = () => {
          if (p5.keyCode === p5.ESCAPE) {
            // close tooltip and clear current polygon and selection
            if (t.previousTippy) {
              const prev = t.previousTippy
              t.previousTippy = null
              prev.hide()
              setTimeout(() => prev.destroy(), 500)
            }
            t.selectedPolygon = -1
            currentPoints = []
          } else if (p5.keyIsDown(p5.CONTROL)) {
            const UNDO_KEYCODE = 90 // Z
            const REDO_KEYCODE = 89 // Y
            if (p5.keyCode === UNDO_KEYCODE) {
              t.undo()
            } else if (p5.keyCode === REDO_KEYCODE) {
              t.redo()
            }
          }
        }

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
          // not set yet
          if (!movedPointOriginalLocation) {
            movedPointOriginalLocation = p5.createVector(closest.dot.x, closest.dot.y)
          }
        }

        p5.mouseReleased = () => {
          if (mouseInCanvas() && (!t.previousTippy || !t.previousTippy.isVisible)) {
            // if the user hasn't started drawing any polygon
            const position = p5.createVector(p5.mouseX, p5.mouseY)
            // was displacing a point
            if (movedPoint) {
              const location = movedPointOriginalLocation
              const point = movedPoint
              const redo = () => {
                t.availablePolygons[point.polygon].dots[point.dotIdx] = position
              }
              const undo = () => {
                t.availablePolygons[point.polygon].dots[point.dotIdx] = location
              }
              movedPointOriginalLocation = null
              movedPoint = null
              t.pushHistory(redo, undo)
              return
            }
            const closest = closestLineInRadius()
            // is deleting a polygon
            if (p5.keyIsDown(DELETE_KEY)) {
              if (closest && closest.distance < EPS * EPS) {
                deletePolygon(closest.polygon, true)
              }
              return
            }
            // clicking on a polygon and not creating a new one
            if (closest.distance < EPS * EPS && currentPoints.length === 0) {
              t.selectedPolygon = closest.polygon
              setTimeout(() => t.createTooltip(), 1)
              return
            }
            // start polygon
            if (currentPoints.length === 0) {
              const closest = closestLineInRadius()
              // clicking existing polygon
              if (closest && closest.distance < EPS * EPS) {
                t.selectedPolygon = closest.polygon
              } else {
                currentPoints.push(position)
              }
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
              const tip = t.createTooltip()
              const index = nextIndex()
              // init polygon
              const poly = new Polygon(currentPoints, index)
              // reset to new selection
              currentPoints = []
              const redo = () => {
                // add a new polygon!
                t.availablePolygons.push(poly)
                t.selectedPolygon = index
                const annot = t.imageData.annotations.find(a => a.polygon && a.polygon.i === poly.i)
                if (annot) {
                  annot.toRemove = false
                  annot.description.annotation = annot
                }
              }

              const undo = () => {
                // delete tooltip
                if (tip) {
                  tip.destroy()
                }
                // do not restore older points: otherwise the user is going to
                // be editing the polygon he started just before
                deletePolygon(index, false)
              }
              this.pushHistory(redo, undo)
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
          const polygon = new Polygon(points, i)
          polygon.hasDescription = true
          annotation.polygon = polygon
          this.selectedBits.push({start: annotation.description.start, end: annotation.description.end, annotation})
          this.availablePolygons.push(polygon)
        })
        // no annotations, take suggestions
        if (!this.imageData.annotations || this.imageData.annotations.length === 0) {
          this.imageData.suggestions.forEach(suggestion => {
            this.selectedBits.push({start: suggestion.start, end: suggestion.end, suggested: true})
          })
        }
        this.selectedBits.sort((b, a) => b.start - a.start)
        // finally, load the P5 canvas
        const p5canvas = new P5(script, 'canvas')
      }).catch(e => handleError(this.$bvToast, 'Could not load annotations', `Cause ${e.response.data.message}`))
    },
  },
  mounted() {
    this.initializeAll()
  },
  created() {
    window.addAnnotation = this.addAnnotation
    // setup history nodes
    this.firstHistoryNode = new HistoryNode(null, null)
    this.lastHistoryNode = new HistoryNode(null, this.firstHistoryNode)
    this.firstHistoryNode.next = this.lastHistoryNode
    this.currentHistoryNode = this.firstHistoryNode
  },
}
</script>

<style scoped>
.helper {
  position: fixed;
  bottom: 0;
  right: 0;
  margin-right: 2em;
}
</style>
