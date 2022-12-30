from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk
import re
import math

class Summary():
    def __init__(self, document):
        self.__document = document
        self.__paragraph = []
        self.__D = 0
        self.__tf = {}
        self.__sentence = document
        self.__sentence_weight = []
        self.__main_sentence = []

        self.__set_sentence()
        self.__set_summary()

    def __break_into_token(self):
        #Clean HTML Tag
        self.__document = re.sub("<[^>]+>", "", self.__document).strip()

        #LowerCase
        self.__document = self.__document.lower()

        #Split Document into Paragraph
        self.__paragraph = self.__document.split("\n")

        #Set Paragraph Length
        self.__D = len(self.__paragraph)
        
        #Tokenization    
        for i in range(0, self.__D):
            self.__paragraph[i] = word_tokenize(self.__paragraph[i])
    
        #Clean Empty List
        i = 0
        end = self.__D
        while True:
            if i == end:
                break
            elif self.__paragraph[i] == [] or self.__paragraph[i].count(" ") >= 1:
                del self.__paragraph[i]
                end-=1
            else:
                i+=1
        
        #Set count paragraph
        self.__D = len(self.__paragraph)
        
        #Remove Delimiter
        for i in range(0, self.__D):
            j = 0
            end = len(self.__paragraph[i])
            while True:
                if j == end:
                    break
                #elif bool(re.search('^[a-zA-Z0-9]*$', self.__paragraph[i][j])) == False: #With Number
                elif bool(re.search('^[a-zA-Z]*$', self.__paragraph[i][j])) == False: #Remove number
                    del self.__paragraph[i][j]
                    end-=1
                else:
                    j+=1
    
    def __stop_list(self):
        #Stoplist (Stopword Removal)
        #nltk.download('stopwords') #Uncomment to download package

        #get english stop word list
        englisth_stops = set(stopwords.words('english'))

        #stop list
        for i in range(0, self.__D):
            j = 0
            end = len(self.__paragraph[i])
            while True:
                if j == end:
                    break
                elif self.__paragraph[i][j] in englisth_stops:
                    del self.__paragraph[i][j]
                    end-=1
                else:
                    j+=1

    def __stemming(self):
        #Porter Stemming
        for i in range(0, self.__D):
            end = len(self.__paragraph[i]) - 1
            for j in range(0, end):
                self.__paragraph[i][j] = PorterStemmer().stem(self.__paragraph[i][j])
    
    def __term_frequency(self):
        for paragraph in self.__paragraph:
            for sentence in paragraph:
                self.__tf[sentence] = paragraph.count(sentence)
    
    def __term_logarithm(self):
        for tf in self.__tf:            
            self.__tf[tf] = 1 + math.log(int(self.__tf[tf]), 10)
    
    def __set_main_sentence(self):
        #Adding sentence
        i = 0
        for paragraph in self.__sentence:
            j = 0
            sentence_temp = []
            for sentence in paragraph:
                t = [sentence, i, j, 0]
                sentence_temp.append(t)
                j+=1
            self.__sentence_weight.append(sentence_temp)
            i+=1
        
        #sentence stemming
        i = 0
        for paragraph in self.__sentence_weight:
            j = 0
            for sentence in paragraph:
                word = []
                word = word_tokenize(sentence[0])
                k = 0
                for w in word:
                    word[k] = PorterStemmer().stem(w)
                    k+=1
                self.__sentence_weight[i][j][0] = word
                j+=1
            i+=1
        
        #Adding sentence weight
        i = 0
        for paragraph in self.__sentence_weight:
            j=0
            for sentence in paragraph:
                sentence_weight = 0
                for word in sentence[0]:
                    for tf in self.__tf:
                        if tf == word:
                            sentence_weight+=self.__tf[tf]
                self.__sentence_weight[i][j][3] = sentence_weight
                j+=1
            i+=1
        
        #Ranking of sentence
        i = 0
        for paragraph in self.__sentence_weight:
            paragraph_length = len(paragraph)
            for j in range(0, paragraph_length-1):
                if self.__sentence_weight[i][j][3] < self.__sentence_weight[i][j+1][3]:
                    self.__sentence_weight[i][j], self.__sentence_weight[i][j+1] = self.__sentence_weight[i][j+1], self.__sentence_weight[i][j]
            i+=1
        
        #Save main sentence
        a = 0
        for paragraph in self.__sentence:
            i = self.__sentence_weight[a][0][1]
            j = self.__sentence_weight[a][0][2]
            self.__main_sentence.append(self.__sentence[i][j])
            a+=1


    def __set_summary(self):
        self.__break_into_token()
        self.__stop_list()
        self.__stemming()
        self.__term_frequency()
        self.__term_logarithm()
        self.__set_main_sentence()
    
    def __set_sentence(self):
        __temp = 0 #

        #Clean HTML Tag
        self.__sentence = re.sub("<[^>]+>", "", self.__sentence).strip()

        #Split Document into Paragraph
        self.__sentence = self.__sentence.split("\n")

        i = 0
        for sentence in self.__sentence:
            self.__sentence[i] = sent_tokenize(sentence)
            i+=1
        
        # #LowerCase
        # self.__sentence = self.__sentence.lower()


        # #Split Paragraph into sentence
        # i = 0
        # for sentence in self.__sentence:
        #     self.__sentence[i] = sentence.split(".")
        #     i+=1
        
        #Remove duplicate whitespace
        i = 0
        for sentence in self.__sentence:
            end = len(sentence)
            for j in range(0, end):
                self.__sentence[i][j] = " ".join(sentence[j].split())
            i+=1

        # #Remove list kosong
        i = 0
        end = len(self.__sentence)
        while True:
            if i == end:
                break
            elif self.__sentence[i] == []:
                del self.__sentence[i]
                end-=1
            else:
                i+=1
        
        #Remove list kosong
        # i = 0
        # paragraph_end = len(self.__sentence)
        # while True:
        #     if i == paragraph_end:
        #         break
        #     sentence_end = len(self.__sentence[i])
        #     j = 0
        #     while True:
        #         if j == sentence_end:
        #             break
        #         elif self.__sentence[i][j] == '':
        #             del self.__sentence[i][j]
        #             sentence_end-=1
        #         else:
        #             j+=1
        #     i+=1


    def get_paragraph(self, index=-1):
        if index != -1: #Return paragraph with index
            return self.__paragraph[index]
        else: #Return all paragraph
            return self.__paragraph
    
    def get_count_paragraph(self, index = -1):
        if index != -1: #Return word count paragraph with index
            return len(self.__paragraph[0])
        else: #Return count paragraph in document
            return self.__D

    def get_tf(self):
        return self.__tf
    
    def get_sentence_weight(self):
        return self.__sentence_weight
    
    def get_main_sentence(self):
        return self.__main_sentence

    def get_summary(self):
        summary = ""
        for s in self.__main_sentence:
            summary += str(s)+" "
        return summary

    def get_sentence(self, indexParagraph = -1, indexSentence = -1):
        if indexParagraph != -1:
            if indexSentence != -1:
                return self.__sentence[indexParagraph][indexSentence]
            else:
                return self.__sentence[indexParagraph]
        else:
            return self.__sentence
    



