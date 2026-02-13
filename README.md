# 📊 Autonomous BI Suite Pro - Universal Edition

An executive-ready business intelligence dashboard that works with **ANY dataset type** - sales, sports, HR, and more!

## 🌟 NEW  - Universal Dataset Support!

### 🎨 **Customizable Colors**
- Choose your own color theme with color pickers
- Quick preset buttons (Purple, Blue, Green, Red)
- All charts and metrics use your custom colors

### 📊 **Works with ANY Dataset**
- ✅ **Sales Data** (Revenue, Customers, Transactions)
- ✅ **Sports Data** (IPL Players, Runs, Wickets, Teams)
- ✅ **HR Data** (Employees, Salary, Departments)
- ✅ **Education Data** (Students, Grades, Courses)
- ✅ **ANY Custom Data** with numeric and categorical columns

### 🔧 **Flexible Column Mapping**
- Manual column selection for Primary Value and Category
- Auto-detection with 20+ common column patterns
- Dataset type selection (auto/sales/sports/hr/generic)
- Dynamic KPI labels based on your data

## 🎉 What's New in Version 2.0

### 🎨 Modern UI Overhaul
- **Dark Mode** - Beautiful light/dark theme toggle
- **Glassmorphism Design** - Frosted glass effect cards and modern styling
- **Animated Gradients** - Dynamic, eye-catching backgrounds
- **Enhanced Metrics** - Hover effects and smooth animations
- **Tabbed Interface** - Organized navigation across 5 sections

### 🚀 Core Features
- 🤖 **AI-Powered Data Processing**: Automatic column normalization using Groq AI
- 📊 **Executive Dashboard**: Enhanced KPI cards with 8+ metrics
- 📈 **Interactive Visualizations**: 8+ chart types with drill-down capability
- 🔄 **Period Comparisons**: Month/Quarter/Year-over-Year analysis
- 💾 **Saved Filters**: Save and reuse filter combinations
- 🚨 **Alert System**: Automated threshold notifications
- 🎲 **Sample Data**: Instant demo with 5,000+ transactions

### 📊 Advanced Analytics Suite
- 📈 **RFM Analysis**: Customer segmentation (Champions, Loyal, At Risk, Lost)
- 💰 **Customer Lifetime Value**: Predictive CLV calculations
- 📅 **Cohort Analysis**: Retention tracking by acquisition cohort
- 🚨 **Anomaly Detection**: Statistical outlier identification (Z-score)
- 🔮 **Revenue Forecasting**: Prophet-based predictions (7-90 days)

### 📤 Export Capabilities
- 📊 **Excel Export**: Multi-sheet workbooks with KPIs and statistics
- 📄 **PDF Reports**: Executive summary documents
- 📥 **CSV Download**: Filtered data export
- 📈 **Forecast Export**: Prediction data download

### 🤖 AI-Powered Insights
- 🎯 **Quick Questions**: Pre-built analysis prompts
- 💡 **Custom Questions**: Ask anything about your data
- 📋 **Structured Insights**: Action plans, root causes, and impact assessments

## 📦 Installation

