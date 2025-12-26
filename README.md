# YouTube Binge Analyzer 📺

Note: This project is currently under active development as part of the CS50p final submission.

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![CS50p](https://img.shields.io/badge/CS50p-Final%20Project-green)](https://cs50.harvard.edu/python/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A CLI utility designed to help users quantify their learning or entertainment time. This tool interfaces with the **YouTube Data API v3** to aggregate video durations from any public playlist and calculates the "true" time spent across different playback speeds.

## 🎯 Project Overview
I built this tool to solve a common problem: knowing exactly how much time is required to complete a technical course or video series. The analyzer doesn't just give a total; it accounts for the efficiency gained through accelerated playback.

## ✨ Key Features
* **API Integration:** Real-time data fetching using the `google-api-python-client`.
* **ISO 8601 Parsing:** Custom regex-based logic to convert YouTube's duration format (e.g., `PT1H2M10S`) into total seconds.
* **Speed Comparisons:** Instant calculation of time saved via 1x, 1.5x, and 2x playback speeds.

## 🛠️ Tech Stack
* **Language:** Python 3
* **APIs:** YouTube Data API v3
* **Libraries:** `re`, `isodate` (or custom parsing), `google-api-python-client`, `python-dotenv`

## 🚀 Installation & Setup
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/youtube-binge-analyzer.git](https://github.com/YOUR_USERNAME/youtube-binge-analyzer.git)
   cd youtube-binge-analyzer
