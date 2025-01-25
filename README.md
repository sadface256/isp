Welcome to the README! If you're reading this, I still haven't cleaned it, sorry :(

crossword.html is just an example crossword, the same as the other ones in there.

crossword_scraper is the base code for scraping one crossword, and getting specific information from it for the collated csv. If you haven't seen it, it has every clue with the format [clue, answer, author, editor, link, date]. 

full_scraper runs crossword_scraper for each crossword in the database. Note that the site uses two different url structures (PS and normal) and also there was a shift from when the puzzles were weekly to being daily. Running full_scraper took me a couple hours total, so I would test anything on example webpages before running something similar again. 

xwordinfo.py is some code from Nick for scraping the grids of each crossword like how Scott wanted. Don't run this-- there's a bug that I haven't fixed on lines 97 and 98 where they only check for one kind of website. XWordInfo renames this container across pages (the older/newer pages have diff names), so finding the other name for it is necessary. (I did and then didn't push the changes, lol.)

Good luck! Scott is great to work with. I hope you have fun!
