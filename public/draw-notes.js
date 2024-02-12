// Constants and initial setup
const LOWEST_NOTE = 52; // F#3
const HIGHEST_NOTE = 76; // D5
const gap_X = 8; // gap_X between rows
const gap_Y = 4; // gap_Y between columns
const midiContainer = document.getElementById('midiContainer');
let rectWidth;
let rectHeight;

const hello_midi = {
    "0": {
        "chord" : "",
        "length" : 0.5,
        "notes": []
    },
    "1": {
        "chord" : "",
        "length" : 2,
        "notes" : [54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75]
    },
    "2": {
        "chord" : "",
        "length" : 3,
        "notes" : [63,64,65,66]
    },
    "3": {
        "chord" : "",
        "length" : 2,
        "notes" : [54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75]
    },
    "4": {
        "chord" : "",
        "length" : 0.5,
        "notes": []
    },
    "5": {
        "chord" : "",
        "length" : 2,
        "notes" : [54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75]
    },
    "6": {
        "chord" : "",
        "length" : 3,
        "notes" : [54,55,56,57,63,64,65,66,72,73,74,75]
    },
    "7": {
        "chord" : "",
        "length" : 0.5,
        "notes": []
    },
    "8": {
        "chord" : "",
        "length" : 2,
        "notes" : [54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75]
    },
    "9": {
        "chord" : "",
        "length" : 3,
        "notes" : [54,55,56,57]
    },
    "10": {
        "chord" : "",
        "length" : 0.5,
        "notes": []
    },
    "11": {
        "chord" : "",
        "length" : 2,
        "notes" : [54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75]
    },
    "12": {
        "chord" : "",
        "length" : 3,
        "notes" : [54,55,56,57]
    },
    "13": {
        "chord" : "",
        "length" : 0.5,
        "notes": []
    },
    "14": {
        "chord" : "",
        "length" : 2,
        "notes" : [54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75]
    },
    "15": {
        "chord" : "",
        "length" : 2,
        "notes" : [54,55,56,57,72,73,74,75]
    },
    "16": {
        "chord" : "",
        "length" : 2,
        "notes" : [54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75]
    }
}



// Class definition for NoteRectangle
class NoteRectangle {
    constructor(key, chordData, note, note_audio = "") {
        this.key = key;
        this.chord = chordData[key]['chord'];
        this.duration = chordData[key]['length'];
        this.note = note;
        this.note_audio = note_audio;
        this.width = rectWidth * (Number(this.duration) / 4);
        this.x = this.calculateXPos(key, chordData); 
        this.y = this.calculateYPos(note); 
        this.height = rectHeight;
    }

    draw() {
        // console.log("  in draw()");
        // console.log("  this.x = " + this.x);
        // console.log("  this.y = " + this.y);
        // console.log("  this.width = " + this.width);
        // console.log("  this.height = " + this.height);

        const noteDiv = document.createElement('div');
        noteDiv.classList.add('note-rectangle');
        noteDiv.style.left = `${this.x}px`;
        noteDiv.style.top = `${this.y}px`;
        noteDiv.style.width = `${this.width}px`;
        noteDiv.style.height = `${this.height}px`;
        midiContainer.appendChild(noteDiv);
    }

    calculateXPos(key, chordData) {
        let total_length = 0 + gap_X;
        for (let i = 0; i < Number(key); i++) {
            // Check if hello_midi has the key before accessing its properties
            if (chordData.hasOwnProperty(i.toString())) {
                let duration = Number(chordData[i.toString()]["length"]);
                total_length += rectWidth * (Number(duration) / 4) + gap_X / 2;
            }
        }
        return total_length;
    }
    

    calculateYPos(noteValue) {
        return (HIGHEST_NOTE - noteValue) * (rectHeight + gap_Y) + gap_Y;
    }
}

// Function to adjust rectangle dimensions and positions on resize
function adjustOnResize() {
    rectWidth = (midiContainer.offsetWidth / 8) - gap_X;
    rectHeight = (midiContainer.offsetHeight - (HIGHEST_NOTE - LOWEST_NOTE) * (gap_Y)) / (HIGHEST_NOTE - LOWEST_NOTE + 1);
    drawRectangles(); // Redraw rectangles with new dimensions
}

// Function to draw rectangles for all chords
function drawRectangles(chordData = hello_midi) {
    while (midiContainer.firstChild) {
        midiContainer.removeChild(midiContainer.firstChild); // Clear existing rectangles
    }

    Object.keys(chordData).forEach(key => {
        chordData[key]["notes"].forEach(note => {
            const noteRect = new NoteRectangle(key, chordData, note);
            noteRect.draw();
        });
    });
}


document.addEventListener('DOMContentLoaded', function() {
    adjustOnResize(); // Ensure this is called after the DOM is fully loaded

    // Button click event listener to fetch and draw new chord data
    document.getElementById('generateButton').addEventListener('click', function() {
        console.log("Generate is pressed");
        fetch('/generate-chords', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
                drawRectangles(data); // Draw rectangles with fetched chord data
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    });

    // Event listener for window resize to dynamically adjust the layout
    window.addEventListener('resize', adjustOnResize);
});

// Initial adjustment and drawing
adjustOnResize();