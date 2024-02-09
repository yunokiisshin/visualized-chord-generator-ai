// Get the canvas element and its context
const canvas = document.getElementById('midiCanvas');
const ctx = canvas.getContext('2d');
// Set canvas size
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// MIDI note range
const LOWEST_NOTE = 54; // F#3
const HIGHEST_NOTE = 74; // D5

// constants for drawings
const screenWidth = canvas.width;
const screenHeight = canvas.height;

const innerWidth = screenWidth - 20;
const innerHeight = screenHeight - 20;

const gap_X = 10; // gap_X between rows
const gap_Y = 5; // gap_Y between columns

const rectWidth = (innerWidth - 7 * (gap_X)) / 8; // Width of each column (and thus each rectangle)
const rectHeight =  (innerHeight - 20 * (gap_Y)) / 21; // Height of the rectangle, can be adjusted

// Function to draw a rectangle based on column index and MIDI note value
function drawNoteRectangle(columnIndex, midiValue) {

  // Calculate the x position based on the column index
  const xPos = gap_X + (columnIndex - 1) * (rectWidth + gap_X);

  // Map the MIDI value to the canvas height
  const yPos = gap_Y + (HIGHEST_NOTE - midiValue) * (rectHeight + gap_Y);

  // Set the style for the rectangle
  ctx.fillStyle = '#4CAF50'; // Green color, you can change this to any color you like

  // Draw the rectangle
  ctx.fillRect(xPos, yPos, rectWidth, rectHeight);
}


// Example usage
for (let i = 1; i <= 8; i++) {
  // random note value between LOWEST_NOTE and HIGHEST_NOTE
  note = Math.floor(Math.random() * (HIGHEST_NOTE - LOWEST_NOTE + 1)) + LOWEST_NOTE;
  drawNoteRectangle(i, note); 
  note = Math.floor(Math.random() * (HIGHEST_NOTE - LOWEST_NOTE + 1)) + LOWEST_NOTE;
  drawNoteRectangle(i, note); 
  note = Math.floor(Math.random() * (HIGHEST_NOTE - LOWEST_NOTE + 1)) + LOWEST_NOTE;
  drawNoteRectangle(i, note); 
  note = Math.floor(Math.random() * (HIGHEST_NOTE - LOWEST_NOTE + 1)) + LOWEST_NOTE;
  drawNoteRectangle(i, note); 
  note = Math.floor(Math.random() * (HIGHEST_NOTE - LOWEST_NOTE + 1)) + LOWEST_NOTE;
  drawNoteRectangle(i, note); 
  note = Math.floor(Math.random() * (HIGHEST_NOTE - LOWEST_NOTE + 1)) + LOWEST_NOTE;
  drawNoteRectangle(i, note); 
}

for (let i = 54; i <= 74; i++) {
  // random note value between LOWEST_NOTE and HIGHEST_NOTE
  drawNoteRectangle(1, i);  
}
