# Fragrance Scraper (Jomashop)

Web Scraper made in Python with Selenium to extract results from the fragrance section on Jomashop.com, filter the results down to fragrances, then search those fragrances on a site like Parfumo to retrieve the notes and accords.

## TO DO:
1. Only scrape results that contain an EDP, EDT, EDC, Cologne, Extrait, Parfum, etc. fragrance type. Do not include gift sets, deodorant, shower gels and others.

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

**Note:** *This can be trimmed down as I plan on scraping for ONLY sprayable body fragrances. I also want capture the gender, but was having a few issues in Python for some reason; not so much the RegEx. Despite Python knowing there was a group for the gender, it would not capture it for some reason. It worked in the testers I used (Debuggex, Regex101))*


#### Below is the Regular Expression used to capture certain pieces within the extracted "name-out-brand" element. 
``` regex.compile(r"^(?:(Men's|Ladies|Unisex)\s+)?(?:-\s*)?([^/]+?)(?=\s?Spray\s?|\s*/|\s+by|\s+\(|\s+\d+\.\d+|\s+(?:Aftershave|Bath and Shower Products|Body Spray|Car Diffuser|Cleansers|Deodorant|Diffuser|Eau De Parfum|Eau De Cologne|Eau De Toilette|Extrait de Parfum|Eau de Cologne|Eau de Parfum|Eau de Toilette|Extrait De Parfum|Free Water|Gift Set|Lotion & Oils|Lotions & Creams|Mist|Oil & Serums|Perfume Oil|Room Fragrance|Room Spray|Scented Candle|Scented Cards|Scrubs, Foams & Exfoliants|Shower Gels|Soap|Solid Parfum|Tools|Wash|EDP|EDT|EDC|Cologne|Shower Gel|Shampoo / Shower Gel)|$)|\((m|u|w)\)", regex.IGNORECASE) ```
- ``` (?:(Men's|Ladies|Unisex)\s+)? ``` and ``` \((m|u|w)\) ``` 
  - Captures any instance of "Men's", "Ladies", or "Unisex" at the start of the string.
  - Captures any instance of "m", "w", or "u", upper or lower, at the end of the string.
    - There are also some "for Men" and "for Women" I have found, but It might be useful to keep those in the name when searching on Parfumo.  
- ``` (?:-\s*)?([^/]+?) ```
  - Matches a possible '-' at the start since some names can have that for some reason after scraping.
  - Searches the string and stops at a '/' when being used to separate the [Name] / [Brand].
- ``` (?=\s?Spray\s?|\s*/|\s+by|\s+\(|\s+\d+\.\d+|\s+(?:Aftershave|Bath and Shower Products|Body Spray|...|EDP|EDT|EDC|Cologne|Shower Gel|Shampoo / Shower Gel)|$) ``` *(added an elipses in the middle because this one is long)*
  - Didn't want to include "Spray" in the name so I am using a positive lookahead to essentially stop the capture once it finds "Spray".
  - Does the same as the above for "by" *(could also probably add the '/' from the part before)*, decimal values *(e.g. sizes like 3.3 oz)*, any of the fragrance types found on the site's fragrance type filters section. I also added a few of my own like EDP, EDT, etc. that can be found in the name.
 

## find_notes([driver], [name_col]):
After scraping the fragrances from Jomashop, it navigates to Parfumo and searches those names, clicks the result, and scrapes the notes and accords.
#### Unfortunately having an issue with selecting the correct result. There are *many* fragrances, and there are some that have very similar names whether that is just how it is named or the regex from the find_frags() function accidentally messed the name up a bit. For now the function call is commented out.
I am currently trying to search through the results list when the name is entered in the searchbox and determine if the current name within the loop has a fragrance type tag of "EAU DE PARFUM", "EAU DE TOILETTE" or other similar types, or not. Some fragrance names from the initial Jomashop scrape can be the same or very similar. So when searching on Parfumo, it can be difficult to select the right result.
