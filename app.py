"""
Autonomous BI Suite - Executive Dashboard with Prescriptive Analytics (Advanced)
Author: Management Analytics Team
Version: 2.0 - Enhanced Edition
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from openai import OpenAI
import os
from typing import Optional, Tuple, Dict, Any, List
import json
from dotenv import load_dotenv
import numpy as np
from io import BytesIO
import base64

# Advanced analytics imports
try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except:
    PROPHET_AVAILABLE = False

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from scipy import stats

# Export imports
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.lib.units import inch
    REPORTLAB_AVAILABLE = True
except:
    REPORTLAB_AVAILABLE = False

import xlsxwriter

# Load environment variables
load_dotenv()

# ============================================================================
# CONFIGURATION & STYLING
# ============================================================================

# Custom CSS for modern UI
def inject_custom_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Custom metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        color: white;
        margin: 0.5rem 0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.3);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        font-weight: 500;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .metric-delta {
        font-size: 1rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }
    
    /* Glassmorphism cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    /* Professional gradient background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Dark mode support */
    [data-theme="dark"] .metric-card {
        background: linear-gradient(135deg, #1e3a8a 0%, #312e81 100%);
    }
    
    /* Button styles */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }2E86DE 0%, #54A0FF
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #e2e8f0;
    }
    
    /* Toast notification */
    .toast {
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        z-index: 9999;
        animation: slideIn 0.3s ease;
    }
    
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 10px 10px 0 0;
        padding: 1rem 2rem;
        font-weight: 600;
        color: #64748b;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #2E86DE 0%, #54A0FF 100%);
        color: white;
    }
    
    /* Chart container */
    .chart-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 1rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    /* Loading animation */
    .stSpinner > div {
        border-top-color: #2E86DE !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(90deg, #2E86DE20 0%, #54A0FF20 100%);
        border-radius: 10px;
        font-weight: 600;
    }
    
    /* Alert boxes */
    .alert-success {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
    }
    
    .alert-warning {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.3);
    }
    
    .alert-info {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1e293b;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #2E86DE 0%, #54A0FF 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #54A0FF 0%, #2E86DE 100%);
    }
    </style>
    """, unsafe_allow_html=True)

st.set_page_config(
    page_title="Autonomous BI Suite Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_custom_css()

# Configure Groq API
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
if GROQ_API_KEY:
    client = OpenAI(
        api_key=GROQ_API_KEY,
        base_url="https://api.groq.com/openai/v1"
    )
else:
    client = None

# ============================================================================
# SAMPLE DATA GENERATION
# ============================================================================

def generate_sample_data() -> pd.DataFrame:
    """Generate sample e-commerce data for demo purposes."""
    np.random.seed(42)
    
    # Generate dates
    date_range = pd.date_range(start='2023-01-01', end='2025-12-31', freq='D')
    n_records = 5000
    
    categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books', 'Toys', 'Food & Beverage']
    regions = ['North America', 'Europe', 'Asia', 'South America', 'Australia']
    customers = [f'Customer_{i:04d}' for i in range(1, 501)]
    products = [f'Product_{cat}_{i:03d}' for cat in categories for i in range(1, 21)]
    
    data = {
        'Transaction Date': np.random.choice(date_range, n_records),
        'Customer ID': np.random.choice(customers, n_records),
        'Product Name': np.random.choice(products, n_records),
        'Category': np.random.choice(categories, n_records),
        'Region': np.random.choice(regions, n_records),
        'Quantity': np.random.randint(1, 10, n_records),
        'Unit Price': np.random.uniform(10, 500, n_records).round(2),
    }
    
    df = pd.DataFrame(data)
    df['Revenue'] = (df['Quantity'] * df['Unit Price']).round(2)
    df['Cost'] = (df['Revenue'] * np.random.uniform(0.4, 0.7, n_records)).round(2)
    df['Profit'] = (df['Revenue'] - df['Cost']).round(2)
    
    return df.sort_values('Transaction Date').reset_index(drop=True)

# ============================================================================
# DATA PROCESSING PIPELINE (Enhanced)
# ============================================================================

def process_data(uploaded_file) -> pd.DataFrame:
    """Process uploaded data with AI-powered normalization."""
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file format. Please upload CSV or Excel files.")
            return None
        
        df = handle_duplicate_columns(df)
        original_rows = len(df)
        df = df.drop_duplicates()
        duplicates_removed = original_rows - len(df)
        
        if GROQ_API_KEY:
            df = normalize_columns_with_ai(df)
        else:
            df.columns = [col.strip().title().replace('_', ' ') for col in df.columns]
        
        df = auto_detect_dates(df)
        df = handle_missing_values(df)
        
        if duplicates_removed > 0:
            show_toast(f"✓ Removed {duplicates_removed} duplicate rows", "success")
        
        return df
        
    except Exception as e:
        st.error(f"Error processing data: {str(e)}")
        return None

def normalize_columns_with_ai(df: pd.DataFrame) -> pd.DataFrame:
    """Use AI to normalize column names to professional business terms."""
    try:
        column_info = []
        for col in df.columns:
            dtype = str(df[col].dtype)
            sample = df[col].dropna().head(3).tolist()
            column_info.append(f"{col} ({dtype}) - samples: {sample}")
        
        prompt = f"""You are a data normalization expert. Given these DataFrame columns, suggest professional business-friendly names.

Current columns:
{chr(10).join(column_info)}

CRITICAL RULES:
1. Use Title Case (e.g., "Transaction Amount", "Customer ID")
2. Replace abbreviations with full terms (e.g., txn -> Transaction, amt -> Amount)
3. Make names executive-ready and self-explanatory
4. Keep names concise but clear
5. **ENSURE ALL NEW NAMES ARE UNIQUE** - If columns have similar meanings, add distinguishing qualifiers

Return ONLY a JSON object mapping old names to new names:
{{"old_name": "New Name", ...}}"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a data normalization expert. Always respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        response_text = response.choices[0].message.content.strip()
        if response_text.startswith('```json'):
            response_text = response_text.split('```json')[1].split('```')[0]
        elif response_text.startswith('```'):
            response_text = response_text.split('```')[1].split('```')[0]
        
        mapping = json.loads(response_text.strip())
        
        new_names = list(mapping.values())
        if len(new_names) != len(set(new_names)):
            seen = {}
            for old_name, new_name in mapping.items():
                if new_name in seen.values():
                    counter = 2
                    base_name = new_name
                    while new_name in seen.values():
                        new_name = f"{base_name} {counter}"
                        counter += 1
                mapping[old_name] = new_name
                seen[old_name] = new_name
        
        df = df.rename(columns=mapping)
        df = handle_duplicate_columns(df)
        
        show_toast("✓ Column names normalized using AI", "success")
        
    except Exception as e:
        st.warning(f"⚠️ AI normalization failed: {str(e)[:100]}")
        df.columns = [col.strip().title().replace('_', ' ') for col in df.columns]
        df = handle_duplicate_columns(df)
    
    return df

def handle_duplicate_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure all column names are unique by appending numbers to duplicates."""
    cols = pd.Series(df.columns)
    for dup in cols[cols.duplicated()].unique():
        dup_positions = [i for i, col in enumerate(df.columns) if col == dup]
        for idx, pos in enumerate(dup_positions[1:], start=2):
            df.columns.values[pos] = f"{dup} {idx}"
    return df

def auto_detect_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Auto-detect and convert date columns."""
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                parsed = pd.to_datetime(df[col], errors='coerce')
                if parsed.notna().sum() / len(df) > 0.5:
                    df[col] = parsed
            except:
                pass
    return df

def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Intelligently handle missing values based on column type."""
    for col in df.columns:
        if df[col].isnull().any():
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(df[col].median())
            elif pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].fillna(method='ffill')
            else:
                mode_val = df[col].mode()
                if len(mode_val) > 0:
                    df[col] = df[col].fillna(mode_val[0])
                else:
                    df[col] = df[col].fillna('Unknown')
    
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                numeric_converted = pd.to_numeric(df[col], errors='coerce')
                if numeric_converted.notna().sum() / len(df) > 0.8:
                    df[col] = numeric_converted
            except:
                pass
    
    return df

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def show_toast(message: str, type: str = "info"):
    """Display a toast notification."""
    color_map = {
        "success": "#10b981",
        "error": "#ef4444",
        "warning": "#f59e0b",
        "info": "#3b82f6"
    }
    color = color_map.get(type, "#3b82f6")
    
    st.markdown(f"""
    <div class="toast" style="background: {color};">
        {message}
    </div>
    <script>
        setTimeout(function() {{
            document.querySelector('.toast').style.opacity = '0';
            setTimeout(function() {{
                document.querySelector('.toast').remove();
            }}, 300);
        }}, 3000);
    </script>
    """, unsafe_allow_html=True)

