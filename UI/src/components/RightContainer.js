import React from 'react';
import { TextField, Typography, Paper, Button } from '@mui/material';

const RightContainer = () => {
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
      />
      <Button variant="contained" color="primary">
        Generate Narrative
      </Button>
      {<Typography variant="body1" sx={{ marginTop: '20px' }}>Narration will come here</Typography>}
    
    </Paper>
  );
};

export default RightContainer;