# s = Summary('''<div class="post-content content-view no-padding img-mg-20 num-on">

#                                     <p></p><p style="text-align: justify;">In the beginning of the 1960s, the people of Bali aspired to have a Tertiary Institution on the island. In order to realize this aspiration, on May 12th 1961, several figures from the educational sector, government, and community leaders conducted a conference led by Prof.Dr. Purbatjaraka,and assisted by Prof. Dr. Ida Bagus Mantra as secretary.<br>
#     The conference discussed the steps required for the preparation of the establishment of a tertiary institution in Bali. An agreement was also reached for the formation of a committee led by dr. Anak Agung Made Djelantik, Head of the Board of Health in Bali, with a team of eight members.</p>

#     <p style="text-align: justify;"><img alt="" src="/upload/images/universitas-udayana.jpg" style="float:left; height:151px; width:300px">Subsequently, the committee formed an institution named the Tertiary Education Institution of Bali, chaired by Ir. Ida Bagus Oka (Coordinator of Public Works Boards in the Southeast Islands Region); vice chaired by Dr. I Gusti Ngurah Gede Ngurah, assisted by two secretaries, Prof. Dr. Ida Bagus Mantra, and Drh. G.D. Teken Temadja. This institution succeeded in forming the Preparatory Committee for the establishment of Udayana University Bali on January 15th,1962.</p>

#     <div>
#     <p style="text-align:justify">By a decision of the Directorate General of Higher Education, Ministry of Education and Culture of Indonesia, Udayana University (UNUD) was officially founded in August 17, 1962. Initially Unud consisted of four faculties: Letters, Medicine, Veterinary Sciences and Animal Husbandry and Education and Teacher Training. The Faculty of Letters was actually established on 29th September 1958, however, the time it was a subsidiary of the Faculty of Letters of Airlangga University in Surabaya (East Java). This Faculty was thenintegrated into Udayana University in 1962. Although it was founded on August 17, the anniversary date of Udayana University is not August 17, but was choosen to be on September 29 to commemorate the date of establishment of the Faculty of Letters in 1958. Unud has develop rapidly, in 2015 the university has 13 faculties, 25 master programs and 10 doctoral programs.</p>

