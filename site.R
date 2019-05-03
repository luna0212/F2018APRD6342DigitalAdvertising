library(readxl)
library(tidyr)
library(dplyr)
library(xlsx)
library(stringi)
library(stringr)

file <- 'subaru.xlsx'
sheets <- excel_sheets('subaru.xlsx')
subaru <- lapply(sheets, function(x) read_excel(path = file, sheet = x))
sheet <- as.data.frame(subaru[6])

# 1. Fix website format
sheet$goodsite <- 0
substrRight <- function(x, n){
  substr(x, nchar(x)-n+1, nchar(x))
}

sheet$goodsite <- ifelse(substrRight(sheet$Matched.Site.Name,4) == '.com' |
                           substrRight(sheet$Matched.Site.Name,4) == '.net' |
                           substrRight(sheet$Matched.Site.Name,4) == '.org' |
                           substrRight(sheet$Matched.Site.Name,3) == '.co' |
                           substrRight(sheet$Matched.Site.Name,6) == '.co.uk' |
                           substrRight(sheet$Matched.Site.Name,5) == '.info'|
                           substrRight(sheet$Matched.Site.Name,3) == '.tv'|
                           substrRight(sheet$Matched.Site.Name,3) == '.io'|
                           substrRight(sheet$Matched.Site.Name,3) == '.be',1,0)

sheet$goodsite <- ifelse(substr(sheet$Matched.Site.Name, start = 1, stop = 4) == 'com.',2,sheet$goodsite)


for (i in 1:nrow(sheet)){
    if (sheet[i,]$goodsite == 2){
      aaa = strsplit(sheet[i,]$Matched.Site.Name, split='[.]')  
      sheet[i,4] <- paste0(aaa[[1]][2], ".com")
      sheet[i,16] <- 1
      }}

# 2. Aggregate unique websites
good.data = sheet[sheet$goodsite == 1,]
site.data = aggregate(CPM~Matched.Site.Name,FUN=length,data=good.data)

write.csv(sheet, file = "0426_site_for_api_all.csv")





