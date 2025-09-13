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
  ReferenceLine
} from 'recharts';

interface Props {
  suggestedPrice: number;
  expectedRevenue: number;
  netProfit: number;
}

const BreakEvenChart: React.FC<Props> = ({ suggestedPrice, expectedRevenue, netProfit }) => {
  const fixedCosts = expectedRevenue - netProfit - (expectedRevenue * 0.6); // Estimated fixed costs
  const variableCostPerUnit = suggestedPrice * 0.6; // 60% of price as variable cost
  
  // Generate break-even data
  const generateBreakEvenData = () => {
    const data = [];
    const maxUnits = Math.ceil((expectedRevenue / suggestedPrice) * 2); // 2x expected volume
    
    for (let units = 0; units <= maxUnits; units += Math.ceil(maxUnits / 20)) {
      const revenue = units * suggestedPrice;
      const totalCosts = fixedCosts + (units * variableCostPerUnit);
      const profit = revenue - totalCosts;
      
      data.push({
        units,
        revenue,
        totalCosts,
        profit,
        unitsLabel: `${units}`
      });
    }
    
    return data;
  };

  const data = generateBreakEvenData();
  
  // Find break-even point
  const breakEvenPoint = data.find(point => point.profit >= 0);
  const breakEvenUnits = breakEvenPoint ? breakEvenPoint.units : 0;

  const formatCurrency = (value: number) => {
    return `৳${(value / 1000).toFixed(0)}K`;
  };

  return (
    <div style={{ width: '100%', height: 400 }}>
      <div style={{ marginBottom: '10px', textAlign: 'center', fontSize: '14px', color: '#666' }}>
        Break-even Point: {breakEvenUnits} units | {formatCurrency(breakEvenUnits * suggestedPrice)} revenue
      </div>
      
      <ResponsiveContainer width="100%" height="90%">
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="units" 
            tick={{ fontSize: 12 }}
            label={{ value: 'Units Sold', position: 'insideBottom', offset: -5 }}
          />
          <YAxis 
            tick={{ fontSize: 12 }}
            label={{ value: 'Amount (BDT)', angle: -90, position: 'insideLeft' }}
            tickFormatter={formatCurrency}
          />
          <Tooltip 
            formatter={(value, name) => [
              formatCurrency(Number(value)), 
              name === 'revenue' ? 'Revenue' : 
              name === 'totalCosts' ? 'Total Costs' : 'Profit/Loss'
            ]}
            labelFormatter={(label) => `Units: ${label}`}
          />
          <Legend />
          
          {/* Break-even reference line */}
          {breakEvenUnits > 0 && (
            <ReferenceLine 
              x={breakEvenUnits} 
              stroke="#ff9800" 
              strokeDasharray="5 5"
              label={{ value: "Break-even", position: "insideTopRight" }}
            />
          )}
          
          {/* Zero profit line */}
          <ReferenceLine 
            y={0} 
            stroke="#666" 
            strokeDasharray="2 2"
          />
          
          <Line
            type="monotone"
            dataKey="revenue"
            stroke="#4caf50"
            strokeWidth={2}
            dot={false}
            name="Revenue"
          />
          <Line
            type="monotone"
            dataKey="totalCosts"
            stroke="#f44336"
            strokeWidth={2}
            dot={false}
            name="Total Costs"
          />
          <Line
            type="monotone"
            dataKey="profit"
            stroke="#2196f3"
            strokeWidth={3}
            dot={false}
            name="Profit/Loss"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default BreakEvenChart;