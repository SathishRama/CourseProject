# CourseProject

This project is part of the CS410 Fall21 course. 

# Project Topic 
Retrieving & ranking customer communication/complaints for optimal routing & resolution of customer concerns

# Description
As part of this project, developed a demo tool that takes a public dataset of 2000 complaints of a Telecom company and helps to rank the complaints using raking rules & query retrieval. The dataset used has 2000 complaints from year 2000 to 2006 on Internet, TV/Cable, Phone and Service. For demo purpose the user need to a year & month to rank the complaints during that period. The tool uses pre-configured query terms & product/sentiment/churn weights to rank/prioritize complaints. 

Below are Product & Sentiment/Churn and their respective query terms used.

{"Internet":"internet xfinity"},{"TV":"tv television cable channel dish"},{"Phone":"phone cellphone wireless voice"},{"Bundle":"bundle"},{"Service":"service outage appointment schedule called hold times"}

{"Negative":"disappointing multiple annoying worst negative suck terrible rude ignorant"},{"Churn":"long time years loyal used to changing cutting"}

# Ranking Approach used

 1. Tool uses product terms to identify the related product(s) & weights for products to generate product score of the complaint.")
 2. Tool tags the complaints into Negative/Sentiment & Churn based on some word terms & weights : sentiment weight & churn weigt ")
 3. Then using above, a final rank/score for the complaint is generated using below scoring function")
     Final score = sum of product scores + churn weight * churn score + Sentiment weight * Sentiment score")
 4. The complaints for the Year & Month are ranked based on the above final score")
 5. The ranked complaints are written to a output file with product tags and scores for reference"
 6. In addition to writing to output file, the tool displays top 5 complaints for the year & month entered and the scores.
 
 
 # To run this tool
 Download data & src folders and run main.py. This tool uses rank_bm25 library so you need to pip install that and other packages used in main.py
