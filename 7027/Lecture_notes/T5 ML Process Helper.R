## step_log
simple_blueprint_4f <-
  recipe(Sale_Price ~ Neighborhood + Gr_Liv_Area + Year_Built + Bldg_Type + Alley + Overall_Qual, data = ames_train_4f) %>%
  step_log(Gr_Liv_Area, base = 10) 

## step_log with offset
simple_blueprint_4f <-
  recipe(Sale_Price ~ Neighborhood + Gr_Liv_Area + Year_Built + Bldg_Type + Alley + Overall_Qual, data = ames_train_4f) %>%
  step_log(Gr_Liv_Area, base = 10, offset = 164) 

## step_center, step_scale
simple_blueprint_4f <-
  recipe(Sale_Price ~ Neighborhood + Gr_Liv_Area + Year_Built + Bldg_Type + Alley + Overall_Qual, data = ames_train_4f) %>%
  step_center(Gr_Liv_Area)  %>%
  step_scale(Gr_Liv_Area)

## step_other
simple_blueprint_4f <-
  recipe(Sale_Price ~ Neighborhood + Gr_Liv_Area + Year_Built + Bldg_Type + Alley + Overall_Qual, data = ames_train_4f) %>%
  step_other(Neighborhood, threshold = 0.3) 

## step_dummy
simple_blueprint_4f <-
  recipe(Sale_Price ~ Neighborhood + Gr_Liv_Area + Year_Built + Bldg_Type + Alley + Overall_Qual, data = ames_train_4f) %>%
  step_dummy(Neighborhood) 

## step_integer
simple_blueprint_4f <-
  recipe(Sale_Price ~ Neighborhood + Gr_Liv_Area + Year_Built + Bldg_Type + Alley + Overall_Qual, data = ames_train_4f) %>%
  step_integer(Overall_Qual) 

## step_nzv
simple_blueprint_4f <-
  recipe(Sale_Price ~ Neighborhood + Gr_Liv_Area + Year_Built + Bldg_Type + Alley + Overall_Qual, data = ames_train_4f) %>%
  step_nzv(all_predictors(), unique_cut = 50, freq_cut = 3) 

## missing data - impute
simple_blueprint_4f <-
  recipe(Sale_Price ~ Neighborhood + Gr_Liv_Area + Year_Built + Bldg_Type + Alley + Overall_Qual, data = ames_train_4f) %>%
  step_impute_median(Year_Built)







# simple_blueprint_4f <- 
#   recipe(Sale_Price ~ Neighborhood + Gr_Liv_Area + Year_Built + Bldg_Type, data = ames_train_4f) %>%
#   step_log(Gr_Liv_Area, base = 10) %>%
#   step_other(Neighborhood, threshold = 0.07) %>% 
#   step_dummy(all_nominal_predictors(), one_hot = TRUE)