1. **Clone or download this project**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Groq API (Optional but Recommended):**
   - Copy `.env.example` to `.env`
   - Get your API key from [Groq Console](https://console.groq.com/)
   - Add your key to `.env`:
     ```
     GROQ_API_KEY=your_actual_api_key_here
     ```

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

5. **Access the dashboard:**
   - Opens automatically in your browser
   - Or navigate to: http://localhost:8501

## 🚀 Quick Start

## 🚀 Quick Start

### Option 1: Use Sample Data (Fastest)
1. Launch the app
2. In sidebar, select "Use Sample Data"
3. Click "Load Sample Data"
4. Start exploring immediately with 5,000+ sample transactions

### Option 2: Upload Your Own Data
1. Click "Upload File" in sidebar
2. Upload CSV or Excel file
3. Data will be automatically cleaned and normalized
4. Apply filters and explore

## 💡 Usage Guide

### 📊 Tab 1: Dashboard
- **View KPIs**: Revenue, Growth, AOV, Transactions at the top
- **Period Comparison**: Select Month/Quarter/Year comparison
- **Visualizations**: 4 auto-selected charts based on your data
- **Filters**: Date range and category filters in sidebar

### 🎯 Tab 2: Advanced Analytics

**RFM Analysis:**
- Segment customers by Recency, Frequency, Monetary value
- Identify Champions, Loyal Customers, At Risk, and Lost segments
- View distribution pie chart

**Customer Lifetime Value:**
- Calculate predicted CLV for each customer
- View top customers by lifetime value
- Analyze CLV distribution

**Cohort Analysis:**
- Track retention by acquisition month
- View retention heatmap
- Identify loyalty patterns

**Anomaly Detection:**
- Adjust sensitivity slider (1.0-3.0 sigma)
- Detect unusual revenue patterns
- Investigate spikes and drops

### 🔮 Tab 3: Forecasting
1. Select forecast period (7-90 days)
2. Click "Generate Forecast"
3. View Prophet model predictions with confidence intervals
4. Download forecast data as CSV

### 📊 Tab 4: Reports
- **Excel Report**: Download comprehensive multi-sheet workbook
- **PDF Summary**: Generate executive summary document
- **CSV Export**: Download filtered data

### 🤖 Tab 5: AI Insights
1. Select a quick question or enter custom question
2. Click "Generate AI Insights"
3. Review structured recommendations:
   - Key insights
   - Root causes
   - Action plans
   - Expected impact
   - Risk considerations

## 🎨 UI Features

### Dark Mode
- Toggle in sidebar control panel
- Smooth theme transitions
- Optimized for both light and dark viewing

### Metric Cards
- Gradient backgrounds
- Hover animations
- Delta indicators
- Icon labels

### Alerts
- Success: Growth exceeding 50%
- Warning: Revenue below threshold
- Error: Declining revenue >10%

### Saved Filters
1. Apply desired filters
2. Enter filter name
3. Click "Save Current Filters"
4. Load anytime from dropdown

## 📋 Data Requirements

### Minimum Required
- At least 2 columns
- Preferably includes:
  - Date/timestamp column
  - Amount/revenue column
  - Category column (optional)
  - Customer ID (optional)

### Optimal Dataset
For full feature functionality:
- **Date Column**: Transaction dates
- **Revenue Column**: Sales amounts
- **Customer Column**: Customer identifiers
- **Category Column**: Product/service categories
- **Quantity Column**: Units sold (optional)

### Supported Formats
- CSV (.csv)
- Excel (.xlsx, .xls)

## 🔧 Advanced Features

### AI Column Normalization
When Groq API is configured:
- Automatically renames columns to business-friendly terms
- Detects column purposes from sample data
- Converts abbreviations to full terms

### Automatic Data Cleaning
- Removes duplicate rows
- Handles missing values intelligently:
  - Numeric: Median imputation
  - Dates: Forward fill
  - Categorical: Mode or 'Unknown'
- Detects and converts date formats
- Identifies numeric columns in text format

### Smart Visualization
Algorithm selects best 2 charts based on:
- Available column types
- Data characteristics
- Business relevance

Priority order:
1. Time series (if dates available)
2. Category breakdown (if categories available)
3. Distribution analysis (if numeric data)
4. Top performers
5. Correlations

## 📊 Analytics Explained

### RFM Scoring
- **Recency (R)**: Days since last purchase (1-5, 5 = recent)
- **Frequency (F)**: Number of purchases (1-5, 5 = frequent)
- **Monetary (M)**: Total spend (1-5, 5 = high value)
- **RFM Score**: Combination like "555" = Champion

### CLV Calculation
```
CLV = Avg Order Value × Purchase Rate × Customer Lifespan (months)
```

### Anomaly Detection
Uses Z-score statistical method:
```
Z-score = (Value - Mean) / Standard Deviation
```
Flags points where |Z| > threshold (default: 2.0)

### Forecasting
**Prophet Model** (preferred):
- Additive/multiplicative seasonality
- Trend changepoint detection
- Holiday effects (configurable)
- Confidence intervals

**Fallback**: 7-day moving average projection

## 🆘 Troubleshooting

### "Prophet Not Available"
```bash
pip install prophet
```

### "PDF Export Requires ReportLab"
```bash
pip install reportlab
```

### AI Features Not Working
- Check `.env` file exists and has valid `GROQ_API_KEY`
- Verify API key at https://console.groq.com
- Check internet connection

### Slow Performance
- Apply date/category filters to reduce data size
- Use sample data for testing
- Close other browser tabs
- Increase Streamlit server resources

### Charts Not Appearing
- Verify data has required columns
- Check for all-null columns
- Try sample data to verify installation

## 📚 Additional Resources

- **Full Features Guide**: See `FEATURES_GUIDE.md`
- **Groq API Docs**: https://console.groq.com/docs
- **Streamlit Docs**: https://docs.streamlit.io
- **Prophet Docs**: https://facebook.github.io/prophet/

## 🎯 Use Cases

### E-commerce
- Track daily revenue trends
- Identify top products
- Segment customers by value
- Forecast holiday sales

### SaaS
- Monitor MRR/ARR
- Calculate customer LTV
- Track cohort retention
- Predict churn

### Retail
- Analyze store performance
- Identify seasonal patterns
- Optimize inventory with forecasts
- Target high-value customers

### Marketing
- Measure campaign ROI
- Segment audience by engagement
- Predict future conversions
- Allocate budget to best channels

## 🔐 Security & Privacy

- All data processing happens locally
- No data stored on external servers
- API calls use encrypted HTTPS
- Optional API usage (works offline without AI features)

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Visualizations**: Plotly
- **Data Processing**: Pandas, NumPy
- **Analytics**: Scikit-learn, SciPy
- **Forecasting**: Prophet
- **AI**: Groq LLM (llama-3.3-70b)
- **Export**: ReportLab (PDF), XlsxWriter (Excel)

## 📝 Version History

### Version 2.0 (February 2026)
- ✨ Complete UI overhaul with modern design
- 🎨 Dark mode support
- 📊 Advanced analytics suite (RFM, CLV, Cohort)
- 🔮 Revenue forecasting with Prophet
- 🚨 Anomaly detection
- 📤 Export to Excel/PDF
- 💾 Saved filters
- 🚨 Alert system
- 🎲 Sample data generator
- 🗂️ Tabbed interface

### Version 1.0 (Initial Release)
- Basic KPI dashboard
- AI column normalization
- Simple visualizations
- AI insights

## 🤝 Contributing

Suggestions and improvements welcome!

## 📄 License

MIT License - Free to use and modify

## 👤 Author

Management Analytics Team

---

## 🎊 Get Started Now!

```bash
pip install -r requirements.txt
streamlit run app.py
```

**Explore the future of business intelligence!** 🚀
- **Avg Order Value**: Average transaction size

### 4. Analyze Visualizations
- **Distribution Chart**: Histogram showing value distribution
- **Categorical Chart**: Bar chart comparing categories

### 5. Get AI Insights
- Scroll to "Autonomous Root Cause Analysis"
- Enter a question (e.g., "Why is revenue declining?")
- Click "Generate Insights"
- Review bulleted insights and prescriptive action plan

## Architecture

### Data Pipeline (`process_data`)
- Detects file type (CSV/Excel)
- Removes duplicates automatically
- Normalizes column names using Grok AI
- Auto-detects date columns
- Handles missing values intelligently

### State Management
- Uses `st.session_state` to persist processed data
- Dashboard only re-renders when filters change
- Efficient data handling for large datasets

### AI Integration
- **Column Normalization**: Converts technical names to business terms
- **Prescriptive Insights**: Generates actionable recommendations
- **Root Cause Analysis**: Analyzes patterns and provides specific action plans

## Example Questions for AI Insights

- "What factors are driving high-value transactions?"
- "Why is revenue declining in recent periods?"
- "Which categories show the strongest growth?"
- "What actions should we take to improve performance?"

## Requirements

- Python 3.8+
- Streamlit 1.31+
- Grok API key (from xAI)

## Notes

- The dashboard is designed for management-level presentations
- All insights are prescriptive (actionable) rather than just descriptive
- Modular code structure for easy customization
- Automatic data type detection and handling
