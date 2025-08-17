import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
} from "recharts";

interface TariffData {
  country: string;
  tariff_rate: number;
  sector: string;
  impact_level: string;
}

interface CountryComparisonProps {
  countries: string[];
  onCountrySelect: (country: string) => void;
}

interface SectorAnalysisProps {
  sectorData: Array<{
    sector: string;
    tariff_rate: number;
    impact_level: string;
    source: string;
    trade_volume: number;
    notes: string;
  }>;
}

interface RegionalImpactProps {
  countries: string[];
  getCountryTariff: (country: string) => number;
}

// Color schemes for different impact levels
const IMPACT_COLORS = {
  Critical: "#dc2626", // red-600
  High: "#ea580c", // orange-600
  Medium: "#d97706", // amber-600
  Low: "#65a30d", // lime-600
  Minimal: "#16a34a", // green-600
};

const REGION_COLORS = {
  Asia: "#3b82f6", // blue-500
  Europe: "#8b5cf6", // violet-500
  Americas: "#ef4444", // red-500
  Africa: "#f59e0b", // amber-500
  "Middle East": "#10b981", // emerald-500
  Oceania: "#06b6d4", // cyan-500
};

export const CountryComparisonChart: React.FC<CountryComparisonProps> = ({
  countries,
  onCountrySelect,
}) => {
  // Sample data - in real app, this would come from API
  const sampleData = countries.slice(0, 10).map((country) => ({
    country,
    tariff_rate: Math.random() * 100, // Replace with real data
    region: "Asia", // Replace with real region data
  }));

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h3 className="text-xl font-bold text-gray-800 mb-4">
        Country Tariff Comparison
      </h3>
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={sampleData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis
              dataKey="country"
              angle={-45}
              textAnchor="end"
              height={80}
              fontSize={12}
            />
            <YAxis
              label={{
                value: "Tariff Rate (%)",
                angle: -90,
                position: "insideLeft",
              }}
              fontSize={12}
            />
            <Tooltip
              formatter={(value: number) => [
                `${value.toFixed(1)}%`,
                "Tariff Rate",
              ]}
              labelFormatter={(label) => `Country: ${label}`}
            />
            <Bar
              dataKey="tariff_rate"
              fill="#3b82f6"
              onClick={(data) => onCountrySelect(data.country)}
              className="cursor-pointer hover:opacity-80 transition-opacity"
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
      <p className="text-sm text-gray-600 mt-2">
        Click on bars to select countries for detailed analysis
      </p>
    </div>
  );
};

