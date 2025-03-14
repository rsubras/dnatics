import React from 'react';
import { AppBar, Toolbar, Typography, Grid } from '@mui/material';
import LeftContainer from './LeftContainer';
import RightContainer from './RightContainer';

const Layout = () => {
  return (
    <div>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6">PowerBI Report Narration App</Typography>
        </Toolbar>
      </AppBar>
      <Grid container style={{ marginTop: '20px' }}>
        <Grid item xs={12} md={7}>
          <LeftContainer />
        </Grid>
        <Grid item xs={12} md={5}>
          <RightContainer />
        </Grid>
      </Grid>
    </div>
  );
};

export default Layout;