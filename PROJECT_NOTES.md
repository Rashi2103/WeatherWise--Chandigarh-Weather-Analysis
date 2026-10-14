# 2-hour build checklist

- [ ] Run `pip install -r requirements.txt`
- [ ] Run `python fetch_weather.py` (needs internet)
- [ ] Run `python prepare_data.py`
- [ ] Run `streamlit run app.py`
- [ ] Check the date range, chart labels, and flagged-day explanation
- [ ] Capture 2 screenshots and add them to `screenshots/`
- [ ] Add your IEEE paper's public DOI/link if available; don't upload copyrighted paper files unless allowed
- [ ] Create GitHub repository and push source files
- [ ] Include the actual data file only if its terms permit redistribution; otherwise exclude it and document how to fetch it

## Interview explanation (practice in your own words)

“I extended my interest in weather analysis into a small educational data product. Python and pandas handle cleaning, SQLite stores records for repeatable SQL analysis, and Streamlit presents trends and threshold-based observations in plain language. I deliberately describe the thresholds as exploratory flags, not disaster predictions. The next step would be validating against official alerts and verified event records.”
