# Instagram Signup Bot

## ⚠️ IMPORTANT WARNING

**This bot is for EDUCATIONAL PURPOSES ONLY.** Automating Instagram account creation:
- Violates Instagram's Terms of Service
- May result in IP bans or legal action
- Is considered a form of automation abuse
- Should NOT be used to create real accounts

Use this code only to learn about web automation concepts in controlled test environments.

## Features

- Automated navigation to Instagram signup page
- Form filling with user data
- Random delays to simulate human behavior
- Chrome browser automation
- Error handling and logging

## Requirements

- Python 3.7+
- Google Chrome browser
- ChromeDriver (automatically managed by webdriver-manager)

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure Google Chrome is installed on your system

## Usage

### Basic Usage

Run the bot with default test data:
```bash
python instagram_bot.py
```

### Custom Usage

Edit the `user_data` dictionary in the `main()` function to use custom test data:

```python
user_data = {
    'email': 'your_test_email@example.com',
    'full_name': 'Your Test Name',
    'username': 'testuser1234',
    'password': 'YourPassword123'
}
```

## How It Works

1. **Initialize**: Sets up Chrome browser with anti-detection options
2. **Navigate**: Opens Instagram signup page
3. **Fill Form**: Enters email, full name, username, and password
4. **Submit**: Clicks the signup button
5. **Handle Additional Steps**: Can handle birthday selection if prompted

## Important Notes

- Instagram frequently changes their page structure, so selectors may need updates
- Instagram uses CAPTCHA and other anti-bot measures
- Email verification is usually required
- Phone number verification may be required
- Using this for actual account creation violates ToS

## Troubleshooting

### ChromeDriver Not Found
The script uses `webdriver-manager` which automatically downloads the correct ChromeDriver. If you encounter issues, make sure Chrome is installed.

### Elements Not Found
Instagram may have changed their page structure. Update the selectors in the code accordingly.

### CAPTCHA Appears
This is Instagram's anti-bot protection. There's no automated way to bypass it ethically.

## Ethical Use

This code is provided for:
- Learning web automation
- Understanding how bots work
- Educational demonstrations
- Testing on your own controlled environments

**Do NOT use this to:**
- Create spam accounts
- Violate any terms of service
- Engage in unauthorized automation
- Create bot networks

## License

This code is provided as-is for educational purposes only.
