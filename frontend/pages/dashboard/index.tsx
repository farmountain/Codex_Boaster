import React, { useState, useEffect } from 'react';
import { Box, Paper, Typography, Tabs, Tab, Grid } from '@mui/material';
import { useQuery } from 'react-query';
import axios from 'axios';
import LogViewer from '../../components/dashboard/LogViewer';
import PerformanceMetrics from '../../components/dashboard/PerformanceMetrics';
import AuditLog from '../../components/dashboard/AuditLog';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`dashboard-tabpanel-${index}`}
      aria-labelledby={`dashboard-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

function Dashboard() {
  const [tab, setTab] = useState(0);

  const { data: logs, isLoading: logsLoading } = useQuery('logs', () =>
    axios.get('/api/dashboard/logs').then(res => res.data)
  );

  const { data: metrics, isLoading: metricsLoading } = useQuery('metrics', () =>
    axios.get('/api/dashboard/performance').then(res => res.data)
  );

  const { data: auditLogs, isLoading: auditLoading } = useQuery('auditLogs', () =>
    axios.get('/api/dashboard/audit').then(res => res.data)
  );

  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Monitoring Dashboard
      </Typography>

      <Tabs
        value={tab}
        onChange={(e, newValue) => setTab(newValue)}
        sx={{ mb: 3 }}
      >
        <Tab label="Logs" />
        <Tab label="Performance" />
        <Tab label="Audit" />
      </Tabs>

      <TabPanel value={tab} index={0}>
        <LogViewer logs={logs || []} />
      </TabPanel>

      <TabPanel value={tab} index={1}>
        <PerformanceMetrics metrics={metrics || []} />
      </TabPanel>

      <TabPanel value={tab} index={2}>
        <AuditLog auditLogs={auditLogs || []} />
      </TabPanel>
    </Paper>
  );
}

export default Dashboard;
