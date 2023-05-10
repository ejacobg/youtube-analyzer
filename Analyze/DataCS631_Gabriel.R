 #install packages for data visulization 
library(scales)
library(gridExtra)
library(ggplot2)
library(ggpubr)
library(GGally)
# Disable scientific notation
options(scipen = 999)
#=====================================================
#read csv files

#read this file for the pie chart 
csv_path <- file.path(getwd(), "most_viewed.csv")
data <- read.csv(csv_path)

#read this file for the bar graphs 
csv_path_total <- file.path(getwd(), "total_views.csv")
data_video <- read.csv(csv_path_total)

#read these files for the comment vs views 
# Read in the first CSV file as a data frame
df1 <- read.csv("views_comments_1.csv")
# Read in the second CSV file as a data frame
df2 <- read.csv("views_comments_1.csv")
# Combine the two data frames using rbind()
df <- rbind(df1, df2)
# Read in the data as a data frame
df <- read.csv("cv_data.csv")
# Read in the data as a data frame
df3 <- read.csv("Degree.csv")
df4 <- read.csv("comments1.csv")
# Read in the second CSV file as a data frame
df5 <- read.csv("comments2.csv")
# Combine the two data frames using rbind()
df_comment <- rbind(df4, df5)
# merge the data frames based on videoID

df_comment_degree <- merge(df3, df_comment, by = "videoID")
#=====================================================
#Create a Pie chart that shows which category is the most popular 

library(ggplot2)
library(dplyr)

# create a new column called "new_category"
data_video$new_category <- ifelse(data_video$percent < 0.1, "Other", data_video$category)

# group the data by "new_category" and calculate the sum of "percent" and "total_views" for each group
data_video_new <- data_video %>%
  group_by(new_category) %>%
  summarize(total_views = sum(total_views),
            percent = sum(percent))

# Define a vector of blues for the fill color scale
blues <- c("#7fcdbb", "#41b6c4", "#1d91c0", "#225ea8", "#253494")

# Create the pie chart with the modified fill scale
ggplot(data_video_new, aes(x = "", y = percent, fill = new_category)) + 
  geom_bar(stat = "identity", width = 1) +
  coord_polar("y", start = 0) +
  labs(title = "Video Views by Category", fill = "Category") +
  scale_fill_manual(values = blues) + # specify the blue color palette
  theme_void() +
  geom_text(aes(label = ifelse(percent >= 0.1, paste0(round(percent * 100), "%"), "")), 
            position = position_stack(vjust = 0.5))

pie_chart

#=====================================================
# Create the bar chart
bar_chart <- ggplot(data, aes(x = category, y = al, fill = category)) +
  geom_bar(stat = "identity") +
  labs(x = "Category", y = "Average video length in seconds", fill = "Category") +
  ggtitle("Video Lengths by Category")+
  theme(axis.text.x = element_blank(),
        axis.ticks.x = element_blank())

bar_chart 
#=====================================================
#Views Vs Comments 

df <- df_comment_degree
# Calculate the median value of views
views_median <- median(df_comment_degree$views)

# Divide the videos into two groups: high views and low views
high_views <- df[df$views > views_median, ]
low_views <- df[df$views <= views_median, ]


# Calculate the mean number of comments for each group
high_views_mean <- mean(high_views$comments)
low_views_mean <- mean(low_views$comments)

# Create a new data frame for the boxplot
boxplot_data <- data.frame(group = c(rep("High Views", nrow(high_views)), rep("Low Views", nrow(low_views))),
                           comments = c(high_views$comments, low_views$comments))

# Create a boxplot with ggplot2
ggplot(boxplot_data, aes(x = group, y = comments)) +
  geom_boxplot() +
  geom_point(aes(color = group), alpha = .5, position = position_jitter(width = .15)) +
  labs(title = "Relationship between Views and Comments on Videos",
       x = "",
       y = "Comments") +
  stat_compare_means(method = "t.test", label = "p.format") 
  
# Create a scatter plot 
ggplot(df_comment_degree, aes(x = views, y = comments)) + 
  geom_point(alpha = .2, color = "#3366FF") +
   scale_size(range = c(1, 10), breaks = seq(0, 20000, by = 5000)) +
  scale_x_continuous(labels = scales::number_format(scale = 1e-6, accuracy = 0.1, suffix = "M")) +
  labs(title = "Scatterplot of Views and Comments on Videos",
       x = "Views",
       y = "Comments")
       
ggplot(df_comment_degree, aes(x = degree, y = comments)) + 
  geom_point(alpha = .2, color = "#3366FF") +
  labs(title = "Scatterplot of Degree and Comments on Videos",
       x = "Degree",
       y = "Comments")
       
#compare the two 

# create a linear regression model
model <- lm(comments ~ views + degree, data = df_comment_degree)

# print the summary of the model
summary(model)
library(ggplot2)

       
  ggplot(df_comment_degree, aes(x = views, y = degree, size = comments)) + 
  geom_point(alpha = .5, color = "#3366FF") +
  scale_size(range = c(1, 10), breaks = seq(0, 20000, by = 5000)) +
  scale_x_continuous(labels = scales::number_format(scale = 1e-6, accuracy = 0.1, suffix = "M")) +
  labs(title = "Impact of Views and Degree on Comments",
       x = "Views",
       y = "Degree",
       size = "Number of Comments")


#=====================================================
