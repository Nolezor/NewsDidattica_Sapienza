# News Didattica Bot

An automated system that scrapes valuable information from Sapienza University's [News Didattica](https://www.phys.uniroma1.it/it/news-didattica) (Physics department) and sends all new updates to a dedicated [Telegram channel](https://t.me/news_didattica_fisica_sapienza).

## How It Works

This bot performs the following operations:
1. Scrapes the Physics department's News Didattica page
2. Compares new data with previously stored data
3. Identifies new updates
4. Formats the updates in Markdown
5. Sends new updates to a Telegram channel
6. Saves the current state for future comparison

## Project Structure

- `main.py` - Main script that orchestrates the scraping and notification process
- `scraper.py` - Contains functions to scrape the website and save data
- `telegram_bot.py` - Handles sending notifications to Telegram
- `scraped.xlsx` - Excel file storing the latest scraped data (generated on first run)
- `.env` - Contains environment variables for bot configuration (you need to create this)
- `.env.example` - Example environment variables file for reference

## Features

- **Error Handling**: Gracefully handles network issues, website changes, and API errors
- **Comprehensive Logging**: Detailed logs of all operations for easy troubleshooting
- **Environment Variables**: Secure configuration using .env files
- **Markdown Formatting**: Clean, formatted messages in Telegram
- **Incremental Updates**: Only sends new information, avoiding duplicates

## Getting Started

### Prerequisites

* Python 3.9 or higher
* Telegram account
* Telegram bot token (obtained from @BotFather)
* Telegram channel where updates will be posted

### Dependencies

All required Python packages are listed in `requirements.txt`, including:
- requests
- pandas
- beautifulsoup4
- python-telegram-bot
- markdownify
- python-dotenv

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/Nolezor/NewsDidattica_Sapienza.git
   cd NewsDidattica_Sapienza
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure your Telegram bot:
   - Create a bot using [@BotFather](https://t.me/BotFather) on Telegram
   - Create a Telegram Channel or get the ID of an existing one
   - Add your bot to the channel as an administrator
   - Create a `.env` file in the project root directory (see `.env.example` for reference)
   - Add your bot TOKEN as `BOT_TOKEN=your_token_here`
   - Add your channel ID as `CHAT_ID=your_channel_id_here`

### First Run

Run the main script to generate the initial Excel file that will be used as a reference for future updates:

```
python main.py
```

On the first run, this will create `scraped.xlsx` with the current state of the News Didattica page.

### Environment Variables

The project uses environment variables for sensitive configuration. Create a `.env` file in the project root with the following variables:

```
BOT_TOKEN=your_telegram_bot_token_here
CHAT_ID=your_telegram_channel_id_here
```

A template file `.env.example` is provided for reference.

### Regular Usage

To check for updates and send notifications:

```
python main.py
```

The script will output logs to the console showing the progress and any issues encountered.

#### Exit Codes

- `0`: Success or no new updates
- `1`: Network error (could not connect to website or Telegram)
- `2`: Data processing error

#### Automation

For automated checking, consider setting up a cron job or scheduled task to run the script at regular intervals.

**Example cron job (Linux/Mac)** - Check every hour:

```
0 * * * * cd /path/to/NewsDidattica_Sapienza && python main.py >> news_bot.log 2>&1
```

## Version History

* 0.1 - Initial release
* 0.2 - Added support for Markdown formatting and updated to the new website structure

## License

This project is licensed under the [GPL-3.0](https://github.com/Nolezor/NewsDidattica_Sapienza/blob/main/LICENSE.md) License - see the LICENSE.md file for details

## Author

* [Nolezor](https://github.com/Nolezor)
