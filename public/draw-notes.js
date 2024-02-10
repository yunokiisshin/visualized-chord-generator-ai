// MIDI note range
const LOWEST_NOTE = 41; // F#3
const HIGHEST_NOTE = 76; // D5

// Preload audio files
// const audios = [];
// for (let i = 54; i < 75; i++) {
//     const audio = new Audio("./notes/" + i + ".wav");
//     audios.push(audio);
// }

// constants for drawings
const gap_X = 8; // gap_X between rows
const gap_Y = 4; // gap_Y between columns

const screenWidth = window.innerWidth;
const screenHeight = window.innerHeight;


// const rectWidth = (screenWidth / 8) - gap_X; // Width of each column (and thus each rectangle)
// const rectHeight =  (screenHeight - (HIGHEST_NOTE - LOWEST_NOTE) * (gap_Y)) / (HIGHEST_NOTE - LOWEST_NOTE + 1); // Height of the rectangle, can be adjusted

// Access the midiContainer element
const midiContainer = document.getElementById('midiContainer');

// Get the current dimensions of the midiContainer
const midiContainerWidth = midiContainer.offsetWidth;
const midiContainerHeight = midiContainer.offsetHeight;

// const rectWidth = (midiContainerWidth / 8) - gap_X; // Adjusted width of each rectangle
// const rectHeight = (midiContainerHeight - (HIGHEST_NOTE - LOWEST_NOTE) * (gap_Y)) / (HIGHEST_NOTE - LOWEST_NOTE + 1); // Adjusted height

let rectWidth;
let rectHeight;


// chord_symbols = "Am7 D7 GM7 Cm7/F7 Bbmaj7 Am7/D7 Gm7/C7 FMaj7"
// a nested dictionary of chords
const chordOutput = {
    '0': {
        "chord": "Am7",
        "length": 4,
        "notes" : [72, 67, 69, 76, 57]
    },

    '1': {
        "chord": "D7",
        "length": 4,
        "notes": [69, 60, 62, 66, 50]
    },

    '2': {
        "chord": "GM7",
        "length": 4,
        "notes": [62, 66, 59, 55, 43]
    },

    '3': {
        "chord": "Cm7",
        "length": 2,
        "notes": [60, 58, 55, 63, 48]
    },

    '4': {
        "chord": "F7",
        "length": 2,
        "notes": [57, 65, 60, 63, 53]
    },

    '5': {
        "chord": "Bbmaj7",
        "length": 4,
        "notes": [58, 62, 65, 57, 46]
    },

    '6': {
        "chord": "Am7",
        "length": 2,
        "notes": [57, 55, 60, 64, 45]
    },

    '7': {
        "chord": "D7",
        "length": 2,
        "notes": [57, 62, 60, 66, 50]
    },

    '8': {
        "chord": "Gm7",
        "length": 2,
        "notes": [58, 53, 55, 62, 43]
    },

    '9': {
        "chord": "C7",
        "length": 2,
        "notes": [55, 58, 64, 60, 48]
    },

    '10': {
        "chord": "FMaj7",
        "length": 4,
        "notes": [57, 64, 60, 65, 53]
    },

}

// note representation class
class NoteRectangle { 
    /**
     * constructor for the note rectangle. Each NoteRectangle object can represent a MIDI note
     * with appropriate functionalities
     * @param {dict} chordOutput: dictionary of chord information; usually 
     *                            from the chordOutput dictionary in the form of chordOutput[i]
     * @param {int} note:      MIDI note number in the form of integers
     * @param {file} audio:       .wav audio file corresponding to the sound of the note
     *                            in the form of audios[i]  
     */
    constructor(key, chordOutputInstance, note, audio) { 
        // chordOutputInstance looks like: 
        // {
        //     "chord": "Bbmaj7",
        //     "length": 4,
        //     "notes": {'root': [58, 70], 'third': [62, 74], 'fifth': [53, 65], 'seventh': [57, 69], 'ninth': [], 'extentions': []}
        // },
        
        // musical qualities
        this.chord = chordOutputInstance['chord'];
        this.duration = chordOutputInstance['length'];
        this.note = note;
        this.audio = audio;
        
        this.key = key;
        this.width = rectWidth * (Number(this.duration) / 4); 
        // console.log("width: " + this.width)
        this.x = this.calculateXPos(chordOutputInstance); 
        this.y = this.calculateYPos(note); 

        // console.log("duration: " + this.duration)
        this.height = rectHeight; 

        // console.log("chordOutputInstance: " + chordOutputInstance)
    }

    draw() { 
        const noteDiv = document.createElement('div');
        noteDiv.classList.add('note-rectangle');

        // Calculate the x and y position
        const xPos = this.x;
        const yPos = this.y;
        // console.log(xPos, yPos);
        const rectWidth = this.width;
        const rectHeight = this.height;

        // Set the style for the rectangle
        noteDiv.style.left = `${xPos}px`;
        noteDiv.style.top = `${yPos}px`;
        noteDiv.style.width = `${rectWidth}px`;
        noteDiv.style.height = `${rectHeight}px`;

        // Append the rectangle to the container
        midiContainer.appendChild(noteDiv);
    }

    calculateXPos() {
        let total_length = 0 + gap_X;
        for (let i = 0; i < Number(this.key); i++) {
            let duration = Number(chordOutput[i.toString()]["length"]);
            total_length += rectWidth * (Number(duration) / 4) + gap_X / 2;
        }
        return total_length;
    }

    calculateYPos(noteValue) {
        return (HIGHEST_NOTE - noteValue) * (rectHeight + gap_Y) + gap_Y ;
    }

    setWidth(width) {
        this.width = width;
    }

    setHeight(height) {
        this.height = height;
    }

    setXPos(x) {
        this.x = x;
    }

    setYPos(y) {
        this.y = y;
    }

    setNote(note) {
        this.note = note;
    }
}

// Function to adjust rectangle dimensions and positions on resize
function adjustOnResize() {
    // Use the container's offsetWidth and offsetHeight as the maximum dimensions
    rectWidth = (midiContainer.offsetWidth / 8) - gap_X;
    rectHeight = (midiContainer.offsetHeight - (HIGHEST_NOTE - LOWEST_NOTE) * (gap_Y)) / (HIGHEST_NOTE - LOWEST_NOTE + 1);

    // Clear existing rectangles
    while (midiContainer.firstChild) {
        midiContainer.removeChild(midiContainer.firstChild);
    }

    // Redraw rectangles with new dimensions
    drawRectangles();
}

// Function to draw rectangles
function drawRectangles() {
    const chordOutputKeyList = Object.keys(chordOutput);
    for (let i = 0; i < chordOutputKeyList.length; i++) {
        const key = chordOutputKeyList[i];
        for (let j = 0; j < chordOutput[key]["notes"].length; j++) {
            const currentNoteRect = new NoteRectangle(key, chordOutput[key], chordOutput[key]["notes"][j], 'audio');
            currentNoteRect.draw();
        }
    }
}

// Event listener for window resize to dynamically adjust the layout
window.addEventListener('resize', adjustOnResize);


// Initial adjustment and drawing
adjustOnResize();

// Function to get a random integer within a range, inclusive
function randomIntInRange(min, max) {
    min = Math.ceil(min); // Ensure min is rounded up to the nearest integer
    max = Math.floor(max); // Ensure max is rounded down to the nearest integer
    return Math.floor(Math.random() * (max - min + 1)) + min; //The maximum and minimum are inclusive
}


drawRectangles();


