# PersonaLink
 Unique links listing a user's results from several personality tests, while allowing the user to take them through the site

 ## 2026 Update
 Right now, I'm working on overhauling this project from my university years. Due to the nature of webscraping, several of the scripts that were used to build this project will now fail due to website changes made over the last 5-6 years. This overhaul consists of both short-term and long-term goals

### Short-Term:
1. Fix the broken scraping and submission scripts to work with the newer versions of the sites
2. Redeploy the site to AWS

### Long-Term:
1. Rewrite the codebase to make it more extensible. At the current moment, each scrape/submit methods for the various webpages are their own separate functions Currently planning on setting up a base class that can be re-used when trying to add new personality tests. Also, consider better structuring the scrape/submit methods by dividing them up into sub-functions for each step, making future edits far easier.
2. Switch from Selenium to APIs where applicable. For example, 16Personalities already has an [unofficial API](https://www.16personalities-api.com), and there are likely various tests which use public APIs. This would make the application more resilient over the years. Selenium was mostly employed back then as a way to experiment with an interesting tool, but it's definitely not the best way to go about this.
3. Add new tests, Arcana/Tarot is a good start.
4. Improve the front-end, right now it's completely basic HTML.
