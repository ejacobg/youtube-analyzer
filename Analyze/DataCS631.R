 #install packages for data visulization 
library(scales)
library(gridExtra)
library(ggplot2)
library(ggpubr)

#read csv file 
csv_path <- file.path(getwd(), "a.csv")
data <- read.csv(csv_path)

#read csv file 
csv_path_total <- file.path(getwd(), "b.csv")
data_video <- read.csv(csv_path_total)


# calculate percentage of total views for each category
data_video$percent <- data_video $total_views / sum(data_video $total_views)

# create a pie chart with category as the label and percent as the value
pie_chart <- ggplot(data_video, aes(x = "", y = percent, fill = category)) + 
  geom_bar(stat = "identity", width = 1) +
  coord_polar("y", start = 0) +
  labs(title = "Video Views by Category", fill = "Category") +
  theme_void()

# add percentage labels to the chart
pie_chart + geom_text(aes(label = paste0(round(percent * 100), "%")), position = position_stack(vjust = 0.5))



# Create the bar chart
bar_chart <- ggplot(data, aes(x = category, y = al, fill = category)) +
  geom_bar(stat = "identity") +
  labs(x = "Category", y = "Average video length in seconds", fill = "Category") +
  ggtitle("Video Lengths by Category")+
  theme(axis.text.x = element_blank(),
        axis.ticks.x = element_blank())

bar_chart 


#Comment and View Ratio 
# Read in the first CSV file as a data frame
df1 <- read.csv("cv1.csv")

# Read in the second CSV file as a data frame
df2 <- read.csv("cv2.csv")

# Combine the two data frames using rbind()
df <- rbind(df1, df2)

correlation <- cor(df$views, df$comments)
correlation
max(df$views)
max(df$comments)

# Load the ggplot2 package
library(ggplot2)
# Create a histogram with ggplot2
ggplot(df, aes(x = views, y = comments)) +
  geom_histogram(stat = "identity", bins = 1, fill = "blue", alpha = 0.5) +
  ggtitle("Views vs Comments") +
  xlab("Views") +
  ylab("Comments")

