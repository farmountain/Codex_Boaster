import React, { useState, useEffect } from 'react';
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
  MenuItem,
} from '@mui/material';
import { format } from 'date-fns';
import { AuditEntry } from '../../types';

interface AuditLogProps {
  auditLogs: AuditEntry[];
}

const AuditLog: React.FC<AuditLogProps> = ({ auditLogs }) => {
  const [filter, setFilter] = useState({
    user: '',
    action: '',
    status: '',
  });

  const filteredLogs = auditLogs.filter(log =>
    (!filter.user || log.user === filter.user) &&
    (!filter.action || log.action === filter.action) &&
    (!filter.status || log.status === filter.status)
  );

  const uniqueUsers = [...new Set(auditLogs.map(log => log.user))];
  const uniqueActions = [...new Set(auditLogs.map(log => log.action))];
  const uniqueStatuses = [...new Set(auditLogs.map(log => log.status))];

  return (
    <Box>
      <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
        <TextField
          select
          label="User"
          value={filter.user}
          onChange={(e) => setFilter({ ...filter, user: e.target.value })}
        >
          <MenuItem value="">All Users</MenuItem>
          {uniqueUsers.map(user => (
            <MenuItem key={user} value={user}>
              {user}
            </MenuItem>
          ))}
        </TextField>

        <TextField
          select
          label="Action"
          value={filter.action}
          onChange={(e) => setFilter({ ...filter, action: e.target.value })}
        >
          <MenuItem value="">All Actions</MenuItem>
          {uniqueActions.map(action => (
            <MenuItem key={action} value={action}>
              {action}
            </MenuItem>
          ))}
        </TextField>

        <TextField
          select
          label="Status"
          value={filter.status}
          onChange={(e) => setFilter({ ...filter, status: e.target.value })}
        >
          <MenuItem value="">All Statuses</MenuItem>
          {uniqueStatuses.map(status => (
            <MenuItem key={status} value={status}>
              {status}
            </MenuItem>
          ))}
        </TextField>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Timestamp</TableCell>
              <TableCell>User</TableCell>
              <TableCell>Action</TableCell>
              <TableCell>Resource</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Message</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredLogs.map((log) => (
              <TableRow key={log.timestamp}>
                <TableCell>{format(new Date(log.timestamp), 'yyyy-MM-dd HH:mm:ss')}</TableCell>
                <TableCell>{log.user}</TableCell>
                <TableCell>{log.action}</TableCell>
                <TableCell>{log.resource}</TableCell>
                <TableCell>
                  <Typography
                    color={
                      log.status === 'success' ? 'success' :
                      log.status === 'failed' ? 'error' :
                      'primary'
                    }
                  >
                    {log.status}
                  </Typography>
                </TableCell>
                <TableCell>{log.message}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};

export default AuditLog;
