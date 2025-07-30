# WhatsApp Chat Analyzer

A comprehensive web application for analyzing WhatsApp chat data using Streamlit. This tool provides detailed insights into chat patterns, user behavior, sentiment analysis, and visual analytics.

## 🚀 Features

### 📊 Analytics Dashboard
- **Message Statistics**: Total messages, words, media files, and links shared
- **User Activity**: Most active users with participation percentages
- **Timeline Analysis**: Daily, weekly, and monthly activity patterns
- **Activity Heatmaps**: Visual representation of chat activity by time and day

### 📈 Visual Analytics
- **Word Clouds**: Generate word clouds for individual users or overall chat
- **Emoji Analysis**: Most used emojis and emoji patterns
- **Sentiment Analysis**: Emotion classification and sentiment trends
- **Interactive Charts**: Plotly-based interactive visualizations

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly, Matplotlib, Seaborn
- **NLP**: NLTK, TextBlob
- **Cloud**: AWS S3 (optional)

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd whatsapp_chat_analysis
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 📖 Usage

1. **Start the application**
   ```bash
   streamlit run app.py
   ```

2. **Upload WhatsApp Chat File**
   - Export your WhatsApp chat as a text file
   - Upload the file through the web interface
   - The app will automatically process and analyze the data

3. **Explore Analytics**
   - Navigate through different analysis sections
   - Filter by individual users or view overall statistics
   - Interact with charts and visualizations

## 📁 Project Structure

```
whatsapp_chat_analysis/
├── app.py                 # Main Streamlit application
├── helper.py             # Core analysis functions
├── preprocessor.py       # Data preprocessing utilities
├── requirements.txt      # Python dependencies
├── stop_hinglish.txt    # Stop words for Hinglish text
├── railway.json         # Railway deployment config
├── Procfile            # Heroku deployment config
└── README.md           # This file
```

## 🔧 Key Components

### `app.py`
Main Streamlit application that handles:
- File upload and processing
- User interface and navigation
- Integration of all analysis modules

### `helper.py`
Core analysis functions including:
- `fetch_stats()`: Basic message statistics
- `most_busy_users()`: User activity analysis
- `word_cloud()`: Word cloud generation
- `sentiment_analysis()`: Emotion and sentiment analysis
- `activity_heatmap()`: Time-based activity visualization

### `preprocessor.py`
Data preprocessing utilities:
- WhatsApp chat format parsing
- DateTime extraction and formatting
- User and message separation
- Time period categorization

## 📊 Supported Analysis

### Message Statistics
- Total messages count
- Word count analysis
- Media file detection
- Link extraction and counting

### User Analytics
- Most active users ranking
- Participation percentages
- Individual user statistics
- User comparison charts

### Temporal Analysis
- Daily activity patterns
- Weekly activity trends
- Monthly activity visualization
- Hourly activity heatmaps

### Content Analysis
- Word frequency analysis
- Emoji usage patterns
- Sentiment analysis
- Emotion classification

## 🌐 Deployment

### Local Development
```bash
streamlit run app.py
```

### Cloud Deployment
The project includes configuration files for:
- **Railway**: `railway.json`
- **Heroku**: `Procfile`

## 🔒 Privacy & Security

- All data processing happens locally
- No chat data is stored permanently
- Optional AWS S3 integration for file storage
- Environment variables for sensitive configuration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues or have questions:
1. Check the existing issues in the repository
2. Create a new issue with detailed description
3. Include error messages and steps to reproduce

## 🔄 Updates

Stay updated with the latest features and improvements by:
- Starring the repository
- Watching for updates
- Checking the releases section

---

**Note**: This tool is designed for personal chat analysis. Please respect privacy and only analyze chats you have permission to analyze. 