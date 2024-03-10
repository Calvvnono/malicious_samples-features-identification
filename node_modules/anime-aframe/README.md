Forked from https://github.com/juliangarnier/anime

animejs for AFRAME use.

Issue: Daydream won't support animejs-based animation in scene due to Polyfill stopping the window's requestAnimationFrame after calibration of Daydream device.

Fix: Use the requestAnimationFrame from AFRAME scene instead of window.

npm package available at https://www.npmjs.com/package/anime-aframe