const midiContainer = document.getElementById('midiContainer');

// MIDI note range
const LOWEST_NOTE = 54; // F#3
const HIGHEST_NOTE = 74; // D5

// Constants for layout
const gap_X = 10; // Gap between rows
const gap_Y = 5; // Gap between columns

const rectWidth = 50; // Width of each rectangle, can be adjusted
const rectHeight = 20; // Height of each rectangle, can be adjusted

// Function to create and position a note rectangle
function createNoteRectangle(columnIndex, midiValue) {
  const noteDiv = document.createElement('div');
  noteDiv.classList.add('note-rectangle');

  // Calculate the x and y position
  const xPos = gap_X + (columnIndex - 1) * (rectWidth + gap_X);
  const yPos = gap_Y + (HIGHEST_NOTE - midiValue) * (rectHeight + gap_Y);

  // Set the style for the rectangle
  noteDiv.style.left = `${xPos}px`;
  noteDiv.style.top = `${yPos}px`;
  noteDiv.style.width = `${rectWidth}px`;
  noteDiv.style.height = `${rectHeight}px`;

  // Append the rectangle to the container
  midiContainer.appendChild(noteDiv);
}

// Example usage
for (let i = 1; i <= 8; i++) {
  for (let j = 0; j < 6; j++) { // Draw 6 rectangles per column
    const note = Math.floor(Math.random() * (HIGHEST_NOTE - LOWEST_NOTE + 1)) + LOWEST_NOTE;
    createNoteRectangle(i, note);
  }
}

for (let i = 54; i <= 74; i++) {
  createNoteRectangle(1, i);
}
