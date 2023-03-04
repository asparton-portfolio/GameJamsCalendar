# Game Jams Calendar

## Project overview
Game Jams Calendar is a personal tool with a simple web front-end which allows you to:
- Fetch upcomming game jams by scraping
- Display their information
- Add the wanted event to my Notion Calendar

## Project architecture

![architecture](https://cdn.discordapp.com/attachments/808748311574085653/1081294748377153627/gjc-architecture.png)

Game Jams Calendar uses a [fast-api](https://fastapi.tiangolo.com/) backend which takes care of:
- Scraping the game jams data on [itch.io](https://itch.io/) website
- Send the information to the front-end
- Insert game jams event inside a Notion database

The back-end uses [Selenium](https://www.selenium.dev/) as the web scraping tool, and the [Notion API](https://developers.notion.com/) for the events insertion.

To display the game jam events and select which ones to save, I built a simple single page [React](https://reactjs.org/) application with [Mantine](https://mantine.dev/) as the UI library.
