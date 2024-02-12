const express = require('express');
const app = express();
const port = 8000;

const cors = require('cors');
app.use(cors());

app.use(express.json()); // For parsing application/json
app.use(express.static('public')); // Serve your static files from 'public' directory

const path = require('path');

const { spawn } = require('child_process'); // To spawn the Python process

app.get('/', (req, res) => {
    // Navigates up one level from the current directory (__dirname), then into the 'public' directory
    res.sendFile(path.join(__dirname, '..', 'public', 'index.html'));
});


app.post('/generate-chords', (req, res) => {
    // Set Content-Type for this response
    res.setHeader('Content-Type', 'application/json');

    // Extract prompt from request body, if provided
    const prompt = req.body.prompt || "Generate a jazz chord progression";

    // Spawn Python process
    const pythonProcess = spawn('python3', ['server/main.py', prompt]); 

    let pythonData = "";
    pythonProcess.stdout.on('data', (data) => {
        pythonData += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });

    pythonProcess.on('close', (code) => {
        console.log(`child process exited with code ${code}`);
        if (code === 0) {
            // Assuming your Python script prints JSON output
            try {
                const output = JSON.parse(pythonData);
                res.json(output); // Send the Python script's output back to the client
            } catch (error) {
                console.error('Error parsing Python script output:', error);
                res.status(500).json({ error: "Failed to parse script output" });
            }
        } else {
            res.status(500).json({ error: "An error occurred while generating the chords" });
        }
    });
});


app.listen(port, () => {
    console.log(`Server listening at http://localhost:${port}`);
});
