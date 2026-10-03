# VERIDEX Frontend

Professional SaaS Market Research Intelligence Platform - Streamlit Frontend

## Overview

VERIDEX Frontend is a Streamlit-based web application for tracking, analyzing, and understanding the competitive landscape in the SaaS market.

## Features

- **Competitor Tracking** - Add and manage SaaS products you want to monitor
- **Pricing Intelligence** - Track pricing strategies and identify market trends
- **Sentiment Analysis** - Monitor customer reviews and satisfaction
- **Price History** - Analyze pricing trends over time
- **Professional Dashboard** - View key metrics and insights at a glance

## Project Structure

frontend/
├── config/ # Configuration and constants
│ ├── theme.py # Design system (colors, typography, spacing)
│ ├── settings.py # App settings and configuration
│ ├── constants.py # Constants and enums
│ └── init.py
├── utils/ # Utility modules
│ ├── api_client.py # Backend API client with caching
│ ├── formatting.py # Data formatting helpers
│ ├── cache.py # Session and local storage
│ ├── validators.py # Input validation
│ ├── helpers.py # Various helpers
│ └── init.py
├── components/ # Reusable UI components
│ ├── cards.py # Metric, stat, info cards
│ ├── tables.py # Data table components
│ ├── charts.py # Chart components
│ ├── forms.py # Form input components
│ ├── notifications.py # Alert/notification components
│ ├── modals.py # Modal/dialog components
│ ├── navbar.py # Top navigation bar
│ ├── sidebar.py # Sidebar navigation
│ └── init.py
├── pages/ # Streamlit pages
│ ├── 01_Dashboard.py # Overview dashboard
│ ├── 02_Competitors.py # Competitor management
│ ├── 03_Pricing_Analysis.py # Pricing tracking
│ ├── 04_Sentiment_Analysis.py # Review monitoring
│ └── 05_Price_History.py # Price trends
├── assets/ # Static assets
│ ├── images/ # Image files
│ └── css/ # CSS files (if needed)
├── .streamlit/
│ └── config.toml # Streamlit configuration
├── streamlit_app.py # Main application entry point
├── requirements.txt # Python dependencies
└── README.md # This file


## Installation

### Prerequisites

- Python 3.8+
- pip or conda
- VERIDEX Backend running (see backend README)

### Setup

1. **Clone the repository**
```bash
   git clone https://github.com/veridex/frontend.git
   cd frontend
```

2. **Create virtual environment**
```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
   pip install -r requirements.txt
```

4. **Configure environment**
```bash
   cp .env.example .env
   # Edit .env with your settings
```

5. **Run the application**
```bash
   streamlit run streamlit_app.py
```

The application will be available at `http://localhost:8501`

## Configuration

### Environment Variables

Create a `.env` file in the frontend directory:

```env
# API Configuration
API_BASE_URL=http://localhost:8000
API_TIMEOUT=30

# App Configuration
APP_NAME=VERIDEX
APP_ENVIRONMENT=development
LOG_LEVEL=INFO

# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost
STREAMLIT_CLIENT_SHOW_ERROR_DETAILS=true
```

### Theme Configuration

Edit `config/theme.py` to customize colors, typography, and spacing.

## Usage

### Pages

1. **Dashboard** - Overview of all data with key metrics
2. **Competitors** - Add, edit, and manage competitors
3. **Pricing Analysis** - Track and analyze competitor pricing
4. **Sentiment Analysis** - Monitor customer reviews and sentiment
5. **Price History** - Analyze pricing changes over time

### Common Tasks

#### Adding a Competitor

1. Navigate to "Competitors" page
2. Click "Add Competitor"
3. Fill in competitor details
4. Click "Add Competitor"

#### Tracking Pricing

1. Navigate to "Pricing Analysis"
2. Click "Add Pricing Tier"
3. Select competitor and enter pricing information
4. Click "Add Pricing Tier"

#### Monitoring Reviews

1. Navigate to "Sentiment Analysis"
2. Click "Add Review"
3. Enter review details and sentiment
4. Click "Add Review"

## Architecture

### Component Structure

- **Pages**: Streamlit page files with complete page logic
- **Components**: Reusable UI building blocks (cards, tables, charts, etc.)
- **Utils**: Helper functions for API communication, data formatting, validation, etc.
- **Config**: Application configuration, constants, and design system

### Data Flow

User Input → Streamlit Page → API Client → Backend API → Database
↓
Components & Utilities


### Caching Strategy

- Session state for current session data
- Local JSON cache for persistent data
- API client with built-in caching
- Streamlit's @st.cache_data for expensive operations

## Development

### Adding a New Page

1. Create file in `pages/` with naming convention: `NN_PageName.py`
2. Import required utilities and components
3. Configure page settings with `st.set_page_config()`
4. Implement main() function
5. Add to sidebar navigation (components/sidebar.py)

### Adding a New Component

1. Create file in `components/` with descriptive name
2. Implement component function with docstring
3. Export in `components/__init__.py`
4. Use in pages or other components

### Styling

- Use `Colors` class from `config/theme.py` for consistent colors
- Use `Typography` class for fonts and sizes
- Use `Spacing` class for margins and padding
- Inline Markdown with HTML for custom styling

### API Integration

Use `api_client` from `utils/api_client.py`:

```python
from utils import api_client

# Get competitors
competitors = api_client.get_all_competitors()

# Create pricing
api_client.create_pricing(data)

# Update review
api_client.update_review(review_id, data)
```

## Performance

- Frontend uses Streamlit's caching mechanisms
- API client implements request caching
- Large datasets paginated (limit=1000)
- Charts rendered with Plotly for interactivity

## Troubleshooting

### API Connection Failed

Error: API Disconnected


**Solution**: Verify backend is running on configured URL in `.env`

### Slow Page Load

**Solution**: Check API response times, reduce data limit, enable caching

### Form Validation Errors

**Solution**: Check `utils/validators.py` for validation rules

## Browser Compatibility

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers supported

## Security

- HTTPS recommended for production
- Authentication via backend API
- CSRF protection enabled
- XSS protection in all outputs
- No sensitive data in session state

## License

Enterprise License - See LICENSE file

## Support

- Documentation: [https://veridex.io/docs](https://veridex.io/docs)
- Issues: [https://github.com/veridex/issues](https://github.com/veridex/issues)
- Email: support@veridex.io

## Contributing

Internal development team only. See CONTRIBUTING.md for guidelines.

---

**Built with Streamlit & FastAPI**

VERIDEX © 2025 - Professional SaaS Market Research Intelligence