import React from 'react';
import UsageTable from './components/UsageTable';
import UsageBarChart from './components/UsageBarChart';
import { Container, Typography } from '@mui/material';

const App: React.FC = () => {
  return (
    <Container>
      <Typography variant="h4"
       gutterBottom
       style={{ textAlign: 'center', marginBottom: '20px', marginTop: '50px' }}>
        Usage Dashboard
      </Typography>
      <UsageBarChart />
      <UsageTable />
    </Container>
  );
};

export default App;
