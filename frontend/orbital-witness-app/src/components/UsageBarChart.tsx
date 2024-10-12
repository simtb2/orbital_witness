import React, { useState, useEffect } from 'react';
import { Bar } from 'react-chartjs-2';
import { fetchUsageData } from '../api';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

interface BarChartData {
  date: string;
  credits: number;
}

const UsageBarChart: React.FC = () => {
  const [barChartData, setBarChartData] = useState<BarChartData[]>([]);

  useEffect(() => {
    fetchUsageData().then((response) => {
      const aggregatedData = response.reduce((acc: { [date: string]: number }, item) => {
        const date = item.timestamp.split(' ')[0];
        acc[date] = (acc[date] || 0) + item.credits_used;
        return acc;
      }, {});

      const formattedData = Object.keys(aggregatedData).map(date => ({
        date,
        credits: aggregatedData[date],
      }));

      setBarChartData(formattedData);
    });
  }, []);

  const data = {
    labels: barChartData.map(d => d.date),
    datasets: [
      {
        label: 'Credits Used',
        data: barChartData.map(d => d.credits),
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Credits Used Per Day',
      },
    },
  };

  return <Bar data={data} options={options} />;
};

export default UsageBarChart;