export const SectorImpactChart: React.FC<SectorAnalysisProps> = ({
  sectorData,
}) => {
  const chartData = sectorData.map((item) => ({
    name: item.sector,
    value: item.tariff_rate,
    impact: item.impact_level,
  }));

  const COLORS = chartData.map(
    (item) =>
      IMPACT_COLORS[item.impact as keyof typeof IMPACT_COLORS] || "#6b7280"
  );

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h3 className="text-xl font-bold text-gray-800 mb-4">
        Sector Impact Analysis
      </h3>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Pie Chart */}
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={chartData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, value }) => `${name}: ${value}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {chartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index]} />
                ))}
              </Pie>
              <Tooltip
                formatter={(value: number) => [`${value}%`, "Tariff Rate"]}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Sector Details */}
        <div className="space-y-3">
          <h4 className="font-semibold text-gray-700">Sector Breakdown</h4>
          {sectorData.map((sector, index) => (
            <div
              key={index}
              className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
            >
              <div className="flex items-center space-x-3">
                <div
                  className="w-4 h-4 rounded-full"
                  style={{
                    backgroundColor:
                      IMPACT_COLORS[
                        sector.impact_level as keyof typeof IMPACT_COLORS
                      ] || "#6b7280",
                  }}
                />
                <span className="font-medium text-gray-800">
                  {sector.sector}
                </span>
              </div>
              <div className="text-right">
                <div
                  className="font-bold text-lg"
                  style={{
                    color:
                      IMPACT_COLORS[
                        sector.impact_level as keyof typeof IMPACT_COLORS
                      ] || "#6b7280",
                  }}
                >
                  {Math.round(sector.tariff_rate)}%
                </div>
                <div className="text-sm text-gray-600 capitalize">
                  {sector.impact_level}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export const RegionalImpactMap: React.FC<RegionalImpactProps> = ({
  countries,
  getCountryTariff,
}) => {
  // Group countries by region (simplified for demo)
  const regionData = countries.reduce(
    (acc, country) => {
      const region = getRegion(country);
      if (!acc[region]) acc[region] = [];
      acc[region].push({
        country,
        tariff_rate: getCountryTariff(country),
      });
      return acc;
    },
    {} as Record<string, Array<{ country: string; tariff_rate: number }>>
  );

  const chartData = Object.entries(regionData).map(([region, countries]) => ({
    region,
    avg_tariff:
      countries.reduce((sum, c) => sum + c.tariff_rate, 0) / countries.length,
    country_count: countries.length,
  }));

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h3 className="text-xl font-bold text-gray-800 mb-4">
        Regional Impact Overview
      </h3>
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="region" fontSize={12} />
            <YAxis
              label={{
                value: "Average Tariff Rate (%)",
                angle: -90,
                position: "insideLeft",
              }}
              fontSize={12}
            />
            <Tooltip
              formatter={(value: number, name: string) => [
                name === "avg_tariff" ? `${value.toFixed(1)}%` : value,
                name === "avg_tariff" ? "Avg Tariff" : "Countries",
              ]}
            />
            <Bar dataKey="avg_tariff" fill="#3b82f6" name="Average Tariff" />
            <Bar dataKey="country_count" fill="#10b981" name="Country Count" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export const TariffTrendChart: React.FC = () => {
  // Sample trend data - in real app, this would show tariff changes over time
  const trendData = [
    { month: "Jan", tariff_rate: 15, affected_countries: 45 },
    { month: "Feb", tariff_rate: 18, affected_countries: 52 },
    { month: "Mar", tariff_rate: 22, affected_countries: 58 },
    { month: "Apr", tariff_rate: 25, affected_countries: 62 },
    { month: "May", tariff_rate: 28, affected_countries: 68 },
    { month: "Jun", tariff_rate: 32, affected_countries: 72 },
    { month: "Jul", tariff_rate: 35, affected_countries: 76 },
  ];

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h3 className="text-xl font-bold text-gray-800 mb-4">
        Tariff Trend Analysis
      </h3>
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={trendData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" fontSize={12} />
            <YAxis
              yAxisId="left"
              label={{
                value: "Tariff Rate (%)",
                angle: -90,
                position: "insideLeft",
              }}
              fontSize={12}
            />
            <YAxis
              yAxisId="right"
              orientation="right"
              label={{
                value: "Affected Countries",
                angle: 90,
                position: "insideRight",
              }}
              fontSize={12}
            />
            <Tooltip />
            <Line
              yAxisId="left"
              type="monotone"
              dataKey="tariff_rate"
              stroke="#3b82f6"
              strokeWidth={3}
              name="Tariff Rate"
            />
            <Line
              yAxisId="right"
              type="monotone"
              dataKey="affected_countries"
              stroke="#10b981"
              strokeWidth={3}
              name="Affected Countries"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
      <p className="text-sm text-gray-600 mt-2">
        Shows the progression of tariff rates and affected countries over time
      </p>
    </div>
  );
};

export const ImpactSummaryCards: React.FC<{ countryData: any }> = ({
  countryData,
}) => {
  // Debug logging
  console.log("ImpactSummaryCards - countryData:", countryData);
  console.log("Affected sectors count:", countryData?.affected_sectors?.length);
  console.log("Affected sectors array:", countryData?.affected_sectors);

  const getImpactLevel = (tariffRate: number) => {
    if (tariffRate >= 50)
      return { level: "Critical", color: "bg-red-600", text: "text-red-600" };
    if (tariffRate >= 30)
      return { level: "High", color: "bg-orange-600", text: "text-orange-600" };
    if (tariffRate >= 15)
      return { level: "Medium", color: "bg-amber-600", text: "text-amber-600" };
    if (tariffRate >= 5)
      return { level: "Low", color: "bg-lime-600", text: "text-lime-600" };
    return { level: "Minimal", color: "bg-green-600", text: "text-green-600" };
  };

  const impact = getImpactLevel(countryData?.tariff_rate || 0);

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      {/* Tariff Rate Card */}
      <div className="bg-white rounded-lg shadow-md p-4 border-l-4 border-blue-500">
        <div className="flex items-center">
          <div className="p-2 bg-blue-100 rounded-lg">
            <svg
              className="w-6 h-6 text-blue-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"
              />
            </svg>
          </div>
          <div className="ml-4">
            <p className="text-sm font-medium text-gray-600">Tariff Rate</p>
            <p className="text-2xl font-bold text-gray-900">
              {Math.round(countryData?.tariff_rate || 0)}%
            </p>
          </div>
        </div>
      </div>

      {/* Impact Level Card */}
      <div className="bg-white rounded-lg shadow-md p-4 border-l-4 border-orange-500">
        <div className="flex items-center">
          <div className="p-2 bg-orange-100 rounded-lg">
            <svg
              className="w-6 h-6 text-orange-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M13 10V3L4 14h7v7l9-11h-7z"
              />
            </svg>
          </div>
          <div className="ml-4">
            <p className="text-sm font-medium text-gray-600">Impact Level</p>
            <p className={`text-2xl font-bold ${impact.text}`}>
              {impact.level}
            </p>
          </div>
        </div>
      </div>

      {/* Affected Sectors Card */}
      <div className="bg-white rounded-lg shadow-md p-4 border-l-4 border-purple-500">
        <div className="flex items-center">
          <div className="p-2 bg-purple-100 rounded-lg">
            <svg
              className="w-6 h-6 text-purple-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"
              />
            </svg>
          </div>
          <div className="ml-4">
            <p className="text-sm font-medium text-gray-600">
              Affected Sectors
            </p>
            <p className="text-2xl font-bold text-gray-900">
              {countryData?.affected_sectors ? countryData.affected_sectors.length : 0}
            </p>
            <p className="text-xs text-gray-500 mt-1">
              {countryData?.affected_sectors?.length > 0 
                ? "sectors impacted" 
                : "no tariffs"}
            </p>
            <p className="text-xs text-blue-500 mt-1">
              {countryData?.name || "Loading..."}
            </p>
          </div>
        </div>
      </div>

      {/* Trade Volume Card */}
      <div className="bg-white rounded-lg shadow-md p-4 border-l-4 border-green-500">
        <div className="flex items-center">
          <div className="p-2 bg-green-100 rounded-lg">
            <svg
              className="w-6 h-6 text-green-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
              />
            </svg>
          </div>
          <div className="ml-4">
            <p className="text-sm font-medium text-gray-600">Trade Volume</p>
            <p className="text-2xl font-bold text-gray-900">
              {(() => {
                const volume = countryData?.trade_volume_millions || 0;
                if (volume >= 1000000) {
                  return `$${(volume / 1000000).toFixed(1)}T`;
                } else if (volume >= 1000) {
                  return `$${(volume / 1000).toFixed(0)}B`;
                } else {
                  return `$${volume.toLocaleString()}M`;
                }
              })()}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

// Helper function to determine region
const getRegion = (country: string): string => {
  const asiaCountries = [
    "China",
    "Japan",
    "South Korea",
    "India",
    "Thailand",
    "Vietnam",
    "Malaysia",
    "Singapore",
    "Indonesia",
    "Philippines",
  ];
  const europeCountries = [
    "European Union",
    "Germany",
    "France",
    "Italy",
    "Spain",
    "Netherlands",
    "Belgium",
    "Sweden",
  ];
  const americasCountries = [
    "Brazil",
    "Mexico",
    "Canada",
    "Argentina",
    "Chile",
    "Peru",
    "Colombia",
    "Venezuela",
  ];
  const africaCountries = [
    "South Africa",
    "Nigeria",
    "Kenya",
    "Ethiopia",
    "Ghana",
    "Uganda",
  ];
  const middleEastCountries = [
    "Saudi Arabia",
    "UAE",
    "Israel",
    "Turkey",
    "Iran",
    "Qatar",
  ];
  const oceaniaCountries = [
    "Australia",
    "New Zealand",
    "Fiji",
    "Papua New Guinea",
  ];

  if (asiaCountries.includes(country)) return "Asia";
  if (europeCountries.includes(country)) return "Europe";
  if (americasCountries.includes(country)) return "Americas";
  if (africaCountries.includes(country)) return "Africa";
  if (middleEastCountries.includes(country)) return "Middle East";
  if (oceaniaCountries.includes(country)) return "Oceania";
  return "Other";
};
