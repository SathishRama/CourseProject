from rank_bm25 import BM25Okapi
import csv
import os
import operator
from datetime import datetime
import traceback

corpus = []
product_tags = []
rank_tags = []
final_scores = {}
doc_dte = []
names = []
print("   ##########################################################################################################")
print(" This demo ranking tool uses TV/Internet/Cable Service complaints of a company from 2000 to 2016.")
print(" You can rank the complaints during a month using query terms & product/sentiment/churn weights to rank/prioritize complaints \n")
print("---Ranking Approach used by tool ----------")
print(" 1. Tool uses product terms to identify the related product(s) & weights for products to generate product score of the complaint.")
print(" 2. Tool tags the complaints into Negative/Sentiment & Churn based on some word terms & weights : sentiment weight & churn weigt ")
print(" 3. Then using above, a final rank/score for the complaint is generated using below scoring function")
print("     Final score = sum of product scores + churn weight * churn score + Sentiment weight * Sentiment score")
print(" 4. The complaints for the Year & Month are ranked based on the above final score")
print(" 5. The ranked complaints are written to a output file with product tags and scores for reference\n")
print(" ==> To run this tool, download data & src folders and run main.py This tool uses rank_bm25 library.")
print("   ############################################################################################################")
print("Enter year between 2000 to 2016 :")
input_year = input("YYYY: ")
print("Enter month ( 0-12 ) :")
input_month = input("MM: ")
input_year = int(input_year)
input_month = int(input_month)
print("Entered year {} and month {}".format(input_year,input_month))
#input_year = 2006
#input_month = 3

# Weights for scoring model
churn_score_multipler = 1.5
sentiment_score_multiplier = 1.2

# queries to gather product ranks
product_queries = [{"Internet":"internet xfinity"},{"TV":"tv television cable channel dish"},{"Phone":"phone cellphone wireless voice"},{"Bundle":"bundle"},{"Service":"service outage appointment schedule called hold times"}]
# Queries to gather ranking inputs ( long time, very dissapointed customer etc )
rank_input_queries = [{"Negative":"disappointing multiple annoying worst negative suck terrible rude ignorant"},{"Churn":"long time years loyal used to changing cutting"}]


cwd = os.getcwd()
file_path = os.path.dirname(os.getcwd()) + '\data\complaints_data.csv'
file = open(file_path,encoding="utf-8")
csvreader = csv.reader(file)
header = next(csvreader)
# print(header)
for doc_id in range(0,2000):
    try :
        row = next(csvreader)
        #print(row[0], row[1],row[2])
        doc = row[3].lower().replace(".","")
        #print(doc)
        # corpus.append(doc)
        # doc_dte.append(row[1])
        dte = row[1]
        #print(dte)
        month,day,year = dte.strip(" ").split("/")
        #print("Debug :",int(year),int(month))
        year = int(year)
        month = int(month)
        if year  == input_year and month == input_month:
            corpus.append(doc)
            doc_dte.append(row[1])
            names.append(row[0])
    except Exception as e :
        #print("Data/Exception while reading a record. Skipping a complaint : ", e)
        pass

#print(corpus)
num_docs = len(corpus)
if num_docs == 0:
    print("No complaints found in the dataset during this year & month. Try again with another year & month")
    exit(0)
# print(" ######################Dates ###########")
# print("Entered year {} and month {}".format(input_year,input_month))
# for dte in doc_dte:
#     day,month,year = dte.split("/")
#     print(year,month,day)
print("\n###   Ranking complaints..... ######")
tokenized_corpus = [doc.split(" ") for doc in corpus]

bm25 = BM25Okapi(tokenized_corpus)

for i in range(0,num_docs):
    product_tags.append({})
    rank_tags.append({})

def score_doc(query):
    tokenized_query = query.split(" ")
    doc_score = bm25.get_scores(tokenized_query)
    return  doc_score

