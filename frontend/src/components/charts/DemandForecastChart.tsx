import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Area,
  AreaChart
} from 'recharts';
import { ForecastData } from '../../types/types';

interface Props {
  data: ForecastData[];
}

const DemandForecastChart: React.FC<Props> = ({ data }) => {
  const chartData = data.map(item => ({
    month: `Month ${item.month}`,
    demand: Math.round(item.demand),
    lower: Math.round(item.confidence_lower),
    upper: Math.round(item.confidence_upper)
  }));

  return (
    <ResponsiveContainer width="100%" height={300}>
      <AreaChart data={chartData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis 
          dataKey="month" 
          tick={{ fontSize: 12 }}
          angle={-45}
          textAnchor="end"
          height={60}
        />
        <YAxis 
          tick={{ fontSize: 12 }}
          label={{ value: 'Demand', angle: -90, position: 'insideLeft' }}
        />
        <Tooltip 
          formatter={(value, name) => [
            typeof value === 'number' ? value.toLocaleString() : value, 
            name === 'demand' ? 'Predicted Demand' : 
            name === 'lower' ? 'Lower Confidence' : 'Upper Confidence'
          ]}
        />
        <Legend />
        
        {/* Confidence interval area */}
        <Area
          type="monotone"
          dataKey="upper"
          stroke="none"
          fill="#e3f2fd"
          fillOpacity={0.4}
        />
        <Area
          type="monotone"
          dataKey="lower"
          stroke="none"
          fill="#ffffff"
          fillOpacity={1}
        />
        
        {/* Main demand line */}
        <Line
          type="monotone"
          dataKey="demand"
          stroke="#1976d2"
          strokeWidth={3}
          dot={{ fill: '#1976d2', strokeWidth: 2, r: 4 }}
          activeDot={{ r: 6 }}
        />
      </AreaChart>
    </ResponsiveContainer>
  );
};

export default DemandForecastChart;