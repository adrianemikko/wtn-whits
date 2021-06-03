# USE YOUR WHITS: Applying the Weighted HITS Algorithm in Analyzing the World Trade Network

Studying the world trade network (WTN) has played a significant role in international trade analysis and in uncovering patterns and structures of economic systems across countries. By using the 2012-2019 BACI-CEPII World Trade dataset, we investigated trends and patterns of international trade and tried to identify which countries are considered as key players by looking at the whole network and in specific product categories, and how they affect each other in the WTN. This was implemented by creating a directed network using import and export countries as nodes and trade flows as edges. Weights were assigned to each edge using the amount of trade (in USD) for that specific trade flow. To identify countries that have the most influence as importers and exporters, we applied a weighted Hyperlink-Induced Topic Search (WHITS) and compared the results using a simple HITS algorithm and by simply getting the node with the highest average degree. We were able to establish that top hubs and authorities differ based on the algorithm used. We observed a linear relationship between a country’s hub and authority score, which means that top hubs are very much likely to become top authorities also. Using 2019 data, China and Mexico appear to be the top hubs overall, while the USA and Hong Kong are the leading authorities.  We also explored who the key players are for the banana, coconut, and footwear product categories. We found that Ecuador-France, India-Netherlands, and China-France are the top hub-authority pairs for each product category, respectively.

## Authors
* [Amorado, Adriane Mikko A.](https://github.com/adrianemikko)
* [Espiritu, Nika Karen O.](https://github.com/nikakaren)
* [Quinto, Joanna G.](https://github.com/joaquin73)

## Datasets
* [2012 to 2019 BACI-CEPII trade flow dataset](http://www.cepii.fr/CEPII/en/bdd_modele/presentation.asp?id=37) (2.75 GB)
* [International Monetary Fund's Direction of Trade Statistics dataset](https://data.imf.org/?sk=9D6028D4-F14A-464C-A2F2-59B2CD424B85) (1.45 GB, _for visuals only_)

## Notes
* Dear peer-reviewers, this is a WIP-in-progress, please bear with us as we fix this for our professional portfolio
