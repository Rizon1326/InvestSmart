import React from 'react';
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Tooltip,
  Legend,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid
} from 'recharts';

interface Props {
  expectedRevenue: number;
  netProfit: number;
  roiPercentage: number;
}

const ROIChart: React.FC<Props> = ({ expectedRevenue, netProfit, roiPercentage }) => {
  const costs = expectedRevenue - netProfit;
  
  const pieData = [
    { name: 'Net Profit', value: netProfit, color: '#4caf50' },
    { name: 'Total Costs', value: costs, color: '#f44336' }
  ];

  const roiData = [
    { name: 'Conservative', roi: roiPercentage * 0.7, color: '#ff9800' },
    { name: 'Expected', roi: roiPercentage, color: '#2196f3' },
    { name: 'Optimistic', roi: roiPercentage * 1.3, color: '#4caf50' }
  ];

  const formatCurrency = (value: number) => {
    return `৳${(value / 1000).toFixed(0)}K`;
  };

  const formatPercentage = (value: number) => {
    return `${value.toFixed(1)}%`;
  };

  return (
    <div style={{ width: '100%', height: 300 }}>
      <div style={{ display: 'flex', height: '100%' }}>
        {/* Revenue Breakdown Pie Chart */}
        <div style={{ flex: 1 }}>
          <h4 style={{ textAlign: 'center', margin: '0 0 10px 0', fontSize: '14px' }}>
            Revenue Breakdown
          </h4>
          <ResponsiveContainer width="100%" height="85%">
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                innerRadius={40}
                outerRadius={80}
                dataKey="value"
                label={(entry) => formatCurrency(entry.value)}
              >
                {pieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip formatter={(value) => formatCurrency(Number(value))} />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* ROI Scenarios Bar Chart */}
        <div style={{ flex: 1 }}>
          <h4 style={{ textAlign: 'center', margin: '0 0 10px 0', fontSize: '14px' }}>
            ROI Scenarios
          </h4>
          <ResponsiveContainer width="100%" height="85%">
            <BarChart data={roiData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="name" 
                tick={{ fontSize: 12 }}
                angle={-15}
                textAnchor="end"
                height={40}
              />
              <YAxis 
                tick={{ fontSize: 12 }}
                label={{ value: 'ROI %', angle: -90, position: 'insideLeft' }}
              />
              <Tooltip formatter={(value) => formatPercentage(Number(value))} />
              <Bar 
                dataKey="roi" 
                fill="#8884d8"
                radius={[4, 4, 0, 0]}
              >
                {roiData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default ROIChart;