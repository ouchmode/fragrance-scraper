# (WIP) Fragrance Scraper (Jomashop)

Web Scraper made in Python with Selenium to extract results from the fragrance section on Jomashop.com, filter the results down to fragrances, then search those fragrances on a site like Parfumo to retrieve the notes and accords.

## TO DO:
1. Pull the fragrance notes from Jomashop for now instead of Parfumo. I mainly wanted to pull from Parfumo originally since I believe the community helps with determining notes, similar to Fragrantica. There are also some other stats on there I wanted to pull eventually. Jomashop for pricing, Parfumo / Fragrantica for descriptions.

## find_frags([driver]):
While on Jomashop.com (the fragrances section), it scrolls down the page a few times to load the content and then scrapes the following:
- ``` class="brand-name" ```
  - The fragrance brand *(e.g. YSL, Creed, Dior, etc.)*
- ``` class="name-out-brand" ```
  - The fragrance name, but sometimes also includes the brand, separated by a '/' or 'by' *(e.g. Aventus / Creed, or Dylan Blue by Versace)*
- ``` class="tag-item discount-label" ```
  - Current discount (#% OFF).
- ``` class="now-price" ```
  - The current price with the discount applied.
- ``` class="was-wrapper" ```
  - The original price before the discount. Likely the actual retail price since Jomashop is a fragrance reseller.

It then adds everything to a dataframe and exports it as a .csv file.

As mentioned above, some of the names are formatted [Name] / [Brand] or [Name] by [Brand], so I had to get clever with a Regular Expression.



#### Below is the Regular Expression used to capture certain pieces within the extracted "name-out-brand" element. 

**Note:** *This can be trimmed down as I plan on scraping for ONLY sprayable body fragrances. I also want capture the gender, but was having a few issues in Python for some reason; not so much the RegEx. Despite Python knowing there was a group for the gender, it would not capture it for some reason. It worked in the testers I used (Debuggex, Regex101))*

``` regex.compile(r"^(?:(Men's|Ladies|Unisex)\s+)?(?:-\s*)?([^/]+?)(?=\s?Spray\s?|\s*/|\s+by|\s+\(|\s+\d+\.\d+|\s+(?:Eau De Parfum|Eau De Cologne|Eau De Toilette|Extrait de Parfum|EDP|EDT|EDC|Cologne)|$)|\((m|u|w)\)", regex.IGNORECASE) ```
- ``` (?:(Men's|Ladies|Unisex)\s+)? ``` and ``` \((m|u|w)\) ``` 
  - Captures any instance of "Men's", "Ladies", or "Unisex" at the start of the string.
  - Captures any instance of "m", "w", or "u", upper or lower, at the end of the string.
    - There are also some "for Men" and "for Women" I have found, but It might be useful to keep those in the name when searching on Parfumo.  
- ``` (?:-\s*)?([^/]+?) ```
  - Matches a possible '-' at the start since some names can have that for some reason after scraping.
  - Searches the string and stops at a '/' when being used to separate the [Name] / [Brand].
- ``` (?=\s?Spray\s?|\s*/|\s+by|\s+\(|\s+\d+\.\d+|\s+(?:Eau De Parfum|Eau De Cologne|Eau De Toilette|Extrait de Parfum|EDP|EDT|EDC|Cologne)|$) ```
  - Didn't want to include "Spray" in the name so I am using a positive lookahead to essentially stop the capture once it finds "Spray".
  - Does the same as the above for "by" *(could also probably add the '/' from the part before instead of doing it where it is now)*, decimal values *(e.g. sizes like 3.3 oz)*, any of the fragrance types found on the site's fragrance type filters section. I also added a few of my own like EDP, EDT, etc. that can be found in the name.