library(tidyverse)
data.car0 <- read.csv("cars04.dat")
sum(is.na(data.car0)) # many missing values!!!! 
data.car <- data.car0[,-c(9,10,12,22,23,25)]
data.car$GPHM <- 100/data.car$MPG.City
data.car <- data.car[,-1]
data.car <- data.car[,-c(18,19)]
data.car <- na.omit(data.car)
sum(is.na(data.car))
dim(data.car)

data.car$Model.Year <- data.car$Model.Year %>% factor()

fit.all <- lm(GPHM~., data.car) # dump everything in the model
summary(fit.all) 

library(glmnet)

Y.car <- data.car$GPHM # extract Y
X.car <- model.matrix(GPHM~., data=data.car)[, -1]
fit.car.lambda <- glmnet(X.car, Y.car, alpha=1, lambda = 0.1) 



