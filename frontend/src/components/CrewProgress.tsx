import React from 'react';
import {
  Box,
  Paper,
  Typography,
  LinearProgress,
  Grid,
  Chip,
  Timeline,
  TimelineItem,
  TimelineSeparator,
  TimelineConnector,
  TimelineContent,
  TimelineDot,
  styled
} from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorIcon from '@mui/icons-material/Error';
import PendingIcon from '@mui/icons-material/Pending';
import { useQuery } from 'react-query';
import axios from 'axios';

const ProgressContainer = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(3),
  background: 'white',
  borderRadius: '12px',
  boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
}));

const StyledTimeline = styled(Timeline)({
  padding: 0,
  '& .MuiTimelineItem-root:before': {
    flex: 0,
    padding: 0,
  },
});

const CrewProgress: React.FC = () => {
  const { data: agents } = useQuery('agents', async () => {
    const response = await axios.get('http://localhost:8000/agents');
    return response.data;
  }, {
    refetchInterval: 2000
  });

  const { data: crewStatus } = useQuery('crewStatus', async () => {
    const response = await axios.get('http://localhost:8000/crew/status');
    return response.data;
  }, {
    refetchInterval: 2000
  });

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircleIcon color="success" />;
      case 'error':
        return <ErrorIcon color="error" />;
      case 'running':
        return <PendingIcon color="primary" />;
      default:
        return <PendingIcon color="disabled" />;
    }
  };

  const calculateOverallProgress = () => {
    if (!agents?.length) return 0;
    const completedAgents = agents.filter(a => a.status === 'completed').length;
    return (completedAgents / agents.length) * 100;
  };

  return (
    <ProgressContainer>
      <Box mb={3}>
        <Typography variant="h6" gutterBottom>
          Crew Execution Progress
        </Typography>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs>
            <LinearProgress
              variant="determinate"
              value={calculateOverallProgress()}
              sx={{ height: 10, borderRadius: 5 }}
            />
          </Grid>
          <Grid item>
            <Typography variant="body2" color="text.secondary">
              {Math.round(calculateOverallProgress())}%
            </Typography>
          </Grid>
        </Grid>
      </Box>

      <Box mb={3}>
        <Typography variant="subtitle2" gutterBottom>
          Current Status
        </Typography>
        <Box display="flex" gap={1}>
          <Chip
            label={`Active: ${agents?.filter(a => a.status === 'running').length || 0}`}
            color="primary"
            size="small"
          />
          <Chip
            label={`Completed: ${agents?.filter(a => a.status === 'completed').length || 0}`}
            color="success"
            size="small"
          />
          <Chip
            label={`Pending: ${agents?.filter(a => a.status === 'idle').length || 0}`}
            color="default"
            size="small"
          />
          <Chip
            label={`Error: ${agents?.filter(a => a.status === 'error').length || 0}`}
            color="error"
            size="small"
          />
        </Box>
      </Box>

      <Box>
        <Typography variant="subtitle2" gutterBottom>
          Execution Timeline
        </Typography>
        <StyledTimeline>
          {agents?.map((agent, index) => (
            <TimelineItem key={agent.name}>
              <TimelineSeparator>
                <TimelineDot color={
                  agent.status === 'completed' ? 'success' :
                  agent.status === 'running' ? 'primary' :
                  agent.status === 'error' ? 'error' : 'grey'
                }>
                  {getStatusIcon(agent.status)}
                </TimelineDot>
                {index < (agents.length - 1) && <TimelineConnector />}
              </TimelineSeparator>
              <TimelineContent>
                <Typography variant="subtitle2">
                  {agent.name}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {agent.role}
                </Typography>
              </TimelineContent>
            </TimelineItem>
          ))}
        </StyledTimeline>
      </Box>
    </ProgressContainer>
  );
};

export default CrewProgress;
