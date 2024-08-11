import express from 'express';
import { Client } from "@gradio/client";
import fs from 'fs';
import path from 'path';
import { promisify } from 'util';
import fetch from 'node-fetch';
import { fileURLToPath } from 'url';
import ffmpeg from 'fluent-ffmpeg';

const app = express();
const port = 3000;
const writeFile = promisify(fs.writeFile);
const mkdir = promisify(fs.mkdir);

// Get the directory name
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

app.use(express.json());
app.use(express.static('public')); // Serve static files from 'public' folder if you place your HTML there

app.post('/generate-audio', async (req, res) => {
    const { input_text } = req.body;

    if (!input_text || typeof input_text !== 'string') {
        return res.status(400).json({ error: 'Invalid input text' });
    }

    try {
        // Connect to Gradio Client
        const client = await Client.connect("mmayya/tts");
        const result = await client.predict("/predict", { text: input_text });
        console.log(result);

        // Assuming result.audio contains the URL to the audio
        const audioUrl = result.data[0].url;
        console.log(audioUrl);
        if (!audioUrl) {
            throw new Error('No audio URL returned');
        }

        res.json({ audioUrl });

    } catch (error) {
        console.error('Error generating audio:', error);
        res.status(500).json({ error: 'An error occurred while generating the audio' });
    }
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
