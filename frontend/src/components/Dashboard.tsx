import React, { useState } from 'react';
import {
  Box,
  Container,
  Paper,
  Typography,
  Grid,
  Card,
  CardContent,
  Alert,
  Snackbar,
} from '@mui/material';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import Header from './Header';
import Sidebar from './Sidebar';
import CrewControl from './CrewControl';
import api from '../config/axios';

interface CrewStats {
  activeAgents: number;
  completedTasks: number;
  successRate: number;
  averageTime: string;
}

interface CrewStatus {
  status: 'idle' | 'running' | 'error';
  startTime?: string;
  error?: string;
}

const Dashboard = () => {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [snackbar, setSnackbar] = useState<{
    open: boolean;
    message: string;
    severity: 'success' | 'error';
  }>({ open: false, message: '', severity: 'success' });

  const queryClient = useQueryClient();

  const { data: crewStats, error: statsError } = useQuery<CrewStats>('crewStats', async () => {
    try {
      const response = await api.get('/crew/stats');
      return response.data;
    } catch (error) {
      console.error('Failed to fetch crew stats:', error);
      return {
        activeAgents: 0,
        completedTasks: 0,
        successRate: 0,
        averageTime: '0m'
      };
    }
  }, {
    refetchInterval: 5000
  });

  const { data: crewStatus, error: statusError } = useQuery<CrewStatus>('crewStatus', async () => {
    try {
      const response = await api.get('/crew/status');
      return response.data;
    } catch (error) {
      console.error('Failed to fetch crew status:', error);
      return {
        status: 'error',
        error: 'Failed to connect to server'
      };
    }
  }, {
    refetchInterval: 2000
  });

  const startCrewMutation = useMutation(
    () => api.post('/crew/start'),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('crewStatus');
        setSnackbar({
          open: true,
          message: 'Crew started successfully',
          severity: 'success'
        });
      },
      onError: () => {
        setSnackbar({
          open: true,
          message: 'Failed to start crew',
          severity: 'error'
        });
      }
    }
  );

  const stopCrewMutation = useMutation(
    () => api.post('/crew/stop'),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('crewStatus');
        setSnackbar({
          open: true,
          message: 'Crew stopped successfully',
          severity: 'success'
        });
      },
      onError: () => {
        setSnackbar({
          open: true,
          message: 'Failed to stop crew',
          severity: 'error'
        });
      }
    }
  );

  const handleSidebarToggle = () => {
    setSidebarOpen(!sidebarOpen);
  };

  const handleCloseSnackbar = () => {
    setSnackbar({ ...snackbar, open: false });
  };

  // Show error message if both stats and status failed
  if (statsError && statusError) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <Alert severity="error" sx={{ maxWidth: 400 }}>
          Failed to connect to the server. Please make sure the backend is running.
        </Alert>
      </Box>
    );
  }

  return (
    <Box sx={{ display: 'flex' }}>
      <Header onMenuClick={handleSidebarToggle} />
      <Sidebar open={sidebarOpen} onClose={handleSidebarToggle} />
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          mt: 8,
          ml: sidebarOpen ? '240px' : 0,
          transition: 'margin 225ms cubic-bezier(0.4, 0, 0.6, 1) 0ms',
        }}
      >
        <Container maxWidth="lg">
          <Typography variant="h4" gutterBottom>
            AI Crew Manager
          </Typography>
          
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Paper sx={{ p: 3, borderRadius: 2 }}>
                <Typography variant="h6" gutterBottom>
                  Crew Overview
                </Typography>
                <Grid container spacing={3}>
                  <Grid item xs={12} sm={6} md={3}>
                    <Card>
                      <CardContent>
                        <Typography color="textSecondary" gutterBottom>
                          Active Agents
                        </Typography>
                        <Typography variant="h5">
                          {crewStats?.activeAgents || 0}
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                  <Grid item xs={12} sm={6} md={3}>
                    <Card>
                      <CardContent>
                        <Typography color="textSecondary" gutterBottom>
                          Completed Tasks
                        </Typography>
                        <Typography variant="h5">
                          {crewStats?.completedTasks || 0}
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                  <Grid item xs={12} sm={6} md={3}>
                    <Card>
                      <CardContent>
                        <Typography color="textSecondary" gutterBottom>
                          Success Rate
                        </Typography>
                        <Typography variant="h5">
                          {crewStats?.successRate || 0}%
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                  <Grid item xs={12} sm={6} md={3}>
                    <Card>
                      <CardContent>
                        <Typography color="textSecondary" gutterBottom>
                          Average Time
                        </Typography>
                        <Typography variant="h5">
                          {crewStats?.averageTime || '0m'}
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                </Grid>
              </Paper>
            </Grid>
          </Grid>
        </Container>

        <CrewControl
          status={crewStatus?.status || 'idle'}
          onStart={() => startCrewMutation.mutate()}
          onStop={() => stopCrewMutation.mutate()}
        />

        <Snackbar
          open={snackbar.open}
          autoHideDuration={6000}
          onClose={handleCloseSnackbar}
          anchorOrigin={{ vertical: 'bottom', horizontal: 'left' }}
        >
          <Alert
            onClose={handleCloseSnackbar}
            severity={snackbar.severity}
            sx={{ width: '100%' }}
          >
            {snackbar.message}
          </Alert>
        </Snackbar>
      </Box>
    </Box>
  );
};

export default Dashboard;