def detect_column_type(df: pd.DataFrame, keywords: list) -> Optional[str]:
    """Detect column by keyword matching and validate data type."""
    candidates = []
    for col in df.columns:
        col_lower = col.lower()
        if any(keyword in col_lower for keyword in keywords):
            candidates.append(col)
    
    if keywords and any(k in ['revenue', 'amount', 'sales', 'price', 'value', 'total', 'profit'] for k in keywords):
        numeric_candidates = [c for c in candidates if pd.api.types.is_numeric_dtype(df[c])]
        if numeric_candidates:
            return numeric_candidates[0]
    
    return candidates[0] if candidates else None

# ============================================================================
# KPI CALCULATION FUNCTIONS (Enhanced)
# ============================================================================

def calculate_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate KPIs from the dataframe - works with any dataset type."""
    kpis = {
        'total_value': 0,
        'avg_value': 0,
        'growth_percent': 0,
        'total_profit': 0,
        'profit_margin': 0,
        'total_records': len(df),
        'unique_entities': 0,
        'value_label': 'Value',
        'entity_label': 'Entities'
    }
    
    # Use user-selected column or auto-detect
    if hasattr(st.session_state, 'numeric_col') and st.session_state.numeric_col and st.session_state.numeric_col != 'None':
        value_col = st.session_state.numeric_col
    else:
        value_col = detect_column_type(df, ['revenue', 'amount', 'sales', 'price', 'value', 'total', 'runs', 'score', 'salary', 'rating', 'points', 'goals'])
    
    # Detect entity column (customer, player, employee, etc.)
    entity_col = detect_column_type(df, ['customer', 'client', 'user', 'player', 'employee', 'person', 'name', 'id'])
    
    if value_col and pd.api.types.is_numeric_dtype(df[value_col]):
        try:
            numeric_data = pd.to_numeric(df[value_col], errors='coerce')
            kpis['total_value'] = numeric_data.sum()
            kpis['avg_value'] = numeric_data.mean()
            kpis['value_label'] = value_col
        except:
            pass
    
    # Try to find profit column
    profit_col = detect_column_type(df, ['profit', 'margin', 'earnings', 'wickets', 'assists'])
    if profit_col and pd.api.types.is_numeric_dtype(df[profit_col]):
        try:
            profit_data = pd.to_numeric(df[profit_col], errors='coerce')
            kpis['total_profit'] = profit_data.sum()
            if kpis['total_value'] > 0:
                kpis['profit_margin'] = (kpis['total_profit'] / kpis['total_value']) * 100
        except:
            pass
    
    if entity_col:
        kpis['unique_entities'] = df[entity_col].nunique()
        kpis['entity_label'] = entity_col
    
    # Calculate growth
    date_col = detect_column_type(df, ['date', 'time', 'timestamp', 'created', 'year'])
    if date_col and value_col:
        try:
            # Check if it's already datetime
            if pd.api.types.is_datetime64_any_dtype(df[date_col]):
                df_sorted = df.sort_values(date_col)
            elif pd.api.types.is_numeric_dtype(df[date_col]):
                # If numeric (like year), sort by it
                df_sorted = df.sort_values(date_col)
            else:
                # Try to convert to datetime
                df_sorted = df.copy()
                df_sorted[date_col] = pd.to_datetime(df_sorted[date_col], errors='coerce')
                df_sorted = df_sorted.sort_values(date_col)
            
            mid_point = len(df_sorted) // 2
            numeric_data = pd.to_numeric(df_sorted[value_col], errors='coerce')
            first_half = numeric_data.iloc[:mid_point].sum()
            second_half = numeric_data.iloc[mid_point:].sum()
            
            if first_half > 0:
                kpis['growth_percent'] = ((second_half - first_half) / first_half) * 100
        except:
            pass
    
    return kpis

def calculate_period_comparison(df: pd.DataFrame, period: str = 'month') -> Dict[str, Any]:
    """Calculate period-over-period comparisons (YoY, MoM, etc.)."""
    date_col = detect_column_type(df, ['date', 'time', 'timestamp', 'created'])
    revenue_col = detect_column_type(df, ['revenue', 'amount', 'sales', 'price', 'value', 'total'])
    
    comparison = {
        'current_period': 0,
        'previous_period': 0,
        'change_percent': 0,
        'change_absolute': 0
    }
    
    if not date_col or not revenue_col:
        return comparison
    
    if not pd.api.types.is_datetime64_any_dtype(df[date_col]):
        return comparison
    
    try:
        df_sorted = df.sort_values(date_col)
        max_date = df_sorted[date_col].max()
        
        if period == 'month':
            current_start = max_date - timedelta(days=30)
            previous_start = current_start - timedelta(days=30)
            previous_end = current_start
        elif period == 'quarter':
            current_start = max_date - timedelta(days=90)
            previous_start = current_start - timedelta(days=90)
            previous_end = current_start
        elif period == 'year':
            current_start = max_date - timedelta(days=365)
            previous_start = current_start - timedelta(days=365)
            previous_end = current_start
        else:
            return comparison
        
        current_data = df_sorted[df_sorted[date_col] >= current_start]
        previous_data = df_sorted[(df_sorted[date_col] >= previous_start) & (df_sorted[date_col] < previous_end)]
        
        comparison['current_period'] = pd.to_numeric(current_data[revenue_col], errors='coerce').sum()
        comparison['previous_period'] = pd.to_numeric(previous_data[revenue_col], errors='coerce').sum()
        comparison['change_absolute'] = comparison['current_period'] - comparison['previous_period']
        
        if comparison['previous_period'] > 0:
            comparison['change_percent'] = (comparison['change_absolute'] / comparison['previous_period']) * 100
        
    except:
        pass
    
    return comparison

# ============================================================================
# ADVANCED ANALYTICS FUNCTIONS
# ============================================================================

def detect_anomalies(df: pd.DataFrame, sensitivity: float = 2.0) -> pd.DataFrame:
    """Detect anomalies in revenue/sales data using z-score method."""
    date_col = detect_column_type(df, ['date', 'time', 'timestamp', 'created'])
    revenue_col = detect_column_type(df, ['revenue', 'amount', 'sales', 'price', 'value', 'total'])
    
    if not date_col or not revenue_col:
        return pd.DataFrame()
    
    if not pd.api.types.is_datetime64_any_dtype(df[date_col]):
        return pd.DataFrame()
    
    try:
        daily_revenue = df.groupby(df[date_col].dt.date)[revenue_col].sum().reset_index()
        daily_revenue.columns = ['Date', 'Revenue']
        
        mean_revenue = daily_revenue['Revenue'].mean()
        std_revenue = daily_revenue['Revenue'].std()
        
        daily_revenue['z_score'] = (daily_revenue['Revenue'] - mean_revenue) / std_revenue
        anomalies = daily_revenue[abs(daily_revenue['z_score']) > sensitivity]
        
        return anomalies.sort_values('Date', ascending=False)
    except:
        return pd.DataFrame()

def calculate_rfm(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate RFM (Recency, Frequency, Monetary) analysis."""
    date_col = detect_column_type(df, ['date', 'time', 'timestamp', 'created'])
    customer_col = detect_column_type(df, ['customer', 'client', 'user'])
    revenue_col = detect_column_type(df, ['revenue', 'amount', 'sales', 'price', 'value', 'total'])
    
    if not all([date_col, customer_col, revenue_col]):
        return pd.DataFrame()
    
    if not pd.api.types.is_datetime64_any_dtype(df[date_col]):
        return pd.DataFrame()
    
    try:
        max_date = df[date_col].max()
        
        rfm = df.groupby(customer_col).agg({
            date_col: lambda x: (max_date - x.max()).days,
            customer_col: 'count',
            revenue_col: 'sum'
        })
        
        rfm.columns = ['Recency', 'Frequency', 'Monetary']
        rfm = rfm.reset_index()
        
        rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5,4,3,2,1], duplicates='drop')
        rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1,2,3,4,5], duplicates='drop')
        rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1,2,3,4,5], duplicates='drop')
        
        rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)
        rfm['RFM_Total'] = rfm[['R_Score', 'F_Score', 'M_Score']].astype(int).sum(axis=1)
        
        def segment_customer(row):
            if row['RFM_Total'] >= 13:
                return 'Champions'
            elif row['RFM_Total'] >= 10:
                return 'Loyal Customers'
            elif row['RFM_Total'] >= 7:
                return 'Potential Loyalists'
            elif row['RFM_Total'] >= 5:
                return 'At Risk'
            else:
                return 'Lost'
        
        rfm['Segment'] = rfm.apply(segment_customer, axis=1)
        
        return rfm
    except:
        return pd.DataFrame()