# Identify products/service  associated with each doc using the common product words
for products in product_queries:
    product = list(products.keys())[0]
    product_query = products[product]
    print("Generating Product Score for {} using terms : ".format(product), product_query)
    prod_score = score_doc(product_query)

    #print(prod_score)
    for i in range(0,len(prod_score)):
        if prod_score[i] > 0 :
            #product_tags[i].append({product:prod_score[i]})
            product_tags[i][product]= round(prod_score[i],2)

for i in range(0,len(product_tags)):
    if len(product_tags[i]) == 0:
        product_tags[i]["Service"] = 1.0



for rank_input in rank_input_queries:
    input = list(rank_input.keys())[0]
    rank_input_query = rank_input[input]
    print("Generating scores for rank Input {} using terms: ".format(input), rank_input_query)
    score = score_doc(rank_input_query)

    #print(score)
    for i in range(0,len(score)):
        if score[i] > 0 :
            rank_tags[i][input] = round(score[i],2)

#print("====== Product & rank Tags ======")
# for i in range(0,num_docs):
#     print(corpus[i])
#     print("Products :", product_tags[i])
#     print("Rank Inputs :", rank_tags[i])

# calculate final rank for the doc based on Product, Product Scores, Rank Inputs Scores etc
#final score = sum of product scores + churn weight * churn score + Sentiment weight * Sentiment score
f = open("output.txt", "w",encoding="utf-8")

print("###   Calculating Final Scores..... ######")
for i in range(0,num_docs):
    # print(corpus[i])
    # print("Products :", product_tags[i])
    # print("Rank Inputs :", rank_tags[i])
    #f.write(corpus[i]+'\n')
    # f.write("Products : {}\n".format(product_tags[i]))
    # f.write("Rank Inputs : {}\n".format(rank_tags[i]))
    num_products = len(product_tags[i])
    products_score = sum(product_tags[i].values())
    input_weight = 0.0
    # print(" *** Calc Rank Inputs *** ")
    # print(rank_tags[i])
    rank_part_score = 0.0
    for each_input in rank_tags[i]:
        if each_input == 'Churn' :
            rank_part_score = rank_part_score + rank_tags[i]['Churn'] * churn_score_multipler
        if each_input == 'Negative' :
            rank_part_score = rank_part_score + rank_tags[i]['Negative'] * sentiment_score_multiplier

    final_score = products_score + rank_part_score
    final_scores[i] = round(final_score,2)
    # print(" Num of products :" , num_products)
    # print("Products Score : ", products_score, " Rank Inputs Score :", rank_part_score)
    # print(" Final scores :", final_score)
    # f.write("Final Score : {}\n".format(final_score))

#print("############################################# Document Score Table ###########################")
#print(final_scores)
ranked_list = sorted(final_scores.items(),key=operator.itemgetter(1),reverse=True)
#print( ranked_list)
print("Number of complaints ranked {}".format(len(ranked_list)))
print("\nBelow are top 5 ranked complaints  {}".format(len(ranked_list)))
top_n = 0
for ranked_score in ranked_list :
    #print(corpus[ranked_score[0]])
    if top_n <5:
        print(doc_dte[ranked_score[0]] + ' by ' + names[ranked_score[0]] )
        print(corpus[ranked_score[0]][0:150] )
        print("Products : {}".format(product_tags[ranked_score[0]]))
        print("Rank Inputs : {}".format(rank_tags[ranked_score[0]]))
        print('Total Score :' + str(ranked_score[1]) )
        top_n = top_n + 1

    f.write(doc_dte[ranked_score[0]] + ' by ' + names[ranked_score[0]] + '\n')
    f.write(corpus[ranked_score[0]] + '\n')
    f.write("Products : {}\n".format(product_tags[ranked_score[0]]))
    f.write("Rank Inputs : {}\n".format(rank_tags[ranked_score[0]]))
    f.write('Total Score :' + str(ranked_score[1]) + '\n')
    f.write("-------------------------------------------                   \n")
f.close()