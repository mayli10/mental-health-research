library(stringr)
library(dplyr)
library(rio)
df <- rio::import("/Users/mayli/GitHub/mental-health-research/reddit-data-final2.csv")

diagnosSubset <- df[grep("diagnos", df$Text), ]
head(diagnosSubset)
write.csv(diagnosSubset,"/Users/mayli/GitHub/mental-health-research/reddit-data-final.csv")

df <- rio::import("/Users/mayli/GitHub/mental-health-research/reddit-data-final2.csv")

df %>%
  filter(str_detect(Text, "diagnos"))