def calculate_customer_lifetime_value(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate Customer Lifetime Value (CLV)."""
    customer_col = detect_column_type(df, ['customer', 'client', 'user'])
    revenue_col = detect_column_type(df, ['revenue', 'amount', 'sales', 'price', 'value', 'total'])
    date_col = detect_column_type(df, ['date', 'time', 'timestamp', 'created'])
    
    if not all([customer_col, revenue_col, date_col]):
        return pd.DataFrame()
    
    try:
        customer_data = df.groupby(customer_col).agg({
            revenue_col: ['sum', 'mean', 'count'],
            date_col: lambda x: (x.max() - x.min()).days
        })
        
        customer_data.columns = ['Total_Revenue', 'Avg_Order_Value', 'Purchase_Frequency', 'Customer_Lifespan_Days']
        customer_data = customer_data.reset_index()
        
        avg_lifespan = customer_data['Customer_Lifespan_Days'].replace(0, 1).mean()
        customer_data['Customer_Lifespan_Days'] = customer_data['Customer_Lifespan_Days'].replace(0, avg_lifespan)
        
        customer_data['Purchase_Rate'] = customer_data['Purchase_Frequency'] / (customer_data['Customer_Lifespan_Days'] / 30)
        customer_data['CLV'] = customer_data['Avg_Order_Value'] * customer_data['Purchase_Rate'] * (customer_data['Customer_Lifespan_Days'] / 30)
        
        customer_data = customer_data.sort_values('CLV', ascending=False)
        
        return customer_data
    except:
        return pd.DataFrame()

def perform_cohort_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Perform cohort analysis based on customer first purchase month."""
    date_col = detect_column_type(df, ['date', 'time', 'timestamp', 'created'])
    customer_col = detect_column_type(df, ['customer', 'client', 'user'])
    
    if not all([date_col, customer_col]):
        return pd.DataFrame()
    
    if not pd.api.types.is_datetime64_any_dtype(df[date_col]):
        return pd.DataFrame()
    
    try:
        df['OrderMonth'] = df[date_col].dt.to_period('M')
        df['CohortMonth'] = df.groupby(customer_col)[date_col].transform('min').dt.to_period('M')
        
        df_cohort = df.groupby(['CohortMonth', 'OrderMonth']).agg({
            customer_col: 'nunique'
        }).reset_index()
        
        df_cohort['Period'] = (df_cohort.OrderMonth - df_cohort.CohortMonth).apply(lambda x: x.n)
        
        cohort_pivot = df_cohort.pivot_table(
            index='CohortMonth',
            columns='Period',
            values=customer_col
        )
        
        cohort_size = cohort_pivot[0]
        retention = cohort_pivot.divide(cohort_size, axis=0) * 100
        
        return retention
    except:
        return pd.DataFrame()

def forecast_revenue(df: pd.DataFrame, periods: int = 30) -> Tuple[pd.DataFrame, go.Figure]:
    """Forecast revenue using Prophet (if available) or simple moving average."""
    date_col = detect_column_type(df, ['date', 'time', 'timestamp', 'created'])
    revenue_col = detect_column_type(df, ['revenue', 'amount', 'sales', 'price', 'value', 'total'])
    
    if not date_col or not revenue_col:
        return pd.DataFrame(), None
    
    if not pd.api.types.is_datetime64_any_dtype(df[date_col]):
        return pd.DataFrame(), None
    
    try:
        daily_revenue = df.groupby(df[date_col].dt.date)[revenue_col].sum().reset_index()
        daily_revenue.columns = ['ds', 'y']
        daily_revenue['ds'] = pd.to_datetime(daily_revenue['ds'])
        
        if PROPHET_AVAILABLE and len(daily_revenue) > 30:
            model = Prophet(daily_seasonality=False, yearly_seasonality=True, weekly_seasonality=True)
            model.fit(daily_revenue)
            
            future = model.make_future_dataframe(periods=periods)
            forecast = model.predict(future)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=daily_revenue['ds'],
                y=daily_revenue['y'],
                mode='lines',
                name='Historical',
                line=dict(color='#667eea', width=2)
            ))
            
            fig.add_trace(go.Scatter(
                x=forecast['ds'],
                y=forecast['yhat'],
                mode='lines',
                name='Forecast',
                line=dict(color='#f59e0b', width=2, dash='dash')
            ))
            
            fig.add_trace(go.Scatter(
                x=forecast['ds'],
                y=forecast['yhat_upper'],
                mode='lines',
                name='Upper Bound',
                line=dict(width=0),
                showlegend=False
            ))
            
            fig.add_trace(go.Scatter(
                x=forecast['ds'],
                y=forecast['yhat_lower'],
                mode='lines',
                name='Lower Bound',
                line=dict(width=0),
                fillcolor='rgba(245, 158, 11, 0.2)',
                fill='tonexty',
                showlegend=False
            ))
            
            fig.update_layout(
                title='Revenue Forecast (Prophet Model)',
                xaxis_title='Date',
                yaxis_title='Revenue',
                hovermode='x unified',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400
            )
            
            return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(periods), fig
        else:
            # Simple moving average forecast
            window = min(7, len(daily_revenue) // 3)
            daily_revenue['MA'] = daily_revenue['y'].rolling(window=window).mean()
            last_ma = daily_revenue['MA'].iloc[-1]
            
            future_dates = pd.date_range(start=daily_revenue['ds'].max() + timedelta(days=1), periods=periods)
            forecast_values = [last_ma] * periods
            
            forecast_df = pd.DataFrame({
                'ds': future_dates,
                'yhat': forecast_values
            })
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=daily_revenue['ds'],
                y=daily_revenue['y'],
                mode='lines',
                name='Historical',
                line=dict(color='#667eea', width=2)
            ))
            
            fig.add_trace(go.Scatter(
                x=forecast_df['ds'],
                y=forecast_df['yhat'],
                mode='lines',
                name='Forecast (Simple MA)',
                line=dict(color='#f59e0b', width=2, dash='dash')
            ))
            
            fig.update_layout(
                title='Revenue Forecast (Moving Average)',
                xaxis_title='Date',
                yaxis_title='Revenue',
                hovermode='x unified',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400
            )
            
            return forecast_df, fig
    except Exception as e:
        st.error(f"Forecast error: {str(e)}")
        return pd.DataFrame(), None

