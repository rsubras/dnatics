import {React, useState} from 'react';
import { TextField, Typography, Paper, Button } from '@mui/material';
import axios from 'axios';

const RightContainer = () => {
  const [narration,setNarration] = useState('');
  const capture = async () => {
    console.log("Inside capture");
    const canvas = document.createElement("canvas");
    const context = canvas.getContext("2d");
    const video = document.createElement("video");
  
    try {
      const stream = await navigator.mediaDevices.getDisplayMedia({
        video: { cursor: "never", displaySurface: "browser" },
        preferCurrentTab: true // Automatically select the current web page
      });
      video.srcObject = stream;
      video.play();

      video.onloadedmetadata = async () => {
        // Add a delay before taking the screenshot
        await new Promise(resolve => setTimeout(resolve, 2000));

        const body = document.body;
        const html = document.documentElement;
        const width = Math.max(body.scrollWidth, body.offsetWidth, html.clientWidth, html.scrollWidth, html.offsetWidth);
        const height = Math.max(body.scrollHeight, body.offsetHeight, html.clientHeight, html.scrollHeight, html.offsetHeight);
        
        canvas.width = width;
        canvas.height = height;
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        const blob = await new Promise((resolve) => canvas.toBlob(resolve));
        
        // Stop the stream
        stream.getTracks().forEach(track => track.stop());
        
        // Save the blob as a file
        /*const url = URL.createObjectURL(blob);
        //const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = 'capture.png';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);*/
      // Save the blob as a file
      const file = new File([blob], 'capture.png', { type: 'image/png' });

      // Create FormData and append the file
      const formData = new FormData();
      formData.append('file', file);

      // Send the image to the FastAPI endpoint
      try {
        console.log("Form Data: ", formData);
        const response = await axios.post('http://localhost:8000/ocr/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
          
        });
        console.log("Response: ", response.data.content);
        setNarration(response.data.content);
      } catch (error) {
        console.error('Error uploading the file:', error);
        alert('Error uploading the file');
      }
    };

   
    } catch (err) {
      console.error("Error: " + err);
    }
  };

  return (
    <Paper style={{ padding: '20px', height: '100%', display: 'flex', flexDirection: 'column' }}>
      <Typography variant="h5" gutterBottom>
        PowerBI Report Narration
      </Typography>
      <TextField
        multiline
        rows={10}
        variant="outlined"
        placeholder="Write your narration about the image here..."
        fullWidth
        style={{ marginTop: '10px' }}
        value={narration}
        onChange={(e) => setNarration(e.target.value)}
      />
      <Button variant="contained" color="primary" onClick={capture}>
        Generate Narrative
      </Button>
      {<Typography variant="body1" sx={{ marginTop: '20px' }}>Narration will come here</Typography>}
    
    </Paper>
  );
};

export default RightContainer;