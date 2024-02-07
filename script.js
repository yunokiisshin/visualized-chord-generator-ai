const canvas = document.getElementById('myCanvas');
const ctx = canvas.getContext('2d');

// Set canvas size
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let isSecondMode = false; // Default to first-mode

// container for note circles
const circles = [];
const colors = ['231,173,255','229,167,237','227,161,219','225,155,201','223,149,183','221,143,165','219,137,147','217,131,129','215,125,111','213,119,93','211,113,75'];
// const colors = ['231,173,255', '219,161,243', '207,149,231', '195,137,219', '183,125,207', '171,113,195', '159,101,183', '147,89,171', '135,77,159', '123,65,147', '111,53,135'];


// Create circle objects
for (let i = 0; i < 11; i++) {
    const circle = {
        ind: i,
        x: (i+1) * canvas.width / 12,
        y: canvas.height/2 + (Math.PI * 2) * (-30) * Math.sin(i * Math.PI / 5),
        radius: 25,
        scale: 1,
        midi: "./MIDI_notes/" + i + ".wav",
        playable: true,
        lastPlayedTime: 0,
        color: colors[i],
        ripple: {
            active: false,
            scale: 0.75,
            opacity: 1,
        },
    };

    circles.push(circle);
}

// Function to draw the circles
function drawCircles() {
    ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear the canvas

    for (let i = 0; i < circles.length; i++) {
        const circle = circles[i];
        if (circle.ripple.active) {
            ctx.beginPath();
            ctx.arc(circle.x, circle.y, circle.radius * circle.ripple.scale, 0, Math.PI * 2, false);
            ctx.fillStyle = `rgba(` + circle.color + `, ${circle.ripple.opacity})`;
            ctx.fill();
            updateRipple(circle);
        }

        // Draw main circles
        ctx.beginPath();
        ctx.arc(circle.x, circle.y, circle.radius * circle.scale, 0, Math.PI * 2, false);
        ctx.fillStyle = 'rgba(' + circle.color + ', 1)';
        ctx.fill();
    }
}


// Update ripple properties
function updateRipple(circle) {
    if (isSecondMode){
    circle.ripple.scale += 0.10 + circle.ind * 0.02 ;
    } else {
        circle.ripple.scale += 0.25;
    }
    // Increase the value to make the ripple effect larger
    circle.ripple.opacity -= 0.01; // Increase the value to make the ripple effect last longer

    if (isSecondMode){
    if (circle.ripple.opacity <= 0) {
        circle.ripple.active = false;
        circle.ripple.scale = 0.75;
        circle.ripple.opacity = 1;
    }
    } else {
        if (circle.ripple.opacity <= 0) {
            circle.ripple.active = false;
            circle.ripple.scale = 0.75;
            circle.ripple.opacity = 1;
        }
    }
}

function updateCirclesWhenWindowChangesSize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    for (let i = 0; i < circles.length; i++) {
        const circle = circles[i];
        circle.x = (i + 1) * canvas.width / 12;
        circle.y = canvas.height / 2 + (Math.PI * 2) * (-30) * Math.sin(i * Math.PI / 5);
        
    }
}



// Function to play the assigned WAV file
function playWav(circle) {
    if (!circle.playable) return;
    const currentTime = Date.now();
    if (currentTime - circle.lastPlayedTime >= 500) {
        const audio = new Audio(circle.midi);
        audio.currentTime = 0.1; // Set the starting time to 0.05 seconds
        audio.play();
        circle.lastPlayedTime = currentTime;
    }
}


function triggerSequentialRipples() {
    let index = 0; // Initialize index to 0
    function animateRipple() {
        const circle = circles[index];
        circle.scale = 1.1;
        circle.ripple.active = true;
        playWav(circle);
        drawCircles();
        const nextCircle = circles[index + 1];
        if (nextCircle && circle.ripple.scale * circle.radius >= Math.sqrt(Math.pow(nextCircle.x - circle.x, 2) + Math.pow(nextCircle.y - circle.y, 2))) {
            index++; // Increment index when ripple hits the next circle
        }   
        
        if (index >= circles.length - 1) {
            if (circles[circles.length - 1].playable) {
                playWav(circles[circles.length - 1]);
                circles[circles.length - 1].playable = false;
                drawCircles();
            }
            index = 0;
            return; // Stop animation if it's the last circle
        }
        requestAnimationFrame(animateRipple);
    }
    animateRipple();
}


function switchTextAndColor() {
    var subtitle = document.getElementById("subtitle");
    if (subtitle.innerHTML === "Find and press keys to play.") {
        subtitle.innerHTML = "Press Space to play.";
        isSecondMode = true;
    } else {
        subtitle.innerHTML = "Find and press keys to play.";
        isSecondMode = false;
    }
    document.body.classList.toggle("second-mode");
}


