# AY23-24_WebDataMining_PageRank

PageRank, developed by Google co-founders Larry Page and Sergey Brin, is an algorithm for ranking web pages based on inbound link quality and quantity. Higher PageRank scores indicate greater authority. It plays a crucial role in web data mining, improving search results by highlighting high-PageRank pages for enhanced accuracy. Additionally, it's valuable for identifying influential pages in various networks, making it essential for network analysis in fields like social networks and web analytics. 

**In our assignment, we implemented PageRank by analyzing over one million Wikipedia pages, producing a sorted list of PageRank values for analysis.**

Refer to the PageRank pdf report, which comprises an explanation of the PageRank implementation and a discussion of the results.

PageRank Formula used: `PR(A) = (1 - d) / N + d * Σ (PR(Ti) / C(Ti))`

where d is the damping factor, (1 - d) / N is the teleport probability, N is the total number of pages, PR(Ti) is the PageRank score of a page Ti that links to page A, and C(Ti) is the number of outbound links from page Ti.