# ============================================================================
# EXPORT FUNCTIONS
# ============================================================================

def export_to_excel(df: pd.DataFrame, kpis: Dict[str, Any]) -> BytesIO:
    """Export dashboard data to Excel with multiple sheets."""
    output = BytesIO()
    
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        workbook = writer.book
        
        # Formats
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#667eea',
            'font_color': 'white',
            'border': 1
        })
        
        kpi_format = workbook.add_format({
            'bold': True,
            'font_size': 14,
            'bg_color': '#f0f0f0'
        })
        
        # KPI Sheet
        kpi_df = pd.DataFrame([kpis])
        kpi_df.to_excel(writer, sheet_name='KPIs', index=False)
        worksheet = writer.sheets['KPIs']
        for col_num, value in enumerate(kpi_df.columns.values):
            worksheet.write(0, col_num, value, header_format)
        
        # Data Sheet
        df.to_excel(writer, sheet_name='Data', index=False)
        worksheet = writer.sheets['Data']
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)
            worksheet.set_column(col_num, col_num, 15)
        
        # Summary Statistics
        summary = df.describe()
        summary.to_excel(writer, sheet_name='Statistics')
        
    output.seek(0)
    return output

def export_to_pdf(df: pd.DataFrame, kpis: Dict[str, Any]) -> BytesIO:
    """Export dashboard summary to PDF."""
    if not REPORTLAB_AVAILABLE:
        return None
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=30,
        alignment=1
    )
    
    # Title
    elements.append(Paragraph("Business Intelligence Report", title_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # KPIs
    elements.append(Paragraph("Key Performance Indicators", styles['Heading2']))
    elements.append(Spacer(1, 0.2*inch))
    
    kpi_data = [
        ['Metric', 'Value'],
        ['Total Revenue', f"${kpis['total_revenue']:,.2f}"],
        ['Growth Rate', f"{kpis['growth_percent']:.1f}%"],
        ['Avg Order Value', f"${kpis['avg_order_value']:,.2f}"],
        ['Total Transactions', f"{kpis['total_transactions']:,}"],
        ['Unique Customers', f"{kpis['unique_customers']:,}"]
    ]
    
    kpi_table = Table(kpi_data, colWidths=[3*inch, 2*inch])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(kpi_table)
    elements.append(Spacer(1, 0.5*inch))
    
    # Data Summary
    elements.append(Paragraph("Data Overview", styles['Heading2']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph(f"Total Records: {len(df)}", styles['Normal']))
    elements.append(Paragraph(f"Date Range: {df.iloc[0]['Transaction Date'] if 'Transaction Date' in df.columns else 'N/A'} to {df.iloc[-1]['Transaction Date'] if 'Transaction Date' in df.columns else 'N/A'}", styles['Normal']))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer

def create_download_link(file_data: BytesIO, filename: str, link_text: str) -> str:
    """Create a download link for file data."""
    b64 = base64.b64encode(file_data.read()).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">{link_text}</a>'

# ============================================================================
# VISUALIZATION FUNCTIONS (Enhanced)
# ============================================================================

def analyze_dataset_structure(df: pd.DataFrame) -> dict:
    """Analyze dataset to determine best visualization strategy."""
    structure = {
        'numeric_cols': df.select_dtypes(include=['float64', 'int64']).columns.tolist(),
        'categorical_cols': df.select_dtypes(include=['object', 'category']).columns.tolist(),
        'datetime_cols': df.select_dtypes(include=['datetime64']).columns.tolist(),
    }
    
    structure['revenue_col'] = detect_column_type(df, ['revenue', 'amount', 'sales', 'price', 'value', 'total'])
    structure['category_col'] = detect_column_type(df, ['category', 'type', 'segment', 'region', 'product'])
    structure['quantity_col'] = detect_column_type(df, ['quantity', 'units', 'qty', 'count'])
    structure['date_col'] = detect_column_type(df, ['date', 'time', 'timestamp', 'order', 'created'])
    structure['name_col'] = detect_column_type(df, ['product', 'name', 'item', 'customer', 'city'])
    
    structure['has_revenue'] = structure['revenue_col'] is not None
    structure['has_category'] = structure['category_col'] is not None
    structure['has_quantity'] = structure['quantity_col'] is not None
    structure['has_date'] = structure['date_col'] is not None and pd.api.types.is_datetime64_any_dtype(df[structure['date_col']])
    structure['has_name'] = structure['name_col'] is not None
    
    return structure

def create_distribution_chart(df: pd.DataFrame) -> go.Figure:
    """Create a Plotly histogram for distribution analysis."""
    # Use user-selected or auto-detected column
    if hasattr(st.session_state, 'numeric_col') and st.session_state.numeric_col and st.session_state.numeric_col != 'None':
        value_col = st.session_state.numeric_col
    else:
        value_col = detect_column_type(df, ['revenue', 'amount', 'sales', 'price', 'value', 'total', 'runs', 'score', 'salary', 'rating', 'points'])
    
    if value_col and pd.api.types.is_numeric_dtype(df[value_col]):
        fig = px.histogram(
            df, 
            x=value_col,
            nbins=30,
            title=f"Distribution of {value_col}",
            labels={value_col: value_col},
            color_discrete_sequence=[st.session_state.primary_color]
        )
        
        fig.update_layout(
            xaxis_title=value_col,
            yaxis_title="Frequency",
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            title_font_size=16,
            height=400
        )
        
        return fig
    return None

def create_categorical_chart(df: pd.DataFrame) -> go.Figure:
    """Create a Plotly bar chart for categorical analysis."""
    # Use user-selected or auto-detected columns
    if hasattr(st.session_state, 'category_col') and st.session_state.category_col and st.session_state.category_col != 'None':
        category_col = st.session_state.category_col
    else:
        category_col = detect_column_type(df, ['category', 'type', 'segment', 'region', 'product', 'department', 'team'])
    
    if hasattr(st.session_state, 'numeric_col') and st.session_state.numeric_col and st.session_state.numeric_col != 'None':
        value_col = st.session_state.numeric_col
    else:
        value_col = detect_column_type(df, ['revenue', 'amount', 'sales', 'price', 'value', 'total', 'runs', 'score', 'salary', 'rating'])
    
    if category_col and value_col and pd.api.types.is_numeric_dtype(df[value_col]):
        grouped = df.groupby(category_col)[value_col].sum().sort_values(ascending=False).head(10)
        
        # Create custom color scale based on user's colors
        import plotly.graph_objects as go
        colors = [st.session_state.primary_color, st.session_state.secondary_color]
        
        fig = px.bar(
            x=grouped.index,
            y=grouped.values,
            title=f"{value_col} by {category_col}",
            labels={'x': category_col, 'y': value_col},
            color=grouped.values,
            color_continuous_scale=[[0, st.session_state.primary_color], [1, st.session_state.secondary_color]]
        )
        
        fig.update_layout(
            xaxis_title=category_col,
            yaxis_title=value_col,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            title_font_size=16,
            height=400
        )
        
        return fig
    return None

def create_time_series_chart(df: pd.DataFrame) -> go.Figure:
    """Create time series trend chart."""
    date_col = detect_column_type(df, ['date', 'time', 'timestamp', 'created', 'order', 'year'])
    
    # Use user-selected or auto-detected column
    if hasattr(st.session_state, 'numeric_col') and st.session_state.numeric_col and st.session_state.numeric_col != 'None':
        value_col = st.session_state.numeric_col
    else:
        value_col = detect_column_type(df, ['revenue', 'amount', 'sales', 'price', 'value', 'total', 'runs', 'score', 'rating'])
    
    if date_col and value_col and pd.api.types.is_datetime64_any_dtype(df[date_col]) and pd.api.types.is_numeric_dtype(df[value_col]):
        time_data = df.groupby(df[date_col].dt.date)[value_col].sum().reset_index()
        time_data.columns = ['Date', value_col]
        
        fig = px.line(
            time_data,
            x='Date',
            y=value_col,
            title=f'{value_col} Trend Over Time',
            markers=True
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            title_font_size=16,
            height=400,
            hovermode='x unified'
        )
        
        fig.update_traces(line_color=st.session_state.primary_color, marker=dict(size=6))
        
        return fig
    return None

def create_top_performers_chart(df: pd.DataFrame) -> go.Figure:
    """Create horizontal bar chart for top performers."""
    # Detect name column
    name_col = detect_column_type(df, ['product', 'name', 'item', 'customer', 'city', 'state', 'player', 'employee', 'team'])
    
    # Use user-selected or auto-detected value column
    if hasattr(st.session_state, 'numeric_col') and st.session_state.numeric_col and st.session_state.numeric_col != 'None':
        value_col = st.session_state.numeric_col
    else:
        value_col = detect_column_type(df, ['revenue', 'amount', 'sales', 'price', 'value', 'total', 'runs', 'score', 'salary', 'rating', 'points'])
    
    if name_col and value_col and pd.api.types.is_numeric_dtype(df[value_col]):
        top_items = df.groupby(name_col)[value_col].sum().sort_values(ascending=True).tail(10)
        
        # Create custom color scale
        colorscale = [[0, st.session_state.primary_color], [1, st.session_state.secondary_color]]
        
        fig = go.Figure(go.Bar(
            x=top_items.values,
            y=top_items.index,
            orientation='h',
            marker=dict(
                color=top_items.values,
                colorscale=colorscale,
                showscale=False
            )
        ))
        
        fig.update_layout(
            title=f'Top 10 {name_col} by {value_col}',
            xaxis_title=value_col,
            yaxis_title=name_col,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            title_font_size=16,
            height=400
        )
        
        return fig
    return None

# ============================================================================
# AI INSIGHTS (Enhanced)
# ============================================================================

def generate_prescriptive_insights(df: pd.DataFrame, user_question: str) -> str:
    """Use AI to generate prescriptive insights and action plans."""
    if not GROQ_API_KEY:
        return "⚠️ Please set GROQ_API_KEY environment variable to enable AI insights."
    
    try:
        summary = f"""
Dataset Overview:
- Total Records: {len(df)}
- Columns: {', '.join(df.columns.tolist())}

Statistical Summary:
{df.describe().to_string()}

Sample Data (first 5 rows):
{df.head().to_string()}
"""
        
        prompt = f"""You are an executive business analyst. Provide CONCISE, CLEAR recommendations for management.

DATA CONTEXT:
{summary}

USER QUESTION:
{user_question}

FORMAT YOUR RESPONSE EXACTLY AS:

**📊 Key Insights:**
• [One clear data point - max 15 words]
• [One clear data point - max 15 words]
• [One clear data point - max 15 words]

**🔍 Root Cause:**
• [Primary driver - max 12 words]
• [Secondary driver - max 12 words]

**🎯 Action Plan:**
1. **[Action Title]:** [Specific step - max 12 words]
2. **[Action Title]:** [Specific step - max 12 words]
3. **[Action Title]:** [Specific step - max 12 words]

**💡 Expected Impact:**
[One sentence on business benefit - max 15 words]

**⚠️ Watch Out For:**
[One risk to monitor - max 12 words]
"""
        
        with st.spinner("🔍 Analyzing data and generating prescriptive insights..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are an executive business analyst providing prescriptive, actionable recommendations."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            return response.choices[0].message.content
        
    except Exception as e:
        return f"⚠️ Error generating insights: {str(e)}"

# ============================================================================
# ALERT SYSTEM
# ============================================================================

def check_alerts(kpis: Dict[str, Any]) -> List[Dict[str, str]]:
    """Check for alert conditions and return alerts."""
    alerts = []
    
    # Value alert (works for revenue, runs, salary, etc.)
    if kpis['total_value'] < 1000 and kpis['total_value'] > 0:
        alerts.append({
            'type': 'warning',
            'title': f'Low {kpis["value_label"]}',
            'message': f"Total {kpis['value_label']} ({kpis['total_value']:,.2f}) is below threshold"
        })
    
    # Growth alert
    if kpis['growth_percent'] < -10:
        alerts.append({
            'type': 'error',
            'title': 'Negative Growth',
            'message': f"{kpis['value_label']} declining by {abs(kpis['growth_percent']):.1f}%"
        })
    elif kpis['growth_percent'] > 50:
        alerts.append({
            'type': 'success',
            'title': 'Exceptional Growth',
            'message': f"{kpis['value_label']} growing by {kpis['growth_percent']:.1f}%"
        })
    
    return alerts

def display_alerts(alerts: List[Dict[str, str]]):
    """Display alert notifications."""
    if not alerts:
        return
    
    for alert in alerts:
        alert_type = alert['type']
        if alert_type == 'success':
            st.success(f"✅ **{alert['title']}:** {alert['message']}")
        elif alert_type == 'warning':
            st.warning(f"⚠️ **{alert['title']}:** {alert['message']}")
        elif alert_type == 'error':
            st.error(f"🚨 **{alert['title']}:** {alert['message']}")
        else:
            st.info(f"ℹ️ **{alert['title']}:** {alert['message']}")

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point."""
    
    # Header with gradient
    st.markdown("""
    <div style="background: linear-gradient(135deg, #2E86DE 0%, #54A0FF 100%); padding: 2rem; border-radius: 15px; margin-bottom: 2rem;">
        <h1 style="color: white; margin: 0; font-size: 2.5rem;">📊 Autonomous BI Suite Pro</h1>
        <p style="color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; font-size: 1.2rem;">Executive Dashboard with Advanced Analytics & AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'processed_df' not in st.session_state:
        st.session_state.processed_df = None
    if 'original_df' not in st.session_state:
        st.session_state.original_df = None
    if 'saved_filters' not in st.session_state:
        st.session_state.saved_filters = {}
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False
    # Fixed professional color scheme
    st.session_state.primary_color = '#2E86DE'  # Professional Blue
    st.session_state.secondary_color = '#54A0FF'  # Light Blue
    if 'dataset_type' not in st.session_state:
        st.session_state.dataset_type = 'auto'
    if 'numeric_col' not in st.session_state:
        st.session_state.numeric_col = None
    if 'category_col' not in st.session_state:
        st.session_state.category_col = None
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h2 style="color: #e2e8f0;">🔧 Control Panel</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Dark mode toggle
        st.session_state.dark_mode = st.checkbox("🌙 Dark Mode", value=st.session_state.dark_mode)
        
        st.markdown("---")
        
        # Data Upload
        st.subheader("📁 Data Source")
        
        data_source = st.radio("Select data source:", ["Upload File", "Use Sample Data"])
        
        if data_source == "Upload File":
            uploaded_file = st.file_uploader(
                "Upload your dataset",
                type=['csv', 'xlsx', 'xls'],
                help="Upload CSV or Excel files"
            )
            
            if uploaded_file is not None:
                if st.session_state.original_df is None or st.button("🔄 Reload Data"):
                    with st.spinner("Processing data..."):
                        df = process_data(uploaded_file)
                        if df is not None:
                            st.session_state.original_df = df
                            st.session_state.processed_df = df
                            st.success("✅ Data loaded successfully!")
        else:
            if st.button("🎲 Load Sample Data") or st.session_state.original_df is None:
                with st.spinner("Generating sample data..."):
                    df = generate_sample_data()
                    st.session_state.original_df = df
                    st.session_state.processed_df = df
                    st.success("✅ Sample data loaded!")
        
        # Filters
        if st.session_state.processed_df is not None:
            st.markdown("---")
            st.subheader("📊 Dataset Configuration")
            
            df = st.session_state.original_df.copy()
            
            # Dataset Type Selection
            st.session_state.dataset_type = st.selectbox(
                "Dataset Type",
                options=['auto', 'sales', 'sports', 'hr', 'generic'],
                help="Select dataset type for optimized analysis"
            )
            
            # Column Mapping
            st.markdown("**Column Mapping** (Optional)")
            st.caption("Map your columns to standard fields for better insights")
            
            all_columns = ['None'] + df.columns.tolist()
            numeric_columns = ['None'] + df.select_dtypes(include=['float64', 'int64']).columns.tolist()
            
            # Primary numeric column
            default_numeric = detect_column_type(df, ['revenue', 'amount', 'sales', 'price', 'value', 'total', 'runs', 'score', 'salary', 'count'])
            numeric_idx = numeric_columns.index(default_numeric) if default_numeric in numeric_columns else 0
            st.session_state.numeric_col = st.selectbox(
                "Primary Value Column",
                options=numeric_columns,
                index=numeric_idx,
                help="Main numeric column for analysis (e.g., Revenue, Runs, Salary)"
            )
            
            # Category column
            default_category = detect_column_type(df, ['category', 'type', 'segment', 'region', 'product', 'team', 'department'])
            category_idx = all_columns.index(default_category) if default_category in all_columns else 0
            st.session_state.category_col = st.selectbox(
                "Category Column",
                options=all_columns,
                index=category_idx,
                help="Column for grouping (e.g., Category, Team, Department)"
            )
            
            st.markdown("---")
            st.subheader("🎛️ Global Filters")
            
            df = st.session_state.original_df.copy()
            
            # Date Range Filter
            date_col = detect_column_type(df, ['date', 'time', 'timestamp', 'created'])
            if date_col and pd.api.types.is_datetime64_any_dtype(df[date_col]):
                min_date = df[date_col].min().date()
                max_date = df[date_col].max().date()
                
                date_range = st.date_input(
                    "Date Range",
                    value=(min_date, max_date),
                    min_value=min_date,
                    max_value=max_date
                )
                
                if len(date_range) == 2:
                    df = df[(df[date_col].dt.date >= date_range[0]) & 
                           (df[date_col].dt.date <= date_range[1])]
            
            # Category Filter
            category_col = st.session_state.category_col if st.session_state.category_col != 'None' else detect_column_type(df, ['category', 'type', 'segment', 'region', 'product', 'department', 'team'])
            if category_col:
                categories = ['All'] + sorted(df[category_col].unique().tolist())
                selected_category = st.selectbox("Category Filter", categories)
                
                if selected_category != 'All':
                    df = df[df[category_col] == selected_category]
            
            st.session_state.processed_df = df
            
            st.markdown("---")
            st.metric("📊 Filtered Records", f"{len(df):,}")
            
            # Save/Load Filters
            st.markdown("---")
            st.subheader("💾 Saved Filters")
            
            filter_name = st.text_input("Filter Name", key="filter_name")
            if st.button("Save Current Filters"):
                if filter_name:
                    st.session_state.saved_filters[filter_name] = {
                        'date_range': date_range if date_col else None,
                        'category': selected_category if category_col else None
                    }
                    show_toast(f"Filter '{filter_name}' saved!", "success")
            
            if st.session_state.saved_filters:
                saved_filter = st.selectbox("Load Saved Filter", ['None'] + list(st.session_state.saved_filters.keys()))
                if saved_filter != 'None' and st.button("Load Filter"):
                    show_toast(f"Filter '{saved_filter}' loaded!", "info")
    
    # Main Content
    if st.session_state.processed_df is not None:
        df = st.session_state.processed_df
        
        # Tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📈 Dashboard",
            "🎯 Advanced Analytics",
            "🔮 Forecasting",
            "📊 Reports",
            "🤖 AI Insights"
        ])
        
        # Tab 1: Dashboard
        with tab1:
            # KPIs
            st.subheader("📈 Key Performance Indicators")
            kpis = calculate_kpis(df)
            
            # Check and display alerts
            alerts = check_alerts(kpis)
            if alerts:
                display_alerts(alerts)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, {st.session_state.primary_color} 0%, {st.session_state.secondary_color} 100%);">
                    <div class="metric-label">Total {kpis['value_label']}</div>
                    <div class="metric-value">{kpis['total_value']:,.2f}</div>
                    <div class="metric-delta">💰 Primary KPI</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                delta_color = "🟢" if kpis['growth_percent'] > 0 else "🔴"
                # Create lighter version for second gradient
                import colorsys
                def adjust_color_lightness(hex_color, factor=1.2):
                    hex_color = hex_color.lstrip('#')
                    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
                    h, l, s = colorsys.rgb_to_hls(rgb[0]/255., rgb[1]/255., rgb[2]/255.)
                    l = min(1, l * factor)
                    s = min(1, s * factor)
                    rgb = colorsys.hls_to_rgb(h, l, s)
                    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
                
                color2_start = adjust_color_lightness(st.session_state.primary_color, 0.8)
                color2_end = adjust_color_lightness(st.session_state.secondary_color, 0.9)
                
                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, {color2_start} 0%, {color2_end} 100%);">
                    <div class="metric-label">Growth Rate</div>
                    <div class="metric-value">{kpis['growth_percent']:.1f}%</div>
                    <div class="metric-delta">{delta_color} Period Growth</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, {adjust_color_lightness(st.session_state.primary_color, 1.1)} 0%, {adjust_color_lightness(st.session_state.secondary_color, 1.2)} 100%);">
                    <div class="metric-label">Avg {kpis['value_label']}</div>
                    <div class="metric-value">{kpis['avg_value']:,.2f}</div>
                    <div class="metric-delta">📊 Per Record</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, {adjust_color_lightness(st.session_state.primary_color, 0.9)} 0%, {adjust_color_lightness(st.session_state.secondary_color, 1.1)} 100%);">
                    <div class="metric-label">Total Records</div>
                    <div class="metric-value">{kpis['total_records']:,}</div>
                    <div class="metric-delta">📋 Count</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Period Comparison
            st.subheader("📊 Period Comparison")
            comparison_period = st.select_slider(
                "Compare to:",
                options=['month', 'quarter', 'year'],
                value='month'
            )
            
            comparison = calculate_period_comparison(df, comparison_period)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(
                    f"Current {comparison_period.title()}",
                    f"${comparison['current_period']:,.2f}"
                )
            with col2:
                st.metric(
                    f"Previous {comparison_period.title()}",
                    f"${comparison['previous_period']:,.2f}"
                )
            with col3:
                st.metric(
                    "Change",
                    f"${comparison['change_absolute']:,.2f}",
                    f"{comparison['change_percent']:.1f}%"
                )
            
            st.markdown("---")
            
            # Charts
            st.subheader("📊 Visual Analytics")
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = create_time_series_chart(df)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = create_categorical_chart(df)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = create_distribution_chart(df)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = create_top_performers_chart(df)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
        
        # Tab 2: Advanced Analytics
        with tab2:
            st.subheader("🎯 Advanced Analytics")
            
            analytics_type = st.selectbox(
                "Select Analysis Type:",
                ["RFM Analysis", "Customer Lifetime Value", "Cohort Analysis", "Anomaly Detection"]
            )
            
            if analytics_type == "RFM Analysis":
                st.markdown("### 📊 RFM (Recency, Frequency, Monetary) Analysis")
                rfm_df = calculate_rfm(df)
                
                if not rfm_df.empty:
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.dataframe(rfm_df.head(20), use_container_width=True)
                    
                    with col2:
                        segment_counts = rfm_df['Segment'].value_counts()
                        fig = px.pie(
                            values=segment_counts.values,
                            names=segment_counts.index,
                            title='Customer Segments',
                            hole=0.4,
                            color_discrete_sequence=px.colors.qualitative.Set3
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    st.markdown("#### 💡 Insights:")
                    st.markdown(f"""
                    - **Champions**: {len(rfm_df[rfm_df['Segment']=='Champions'])} customers (highest value)
                    - **At Risk**: {len(rfm_df[rfm_df['Segment']=='At Risk'])} customers (need attention)
                    - **Lost**: {len(rfm_df[rfm_df['Segment']=='Lost'])} customers (win-back campaigns)
                    """)
                else:
                    st.info("RFM analysis requires customer and transaction data.")
            
            elif analytics_type == "Customer Lifetime Value":
                st.markdown("### 💰 Customer Lifetime Value Analysis")
                clv_df = calculate_customer_lifetime_value(df)
                
                if not clv_df.empty:
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.dataframe(clv_df.head(20), use_container_width=True)
                    
                    with col2:
                        avg_clv = clv_df['CLV'].mean()
                        top_clv = clv_df['CLV'].max()
                        
                        st.metric("Average CLV", f"${avg_clv:,.2f}")
                        st.metric("Top Customer CLV", f"${top_clv:,.2f}")
                        
                        fig = px.histogram(
                            clv_df,
                            x='CLV',
                            nbins=30,
                            title='CLV Distribution',
                            color_discrete_sequence=['#667eea']
                        )
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("CLV analysis requires customer and transaction data.")
            
            elif analytics_type == "Cohort Analysis":
                st.markdown("### 📅 Cohort Retention Analysis")
                cohort_df = perform_cohort_analysis(df)
                
                if not cohort_df.empty:
                    fig = px.imshow(
                        cohort_df,
                        title='Cohort Retention Heatmap (%)',
                        labels=dict(x="Period", y="Cohort", color="Retention %"),
                        color_continuous_scale='RdYlGn',
                        aspect='auto'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.markdown("#### 💡 How to Read:")
                    st.markdown("""
                    - **Rows**: Customer acquisition cohorts (by month)
                    - **Columns**: Periods after acquisition
                    - **Colors**: Green = high retention, Red = low retention
                    """)
                else:
                    st.info("Cohort analysis requires customer and transaction date data.")
            
            elif analytics_type == "Anomaly Detection":
                st.markdown("### 🚨 Anomaly Detection")
                
                sensitivity = st.slider("Sensitivity (Z-Score)", 1.0, 3.0, 2.0, 0.5)
                anomalies_df = detect_anomalies(df, sensitivity)
                
                if not anomalies_df.empty:
                    st.markdown(f"**Found {len(anomalies_df)} anomalies**")
                    
                    fig = px.scatter(
                        anomalies_df,
                        x='Date',
                        y='Revenue',
                        size=abs(anomalies_df['z_score']),
                        color='z_score',
                        title='Revenue Anomalies',
                        color_continuous_scale='RdYlGn',
                        color_continuous_midpoint=0
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.dataframe(anomalies_df, use_container_width=True)
                else:
                    st.success("✅ No significant anomalies detected!")
        
        # Tab 3: Forecasting
        with tab3:
            st.subheader("🔮 Revenue Forecasting")
            
            forecast_days = st.slider("Forecast Period (days)", 7, 90, 30)
            
            if st.button("🚀 Generate Forecast", type="primary"):
                with st.spinner("Building forecast model..."):
                    forecast_df, forecast_fig = forecast_revenue(df, forecast_days)
                    
                    if forecast_fig:
                        st.plotly_chart(forecast_fig, use_container_width=True)
                        
                        if not forecast_df.empty:
                            st.markdown("### 📊 Forecast Data")
                            st.dataframe(forecast_df, use_container_width=True)
                            
                            # Download forecast
                            csv = forecast_df.to_csv(index=False)
                            st.download_button(
                                label="📥 Download Forecast CSV",
                                data=csv,
                                file_name=f"forecast_{datetime.now().strftime('%Y%m%d')}.csv",
                                mime="text/csv"
                            )
                    else:
                        st.error("Unable to generate forecast. Check data quality.")
        
        # Tab 4: Reports
        with tab4:
            st.subheader("📊 Export Reports")
            
            st.markdown("### 📥 Download Options")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Excel Report")
                st.markdown("Comprehensive report with KPIs, data, and statistics")
                
                if st.button("📊 Generate Excel Report", key="excel"):
                    with st.spinner("Generating Excel report..."):
                        kpis = calculate_kpis(df)
                        excel_file = export_to_excel(df, kpis)
                        
                        st.download_button(
                            label="📥 Download Excel",
                            data=excel_file,
                            file_name=f"bi_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                        show_toast("Excel report generated!", "success")
            
            with col2:
                st.markdown("#### PDF Summary")
                st.markdown("Executive summary with key metrics")
                
                if REPORTLAB_AVAILABLE:
                    if st.button("📄 Generate PDF Report", key="pdf"):
                        with st.spinner("Generating PDF report..."):
                            kpis = calculate_kpis(df)
                            pdf_file = export_to_pdf(df, kpis)
                            
                            if pdf_file:
                                st.download_button(
                                    label="📥 Download PDF",
                                    data=pdf_file,
                                    file_name=f"bi_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                                    mime="application/pdf"
                                )
                                show_toast("PDF report generated!", "success")
                else:
                    st.warning("PDF export requires reportlab package")
            
            st.markdown("---")
            
            st.markdown("### 📋 Data Export")
            
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download Filtered Data (CSV)",
                data=csv,
                file_name=f"filtered_data_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        # Tab 5: AI Insights
        with tab5:
            st.subheader("🤖 AI-Powered Insights")
            
            st.markdown("""
            <div class="glass-card">
                <h3>💡 Ask Questions About Your Data</h3>
                <p>Get AI-powered prescriptive recommendations and actionable insights.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Quick Questions
            st.markdown("#### 🎯 Quick Questions")
            quick_questions = [
                "Why is revenue declining in certain categories?",
                "What factors drive high-value transactions?",
                "Which customer segments should we focus on?",
                "How can we improve profit margins?",
                "What are the key growth opportunities?"
            ]
            
            quick_question = st.selectbox("Select a quick question:", ["Custom Question..."] + quick_questions)
            
            if quick_question == "Custom Question...":
                user_question = st.text_area(
                    "Or ask your own question:",
                    placeholder="e.g., Why is revenue declining in Q4? What factors contribute to customer churn?",
                    height=100
                )
            else:
                user_question = quick_question
                st.info(f"Selected: {user_question}")
            
            if st.button("🔍 Generate AI Insights", type="primary", key="ai_insights"):
                if user_question and user_question != "Custom Question...":
                    insights = generate_prescriptive_insights(df, user_question)
                    
                    st.markdown("---")
                    st.markdown("### 💡 AI-Generated Insights")
                    st.markdown(f"""
                    <div class="glass-card">
                        {insights}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning("Please enter a question first.")
            
            # Data Preview
            with st.expander("📋 View Current Data"):
                st.dataframe(df, use_container_width=True)
    
    else:
        # Welcome Screen
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 3rem;">
            <h2>👋 Welcome to Autonomous BI Suite Pro</h2>
            <p style="font-size: 1.2rem; margin-top: 1rem;">
                Your comprehensive business intelligence platform with AI-powered analytics
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="glass-card">
                <h3>🚀 Core Features</h3>
                <ul>
                    <li>🤖 AI-Powered Data Processing</li>
                    <li>📊 Dynamic KPI Dashboard</li>
                    <li>📈 Interactive Visualizations</li>
                    <li>🔄 Period Comparisons (YoY, MoM)</li>
                    <li>🎯 Prescriptive Analytics</li>
                    <li>💾 Saved Filter Presets</li>
                    <li>🚨 Automated Alerts</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="glass-card">
                <h3>🎯 Advanced Analytics</h3>
                <ul>
                    <li>📊 RFM Customer Segmentation</li>
                    <li>💰 Customer Lifetime Value</li>
                    <li>📅 Cohort Analysis</li>
                    <li>🚨 Anomaly Detection</li>
                    <li>🔮 Revenue Forecasting</li>
                    <li>📄 PDF/Excel Export</li>
                    <li>🤖 AI-Powered Insights</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="glass-card" style="margin-top: 2rem;">
            <h3>🎬 Getting Started</h3>
            <ol style="font-size: 1.1rem; line-height: 2;">
                <li><strong>Upload Data</strong> or use sample data from the sidebar</li>
                <li><strong>Apply Filters</strong> to focus on specific segments</li>
                <li><strong>Explore Tabs</strong> for different analytics views</li>
                <li><strong>Ask AI</strong> questions to get prescriptive insights</li>
                <li><strong>Export Reports</strong> in Excel or PDF format</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
