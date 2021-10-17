<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<style>
.no-drag { /* TODO: move this in a .css file */
  user-drag: none;
  -webkit-user-drag: none;
  user-select: none;
  -moz-user-select: none;
  -webkit-user-select: none;
  -ms-user-select: none;
}
</style>