#     <p style="text-align:justify"><br>
#     Udayana University today’s is listed as one of the 50“Promising Universities of Indonesia” published by theMinistry of Education of Republic Indonesia, out of nearly 2.500 higher education institutions around the country.The university has a strong position as one of the leading university particularly in the Eastern Indonesian Territory.</p>
#     </div>
#     <p></p>

#                                     <div class="banner-end"></div>

#                                 </div>''')

# s = Summary('''In 1918, the Dutch authorities in the Dutch East Indies established a partly-elected People's Council, the Volksraad, which for the first time gave Indonesian nationalists a voice. Meanwhile, Indonesian students studying in the Netherlands formed the Perhimpoenan Indonesia, or Indonesian Association. Among its leaders were future Indonesian vice-president Mohammad Hatta and future prime minister Sutan Sjahrir. In September 1927, Hatta and other members were arrested for inciting resistance to Dutch authority in the East Indies, but thanks to a rousing defense speech by Hatta, they were acquitted.[6][7] Back in the East Indies, in 1927, nationalist and future Indonesian president Sukarno turned his study club into the Indonesian Nationalist Association, which in May 1928 became the Indonesian National Party (PNI). The party aimed to achieve Indonesian independence through mass-based non-cooperation with the authorities. In October 1928, the representatives at a Youth Congress held in Batavia, the capital, adopted the ideals of one motherland, Indonesia; one nation, the nation of Indonesia; and one language, the Indonesian language. This expression of national unity was a reaction to the older generation, which tended to identify with their region or ethnicity, and subsequently became known as the Youth Pledge.[8][9][10]
# The PNI grew rapidly, causing concern for the authorities, who arrested Sukarno and seven party leaders in December 1929. They were put on trial for being a threat to public order and in September 1930 received sentences of one to four years – Sukarno received the longest sentence. The PNI dissolved itself in 1931, and in the same year, Sjahrir returned from the Netherlands and established a party called the New PNI which rather than focussing on mass action and being dependent on one leader, aimed to create a group of leaders who could ensure continuity if any were arrested. In 1931, Sukarno was released and joined the small Indonesia Party (Partindo), while in August 1932, Hatta returned from the Netherlands and assumed the leadership of the rival New PNI, which had a more Marxist and revolutionary platform than Partindo. Sukarno was arrested again in August 1933, and was exiled first to Flores, then to Bencoolen, while Hatta and Sjahrir were arrested and exiled to the Boven Digul detention camp in western New Guinea.[11][12][13]

# The detention of these nationalist figures effectively ended the non-cooperation movement, and in December 1935 the moderate Indonesian National Union and Budi Utomo merged to form the Great Indonesia Party (Parindra), which aimed to work with the Dutch to achieve Indonesian independence. When in 1936, Volksraad member Soetardjo submitted a petition asking for a conference to be held that would lead to Indonesian self-government as part of a Dutch-Indonesian union over a decade, Parindra was lukewarm, resenting the possibility of Soetardjo succeeding where the other nationalist organizations had failed.[14] The petition was passed by a majority of the Volksraad, but rejected by the Dutch in November 1938. In May 1937, Parindra, the Indonesian People's Movement (Gerindo), was established by younger Marxists including Amir Sjarifuddin, another future prime minister, to campaign for the formation of an Indonesian parliament in cooperation with the Dutch, which was the same aim of the Indonesian Political Federation (GAPI), formed two years later from a merger of almost all the nationalist organizations. However, the outbreak of the Second World War resulted in the occupation of the Netherlands, and the Dutch government in exile was in no position to respond to GAPI's request for a Dutch-Indonesian union and an elected legislature, although Dutch Queen Wilhelmina made a speech in London in May 1941 promising unspecified changes to the relationship with the East Indies after the war.[15][16]

# On 23 January 1942, three years before the 1945 proclamation, an independence activist Nani Wartabone declared "Indonesian independence" after he and his people won in a revolt in Gorontalo against the Dutch who were afraid of Japanese invasion of Celebes. He was later imprisoned by the Japanese after they had invaded the area.[17]''')

# print(s.get_paragraph())
# print(s.getCountParagraph(1))
# print(s.get_sentence_weight())
# print(s.get_tf())
# print(str(s.get_sentence()) + "\n")
# print(s.get_main_sentence())
# print(s.get_summary())
