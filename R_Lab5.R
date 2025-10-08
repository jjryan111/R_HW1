library(ggplot2)
iris <- read.csv('/Users/jj/Downloads/R_Stuff/iris.csv')
lm_model <- lm(sepal.length ~ sepal.width, data = iris )
summary(lm_model)
