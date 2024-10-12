// src/components/UsageTable.tsx
import React, { useState, useEffect } from 'react';
import { fetchUsageData } from '../api';
import { Table, TableBody, TableCell, TableHead, TableRow, Paper } from '@mui/material';

interface UsageData {
  message_id: number;
  timestamp: string;
  report_name: string | null;
  credits_used: number;
}

const UsageTable: React.FC = () => {
  const [data, setData] = useState<UsageData[]>([]);

  useEffect(() => {
    fetchUsageData().then((response: UsageData[]) => setData(response));
  }, []);

  return (
    <Paper>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Message ID</TableCell>
            <TableCell>Timestamp</TableCell>
            <TableCell>Report Name</TableCell>
            <TableCell>Credits Used</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {data.map((row) => (
            <TableRow key={row.message_id}>
              <TableCell>{row.message_id}</TableCell>
              <TableCell>{row.timestamp}</TableCell>
              <TableCell>{row.report_name || ''}</TableCell>
              <TableCell>{row.credits_used.toFixed(2)}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </Paper>
  );
};

export default UsageTable;
