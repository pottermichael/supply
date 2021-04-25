var framesPerSecond = 15;
var initialOpacity = 1;
var opacity = initialOpacity;
var initialRadius = 8;
var radius = initialRadius;
var maxRadius = 50;

function animateMarker(timestamp) {
    setTimeout(function(){
        requestAnimationFrame(animateMarker);

        radius += (maxRadius - radius) / framesPerSecond;
        opacity -= ( .9 / framesPerSecond );

        map.setPaintProperty('point', 'circle-radius', radius);
        map.setPaintProperty('point', 'circle-opacity', opacity);

        if (opacity <= 0) {
            radius = initialRadius;
            opacity = initialOpacity;
        }
    }, 1000 / framesPerSecond);
}
