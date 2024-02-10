const express = require('express');
const app = express();
const port = 8000;

const cors = require('cors');
app.use(cors());

app.use(express.static('public')); // Serve your static files from 'public' directory

const path = require('path');

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '..', 'public', 'index.html'));
});



app.get('/generate-chords', (req, res) => {
    // Simulate generating chords (replace this with your actual logic)
    const chords = ['Cmaj7', 'Dm7', 'G7', 'Em7'];

    // Respond with the generated chords
    res.json({ chords: chords });
});

app.listen(port, () => {
    console.log(`Server listening at http://localhost:${port}`);
});

