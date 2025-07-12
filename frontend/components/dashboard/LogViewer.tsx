import React, { useState, useEffect } from 'react';
import { LogEntry } from '../../types';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Box,
  TextField,
  Button,
  Typography,
} from '@mui/material';
import { format } from 'date-fns';

interface LogViewerProps {
  logs: LogEntry[];
}

const LogViewer: React.FC<LogViewerProps> = ({ logs }) => {
  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Timestamp</TableCell>
            <TableCell>Level</TableCell>
            <TableCell>Message</TableCell>
            <TableCell>Context</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {logs.map((log) => (
            <TableRow key={log.timestamp}>
              <TableCell>{format(new Date(log.timestamp), 'yyyy-MM-dd HH:mm:ss')}</TableCell>
              <TableCell>
                <Typography
                  color={
                    log.level === 'ERROR' ? 'error' :
                    log.level === 'WARNING' ? 'warning' :
                    log.level === 'INFO' ? 'primary' :
                    'secondary'
                  }
                >
                  {log.level}
                </Typography>
              </TableCell>
              <TableCell>{log.message}</TableCell>
              <TableCell>
                <pre style={{ whiteSpace: 'pre-wrap' }}>
                  {JSON.stringify(log.context, null, 2)}
                </pre>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default LogViewer;
