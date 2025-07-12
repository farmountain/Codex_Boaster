import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Grid,
  Card,
  CardContent,
  CardHeader,
  LinearProgress,
} from '@mui/material';
import { PerformanceMetric } from '../../types';
import { format } from 'date-fns';

interface PerformanceMetricsProps {
  metrics: PerformanceMetric[];
}

const PerformanceMetrics: React.FC<PerformanceMetricsProps> = ({ metrics }) => {
  const getLatestMetric = (component: string, metric: string) => {
    return metrics
      .filter(m => m.component === component && m.metric === metric)
      .sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime())
      .shift();
  };

  const metricsByComponent = metrics.reduce((acc, metric) => {
    if (!acc[metric.component]) {
      acc[metric.component] = {};
    }
    if (!acc[metric.component][metric.metric]) {
      acc[metric.component][metric.metric] = [];
    }
    acc[metric.component][metric.metric].push(metric);
    return acc;
  }, {} as Record<string, Record<string, PerformanceMetric[]>>);

  return (
    <Box>
      {Object.entries(metricsByComponent).map(([component, metrics]) => (
        <Paper key={component} sx={{ mb: 2 }}>
          <Typography variant="h6" sx={{ p: 2 }}>
            {component}
          </Typography>
          <Grid container spacing={2}>
            {Object.entries(metrics).map(([metricName, metricData]) => {
              const latest = getLatestMetric(component, metricName);
              return (
                <Grid item xs={12} sm={6} md={4} key={metricName}>
                  <Card>
                    <CardHeader title={metricName} />
                    <CardContent>
                      <Typography variant="h6" component="div">
                        {latest?.value}
                      </Typography>
                      <Typography color="text.secondary" sx={{ mb: 1 }}>
                        Last updated: {format(new Date(latest?.timestamp || ''), 'HH:mm:ss')}
                      </Typography>
                      <LinearProgress
                        variant="determinate"
                        value={(latest?.value || 0) * 100}
                      />
                    </CardContent>
                  </Card>
                </Grid>
              );
            })}
          </Grid>
        </Paper>
      ))}
    </Box>
  );
};

export default PerformanceMetrics;