// Event listener for keydown
document.addEventListener('keydown', function(event) {
    if (isSecondMode && event.key === ' ') {
        triggerSequentialRipples();
    } else if (!isSecondMode) {
        if(event.key === 'a' || event.key === 'A') {
            const circle = circles[0];
            circle.scale = 1.1; // Increase circle size by 10%
            
            circle.ripple.active = true; // Activate ripple effect
            drawCircles();
            
            playWav(circle);
        }

        if(event.key === 's' || event.key === 'S') {
            const circle = circles[1];
            circle.scale = 1.1; // Increase circle size by 10%
            
            circle.ripple.active = true; // Activate ripple effect
            drawCircles();
            
            playWav(circle);
        }

        if(event.key === 'd' || event.key === 'D') {
            const circle = circles[2];
            circle.scale = 1.1; // Increase circle size by 10%
            
            circle.ripple.active = true; // Activate ripple effect
            drawCircles();
            
            playWav(circle);
        }

        if(event.key === 'f' || event.key === 'F') {
            const circle = circles[3];
            circle.scale = 1.1; // Increase circle size by 10%
            
            circle.ripple.active = true; // Activate ripple effect
            drawCircles();
            
            playWav(circle);
        }

        if(event.key === 'g' || event.key === 'G') {
            const circle = circles[4];
            circle.scale = 1.1; // Increase circle size by 10%
            
            circle.ripple.active = true; // Activate ripple effect
            drawCircles();
            
            playWav(circle);
        }

        if(event.key === 'h' || event.key === 'H') {
            const circle = circles[5];
            circle.scale = 1.1; // Increase circle size by 10%
            
            circle.ripple.active = true; // Activate ripple effect
            drawCircles();
            
            playWav(circle);
        }

        if(event.key === 'j' || event.key === 'J') {
            const circle = circles[6];
            circle.scale = 1.1; // Increase circle size by 10%
            
            circle.ripple.active = true; // Activate ripple effect
            drawCircles();
            
            playWav(circle);
        }

        if(event.key === 'k' || event.key === 'K') {
            const circle = circles[7];
            circle.scale = 1.1; // Increase circle size by 10%
            
            circle.ripple.active = true; // Activate ripple effect
            drawCircles();
            
            playWav(circle);
        }

        if(event.key === 'l' || event.key === 'L') {
            const circle = circles[8];
            circle.scale = 1.1; // Increase circle size by 10%
            
            circle.ripple.active = true; // Activate ripple effect
            drawCircles();

            playWav(circle);
        }

        if(event.key === ';' || event.key === ':') {
            const circle = circles[9];
            circle.scale = 1.1; // Increase circle size by 10%
            
            circle.ripple.active = true; // Activate ripple effect
            drawCircles();

            playWav(circle);
        }

        if(event.key === "'" || event.key === '"') {
            const circle = circles[10];
            circle.scale = 1.1; // Increase circle size by 10%
            
            circle.ripple.active = true; // Activate ripple effect
            drawCircles();

            playWav(circle);
        }

    }
    

});

// Event listener for keyup
document.addEventListener('keyup', function(event) {
    if(event.key === 'a' || event.key === 'A') {
        const circle = circles[0];
        circle.scale = 1; // Reset circle size
        drawCircles();
        circle.playable = true;
    }

    if(event.key === 's' || event.key === 'S') {
        const circle = circles[1];
        circle.scale = 1; // Reset circle size
        drawCircles();
        circle.playable = true;
    }

    if(event.key === 'd' || event.key === 'D') {
        const circle = circles[2];
        circle.scale = 1; // Reset circle size
        drawCircles();
        circle.playable = true;
    }

    if(event.key === 'f' || event.key === 'F') {
        const circle = circles[3];
        circle.scale = 1; // Reset circle size
        drawCircles();
        circle.playable = true;
    }

    if(event.key === 'g' || event.key === 'G') {
        const circle = circles[4];
        circle.scale = 1; // Reset circle size
        drawCircles();
        circle.playable = true;
    }

    if(event.key === 'h' || event.key === 'H') {
        const circle = circles[5];
        circle.scale = 1; // Reset circle size
        drawCircles();
        circle.playable = true;
    }

    if(event.key === 'j' || event.key === 'J') {
        const circle = circles[6];
        circle.scale = 1; // Reset circle size
        drawCircles();
        circle.playable = true;
    }

    if(event.key === 'k' || event.key === 'K') {
        const circle = circles[7];
        circle.scale = 1; // Reset circle size
        drawCircles();
        circle.playable = true;
    }

    if(event.key === 'l' || event.key === 'L') {
        const circle = circles[8];
        circle.scale = 1; // Reset circle size
        drawCircles();
        circle.playable = true;
    }

    if(event.key === ';' || event.key === ':') {
        const circle = circles[9];
        circle.scale = 1; // Reset circle size
        drawCircles();
        circle.playable = true;
    }

    if(event.key === "'" || event.key === '"') {
        const circle = circles[10];
        circle.scale = 1; // Reset circle size
        drawCircles();
        circle.playable = true;
    }
});

window.addEventListener('resize', function() {
    const oldWidth = canvas.width;
    const oldHeight = canvas.height;

    // Update canvas size
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    // Update circle positions and sizes without affecting ripple states
    for (let i = 0; i < circles.length; i++) {
        const circle = circles[i];
        // Scale the position and radius relative to the new canvas size
        circle.x = circle.x * (canvas.width / oldWidth);
        circle.y = circle.y * (canvas.height / oldHeight);
        circle.radius = circle.radius * (canvas.width / oldWidth);
        // Do not reset ripple properties here
    }

    // Redraw circles
    drawCircles();
});



function animate() {
    requestAnimationFrame(animate);
    drawCircles();
}

updateCirclesWhenWindowChangesSize();
animate();