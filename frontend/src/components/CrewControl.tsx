import React from 'react';
import {
  Box,
  Fab,
  Typography,
  CircularProgress,
} from '@mui/material';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import StopIcon from '@mui/icons-material/Stop';

interface CrewControlProps {
  status: 'idle' | 'running' | 'error';
  onStart: () => void;
  onStop: () => void;
}

const CrewControl: React.FC<CrewControlProps> = ({ status, onStart, onStop }) => {
  return (
    <Box sx={{ position: 'fixed', right: 32, bottom: 32, display: 'flex', alignItems: 'center', gap: 2 }}>
      <Typography
        variant="subtitle1"
        sx={{
          padding: '8px 16px',
          borderRadius: 2,
          backgroundColor: status === 'running' ? 'success.light' :
                         status === 'error' ? 'error.light' :
                         'grey.300',
          color: status === 'running' ? 'success.dark' :
                 status === 'error' ? 'error.dark' :
                 'grey.700',
        }}
      >
        {status === 'running' ? 'Crew Active' :
         status === 'error' ? 'Error' :
         'Crew Idle'}
      </Typography>
      
      <Fab
        color="primary"
        onClick={status === 'running' ? onStop : onStart}
        sx={{
          background: status === 'running' ? 'error.main' : 'success.main',
          '&:hover': {
            background: status === 'running' ? 'error.dark' : 'success.dark',
          },
        }}
      >
        {status === 'running' ? (
          <StopIcon />
        ) : status === 'idle' ? (
          <PlayArrowIcon />
        ) : (
          <CircularProgress size={24} color="inherit" />
        )}
      </Fab>
    </Box>
  );
};

export default CrewControl;
